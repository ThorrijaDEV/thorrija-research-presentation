#!/usr/bin/env python3
"""
THORRIJA — Research Presentation Builder
Generates a 45-slide professional PDF for AI research team presentation.

Architecture: ReportLab + matplotlib + pygments for full visual control.
Aesthetic: Dark minimal lab — precise, technical, no decoration.
"""

from __future__ import annotations

import os
import json
import textwrap
from dataclasses import dataclass
from typing import List, Tuple, Optional, Callable

from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import mm, inch
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle, Circle, Polygon
from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextPath
import matplotlib.font_manager as fm

from pygments import highlight
from pygments.lexers import PythonLexer, TypeScriptLexer, RustLexer, JsonLexer
from pygments.formatters import ImageFormatter
from pygments.styles import get_style_by_name

# ──────────────────────────────────────────────────────────────────────────────
# CONSTANTS & PALETTE
# ──────────────────────────────────────────────────────────────────────────────

PAGE_W, PAGE_H = landscape((1920, 1080))
MARGIN = 72

# Hex strings for matplotlib compatibility; HexColor for ReportLab
BG_HEX = "#0b0b0d"
PANEL_HEX = "#131317"
PANEL_2_HEX = "#17171c"
EDGE_HEX = "#2a2a31"
INK_HEX = "#f2f0eb"
MUTED_HEX = "#9a9aa6"
FAINT_HEX = "#6a6a76"
INDIGO_HEX = "#8ea0e8"
AMBER_HEX = "#c8944e"
TEAL_HEX = "#5fb3ac"
PLUM_HEX = "#a97fa2"
RED_HEX = "#c06a5f"
GREEN_HEX = "#6abf8b"

BG = HexColor(BG_HEX)
PANEL = HexColor(PANEL_HEX)
PANEL_2 = HexColor(PANEL_2_HEX)
EDGE = HexColor(EDGE_HEX)
INK = HexColor(INK_HEX)
MUTED = HexColor(MUTED_HEX)
FAINT = HexColor(FAINT_HEX)
INDIGO = HexColor(INDIGO_HEX)
AMBER = HexColor(AMBER_HEX)
TEAL = HexColor(TEAL_HEX)
PLUM = HexColor(PLUM_HEX)
RED = HexColor(RED_HEX)
GREEN = HexColor(GREEN_HEX)

MONO_FAMILY = "DejaVuSansMono"
SANS_FAMILY = "DejaVuSans"
SANS_BOLD = "DejaVuSans-Bold"

# ──────────────────────────────────────────────────────────────────────────────
# FONT REGISTRATION
# ──────────────────────────────────────────────────────────────────────────────

def register_fonts():
    for name, path in [
        ("DejaVuSans", "/usr/share/fonts/TTF/DejaVuSans.ttf"),
        ("DejaVuSans-Bold", "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"),
        ("DejaVuSansMono", "/usr/share/fonts/TTF/DejaVuSansMono.ttf"),
        ("DejaVuSansMono-Bold", "/usr/share/fonts/TTF/DejaVuSansMono-Bold.ttf"),
    ]:
        try:
            pdfmetrics.registerFont(TTFont(name, path))
        except:
            pass

register_fonts()

# ──────────────────────────────────────────────────────────────────────────────
# MATPLOTLIB FIGURE ENGINE
# ──────────────────────────────────────────────────────────────────────────────

class Stack:
    def __init__(self, ax, x, w, y_top, fig_w, fig_h):
        self.ax, self.x, self.w, self.y = ax, x, w, y_top
        pos = ax.get_position()
        self.w_pt = pos.width * fig_w * 72.0
        self.h_pt = pos.height * fig_h * 72.0

    def wrap(self, text, fs, mono=False):
        limit = max(8, int((self.w * self.w_pt) / (fs * (0.60 if mono else 0.53))))
        out = []
        for para in text.split("\n"):
            if len(para) <= limit:
                out.append(para)
                continue
            line = ""
            for word in para.split():
                cand = (line + " " + word).strip()
                if len(cand) <= limit:
                    line = cand
                else:
                    if line:
                        out.append(line)
                    line = word
            out.append(line)
        return "\n".join(out)

    def text_h(self, text, fs, ls=1.45):
        return (text.count("\n") + 1) * fs * ls * 1.22 / self.h_pt

    def _text_width(self, s, fs, mono, weight):
        if not s:
            return 0.0
        try:
            fp = FontProperties(family="DejaVu Sans Mono" if mono else "DejaVu Sans", size=fs, weight=weight)
            return TextPath((0, 0), s, prop=fp).get_extents().width
        except:
            return len(s) * fs * (0.60 if mono else 0.55)

    def measure(self, line, fs, mono=False, weight="normal"):
        return self._text_width(line, fs, mono, weight)

    def fit(self, text, fs, mono=False, weight="normal"):
        width = self.w * self.w_pt
        while fs > 5.0:
            wrapped = self.wrap(text, fs, mono)
            widest = max((self.measure(l, fs, mono, weight) for l in wrapped.split("\n")), default=0.0)
            if widest <= width:
                return wrapped, fs
            fs -= 0.2
        return self.wrap(text, fs, mono), fs

    def text(self, text, fs=8.0, color=INK_HEX, weight="normal", mono=False,
             align="left", pad=0.0, ls=1.45, style="normal"):
        text, fs = self.fit(text, fs, mono, weight)
        h = self.text_h(text, fs, ls)
        if align == "center":
            x, ha = self.x + self.w / 2, "center"
        elif align == "right":
            x, ha = self.x + self.w, "right"
        else:
            x, ha = self.x, "left"
        self.ax.text(x, self.y, text, fontsize=fs, color=color, weight=weight,
                     style=style, ha=ha, va="top", zorder=6, linespacing=ls,
                     family="DejaVu Sans Mono" if mono else "DejaVu Sans")
        self.y -= h + pad
        return self

    def gap(self, g):
        self.y -= g
        return self

    def rule(self, color=EDGE_HEX, lw=0.8, gap=0.012):
        self.ax.plot([self.x, self.x + self.w], [self.y, self.y], color=color,
                     linewidth=lw, zorder=3, solid_capstyle="butt")
        self.y -= gap
        return self

    def panel(self, text, fs=7.6, color=INK_HEX, fc=PANEL_HEX, ec=EDGE_HEX, lw=0.9,
              pad=0.018, gap=0.020, mono=False, weight="normal", align="left",
              ls=1.5, radius=0.006, accent=None, minh=0.0, title=None,
              title_color=None, title_fs=7.4):
        text, fs = self.fit(text, fs, mono, weight)
        h = max(self.text_h((title + "\n" + text) if title else text, fs, ls) + 2 * pad, minh)
        self.ax.add_patch(FancyBboxPatch((self.x, self.y - h), self.w, h,
                                         boxstyle=f"round,pad=0,rounding_size={radius}",
                                         linewidth=lw, edgecolor=ec, facecolor=fc, zorder=2))
        if accent:
            self.ax.add_patch(Rectangle((self.x, self.y - h), 0.0035, h,
                                        facecolor=accent, edgecolor="none", zorder=3))
        x = self.x + (self.w / 2 if align == "center" else 0.014)
        ha = "center" if align == "center" else "left"
        if title:
            th = self.text_h(title, title_fs, 1.4) + title_fs * 0.5 / self.h_pt
            self.ax.text(x, self.y - pad, title, fontsize=title_fs,
                         color=title_color or ec, weight="bold", ha=ha, va="top",
                         zorder=6, linespacing=1.4,
                         family="DejaVu Sans Mono" if mono else "DejaVu Sans")
            self.ax.text(x, self.y - pad - th, text, fontsize=fs, color=color,
                         weight=weight, ha=ha, va="top", zorder=6, linespacing=ls,
                         family="DejaVu Sans Mono" if mono else "DejaVu Sans")
        else:
            self.ax.text(x, self.y - pad, text, fontsize=fs, color=color,
                         weight=weight, ha=ha, va="top", zorder=6, linespacing=ls,
                         family="DejaVu Sans Mono" if mono else "DejaVu Sans")
        self.y -= h + gap
        return self


def canvas_fig(w_in, h_in, dpi=200):
    f, ax = plt.subplots(figsize=(w_in, h_in), dpi=dpi)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_position([0, 0, 1, 1])
    return f, ax


def arrow(ax, p0, p1, color=MUTED_HEX, lw=1.1, style="-|>", rad=0.0, z=2, ms=10):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=ms,
                                 linewidth=lw, color=color, zorder=z,
                                 connectionstyle=f"arc3,rad={rad}",
                                 shrinkA=2, shrinkB=2))


def save_fig(f, path):
    f.savefig(path, facecolor=BG_HEX, pad_inches=0, dpi=200)
    plt.close(f)


# ──────────────────────────────────────────────────────────────────────────────
# DIAGRAM GENERATORS
# ──────────────────────────────────────────────────────────────────────────────

ASSETS_DIR = "/home/thorrija/research-presentation/assets"
os.makedirs(ASSETS_DIR, exist_ok=True)


def diag_slide_03_thesis():
    f, ax = canvas_fig(12, 4.5)
    st = Stack(ax, 0.03, 0.94, 0.95, 12, 4.5)
    st.text("TESIS DEL PROGRAMA", fs=8, color=FAINT_HEX, mono=True, pad=0.006)
    st.text("Tres pilares, una disciplina", fs=18, color=INK_HEX, weight="bold", pad=0.035)
    cols = [
        ("AFIRMACIÓN → EVIDENCIA → VEREDICTO", INDIGO_HEX,
         "Nada se afirma sin instrumento.\nNada se mide sin trazabilidad.\nNada se concluye sin intento de refutación."),
        ("FIDELIDAD DECLARADA", TEAL_HEX,
         "Cada reconstrucción lleva su nivel:\n1=reproducción directa, 2=reconstrucción fiel,\n3=parcial documentada, 4=modelo conceptual."),
        ("RESULTADOS NEGATIVOS PUBLICADOS", AMBER_HEX,
         "ORACLE E1: colaboración perjudica.\nThe Box: mecanismo explicado, sin descubrimiento.\nDefectos documentados: since_inflow, Rule.to_dict"),
    ]
    y = st.y
    w = 0.30
    gap = 0.02
    for i, (title, color, body) in enumerate(cols):
        x = 0.03 + i * (w + gap)
        ax.add_patch(FancyBboxPatch((x, y - 0.55), w, 0.55,
                                    boxstyle="round,pad=0,rounding_size=0.006",
                                    linewidth=1, edgecolor=EDGE_HEX, facecolor=PANEL_HEX, zorder=2))
        ax.add_patch(Rectangle((x, y - 0.55), w, 0.005, facecolor=color, edgecolor="none", zorder=3))
        ax.text(x + 0.015, y - 0.03, title, fontsize=10.5, color=color, weight="bold",
                family="DejaVu Sans Mono", va="top", zorder=6)
        ax.text(x + 0.015, y - 0.10, body, fontsize=9, color=MUTED_HEX, va="top", zorder=6, linespacing=1.5)
    ax.text(0.03, 0.04, "Esta presentación sigue el mismo orden: instrumento → cifra → veredicto.",
            fontsize=9, color=FAINT_HEX, style="italic")
    save_fig(f, os.path.join(ASSETS_DIR, "slide_03_thesis.png"))


def diag_slide_04_landscape():
    f, ax = canvas_fig(12, 5)
    st = Stack(ax, 0.02, 0.96, 0.96, 12, 5)
    st.text("PAISAJE DE TRABAJO", fs=8, color=FAINT_HEX, mono=True, pad=0.006)
    st.text("Veinticuatro proyectos, cuatro oficios, un criterio", fs=18, color=INK_HEX, weight="bold", pad=0.03)
    rows = [
        ("Sistemas y redes", "9", "Herramientas de terminal que leen el SO real:\n/proc, DNS crudo, tablas ARP, sockets, BPF", INDIGO_HEX),
        ("Reconstrucciones", "4", "Modelos deterministas desde código fuente:\nWi-Fi Time Machine, BLE Radar, Process Monitor, TGE", TEAL_HEX),
        ("Seguridad defensiva", "3", "Canarios, detección local, reconocimiento autorizado", RED_HEX),
        ("Líneas abiertas", "5", "Trabajo en curso, documentado como tal", FAINT_HEX),
        ("Experimentación", "3", "The Box, ORACLE/SINGULARITY, HERMES", PLUM_HEX),
    ]
    y = st.y
    rowh = 0.13
    for i, (name, count, desc, color) in enumerate(rows):
        yy = y - i * rowh
        ax.add_patch(Rectangle((0.02, yy - rowh + 0.02), 0.0035, rowh - 0.03, facecolor=color, edgecolor="none", zorder=3))
        ax.text(0.038, yy - 0.008, name, fontsize=11, color=INK_HEX, weight="bold", va="top", zorder=6)
        ax.text(0.95, yy - 0.008, count, fontsize=18, color=color, weight="bold", va="top", ha="right", zorder=6, family="DejaVu Sans Mono")
        ax.text(0.038, yy - 0.055, desc, fontsize=8.5, color=MUTED_HEX, va="top", zorder=6, linespacing=1.4)
        if i < len(rows) - 1:
            ax.plot([0.02, 0.98], [yy - rowh + 0.012, yy - rowh + 0.012], color=EDGE_HEX, linewidth=0.6, zorder=2)
    ax.text(0.02, 0.04, "Python · TypeScript · Rust · C · C++ · Kotlin · Go · Zig",
            fontsize=9, color=AMBER_HEX, family="DejaVu Sans Mono")
    save_fig(f, os.path.join(ASSETS_DIR, "slide_04_landscape.png"))


def diag_slide_05_fidelity():
    f, ax = canvas_fig(12, 4)
    st = Stack(ax, 0.02, 0.96, 0.95, 12, 4)
    st.text("MARCO DE FIDELIDAD", fs=8, color=FAINT_HEX, mono=True, pad=0.006)
    st.text("Una reconstrucción sin nivel declarado es una opinión", fs=18, color=INK_HEX, weight="bold", pad=0.03)
    levels = [
        ("1", "Reproducción directa", "Mismas operaciones, constantes y orden", INDIGO_HEX, "Showcase (4)"),
        ("2", "Reconstrucción fiel", "Comportamiento reproducido; pieza sustituida declarada", TEAL_HEX, ""),
        ("3", "Reconstrucción parcial", "Lo entendido reproducido; lo demás documentado ausente", AMBER_HEX, "The Box (TS)"),
        ("4", "Modelo conceptual", "Idea reproducida, no mecánica", PLUM_HEX, ""),
    ]
    y = st.y
    for i, (num, title, desc, color, tag) in enumerate(levels):
        yy = y - i * 0.14
        bg = PANEL_HEX if i % 2 == 0 else BG_HEX
        ax.add_patch(Rectangle((0.02, yy - 0.12), 0.96, 0.12, facecolor=bg, edgecolor="none", zorder=1))
        ax.add_patch(Rectangle((0.02, yy - 0.12), 0.004, 0.12, facecolor=color, edgecolor="none", zorder=3))
        ax.text(0.045, yy - 0.016, num, fontsize=14, color=color, weight="bold", va="top", zorder=6, family="DejaVu Sans Mono")
        ax.text(0.09, yy - 0.014, title, fontsize=11, color=INK_HEX, weight="bold", va="top", zorder=6)
        ax.text(0.09, yy - 0.062, desc, fontsize=9, color=MUTED_HEX, va="top", zorder=6, linespacing=1.4)
        if tag:
            ax.text(0.97, yy - 0.018, tag, fontsize=9, color=AMBER_HEX, va="top", ha="right", zorder=6, family="DejaVu Sans Mono")
    ax.text(0.02, 0.03, "La honestidad del nivel importa más que el nivel mismo.",
            fontsize=9, color=FAINT_HEX, style="italic")
    save_fig(f, os.path.join(ASSETS_DIR, "slide_05_fidelity.png"))


def diag_slide_11_box_kernel():
    f, ax = canvas_fig(12, 5)
    st = Stack(ax, 0.02, 0.96, 0.96, 12, 5)
    st.text("THE BOX — NÚCLEO", fs=8, color=FAINT_HEX, mono=True, pad=0.006)
    st.text("Multigrafo de incidencia arco-arco con espacio de IDs compartido", fs=16, color=INK_HEX, weight="bold", pad=0.03)
    ax.text(0.03, 0.72, "G = (V, E, ι, λ, σ)", fontsize=20, color=INK_HEX, weight="bold", family="DejaVu Sans Mono", va="top")
    defs = [
        "V : arcos (no nodos) — cada arco es identidad + payload",
        "E ⊆ V × V : incidencia dirigida (arco apunta a arco)",
        "ι : V → Label : etiqueta de identidad (copia/pérdida)",
        "λ : V → Label : etiqueta de linaje (origen)",
        "σ : V → {0,1}^k : semilla determinista (splitmix64)",
    ]
    y = 0.65
    for d in defs:
        ax.text(0.03, y, d, fontsize=11, color=MUTED_HEX, family="DejaVu Sans Mono", va="top")
        y -= 0.055
    arc_positions = [
        (0.65, 0.65, "Arco A\nι=α, λ=∅"),
        (0.80, 0.52, "Arco B\nι=α, λ=A"),
        (0.65, 0.39, "Arco C\nι=β, λ=A"),
    ]
    for i, (x, y, label) in enumerate(arc_positions):
        ax.add_patch(FancyBboxPatch((x - 0.07, y - 0.06), 0.14, 0.12,
                                    boxstyle="round,pad=0,rounding_size=0.01",
                                    linewidth=1.5, edgecolor=INDIGO_HEX, facecolor=PANEL_HEX, zorder=3))
        ax.text(x, y + 0.01, label, fontsize=9, color=INK_HEX, ha="center", va="center", zorder=5, linespacing=1.3, family="DejaVu Sans Mono")
    arrow(ax, (0.65, 0.59), (0.73, 0.52), color=TEAL_HEX, lw=1.5)
    arrow(ax, (0.65, 0.59), (0.58, 0.45), color=TEAL_HEX, lw=1.5, rad=-0.3)
    ax.add_patch(FancyBboxPatch((0.03, 0.15), 0.94, 0.12,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=AMBER_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.text(0.5, 0.22, "Los arcos SON las identidades. No hay nodos separados.\nLa incidencia arco→arco crea linaje. La etiqueta compartida crea identidad.",
            fontsize=11, color=AMBER_HEX, weight="bold", ha="center", va="center", zorder=5, linespacing=1.5)
    save_fig(f, os.path.join(ASSETS_DIR, "slide_11_box_kernel.png"))


def diag_slide_12_box_rules():
    f, ax = canvas_fig(12, 5)
    st = Stack(ax, 0.02, 0.96, 0.96, 12, 5)
    st.text("THE BOX — SEIS REGLAS", fs=8, color=FAINT_HEX, mono=True, pad=0.006)
    st.text("Ninguna menciona identidad, linaje o comunidad. Emergen.", fs=16, color=INK_HEX, weight="bold", pad=0.03)
    rules = [
        ("R1", "transform", "Una transformación produce arcos"),
        ("R2", "label", "Cada arco lleva una etiqueta"),
        ("R3", "copy", "Las etiquetas se copian o se pierden"),
        ("R4", "match", "Los arcos se emparejan por etiqueta"),
        ("R5", "bind", "El emparejamiento crea un arco nuevo"),
        ("R6", "close", "Nada más está programado"),
    ]
    y = st.y
    for i, (code, name, desc) in enumerate(rules):
        yy = y - i * 0.12
        ax.add_patch(Rectangle((0.02, yy - 0.095), 0.0035, 0.07, facecolor=INDIGO_HEX, edgecolor="none", zorder=3))
        ax.text(0.038, yy - 0.012, f"{code}: {name}", fontsize=11.5, color=INK_HEX, weight="bold", va="top", zorder=6, family="DejaVu Sans Mono")
        ax.text(0.038, yy - 0.052, desc, fontsize=10, color=MUTED_HEX, va="top", zorder=6)
        if i < len(rules) - 1:
            ax.plot([0.02, 0.48], [yy - 0.1, yy - 0.1], color=EDGE_HEX, linewidth=0.5, zorder=2)
    ax.plot([0.50, 0.50], [y + 0.01, 0.12], color=EDGE_HEX, linewidth=0.8)
    xr = 0.53
    ax.text(xr, y, "LO QUE SE DERIVA (no programado)", fontsize=10, color=FAINT_HEX, family="DejaVu Sans Mono", va="top")
    derived = [
        ("identidad", "un objeto = historia de sus etiquetas", INDIGO_HEX),
        ("linaje", "de qué arco nació, y de cuál nació ése", TEAL_HEX),
        ("comunidad", "quién comparte etiqueta con quién", AMBER_HEX),
    ]
    for i, (name, gloss, color) in enumerate(derived):
        yy = y - 0.06 - i * 0.13
        bh = 0.10
        ax.add_patch(FancyBboxPatch((xr, yy - bh + 0.02), 0.44, bh,
                                    boxstyle="round,pad=0,rounding_size=0.006",
                                    linewidth=0.9, edgecolor=EDGE_HEX, facecolor=PANEL_HEX, zorder=2))
        ax.add_patch(Rectangle((xr, yy - bh + 0.02), 0.003, bh, facecolor=color, edgecolor="none", zorder=3))
        ax.text(xr + 0.015, yy, name, fontsize=11, color=INK_HEX, weight="bold", va="top", zorder=6, family="DejaVu Sans Mono")
        ax.text(xr + 0.015, yy - 0.04, gloss, fontsize=9.5, color=MUTED_HEX, va="top", zorder=6)
    save_fig(f, os.path.join(ASSETS_DIR, "slide_12_box_rules.png"))


def diag_slide_13_box_identity():
    f, ax = canvas_fig(12, 4.5)
    st = Stack(ax, 0.02, 0.96, 0.96, 12, 4.5)
    st.text("EMERGENCIA DE IDENTIDAD", fs=8, color=FAINT_HEX, mono=True, pad=0.006)
    st.text("R1+R2+R3+R4 → identidad como historia de etiquetas", fs=16, color=INK_HEX, weight="bold", pad=0.03)
    steps = [
        ("t=0", "Arco A creado\nι=α (nueva)"),
        ("t=1", "transform(A) → Arco B\nι=α (copia por R3)"),
        ("t=2", "transform(B) → Arco C\nι=α (copia por R3)"),
        ("t=3", "match(A, C) por ι=α\n→ Arco D (R5)"),
    ]
    y = 0.75
    for i, (t, desc) in enumerate(steps):
        x = 0.05 + i * 0.23
        ax.add_patch(FancyBboxPatch((x, y - 0.12), 0.20, 0.12,
                                    boxstyle="round,pad=0,rounding_size=0.008",
                                    linewidth=1.5 if i==0 else 1, edgecolor=INDIGO_HEX if i==0 else TEAL_HEX, facecolor=PANEL_HEX, zorder=2))
        ax.text(x + 0.1, y - 0.02, t, fontsize=10, color=AMBER_HEX, weight="bold", ha="center", va="top", zorder=5, family="DejaVu Sans Mono")
        ax.text(x + 0.1, y - 0.06, desc, fontsize=9, color=MUTED_HEX, ha="center", va="top", zorder=5, linespacing=1.3, family="DejaVu Sans Mono")
        if i < len(steps) - 1:
            arrow(ax, (x + 0.20, y - 0.06), (x + 0.23, y - 0.06), color=FAINT_HEX, lw=1)
    ax.add_patch(FancyBboxPatch((0.02, 0.12), 0.96, 0.18,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=AMBER_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.text(0.5, 0.23, "Identidad = clase de equivalencia por ι compartida.\nNo hay 'objeto' separado. El objeto ES la historia de ι.",
            fontsize=12, color=AMBER_HEX, weight="bold", ha="center", va="center", zorder=5, linespacing=1.5)
    ax.text(0.5, 0.06, "Medible: contar arcos con ι idéntica. Reproducible: misma semilla → misma historia.",
            fontsize=9, color=MUTED_HEX, ha="center", va="center", zorder=5, linespacing=1.5)
    save_fig(f, os.path.join(ASSETS_DIR, "slide_13_box_identity.png"))


def diag_slide_14_box_experiments():
    f, ax = canvas_fig(12, 5)
    st = Stack(ax, 0.02, 0.96, 0.96, 12, 5)
    st.text("EXPERIMENTOS CONTROLADOS: R1, R5, R6", fs=8, color=FAINT_HEX, mono=True, pad=0.006)
    st.text("Tres experimentos, un hallazgo admitido, dos defectos estructurales", fs=16, color=INK_HEX, weight="bold", pad=0.03)
    # R1
    ax.add_patch(FancyBboxPatch((0.02, 0.65), 0.47, 0.28,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=INDIGO_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.text(0.04, 0.88, "R1: DESCEND gate", fontsize=11, color=INDIGO_HEX, weight="bold", family="DejaVu Sans Mono")
    ax.text(0.04, 0.82, "Hipótesis: gate descendente evita punto fijo prematuro", fontsize=9, color=MUTED_HEX)
    ax.text(0.04, 0.75, "Resultado: mean_depth sobrevive (p=0.00111, n=10k)", fontsize=9.5, color=TEAL_HEX, weight="bold")
    ax.text(0.04, 0.69, "Mecanismo: perturbación periódica inyecta entropía controlada", fontsize=9, color=MUTED_HEX)
    # R5
    ax.add_patch(FancyBboxPatch((0.51, 0.65), 0.47, 0.28,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=TEAL_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.text(0.53, 0.88, "R5: Perturbación periódica", fontsize=11, color=TEAL_HEX, weight="bold", family="DejaVu Sans Mono")
    ax.text(0.53, 0.82, "Sin perturbación → FIXED_POINT (absorbido)", fontsize=9, color=MUTED_HEX)
    ax.text(0.53, 0.75, "Con perturbación → never settles (vivo)", fontsize=9.5, color=AMBER_HEX, weight="bold")
    ax.text(0.53, 0.69, "Fenómeno: la estructura se sostiene por interrupción externa", fontsize=9, color=MUTED_HEX)
    # R6
    ax.add_patch(FancyBboxPatch((0.02, 0.34), 0.47, 0.28,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=AMBER_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.text(0.04, 0.57, "R6: Semilla → determinismo", fontsize=11, color=AMBER_HEX, weight="bold", family="DejaVu Sans Mono")
    ax.text(0.04, 0.51, "splitmix64: misma semilla → misma traza completa", fontsize=9, color=MUTED_HEX)
    ax.text(0.04, 0.45, "Verificable: hash de traza completa reproducible", fontsize=9, color=MUTED_HEX)
    # Defects
    ax.add_patch(FancyBboxPatch((0.51, 0.34), 0.47, 0.28,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=RED_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.add_patch(Rectangle((0.51, 0.34), 0.0035, 0.28, facecolor=RED_HEX, edgecolor="none", zorder=3))
    ax.text(0.53, 0.57, "DEFECTOS ESTRUCTURALES", fontsize=11, color=RED_HEX, weight="bold", family="DejaVu Sans Mono")
    ax.text(0.53, 0.51, "• since_inflow: semántica ambigua en emparejamiento", fontsize=9, color=MUTED_HEX)
    ax.text(0.53, 0.45, "• Rule.to_dict(): omisión rompe serialización completa", fontsize=9, color=MUTED_HEX)
    ax.text(0.53, 0.39, "Ambos bloquean generalidad más allá de experimentos controlados", fontsize=8.5, color=FAINT_HEX, style="italic")
    save_fig(f, os.path.join(ASSETS_DIR, "slide_14_box_experiments.png"))


def diag_slide_15_box_ts():
    f, ax = canvas_fig(12, 4)
    st = Stack(ax, 0.02, 0.96, 0.96, 12, 4)
    st.text("PUERTO TYPESCRIPT — FIDELIDAD NIVEL 3", fs=8, color=FAINT_HEX, mono=True, pad=0.006)
    st.text("Estructura idéntica, hashes divergentes — la diferencia está declarada", fs=15, color=INK_HEX, weight="bold", pad=0.03)
    # Rust
    ax.add_patch(FancyBboxPatch((0.02, 0.15), 0.47, 0.75,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=EDGE_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.add_patch(Rectangle((0.02, 0.15), 0.0035, 0.75, facecolor=INDIGO_HEX, edgecolor="none", zorder=3))
    ax.text(0.04, 0.85, "RUST (referencia)", fontsize=10, color=INDIGO_HEX, weight="bold", family="DejaVu Sans Mono")
    rust_props = [
        "ArcIncidenceGraph: Vec<Arc>, incidence: Vec<Vec<usize>>",
        "Label: u64 (splitmix64 determinista)",
        "since_inflow: Option<usize> — semántica precisa",
        "Rule.to_dict(): serialización completa",
        "Hash de traza: blake3 determinista",
        "100% pruebas propiedad (proptest)",
    ]
    y = 0.78
    for p in rust_props:
        ax.text(0.04, y, f"• {p}", fontsize=9, color=MUTED_HEX, family="DejaVu Sans Mono")
        y -= 0.055
    # TS
    ax.add_patch(FancyBboxPatch((0.51, 0.15), 0.47, 0.75,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=EDGE_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.add_patch(Rectangle((0.51, 0.15), 0.0035, 0.75, facecolor=TEAL_HEX, edgecolor="none", zorder=3))
    ax.text(0.53, 0.85, "TYPESCRIPT (puerto)", fontsize=10, color=TEAL_HEX, weight="bold", family="DejaVu Sans Mono")
    ts_props = [
        "ArcIncidenceGraph: Arc[], incidence: number[][]",
        "Label: bigint (splitmix64 portado)",
        "since_inflow: number | null — SEMÁNTICA AMBIGUA",
        "Rule.to_dict(): AUSENTE (defecto conocido)",
        "Hash de traza: N/A (no comparable byte a byte)",
        "Estructura validada: mismos conteos, mismas relaciones",
    ]
    y = 0.78
    for p in ts_props:
        ax.text(0.53, y, f"• {p}", fontsize=9, color=MUTED_HEX, family="DejaVu Sans Mono")
        y -= 0.055
    # Fidelity badge
    ax.add_patch(FancyBboxPatch((0.02, 0.02), 0.96, 0.10,
                                boxstyle="round,pad=0,rounding_size=0.006",
                                linewidth=1, edgecolor=AMBER_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.text(0.5, 0.07, "NIVEL 3 — Reconstrucción parcial: estructura reproducida, serialización y since_inflow documentados como ausentes",
            fontsize=10, color=AMBER_HEX, weight="bold", ha="center", va="center", family="DejaVu Sans Mono")
    save_fig(f, os.path.join(ASSETS_DIR, "slide_15_box_ts.png"))


def diag_slide_16_box_limitations():
    f, ax = canvas_fig(12, 4)
    st = Stack(ax, 0.02, 0.96, 0.96, 12, 4)
    st.text("THE BOX — LIMITACIONES HONESTAS", fs=8, color=FAINT_HEX, mono=True, pad=0.006)
    st.text("Veredicto: «mecanismo explicado, sin descubrimiento»", fs=16, color=INK_HEX, weight="bold", pad=0.03)
    limits = [
        ("Sin generalidad", "Los dos defectos (since_inflow, Rule.to_dict) impiden\nusar el sustrato fuera de experimentos controlados.", RED_HEX),
        ("Sin hardware", "Ni sensores, ni actuadores, ni entorno físico.\nTodo es simulación determinista en memoria.", RED_HEX),
        ("Sin aprendizaje", "No hay actualización de pesos, gradientes, plasticidad.\nLa estructura es fija por reglas R1–R6.", RED_HEX),
        ("Una métrica admitida", "mean_depth bajo perturbación (p=0.00111).\nExplicado por mecanismo DESCEND, no descubierto.", AMBER_HEX),
        ("Sin comparación externa", "No hay baseline vs. redes neuronales, grafos, autómatas.\nEl sustrato solo se compara consigo mismo.", FAINT_HEX),
        ("Puerto TS = nivel 3", "Estructura validada, serialización ausente.\nNo afirmo equivalencia de hashes cross-language.", FAINT_HEX),
    ]
    y = st.y
    for i, (title, desc, color) in enumerate(limits):
        yy = y - i * 0.13
        ax.add_patch(Rectangle((0.02, yy - 0.11), 0.0035, 0.09, facecolor=color, edgecolor="none", zorder=3))
        ax.text(0.038, yy - 0.01, title, fontsize=11, color=INK_HEX, weight="bold", va="top", zorder=6)
        ax.text(0.038, yy - 0.05, desc, fontsize=9, color=MUTED_HEX, va="top", zorder=6, linespacing=1.4)
    ax.text(0.02, 0.04, "La honestidad sobre lo que NO hace el sistema es parte del método.",
            fontsize=9, color=FAINT_HEX, style="italic")
    save_fig(f, os.path.join(ASSETS_DIR, "slide_16_box_limitations.png"))


def diag_slide_20_singularity_arch():
    f, ax = canvas_fig(12, 5)
    st = Stack(ax, 0.02, 0.96, 0.96, 12, 5)
    st.text("SINGULARITY — ARQUITECTURA DE AGENTES", fs=8, color=FAINT_HEX, mono=True, pad=0.006)
    st.text("Cinco agentes especializados, verificación independiente, sin confianza mutua", fs=15, color=INK_HEX, weight="bold", pad=0.03)
    ax.add_patch(FancyBboxPatch((0.35, 0.55), 0.30, 0.18,
                                boxstyle="round,pad=0,rounding_size=0.01",
                                linewidth=1.5, edgecolor=INDIGO_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.text(0.5, 0.67, "ORCHESTRATOR", fontsize=11, color=INDIGO_HEX, weight="bold", ha="center", va="center", family="DejaVu Sans Mono")
    ax.text(0.5, 0.59, "routing · lifecycle · contracts", fontsize=8.5, color=MUTED_HEX, ha="center", va="center")
    agents = [
        (0.05, 0.70, "PLANNER", "descomposición\nde tareas", INDIGO_HEX),
        (0.05, 0.38, "RESEARCHER", "búsqueda +\nsíntesis", TEAL_HEX),
        (0.55, 0.70, "CODER", "implementación\ndeterminista", AMBER_HEX),
        (0.55, 0.38, "CRITIC", "verificación\nindependiente", RED_HEX),
        (0.92, 0.54, "SYNTHESIZER", "integración +\nartefactos", PLUM_HEX),
    ]
    for x, y, name, desc, color in agents:
        ax.add_patch(FancyBboxPatch((x, y), 0.20, 0.25,
                                    boxstyle="round,pad=0,rounding_size=0.008",
                                    linewidth=1, edgecolor=color, facecolor=PANEL_HEX, zorder=2))
        ax.add_patch(Rectangle((x, y), 0.003, 0.25, facecolor=color, edgecolor="none", zorder=3))
        ax.text(x + 0.1, y + 0.18, name, fontsize=10, color=INK_HEX, weight="bold", ha="center", va="center", family="DejaVu Sans Mono")
        ax.text(x + 0.1, y + 0.08, desc, fontsize=8, color=MUTED_HEX, ha="center", va="center", linespacing=1.3)
        if name == "PLANNER":
            arrow(ax, (x + 0.20, y + 0.12), (0.35, 0.63), color=FAINT_HEX, lw=1, rad=-0.2)
        elif name == "RESEARCHER":
            arrow(ax, (x + 0.20, y + 0.12), (0.35, 0.58), color=FAINT_HEX, lw=1, rad=0.2)
        elif name == "CODER":
            arrow(ax, (x - 0.02, y + 0.12), (0.65, 0.63), color=FAINT_HEX, lw=1, rad=0.2)
        elif name == "CRITIC":
            arrow(ax, (x - 0.02, y + 0.12), (0.65, 0.58), color=FAINT_HEX, lw=1, rad=-0.2)
        elif name == "SYNTHESIZER":
            arrow(ax, (x - 0.02, y + 0.12), (0.65, 0.63), color=FAINT_HEX, lw=1)
    ax.add_patch(FancyBboxPatch((0.02, 0.08), 0.96, 0.14,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=GREEN_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.text(0.5, 0.16, "CAPA DE VERIFICACIÓN INDEPENDIENTE — Nunca confía en auto-reportes de agentes\nEjecuta pruebas de propiedad · Compara trazas · Valida contratos · Rechaza si no reproduce",
            fontsize=10, color=GREEN_HEX, weight="bold", ha="center", va="center", linespacing=1.5)
    save_fig(f, os.path.join(ASSETS_DIR, "slide_20_singularity_arch.png"))


def diag_slide_21_oracle_agents():
    f, ax = canvas_fig(12, 4.5)
    st = Stack(ax, 0.02, 0.96, 0.96, 12, 4.5)
    st.text("ORACLE — CINCO AGENTES, DOS ENTORNOS", fs=8, color=FAINT_HEX, mono=True, pad=0.006)
    st.text("Diseño experimental: aislamiento vs. colaboración", fs=15, color=INK_HEX, weight="bold", pad=0.03)
    agents = [
        ("NAVIGATOR", "exploración\ndirigida", INDIGO_HEX, "gridworld"),
        ("MAPPER", "construcción\nde mapa", TEAL_HEX, "gridworld"),
        ("PLANNER", "búsqueda de\npolítica óptima", AMBER_HEX, "gridworld"),
        ("EXECUTOR", "ejecución\ndeterminista", PLUM_HEX, "gridworld"),
        ("VERIFIER", "validación\nindependiente", GREEN_HEX, "ambos"),
    ]
    for i, (name, desc, color, env) in enumerate(agents):
        x = 0.03 + i * 0.19
        ax.add_patch(FancyBboxPatch((x, 0.55), 0.17, 0.35,
                                    boxstyle="round,pad=0,rounding_size=0.008",
                                    linewidth=1, edgecolor=color, facecolor=PANEL_HEX, zorder=2))
        ax.add_patch(Rectangle((x, 0.55), 0.003, 0.35, facecolor=color, edgecolor="none", zorder=3))
        ax.text(x + 0.085, 0.83, name, fontsize=9.5, color=color, weight="bold", ha="center", va="center", family="DejaVu Sans Mono")
        ax.text(x + 0.085, 0.72, desc, fontsize=8, color=MUTED_HEX, ha="center", va="center", linespacing=1.3)
        ax.text(x + 0.085, 0.58, f"env: {env}", fontsize=7.5, color=FAINT_HEX, ha="center", va="center", family="DejaVu Sans Mono")
    ax.add_patch(FancyBboxPatch((0.03, 0.12), 0.47, 0.35,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=INDIGO_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.text(0.265, 0.42, "PROTOCOLO A — AISLAMIENTO", fontsize=10, color=INDIGO_HEX, weight="bold", ha="center", va="center")
    ax.text(0.265, 0.35, "Cada agente ejecuta su rol sin comunicación.\nVerificador valida salida de cada uno.", fontsize=8.5, color=MUTED_HEX, ha="center", va="center", linespacing=1.4)
    ax.text(0.265, 0.20, "Hipótesis: línea base de rendimiento individual", fontsize=8, color=FAINT_HEX, ha="center", va="center", style="italic")
    ax.add_patch(FancyBboxPatch((0.51, 0.12), 0.47, 0.35,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=AMBER_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.text(0.745, 0.42, "PROTOCOLO B — COLABORACIÓN", fontsize=10, color=AMBER_HEX, weight="bold", ha="center", va="center")
    ax.text(0.745, 0.35, "Agentes intercambian mensajes estructurados.\nOrquestador coordina ciclo plan-ejecutar-verificar.", fontsize=8.5, color=MUTED_HEX, ha="center", va="center", linespacing=1.4)
    ax.text(0.745, 0.20, "Hipótesis: colaboración mejora rendimiento", fontsize=8, color=FAINT_HEX, ha="center", va="center", style="italic")
    save_fig(f, os.path.join(ASSETS_DIR, "slide_21_oracle_agents.png"))


def diag_slide_23_oracle_e1():
    f, ax = canvas_fig(12, 4.5)
    st = Stack(ax, 0.02, 0.96, 0.96, 12, 4.5)
    st.text("ORACLE E1 — RESULTADO NEGATIVO", fs=8, color=FAINT_HEX, mono=True, pad=0.006)
    st.text("Colaboración perjudica rendimiento. El dato contradice la hipótesis.", fs=15, color=INK_HEX, weight="bold", pad=0.03)
    protocols = ["Protocolo A\n(Aislamiento)", "Protocolo B\n(Colaboración)"]
    means = [0.78, 0.62]
    cis = [(0.74, 0.82), (0.57, 0.67)]
    colors = [INDIGO_HEX, AMBER_HEX]
    bar_w = 0.25
    for i, (label, mean, (lo, hi), color) in enumerate(zip(protocols, means, cis, colors)):
        x = 0.25 + i * 0.5
        ax.add_patch(Rectangle((x - bar_w/2, 0.15), bar_w, mean * 0.5,
                               facecolor=color, edgecolor="none", alpha=0.8, zorder=3))
        ax.plot([x, x], [lo * 0.5 + 0.15, hi * 0.5 + 0.15], color=color, lw=2, zorder=4)
        ax.plot([x - 0.03, x + 0.03], [lo * 0.5 + 0.15, lo * 0.5 + 0.15], color=color, lw=2)
        ax.plot([x - 0.03, x + 0.03], [hi * 0.5 + 0.15, hi * 0.5 + 0.15], color=color, lw=2)
        ax.text(x, 0.10, label, fontsize=10, color=INK_HEX, ha="center", va="top", linespacing=1.3)
        ax.text(x, mean * 0.5 + 0.18, f"{mean:.2f}", fontsize=11, color=color, weight="bold", ha="center", va="bottom")
    ax.plot([0.20, 0.20], [0.15, 0.65], color=EDGE_HEX, lw=0.8)
    for tick in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        ax.text(0.18, 0.15 + tick * 0.5, f"{tick:.1f}", fontsize=8, color=MUTED_HEX, ha="right", va="center")
    ax.add_patch(FancyBboxPatch((0.02, 0.55), 0.96, 0.38,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=RED_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.add_patch(Rectangle((0.02, 0.55), 0.0035, 0.38, facecolor=RED_HEX, edgecolor="none", zorder=3))
    ax.text(0.04, 0.88, "ANÁLISIS ESTADÍSTICO", fontsize=11, color=RED_HEX, weight="bold", family="DejaVu Sans Mono")
    stats = [
        "Δ = -0.16 (IC 95%: -0.21 a -0.11), p < 0.001, n=500 semillas/protocolo",
        "Test: Mann-Whitney U (no paramétrico, distribuciones no normales)",
        "Tamaño de efecto: Cliff's δ = -0.47 (efecto medio-grande)",
        "Potencia post-hoc: 0.99 (α=0.05, dos colas)",
        "Verificación: bootstrap 10k réplicas confirma IC",
        "Conclusión: Comunicación introduce overhead de coordinación\nque supera ganancia de información compartida en este dominio",
    ]
    y = 0.80
    for s in stats:
        ax.text(0.04, y, f"• {s}", fontsize=9, color=MUTED_HEX if not s.startswith("Conclusión") else FAINT_HEX, family="DejaVu Sans Mono", linespacing=1.4)
        y -= 0.055
    save_fig(f, os.path.join(ASSETS_DIR, "slide_23_oracle_e1.png"))


def diag_slide_28_hermes_arch():
    f, ax = canvas_fig(12, 5)
    st = Stack(ax, 0.02, 0.96, 0.96, 12, 5)
    st.text("HERMES — 9 TIPOS DE AGENTE, ORQUESTADOR", fs=8, color=FAINT_HEX, mono=True, pad=0.006)
    st.text("Autonomía por diseño, intervención automática, métricas de deriva", fs=15, color=INK_HEX, weight="bold", pad=0.03)
    agent_types = [
        ("OBSERVER", "monitoreo\npasivo", INDIGO_HEX),
        ("ANALYZER", "detección\npatrones", TEAL_HEX),
        ("PLANNER", "generación\nopciones", AMBER_HEX),
        ("EXECUTOR", "ejecución\ndeterminista", PLUM_HEX),
        ("VALIDATOR", "verificación\ncontratos", GREEN_HEX),
        ("CORRECTOR", "reparación\nautomatizada", RED_HEX),
        ("SYNCHRONIZER", "consistencia\ndistribuida", INDIGO_HEX),
        ("ARCHIVIST", "trazabilidad\ncompleta", TEAL_HEX),
        ("GOVERNOR", "políticas +\nlímites", AMBER_HEX),
    ]
    for i, (name, desc, color) in enumerate(agent_types):
        row = i // 3
        col = i % 3
        x = 0.03 + col * 0.32
        y = 0.62 - row * 0.18
        ax.add_patch(FancyBboxPatch((x, y), 0.30, 0.16,
                                    boxstyle="round,pad=0,rounding_size=0.006",
                                    linewidth=0.8, edgecolor=color, facecolor=PANEL_HEX, zorder=2))
        ax.add_patch(Rectangle((x, y), 0.003, 0.16, facecolor=color, edgecolor="none", zorder=3))
        ax.text(x + 0.01, y + 0.10, name, fontsize=8.5, color=color, weight="bold", va="top", family="DejaVu Sans Mono")
        ax.text(x + 0.01, y + 0.03, desc, fontsize=7.5, color=MUTED_HEX, va="top", linespacing=1.2)
    ax.add_patch(FancyBboxPatch((0.03, 0.08), 0.94, 0.18,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1.5, edgecolor=GREEN_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.text(0.5, 0.21, "ORQUESTADOR: routing por contrato · ciclo de vida · reglas de autonomía · intervenciones automáticas (drift > umbral)",
            fontsize=10, color=GREEN_HEX, weight="bold", ha="center", va="center")
    ax.text(0.5, 0.13, "Métricas: latencia P99, tasa de intervención, deriva semántica, reproducibilidad de traza",
            fontsize=9, color=MUTED_HEX, ha="center", va="center")
    save_fig(f, os.path.join(ASSETS_DIR, "slide_28_hermes_arch.png"))


def diag_slide_37_synthesis():
    f, ax = canvas_fig(12, 4.5)
    st = Stack(ax, 0.02, 0.96, 0.96, 12, 4.5)
    st.text("TRES SUSTRATOS, UNA FILOSOFÍA", fs=8, color=FAINT_HEX, mono=True, pad=0.006)
    st.text("The Box · SINGULARITY/ORACLE · HERMES — misma disciplina de verificación", fs=15, color=INK_HEX, weight="bold", pad=0.03)
    substrates = [
        ("THE BOX", "Sustrato generativo\nmínimo", "Reglas R1–R6 → identidad,\nlinaje, comunidad", "Nivel 3 (TS)\nMecanismo explicado", INDIGO_HEX, "CL-0001,0004,0006"),
        ("SINGULARITY/\nORACLE", "Sistema multi-agente\ncon verificación", "5 agentes + verificador\nindependiente", "E1: resultado\nnegativo verificado", TEAL_HEX, "CL-0009,0010,0011"),
        ("HERMES", "Orquestación\noperacional", "9 agentes + governor +\nintervención automática", "Especificación\n(SPECULATIVO)", AMBER_HEX, "CL-0019,0020,0021"),
    ]
    for i, (name, desc, mechanism, fidelity, color, refs) in enumerate(substrates):
        x = 0.02 + i * 0.325
        ax.add_patch(FancyBboxPatch((x, 0.12), 0.30, 0.78,
                                    boxstyle="round,pad=0,rounding_size=0.008",
                                    linewidth=1, edgecolor=color, facecolor=PANEL_HEX, zorder=2))
        ax.add_patch(Rectangle((x, 0.12), 0.0035, 0.78, facecolor=color, edgecolor="none", zorder=3))
        ax.text(x + 0.15, 0.85, name, fontsize=12, color=color, weight="bold", ha="center", va="top", family="DejaVu Sans Mono")
        ax.text(x + 0.15, 0.75, desc, fontsize=9, color=MUTED_HEX, ha="center", va="top", linespacing=1.3)
        ax.text(x + 0.15, 0.60, mechanism, fontsize=9, color=INK_HEX, ha="center", va="top", linespacing=1.4)
        ax.add_patch(FancyBboxPatch((x + 0.02, 0.38), 0.26, 0.14,
                                    boxstyle="round,pad=0,rounding_size=0.006",
                                    linewidth=1, edgecolor=color, facecolor=PANEL_2_HEX, zorder=3))
        ax.text(x + 0.15, 0.47, fidelity, fontsize=9, color=color, weight="bold", ha="center", va="center", linespacing=1.3)
        ax.text(x + 0.15, 0.22, refs, fontsize=7.5, color=FAINT_HEX, ha="center", va="top", family="DejaVu Sans Mono")
    ax.add_patch(FancyBboxPatch((0.02, 0.02), 0.96, 0.08,
                                boxstyle="round,pad=0,rounding_size=0.006",
                                linewidth=1, edgecolor=AMBER_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.text(0.5, 0.06, "HILO COMÚN: Verificación independiente · Fidelidad declarada · Resultados negativos publicados · Defectos documentados",
            fontsize=9.5, color=AMBER_HEX, weight="bold", ha="center", va="center", family="DejaVu Sans Mono")
    save_fig(f, os.path.join(ASSETS_DIR, "slide_37_synthesis.png"))


def diag_slide_40_limitations_heatmap():
    f, ax = canvas_fig(12, 4)
    st = Stack(ax, 0.02, 0.96, 0.96, 12, 4)
    st.text("MAPA DE LIMITACIONES — TRES SUSTRATOS", fs=8, color=FAINT_HEX, mono=True, pad=0.006)
    st.text("Rojo = bloquea generalidad · Ámbar = reduce alcance · Gris = documentado", fs=14, color=INK_HEX, weight="bold", pad=0.03)
    rows = [
        "Defectos estructurales",
        "Sin hardware / entorno real",
        "Sin aprendizaje / plasticidad",
        "Sin baseline externo",
        "Serialización incompleta",
        "Verificación no exhaustiva",
        "Especificación no implementada",
        "Métricas de deriva no validadas",
    ]
    cols = ["The Box", "ORACLE", "HERMES"]
    severity = [
        [3, 0, 0],
        [3, 2, 2],
        [3, 1, 1],
        [3, 2, 2],
        [3, 1, 0],
        [1, 2, 2],
        [0, 0, 3],
        [0, 0, 2],
    ]
    cell_w, cell_h = 0.25, 0.095
    start_x, start_y = 0.15, 0.85
    sev_colors = {0: BG_HEX, 1: FAINT_HEX, 2: AMBER_HEX, 3: RED_HEX}
    for j, col in enumerate(cols):
        x = start_x + j * cell_w
        ax.text(x + cell_w/2, start_y + 0.03, col, fontsize=10, color=INK_HEX, weight="bold", ha="center", va="bottom", family="DejaVu Sans Mono")
    for i, row in enumerate(rows):
        y = start_y - i * cell_h
        ax.text(start_x - 0.01, y + cell_h/2, row, fontsize=8.5, color=MUTED_HEX, ha="right", va="center")
        for j in range(3):
            x = start_x + j * cell_w
            s = severity[i][j]
            fc = sev_colors[s]
            ax.add_patch(Rectangle((x, y), cell_w, cell_h, facecolor=fc, edgecolor=EDGE_HEX, linewidth=0.5, zorder=2))
            if s > 0:
                labels = {1: "doc", 2: "alcance", 3: "bloquea"}
                ax.text(x + cell_w/2, y + cell_h/2, labels[s], fontsize=7.5, color=INK_HEX if s<3 else BG_HEX, weight="bold", ha="center", va="center")
    ax.text(0.02, 0.05, "LEYENDA:  █ bloquea generalidad    █ reduce alcance    █ documentado    █ no aplica",
            fontsize=8.5, color=MUTED_HEX, family="DejaVu Sans Mono")
    save_fig(f, os.path.join(ASSETS_DIR, "slide_40_limitations_heatmap.png"))


def diag_slide_41_open_problems():
    f, ax = canvas_fig(12, 4.5)
    st = Stack(ax, 0.02, 0.96, 0.96, 12, 4.5)
    st.text("PROBLEMAS ABIERTOS — LÍNEAS DE INVESTIGACIÓN", fs=8, color=FAINT_HEX, mono=True, pad=0.006)
    st.text("Preguntas que el trabajo actual no resuelve y que guían lo siguiente", fs=15, color=INK_HEX, weight="bold", pad=0.03)
    problems = [
        ("P1", "Generalidad del sustrato The Box", "Resolver since_inflow + Rule.to_dict → ¿permite composición recursiva arbitraria?", INDIGO_HEX),
        ("P2", "Colaboración efectiva en multi-agente", "E1 muestra overhead > ganancia. ¿Qué topologías/contratos invierten la desigualdad?", TEAL_HEX),
        ("P3", "Verificación de propiedades emergentes", "Hoy: verificación estructural. Mañana: verificación semántica de identidad/linaje.", AMBER_HEX),
        ("P4", "Puente simulación → hardware", "The Box es puro software. ¿Qué mínima interfaz sensor/actuador preserva determinismo?", PLUM_HEX),
        ("P5", "Métricas de deriva en HERMES", "Drift semántico definido pero no validado empíricamente. ¿Cómo medir sin ground truth?", RED_HEX),
        ("P6", "Reproducibilidad cross-language", "Rust ↔ TS estructura OK, hashes divergen. ¿Nivel 2 alcanzable sin serialización binaria?", FAINT_HEX),
    ]
    y = st.y
    for i, (code, title, question, color) in enumerate(problems):
        yy = y - i * 0.13
        ax.add_patch(Rectangle((0.02, yy - 0.11), 0.0035, 0.09, facecolor=color, edgecolor="none", zorder=3))
        ax.text(0.038, yy - 0.008, f"{code}: {title}", fontsize=11, color=INK_HEX, weight="bold", va="top", zorder=6)
        ax.text(0.038, yy - 0.05, question, fontsize=9.5, color=MUTED_HEX, va="top", zorder=6, linespacing=1.4)
    save_fig(f, os.path.join(ASSETS_DIR, "slide_41_open_problems.png"))


def diag_slide_43_repro():
    f, ax = canvas_fig(12, 4)
    st = Stack(ax, 0.02, 0.96, 0.96, 12, 4)
    st.text("ARTEFACTOS DE REPRODUCIBILIDAD", fs=8, color=FAINT_HEX, mono=True, pad=0.006)
    st.text("Cada claim en esta presentación es reproducible con estos comandos", fs=15, color=INK_HEX, weight="bold", pad=0.03)
    artifacts = [
        ("The Box (Rust)", "cargo test --package the-box -- --nocapture\ncargo run --example r1_descend -- --seeds 10000\ncargo run --example r5_perturb -- --seeds 10000", INDIGO_HEX),
        ("The Box (TypeScript)", "cd the-box-ts && npm test\nnpm run verify:structure -- --compare-rust", TEAL_HEX),
        ("ORACLE E1", "cd oracle && python -m pytest experiments/e1_negative.py -v\npython -m pytest experiments/e1_negative.py --bootstrap 10000", AMBER_HEX),
        ("Showcase", "cd showcase && npm run test && npm run build\n# 182 tests, 160.69 kB JS, zero runtime deps", PLUM_HEX),
        ("SINGULARITY", "cd singularity && cargo test --workspace\ncargo run --example orchestrator_demo", INDIGO_HEX),
        ("HERMES (spec)", "cat hermes/SPEC.md  # especificación completa, no implementada", FAINT_HEX),
    ]
    y = st.y
    for name, cmds, color in artifacts:
        ax.add_patch(Rectangle((0.02, y - 0.055), 0.0035, 0.05, facecolor=color, edgecolor="none", zorder=3))
        ax.text(0.038, y - 0.008, name, fontsize=10, color=color, weight="bold", va="top", zorder=6, family="DejaVu Sans Mono")
        ax.text(0.038, y - 0.04, cmds, fontsize=8, color=MUTED_HEX, va="top", zorder=6, family="DejaVu Sans Mono", linespacing=1.3)
        y -= 0.12
    ax.text(0.02, 0.03, "Repositorio: github.com/ThorrijaDEV  ·  Todos los experimentos versionados con semillas fijas.",
            fontsize=9, color=FAINT_HEX, style="italic")
    save_fig(f, os.path.join(ASSETS_DIR, "slide_43_repro.png"))


def generate_all_diagrams():
    print("Generating diagrams...")
    diag_slide_03_thesis(); print("  slide_03_thesis.png")
    diag_slide_04_landscape(); print("  slide_04_landscape.png")
    diag_slide_05_fidelity(); print("  slide_05_fidelity.png")
    diag_slide_11_box_kernel(); print("  slide_11_box_kernel.png")
    diag_slide_12_box_rules(); print("  slide_12_box_rules.png")
    diag_slide_13_box_identity(); print("  slide_13_box_identity.png")
    diag_slide_14_box_experiments(); print("  slide_14_box_experiments.png")
    diag_slide_15_box_ts(); print("  slide_15_box_ts.png")
    diag_slide_16_box_limitations(); print("  slide_16_box_limitations.png")
    diag_slide_20_singularity_arch(); print("  slide_20_singularity_arch.png")
    diag_slide_21_oracle_agents(); print("  slide_21_oracle_agents.png")
    diag_slide_23_oracle_e1(); print("  slide_23_oracle_e1.png")
    diag_slide_28_hermes_arch(); print("  slide_28_hermes_arch.png")
    diag_slide_37_synthesis(); print("  slide_37_synthesis.png")
    diag_slide_40_limitations_heatmap(); print("  slide_40_limitations_heatmap.png")
    diag_slide_41_open_problems(); print("  slide_41_open_problems.png")
    diag_slide_43_repro(); print("  slide_43_repro.png")
    print("All diagrams generated.")


# ──────────────────────────────────────────────────────────────────────────────
# SLIDE RENDERER (ReportLab)
# ──────────────────────────────────────────────────────────────────────────────

class SlideRenderer:
    def __init__(self, c: canvas.Canvas):
        self.c = c
        self.w, self.h = PAGE_W, PAGE_H

    def bg(self):
        self.c.setFillColor(BG)
        self.c.rect(0, 0, self.w, self.h, fill=1, stroke=0)

    def rule_h(self, y, x0=MARGIN, x1=None, color=EDGE, w=0.8):
        if x1 is None:
            x1 = self.w - MARGIN
        self.c.setStrokeColor(color)
        self.c.setLineWidth(w)
        self.c.line(x0, y, x1, y)

    def rule_v(self, x, y0, y1, color=EDGE, w=0.8):
        self.c.setStrokeColor(color)
        self.c.setLineWidth(w)
        self.c.line(x, y0, x, y1)

    def text(self, x, y, text, fs=14, color=INK, font=SANS_FAMILY, align=TA_LEFT, leading=None):
        style = ParagraphStyle('tmp', fontName=font, fontSize=fs, leading=leading or fs*1.3,
                               textColor=color, alignment=align)
        p = Paragraph(text, style)
        w, h = p.wrap(self.w - 2*MARGIN, self.h)
        p.drawOn(self.c, x, y - h)
        return h

    def mono(self, x, y, text, fs=12, color=INK, align=TA_LEFT):
        return self.text(x, y, text, fs, color, MONO_FAMILY, align)

    def badge(self, x, y, label, fs=10, color=AMBER, bg=PANEL, pad_x=8, pad_y=3):
        self.c.setFillColor(bg)
        self.c.setStrokeColor(EDGE)
        self.c.setLineWidth(0.5)
        tw = self.c.stringWidth(label, MONO_FAMILY, fs) + 2*pad_x
        th = fs + 2*pad_y
        self.c.roundRect(x, y - th + pad_y, tw, th, 3, fill=1, stroke=1)
        self.c.setFillColor(color)
        self.c.setFont(MONO_FAMILY, fs)
        self.c.drawString(x + pad_x, y - fs - pad_y + 2, label)

    def panel_box(self, x, y, w, h, fc=PANEL, ec=EDGE, accent=None):
        self.c.setFillColor(fc)
        self.c.setStrokeColor(ec)
        self.c.setLineWidth(0.8)
        self.c.roundRect(x, y, w, h, 4, fill=1, stroke=1)
        if accent:
            self.c.setFillColor(accent)
            self.c.rect(x, y, 3, h, fill=1, stroke=0)

    def image(self, x, y, img_path, max_w=None, max_h=None):
        from PIL import Image
        im = Image.open(img_path)
        iw, ih = im.size
        if max_w and iw > max_w:
            scale = max_w / iw
            iw, ih = max_w, ih * scale
        if max_h and ih > max_h:
            scale = max_h / ih
            iw, ih = iw * scale, max_h
        self.c.drawImage(img_path, x, y - ih, width=iw, height=ih, preserveAspectRatio=True, mask='auto')
        return iw, ih

    def footer(self, slide_num: int, total: int, tag: str = ""):
        self.c.setFont(MONO_FAMILY, 9)
        self.c.setFillColor(FAINT)
        left = f"{slide_num}/{total}"
        right = tag
        self.c.drawString(MARGIN, MARGIN/2, left)
        tw = self.c.stringWidth(right, MONO_FAMILY, 9)
        self.c.drawString(self.w - MARGIN - tw, MARGIN/2, right)


# ──────────────────────────────────────────────────────────────────────────────
# SLIDE DEFINITIONS
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class Slide:
    num: int
    title: str
    content_fn: Callable[['SlideRenderer'], None]
    diagram: Optional[str] = None
    speaker_notes: str = ""
    qa: List[str] = None

    def __post_init__(self):
        if self.qa is None:
            self.qa = []


def render_wrapped_code(r: SlideRenderer, code: str, x: float, y: float, max_w: float):
    lines = code.strip().split("\n")
    r.c.setFont(MONO_FAMILY, 8.5)
    r.c.setFillColor(MUTED)
    line_h = 11
    for i, line in enumerate(lines):
        if y - i * line_h < MARGIN + 20:
            break
        if len(line) > 100:
            for chunk in [line[j:j+100] for j in range(0, len(line), 100)]:
                r.c.drawString(x, y - i * line_h, chunk)
                i += 1
        else:
            r.c.drawString(x, y - i * line_h, line)


def make_slides() -> List[Slide]:
    slides = []

    # ─── ACT 1: ORIENTATION (Slides 1-9) ───
    slides.append(Slide(
        num=1, title="THORRIJA",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(SANS_BOLD, 72), r.c.setFillColor(INK),
            r.c.drawCentredString(r.w/2, r.h*0.55, "THORRIJA"),
            r.c.setFont(MONO_FAMILY, 20), r.c.setFillColor(MUTED),
            r.c.drawCentredString(r.w/2, r.h*0.45, "Nota de presentación — Equipo de investigación IA"),
            r.c.setFont(MONO_FAMILY, 12), r.c.setFillColor(FAINT),
            r.c.drawCentredString(r.w/2, r.h*0.35, "Noviembre 2026"),
            r.rule_h(r.h*0.3, color=AMBER),
            r.c.setFont(MONO_FAMILY, 11), r.c.setFillColor(AMBER),
            r.c.drawCentredString(r.w/2, r.h*0.25, "github.com/ThorrijaDEV  ·  thorrijadev.github.io/showcase"),
            r.footer(1, 45, "THORRIJA")
        ),
        speaker_notes="Portada. No leer el título. Esperar silencio. 'Esta presentación no es sobre ideas. Es sobre sistemas que se pueden ejecutar, medir y refutar.' Pausa. 'Veinticuatro proyectos. Cuatro años. Una regla: nada se afirma sin evidencia.'",
        qa=["¿Cuál es tu formación académica?", "¿En qué empresa trabajas actualmente?", "¿Por qué esta estética?"]
    ))

    slides.append(Slide(
        num=2, title="Posición",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(INDIGO),
            r.c.drawString(MARGIN, r.h - MARGIN, "01 — POSICIÓN"),
            r.c.setFont(SANS_BOLD, 36), r.c.setFillColor(INK),
            r.c.drawString(MARGIN, r.h - MARGIN - 60, "No vengo a presentar ideas."),
            r.c.drawString(MARGIN, r.h - MARGIN - 110, "Vengo a presentar sistemas"),
            r.c.drawString(MARGIN, r.h - MARGIN - 160, "que se pueden ejecutar, medir y refutar."),
            r.rule_h(r.h - MARGIN - 200, color=AMBER),
            r.c.setFont(MONO_FAMILY, 60), r.c.setFillColor(AMBER),
            r.c.drawString(MARGIN, r.h - MARGIN - 380, "24"),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(MUTED),
            r.c.drawString(MARGIN, r.h - MARGIN - 300, "proyectos construidos,\ncon su estado declarado"),
            r.c.setFont(MONO_FAMILY, 60), r.c.setFillColor(AMBER),
            r.c.drawString(r.w/2 - 100, r.h - MARGIN - 380, "182"),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(MUTED),
            r.c.drawString(r.w/2 - 100, r.h - MARGIN - 300, "pruebas automatizadas,\nverificadas esta semana"),
            r.c.setFont(MONO_FAMILY, 60), r.c.setFillColor(AMBER),
            r.c.drawString(r.w - MARGIN - 200, r.h - MARGIN - 380, "1"),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(MUTED),
            r.c.drawString(r.w - MARGIN - 200, r.h - MARGIN - 300, "regla: nada se afirma\nsin evidencia"),
            r.c.setFont(SANS_FAMILY, 16), r.c.setFillColor(INK),
            r.c.drawString(MARGIN, r.h - MARGIN - 500, "Esta presentación sigue el mismo orden:"),
            r.c.setFont(MONO_FAMILY, 16), r.c.setFillColor(INDIGO),
            r.c.drawString(MARGIN, r.h - MARGIN - 530, "AFIRMACIÓN → EVIDENCIA → VEREDICTO"),
            r.footer(2, 45, "POSICIÓN")
        ),
        speaker_notes="Slide de tesis. Cada número tiene peso. 24 proyectos — no ejercicios, no tutoriales. 182 tests — no coverage teatral, tests de propiedad que fallan si el comportamiento cambia. 1 regla — es la única que importa. Si no puedes ejecutar mi código y obtener el mismo resultado, no me creas. La estética oscura no es decoración: reduce ruido cognitivo. Los investigadores saben leer diagramas; no necesitan iconos.",
        qa=["¿Qué significa 'estado declarado'?", "¿Cómo defines 'refutar' en tu contexto?", "¿Por qué 182 tests exactamente?"]
    ))

    slides.append(Slide(
        num=3, title="Tesis del programa",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(INDIGO),
            r.c.drawString(MARGIN, r.h - MARGIN, "02 — TESIS DEL PROGRAMA"),
            r.image(MARGIN, r.h - MARGIN - 60, os.path.join(ASSETS_DIR, "slide_03_thesis.png"), max_w=r.w - 2*MARGIN),
            r.footer(3, 45, "TESIS")
        ),
        diagram="slide_03_thesis.png",
        speaker_notes="Tres pilares. Primero: el orden epistémico. Afirmación → Evidencia → Veredicto. No se invierte. Segundo: fidelidad declarada. Cada reconstrucción lleva su nivel. No hay 'casi funciona'. Tercero: resultados negativos publicados. ORACLE E1 muestra que colaboración perjudica. The Box: mecanismo explicado, sin descubrimiento. Dos defectos estructurales documentados. Esto no es humildad performativa; es ingeniería. Si no publicas lo que no funciona, no estás haciendo ciencia.",
        qa=["¿Por qué ese orden epistémico?", "¿Qué pasa si una reconstrucción no tiene nivel declarado?", "¿Cómo decides publicar un resultado negativo?"]
    ))

    slides.append(Slide(
        num=4, title="Paisaje de trabajo",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(INDIGO),
            r.c.drawString(MARGIN, r.h - MARGIN, "03 — PAISAJE DE TRABAJO"),
            r.image(MARGIN, r.h - MARGIN - 60, os.path.join(ASSETS_DIR, "slide_04_landscape.png"), max_w=r.w - 2*MARGIN),
            r.footer(4, 45, "PAISAJE")
        ),
        diagram="slide_04_landscape.png",
        speaker_notes="Veinticuatro proyectos, cinco categorías. Sistemas y redes (9): herramientas que leen /proc, DNS crudo, BPF — no wrappers bonitos. Reconstrucciones (4): cuatro modelos deterministas desde código fuente, cada uno con su nivel de fidelidad. Seguridad defensiva (3): canarios, detección local, reconocimiento autorizado — nada ofensivo. Líneas abiertas (5): trabajo en curso, documentado como tal. Experimentación (3): The Box, ORACLE/SINGULARITY, HERMES — son los tres sustratos que veremos en profundidad. Siete lenguajes. No por coleccionismo: cada uno se eligió por restricción técnica real.",
        qa=["¿Por qué Rust para The Box y TS para el puerto?", "¿Qué hay en 'líneas abiertas' exactamente?", "¿Cómo priorizas qué proyecto continuar?"]
    ))

    slides.append(Slide(
        num=5, title="Marco de fidelidad",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(INDIGO),
            r.c.drawString(MARGIN, r.h - MARGIN, "04 — MARCO DE FIDELIDAD"),
            r.image(MARGIN, r.h - MARGIN - 60, os.path.join(ASSETS_DIR, "slide_05_fidelity.png"), max_w=r.w - 2*MARGIN),
            r.footer(5, 45, "FIDELIDAD")
        ),
        diagram="slide_05_fidelity.png",
        speaker_notes="Cuatro niveles. Nivel 1: reproducción directa — mismas operaciones, mismas constantes, mismo orden. Los cuatro proyectos del Showcase son nivel 1. Nivel 2: reconstrucción fiel — comportamiento reproducido, pieza sustituida declarada. Nivel 3: reconstrucción parcial — lo entendido reproducido, lo demás documentado como ausente. The Box en TypeScript es nivel 3. Nivel 4: modelo conceptual — idea reproducida, no mecánica. La honestidad del nivel importa más que el nivel mismo. Un nivel 3 honesto vale más que un nivel 1 fingido.",
        qa=["¿Cómo validas que un nivel 1 es realmente nivel 1?", "¿Hay proyectos en nivel 2?", "¿Por qué no colapsar a binario (funciona/no funciona)?"]
    ))

    slides.append(Slide(
        num=6, title="Preguntas centrales",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(INDIGO),
            r.c.drawString(MARGIN, r.h - MARGIN, "05 — PREGUNTAS CENTRALES"),
            r.c.setFont(SANS_BOLD, 28), r.c.setFillColor(INK),
            r.c.drawString(MARGIN, r.h - MARGIN - 80, "¿Cómo verificas lo que construyes sin confiar en ti mismo?"),
            r.c.setFont(SANS_FAMILY, 18), r.c.setFillColor(MUTED),
            r.c.drawString(MARGIN, r.h - MARGIN - 140, "¿Qué minimalismo genera estructura sin programarla?"),
            r.c.drawString(MARGIN, r.h - MARGIN - 190, "¿Cuándo la colaboración entre agentes perjudica?"),
            r.c.drawString(MARGIN, r.h - MARGIN - 240, "¿Cómo mides deriva semántica sin ground truth?"),
            r.c.drawString(MARGIN, r.h - MARGIN - 290, "¿Qué defectos estructurales bloquean la generalidad?"),
            r.rule_h(r.h - MARGIN - 330, color=AMBER),
            r.c.setFont(SANS_FAMILY, 16), r.c.setFillColor(INK),
            r.c.drawString(MARGIN, r.h - MARGIN - 370, "Tres sustratos experimentales para abordarlas:"),
            r.c.setFont(MONO_FAMILY, 16), r.c.setFillColor(INDIGO),
            r.c.drawString(MARGIN + 40, r.h - MARGIN - 410, "THE BOX — sustrato generativo mínimo (reglas → estructura)"),
            r.c.setFont(MONO_FAMILY, 16), r.c.setFillColor(TEAL),
            r.c.drawString(MARGIN + 40, r.h - MARGIN - 450, "SINGULARITY/ORACLE — multi-agente + verificación independiente"),
            r.c.setFont(MONO_FAMILY, 16), r.c.setFillColor(AMBER),
            r.c.drawString(MARGIN + 40, r.h - MARGIN - 490, "HERMES — orquestación operacional (especificación)"),
            r.footer(6, 45, "PREGUNTAS")
        ),
        speaker_notes="Cinco preguntas. No son retóricas; cada una tiene un sustrato experimental. 1) Verificación sin confianza → motor de verificación independiente en SINGULARITY/ORACLE. 2) Minimalismo generativo → The Box (6 reglas → identidad/linaje/comunidad). 3) Colaboración perjudicial → ORACLE E1 (resultado negativo verificado). 4) Deriva semántica → HERMES (métricas definidas, no validadas). 5) Defectos estructurales → The Box (since_inflow, Rule.to_dict). Estas preguntas guían todo lo que sigue.",
        qa=["¿Por qué estas cinco y no otras?", "¿Qué significa 'ground truth' en deriva semántica?", "¿Cuál es la más difícil de responder?"]
    ))

    slides.append(Slide(
        num=7, title="Transición → The Box",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(INDIGO),
            r.c.drawString(MARGIN, r.h - MARGIN, "06 — ACTO 2: THE BOX"),
            r.rule_h(r.h - MARGIN - 50, color=INDIGO),
            r.c.setFont(SANS_BOLD, 42), r.c.setFillColor(INK),
            r.c.drawString(MARGIN, r.h - MARGIN - 150, "Sustrato generativo mínimo"),
            r.c.setFont(SANS_FAMILY, 20), r.c.setFillColor(MUTED),
            r.c.drawString(MARGIN, r.h - MARGIN - 220, "Seis reglas. Ninguna menciona identidad, linaje o comunidad."),
            r.c.drawString(MARGIN, r.h - MARGIN - 260, "Las tres emergen. Medibles. Reproducibles."),
            r.c.drawString(MARGIN, r.h - MARGIN - 300, "Un hallazgo admitido (p=0.00111). Dos defectos que bloquean generalidad."),
            r.c.drawString(MARGIN, r.h - MARGIN - 340, "Puerto TypeScript: nivel 3 — estructura idéntica, serialización ausente."),
            r.footer(7, 45, "THE BOX")
        ),
        speaker_notes="Transición al Acto 2. The Box es el sustrato más puro: seis reglas, nada más. Lo que veremos: el kernel formal (multigrafo arco-arco), las seis reglas, cómo emerge identidad, los experimentos controlados (R1, R5, R6), los dos defectos estructurales, el puerto TypeScript, y las limitaciones honestas. Veredicto final: mecanismo explicado, sin descubrimiento. Si esperas un paper de Nature, no está aquí. Si quieres ver ingeniería honesta, sí.",
        qa=["¿Por qué empezar con The Box?", "¿Qué significa 'mecanismo explicado'?", "¿Cuánto tiempo llevas en The Box?"]
    ))

    slides.append(Slide(
        num=8, title="The Box — Kernel formal",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(INDIGO),
            r.c.drawString(MARGIN, r.h - MARGIN, "07 — NÚCLEO FORMAL"),
            r.image(MARGIN, r.h - MARGIN - 60, os.path.join(ASSETS_DIR, "slide_11_box_kernel.png"), max_w=r.w - 2*MARGIN),
            r.footer(8, 45, "KERNEL")
        ),
        diagram="slide_11_box_kernel.png",
        speaker_notes="Kernel formal: G = (V, E, ι, λ, σ). V son arcos — no nodos. Cada arco ES una identidad + payload. E es incidencia dirigida: arco apunta a arco. ι es etiqueta de identidad (copia/pérdida por R3). λ es etiqueta de linaje (origen). σ es semilla determinista (splitmix64). No hay nodos separados. Los arcos SON las identidades. La incidencia arco→arco crea linaje. La etiqueta compartida crea identidad. Medible: contar arcos con ι idéntica. Reproducible: misma semilla → misma traza completa. Esto no es teoría de grafos decorativa; es la estructura de datos exacta que ejecuta el motor.",
        qa=["¿Por qué arcos y no nodos?", "¿Qué es splitmix64 y por qué no otro PRNG?", "¿Cómo serializas esto?"]
    ))

    slides.append(Slide(
        num=9, title="The Box — Seis reglas",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(INDIGO),
            r.c.drawString(MARGIN, r.h - MARGIN, "08 — SEIS REGLAS"),
            r.image(MARGIN, r.h - MARGIN - 60, os.path.join(ASSETS_DIR, "slide_12_box_rules.png"), max_w=r.w - 2*MARGIN),
            r.footer(9, 45, "REGLAS")
        ),
        diagram="slide_12_box_rules.png",
        speaker_notes="Seis reglas. R1: transform — una transformación produce arcos. R2: label — cada arco lleva una etiqueta. R3: copy — las etiquetas se copian o se pierden. R4: match — los arcos se emparejan por etiqueta. R5: bind — el emparejamiento crea un arco nuevo. R6: close — nada más está programado. Ninguna menciona identidad, linaje o comunidad. A la derecha: lo que se deriva. Identidad = historia de etiquetas compartidas. Linaje = de qué arco nació, y de cuál nació ése. Comunidad = quién comparte etiqueta con quién. Ninguna de las tres está escrita en las reglas. Se calculan después, sobre la traza, y se pueden medir.",
        qa=["¿Por qué R6 'nada más está programado'?", "¿Qué pasa si añades una séptima regla?", "¿Cómo validas que no hay comportamiento emergente no documentado?"]
    ))

    # ─── ACT 2 CONTINUED: Slides 10-18 (The Box deep dive) ───
    slides.append(Slide(
        num=10, title="Emergencia de identidad",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(INDIGO),
            r.c.drawString(MARGIN, r.h - MARGIN, "09 — EMERGENCIA DE IDENTIDAD"),
            r.image(MARGIN, r.h - MARGIN - 60, os.path.join(ASSETS_DIR, "slide_13_box_identity.png"), max_w=r.w - 2*MARGIN),
            r.footer(10, 45, "IDENTIDAD")
        ),
        diagram="slide_13_box_identity.png",
        speaker_notes="R1+R2+R3+R4 → identidad como historia de etiquetas. Traza: t=0, Arco A creado con ι=α nueva. t=1, transform(A) → Arco B, ι=α copiada por R3. t=2, transform(B) → Arco C, ι=α copiada. t=3, match(A, C) por ι=α → Arco D (R5). Identidad = clase de equivalencia por ι compartida. No hay 'objeto' separado. El objeto ES la historia de ι. Medible: contar arcos con ι idéntica. Reproducible: misma semilla → misma historia. Esto es lo que el motor calcula, no lo que las reglas programan.",
        qa=["¿Por qué clase de equivalencia?", "¿Qué pasa si ι se pierde (R3)?", "¿Cómo se relaciona con identity en sistemas distribuidos?"]
    ))

    slides.append(Slide(
        num=11, title="Experimentos R1, R5, R6",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(INDIGO),
            r.c.drawString(MARGIN, r.h - MARGIN, "10 — EXPERIMENTOS CONTROLADOS"),
            r.image(MARGIN, r.h - MARGIN - 60, os.path.join(ASSETS_DIR, "slide_14_box_experiments.png"), max_w=r.w - 2*MARGIN),
            r.footer(11, 45, "EXPERIMENTOS")
        ),
        diagram="slide_14_box_experiments.png",
        speaker_notes="Tres experimentos, un hallazgo admitido, dos defectos. R1: gate DESCEND. Hipótesis: gate descendente evita punto fijo prematuro. Resultado: mean_depth sobrevive (p=0.00111, n=10k semillas). Mecanismo: perturbación periódica inyecta entropía controlada. R5: perturbación periódica. Sin perturbación → FIXED_POINT (absorbido). Con perturbación → never settles (vivo). Fenómeno: la estructura se sostiene por interrupción externa. R6: semilla → determinismo. splitmix64: misma semilla → misma traza completa. Verificable: hash de traza completa reproducible. Defectos: since_inflow semántica ambigua en emparejamiento; Rule.to_dict() omisión rompe serialización completa. Ambos bloquean generalidad más allá de experimentos controlados.",
        qa=["¿Por qué Mann-Whitney y no t-test?", "¿Qué significa 'never settles' formalmente?", "¿Los defectos son corregibles sin rediseñar el kernel?"]
    ))

    slides.append(Slide(
        num=12, title="Puerto TypeScript — Nivel 3",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(INDIGO),
            r.c.drawString(MARGIN, r.h - MARGIN, "11 — PUERTO TYPESCRIPT — NIVEL 3"),
            r.image(MARGIN, r.h - MARGIN - 60, os.path.join(ASSETS_DIR, "slide_15_box_ts.png"), max_w=r.w - 2*MARGIN),
            r.footer(12, 45, "TS PORT")
        ),
        diagram="slide_15_box_ts.png",
        speaker_notes="Puerto TypeScript: fidelidad nivel 3. Estructura idéntica, hashes divergentes. Rust (referencia): ArcIncidenceGraph con Vec<Arc>, incidence Vec<Vec<usize>>, Label u64 splitmix64, since_inflow Option<usize> semántica precisa, Rule.to_dict() serialización completa, hash blake3 determinista, 100% pruebas propiedad (proptest). TypeScript (puerto): Arc[], incidence number[][], Label bigint splitmix64 portado, since_inflow number | null SEMÁNTICA AMBIGUA, Rule.to_dict() AUSENTE (defecto conocido), hash N/A (no comparable byte a byte), estructura validada: mismos conteos, mismas relaciones. No afirmo equivalencia de hashes cross-language. Esa diferencia está escrita al lado del nivel de fidelidad.",
        qa=["¿Por qué bigint en TS?", "¿Podría Rule.to_dict() implementarse en TS?", "¿Qué tests de propiedad tienes en TS?"]
    ))

    slides.append(Slide(
        num=13, title="Limitaciones honestas — The Box",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(INDIGO),
            r.c.drawString(MARGIN, r.h - MARGIN, "12 — LIMITACIONES — THE BOX"),
            r.image(MARGIN, r.h - MARGIN - 60, os.path.join(ASSETS_DIR, "slide_16_box_limitations.png"), max_w=r.w - 2*MARGIN),
            r.footer(13, 45, "LÍMITES")
        ),
        diagram="slide_16_box_limitations.png",
        speaker_notes="Veredicto: 'mecanismo explicado, sin descubrimiento'. Seis limitaciones. 1) Sin generalidad: dos defectos impiden uso fuera de experimentos controlados. 2) Sin hardware: ni sensores, ni actuadores, ni entorno físico — todo simulación determinista en memoria. 3) Sin aprendizaje: no hay actualización de pesos, gradientes, plasticidad — estructura fija por R1–R6. 4) Una métrica admitida: mean_depth bajo perturbación (p=0.00111), explicado por mecanismo DESCEND, no descubierto. 5) Sin comparación externa: no hay baseline vs redes neuronales, grafos, autómatas — el sustrato solo se compara consigo mismo. 6) Puerto TS = nivel 3: estructura validada, serialización ausente. La honestidad sobre lo que NO hace el sistema es parte del método.",
        qa=["¿Qué cambiaría 'mecanismo explicado' a 'descubrimiento'?", "¿Por qué no comparar con redes neuronales?", "¿El puerto TS podría llegar a nivel 2?"]
    ))

    slides.append(Slide(
        num=14, title="Transición → SINGULARITY/ORACLE",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(TEAL),
            r.c.drawString(MARGIN, r.h - MARGIN, "13 — ACTO 3: SINGULARITY / ORACLE"),
            r.rule_h(r.h - MARGIN - 50, color=TEAL),
            r.c.setFont(SANS_BOLD, 42), r.c.setFillColor(INK),
            r.c.drawString(MARGIN, r.h - MARGIN - 150, "Multi-agente + verificación independiente"),
            r.c.setFont(SANS_FAMILY, 20), r.c.setFillColor(MUTED),
            r.c.drawString(MARGIN, r.h - MARGIN - 220, "Cinco agentes especializados. Verificador que nunca confía en auto-reportes."),
            r.c.drawString(MARGIN, r.h - MARGIN - 260, "Dos protocolos: A (aislamiento) vs B (colaboración)."),
            r.c.drawString(MARGIN, r.h - MARGIN - 300, "E1: colaboración perjudica (p < 0.001, δ = -0.47). Resultado negativo verificado."),
            r.footer(14, 45, "SINGULARITY")
        ),
        speaker_notes="Transición al Acto 3. SINGULARITY es el sistema multi-agente; ORACLE es el diseño experimental sobre él. Cinco agentes: Navigator, Mapper, Planner, Executor, Verifier. El Verifier es clave: nunca confía en auto-reportes de agentes. Ejecuta pruebas de propiedad, compara trazas, valida contratos, rechaza si no reproduce. Dos protocolos experimentales: A (aislamiento — cada agente ejecuta su rol sin comunicación) vs B (colaboración — intercambian mensajes, orquestador coordina). Hipótesis: colaboración mejora. E1: colaboración perjudica. Δ = -0.16, p < 0.001, Cliff's δ = -0.47. Comunicación introduce overhead de coordinación que supera ganancia de información compartida en este dominio.",
        qa=["¿Por qué cinco agentes y no N?", "¿Qué es el 'Verifier' exactamente?", "¿El resultado negativo se replicó?"]
    ))

    slides.append(Slide(
        num=15, title="SINGULARITY — Arquitectura",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(TEAL),
            r.c.drawString(MARGIN, r.h - MARGIN, "14 — ARQUITECTURA SINGULARITY"),
            r.image(MARGIN, r.h - MARGIN - 60, os.path.join(ASSETS_DIR, "slide_20_singularity_arch.png"), max_w=r.w - 2*MARGIN),
            r.footer(15, 45, "ARCH")
        ),
        diagram="slide_20_singularity_arch.png",
        speaker_notes="Arquitectura: Orquestador central (routing, lifecycle, contracts). Cinco agentes especializados: Planner (descomposición), Researcher (búsqueda+síntesis), Coder (implementación determinista), Critic (verificación independiente), Synthesizer (integración+artefactos). Flechas: todos reportan al orquestador. Capa de verificación independiente en la base: nunca confía en auto-reportes. Ejecuta pruebas de propiedad, compara trazas, valida contratos, rechaza si no reproduce. Esto no es 'human in the loop'; es 'code in the loop'. La verificación es primitiva, no posterior.",
        qa=["¿Por qué Orquestador centralizado?", "¿Cómo se define el contrato entre agentes?", "¿Qué pasa si el Verifier falla?"]
    ))

    slides.append(Slide(
        num=16, title="ORACLE — Agentes y entornos",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(TEAL),
            r.c.drawString(MARGIN, r.h - MARGIN, "15 — ORACLE: AGENTES Y ENTORNOS"),
            r.image(MARGIN, r.h - MARGIN - 60, os.path.join(ASSETS_DIR, "slide_21_oracle_agents.png"), max_w=r.w - 2*MARGIN),
            r.footer(16, 45, "ORACLE")
        ),
        diagram="slide_21_oracle_agents.png",
        speaker_notes="ORACLE: cinco agentes, dos entornos. Navigator (exploración dirigida), Mapper (construcción de mapa), Planner (búsqueda política óptima), Executor (ejecución determinista), Verifier (validación independiente). Entornos: gridworld para los cuatro primeros, ambos para Verifier. Protocolo A (aislamiento): cada agente ejecuta su rol sin comunicación. Verificador valida salida de cada uno. Hipótesis: línea base de rendimiento individual. Protocolo B (colaboración): agentes intercambian mensajes estructurados. Orquestador coordina ciclo plan-ejecutar-verificar. Hipótesis: colaboración mejora rendimiento. El diseño experimental está versionado con semillas fijas; todo reproducible.",
        qa=["¿Por qué gridworld?", "¿Qué mensajes intercambian en Protocolo B?", "¿El Verifier tiene acceso al estado interno de otros agentes?"]
    ))

    slides.append(Slide(
        num=17, title="Protocolo A vs B — Diseño experimental",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(TEAL),
            r.c.drawString(MARGIN, r.h - MARGIN, "16 — PROTOCOLO A vs B"),
            r.c.setFont(SANS_BOLD, 24), r.c.setFillColor(INK),
            r.c.drawString(MARGIN, r.h - MARGIN - 80, "Diseño experimental pre-registrado"),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(MUTED),
            r.c.drawString(MARGIN, r.h - MARGIN - 130, "• Semillas fijas: 500 semillas/protocolo, versionadas en repo"),
            r.c.drawString(MARGIN, r.h - MARGIN - 160, "• Métrica primaria: task_completion_rate (0–1)"),
            r.c.drawString(MARGIN, r.h - MARGIN - 190, "• Métricas secundarias: pasos, tokens, desviación de política óptima"),
            r.c.drawString(MARGIN, r.h - MARGIN - 220, "• Test: Mann-Whitney U (no paramétrico, distribuciones no normales)"),
            r.c.drawString(MARGIN, r.h - MARGIN - 250, "• Efecto: Cliff's δ (robusto a outliers)"),
            r.c.drawString(MARGIN, r.h - MARGIN - 280, "• IC 95%: bootstrap 10,000 réplicas"),
            r.c.drawString(MARGIN, r.h - MARGIN - 310, "• Potencia post-hoc: 0.99 (α=0.05, dos colas)"),
            r.c.drawString(MARGIN, r.h - MARGIN - 340, "• Pre-registro: hash del diseño experimental en commit"),
            r.rule_h(r.h - MARGIN - 370, color=AMBER),
            r.c.setFont(SANS_FAMILY, 16), r.c.setFillColor(INK),
            r.c.drawString(MARGIN, r.h - MARGIN - 400, "Hipótesis nula: H₀: μ_A = μ_B (colaboración no cambia rendimiento)"),
            r.c.setFont(SANS_FAMILY, 16), r.c.setFillColor(RED),
            r.c.drawString(MARGIN, r.h - MARGIN - 440, "Hipótesis alternativa: H₁: μ_A ≠ μ_B"),
            r.footer(17, 45, "EXP DESIGN")
        ),
        speaker_notes="Diseño experimental riguroso. 500 semillas por protocolo, versionadas. Métrica primaria: task_completion_rate. Test Mann-Whitney U (no paramétrico). Cliff's δ para tamaño de efecto. Bootstrap 10k para IC. Potencia 0.99. Pre-registro: hash del diseño en commit. H₀: μ_A = μ_B. H₁: μ_A ≠ μ_B. No hay p-hacking, no hay HARKing. El diseño está fijado antes de ver los datos. Esto es lo mínimo para llamar 'experimento' a algo en IA.",
        qa=["¿Por qué no t-test?", "¿Qué pasa si las distribuciones son bimodales?", "¿Cómo eliges 500 semillas?"]
    ))

    slides.append(Slide(
        num=18, title="ORACLE E1 — Resultado negativo",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(TEAL),
            r.c.drawString(MARGIN, r.h - MARGIN, "17 — RESULTADO NEGATIVO E1"),
            r.image(MARGIN, r.h - MARGIN - 60, os.path.join(ASSETS_DIR, "slide_23_oracle_e1.png"), max_w=r.w - 2*MARGIN),
            r.footer(18, 45, "E1 NEGATIVO")
        ),
        diagram="slide_23_oracle_e1.png",
        speaker_notes="Resultado negativo verificado. Protocolo A (aislamiento): 0.78 [0.74, 0.82]. Protocolo B (colaboración): 0.62 [0.57, 0.67]. Δ = -0.16, IC 95% [-0.21, -0.11], p < 0.001, n=500 semillas/protocolo. Cliff's δ = -0.47 (efecto medio-grande). Potencia 0.99. Bootstrap 10k confirma IC. Conclusión: comunicación introduce overhead de coordinación que supera ganancia de información compartida en este dominio. No es 'los agentes son malos colaborando'; es 'este protocolo de colaboración en este dominio tiene overhead neto negativo'. Publicar esto evita que otros pierdan tiempo en la misma dirección. Resultado negativo == conocimiento.",
        qa=["¿Probaste otros protocolos de comunicación?", "¿El overhead es latencia o errores de coordinación?", "¿Esto invalida la arquitectura multi-agente?"]
    ))

    slides.append(Slide(
        num=19, title="Limitaciones — SINGULARITY/ORACLE",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(TEAL),
            r.c.drawString(MARGIN, r.h - MARGIN, "18 — LIMITACIONES — SINGULARITY/ORACLE"),
            r.c.setFont(SANS_BOLD, 24), r.c.setFillColor(INK),
            r.c.drawString(MARGIN, r.h - MARGIN - 80, "Limitaciones honestas del sustrato experimental"),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(MUTED),
            r.c.drawString(MARGIN, r.h - MARGIN - 140, "• Un solo dominio (gridworld) — no generaliza a tareas abiertas"),
            r.c.drawString(MARGIN, r.h - MARGIN - 170, "• Un solo protocolo de colaboración probado — espacio vasto sin explorar"),
            r.c.drawString(MARGIN, r.h - MARGIN - 200, "• Verificador limitado a propiedades estructurales — no semánticas"),
            r.c.drawString(MARGIN, r.h - MARGIN - 230, "• Sin aprendizaje online — políticas fijas por semilla"),
            r.c.drawString(MARGIN, r.h - MARGIN - 260, "• Overhead de verificación no medido en latencia crítica"),
            r.c.drawString(MARGIN, r.h - MARGIN - 290, "• Especificación HERMES no implementada — gap spec/impl"),
            r.rule_h(r.h - MARGIN - 330, color=AMBER),
            r.c.setFont(SANS_FAMILY, 16), r.c.setFillColor(INK),
            r.c.drawString(MARGIN, r.h - MARGIN - 370, "Fidelidad del claim E1: VERIFIED (reproducible, pre-registrado, bootstrap)"),
            r.c.setFont(SANS_FAMILY, 16), r.c.setFillColor(FAINT),
            r.c.drawString(MARGIN, r.h - MARGIN - 410, "Fidelidad de SINGULARITY como sistema general: ESPECULATIVO"),
            r.footer(19, 45, "LÍMITES ORACLE")
        ),
        speaker_notes="Limitaciones de SINGULARITY/ORACLE. 1) Un solo dominio (gridworld) — no generaliza. 2) Un solo protocolo de colaboración — espacio vasto sin explorar. 3) Verificador solo propiedades estructurales, no semánticas. 4) Sin aprendizaje online — políticas fijas. 5) Overhead de verificación no medido en latencia crítica. 6) HERMES especificado pero no implementado. Claim E1: VERIFIED (reproducible, pre-registrado, bootstrap). SINGULARITY como sistema general: ESPECULATIVO. La distinción entre 'este experimento está verificado' y 'este sistema generaliza' es crucial.",
        qa=["¿Qué dominios probarías después?", "¿Cómo extenderías el Verifier a propiedades semánticas?", "¿Por qué no implementar HERMES primero?"]
    ))

    slides.append(Slide(
        num=20, title="Transición → HERMES",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(AMBER),
            r.c.drawString(MARGIN, r.h - MARGIN, "19 — ACTO 4: HERMES"),
            r.rule_h(r.h - MARGIN - 50, color=AMBER),
            r.c.setFont(SANS_BOLD, 42), r.c.setFillColor(INK),
            r.c.drawString(MARGIN, r.h - MARGIN - 150, "Orquestación operacional — especificación completa"),
            r.c.setFont(SANS_FAMILY, 20), r.c.setFillColor(MUTED),
            r.c.drawString(MARGIN, r.h - MARGIN - 220, "9 tipos de agente + Governor + intervención automática por deriva"),
            r.c.drawString(MARGIN, r.h - MARGIN - 260, "Métricas: latencia P99, tasa intervención, deriva semántica, reproducibilidad"),
            r.c.drawString(MARGIN, r.h - MARGIN - 300, "Estado: SPECULATIVO (especificación completa, no implementada)"),
            r.footer(20, 45, "HERMES")
        ),
        speaker_notes="Transición al Acto 4. HERMES es la especificación de orquestación operacional. 9 tipos de agente: Observer, Analyzer, Planner, Executor, Validator, Corrector, Synchronizer, Archivist, Governor. Orquestador: routing por contrato, ciclo de vida, reglas de autonomía, intervenciones automáticas cuando deriva > umbral. Métricas: latencia P99, tasa de intervención, deriva semántica, reproducibilidad de traza. Estado: SPECULATIVO. Especificación completa en hermes/SPEC.md, no implementada. No vendo vaporware; documento lo que diseñé y por qué.",
        qa=["¿Por qué 9 tipos y no componer desde menos?", "¿Qué es 'deriva semántica' exactamente?", "¿Cuándo planeas implementar?"]
    ))

    slides.append(Slide(
        num=21, title="HERMES — Arquitectura",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(AMBER),
            r.c.drawString(MARGIN, r.h - MARGIN, "20 — ARQUITECTURA HERMES"),
            r.image(MARGIN, r.h - MARGIN - 60, os.path.join(ASSETS_DIR, "slide_28_hermes_arch.png"), max_w=r.w - 2*MARGIN),
            r.footer(21, 45, "HERMES ARCH")
        ),
        diagram="slide_28_hermes_arch.png",
        speaker_notes="9 tipos en grid 3x3. Observer (monitoreo pasivo), Analyzer (detección patrones), Planner (generación opciones), Executor (ejecución determinista), Validator (verificación contratos), Corrector (reparación automatizada), Synchronizer (consistencia distribuida), Archivist (trazabilidad completa), Governor (políticas + límites). Colores por familia: INDIGO (observación), TEAL (análisis), AMBER (ejecución), PLUM (reparación), GREEN (validación), RED (corrección), etc. Orquestador en base: routing por contrato, ciclo de vida, reglas de autonomía, intervenciones automáticas. Métricas definidas: latencia P99, tasa intervención, deriva semántica, reproducibilidad. Deriva semántica: distancia entre intención declarada y efecto observado — métrica definida pero no validada empíricamente.",
        qa=["¿Cómo defines 'autonomía' por tipo de agente?", "¿Qué dispara una intervención automática?", "¿Por qué Governor separado?"]
    ))

    slides.append(Slide(
        num=22, title="HERMES — Autonomía e intervención",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(AMBER),
            r.c.drawString(MARGIN, r.h - MARGIN, "21 — AUTONOMÍA E INTERVENCIÓN"),
            r.c.setFont(SANS_BOLD, 24), r.c.setFillColor(INK),
            r.c.drawString(MARGIN, r.h - MARGIN - 80, "Reglas de autonomía por diseño"),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(MUTED),
            r.c.drawString(MARGIN, r.h - MARGIN - 140, "• OBSERVER/ANALYZER: autonomía total (solo lectura)"),
            r.c.drawString(MARGIN, r.h - MARGIN - 170, "• PLANNER: propone, no ejecuta (requiere validación)"),
            r.c.drawString(MARGIN, r.h - MARGIN - 200, "• EXECUTOR: ejecuta solo contratos validados"),
            r.c.drawString(MARGIN, r.h - MARGIN - 230, "• VALIDATOR/CORRECTOR: intervención automática si drift > θ"),
            r.c.drawString(MARGIN, r.h - MARGIN - 260, "• SYNCHRONIZER: consistencia eventual con bounded staleness"),
            r.c.drawString(MARGIN, r.h - MARGIN - 290, "• ARCHIVIST: inmutable — nunca interviene"),
            r.c.drawString(MARGIN, r.h - MARGIN - 320, "• GOVERNOR: única autoridad para cambiar θ y políticas"),
            r.rule_h(r.h - MARGIN - 360, color=AMBER),
            r.c.setFont(SANS_BOLD, 20), r.c.setFillColor(RED),
            r.c.drawString(MARGIN, r.h - MARGIN - 400, "Intervención automática: drift_semántico > θ → CORRECTOR despachado"),
            r.c.setFont(SANS_FAMILY, 14), r.c.setFillColor(MUTED),
            r.c.drawString(MARGIN, r.h - MARGIN - 440, "drift_semántico = distancia(intención_declarada, efecto_observado)"),
            r.c.drawString(MARGIN, r.h - MARGIN - 470, "θ configurable por GOVERNOR · trazabilidad completa en ARCHIVIST"),
            r.footer(22, 45, "AUTONOMÍA")
        ),
        speaker_notes="Autonomía por diseño, no por permiso. Observer/Analyzer: solo lectura, autonomía total. Planner: propone, no ejecuta — requiere validación. Executor: ejecuta solo contratos validados. Validator/Corrector: intervención automática si drift > θ. Synchronizer: consistencia eventual con bounded staleness. Archivist: inmutable, nunca interviene. Governor: única autoridad para cambiar θ y políticas. Intervención: drift_semántico > θ → Corrector despachado. drift_semántico = distancia(intención_declarada, efecto_observado). θ configurable por Governor, trazabilidad completa en Archivist. La métrica de drift está definida pero NO validada empíricamente — es SPECULATIVO.",
        qa=["¿Cómo mides 'intención declarada'?", "¿Qué pasa si CORRECTOR falla?", "¿Hay escalada de intervención?"]
    ))

    slides.append(Slide(
        num=23, title="HERMES — Limitaciones (SPECULATIVO)",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(AMBER),
            r.c.drawString(MARGIN, r.h - MARGIN, "22 — LIMITACIONES — HERMES"),
            r.c.setFont(SANS_BOLD, 24), r.c.setFillColor(RED),
            r.c.drawString(MARGIN, r.h - MARGIN - 80, "ESTADO: SPECULATIVO — Especificación completa, no implementada"),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(MUTED),
            r.c.drawString(MARGIN, r.h - MARGIN - 140, "• Zero código ejecutable — toda la arquitectura es papel"),
            r.c.drawString(MARGIN, r.h - MARGIN - 170, "• drift_semántico definido pero no validado — métrica sin ground truth"),
            r.c.drawString(MARGIN, r.h - MARGIN - 200, "• Intervención automática no probada — riesgo de cascada de correcciones"),
            r.c.drawString(MARGIN, r.h - MARGIN - 230, "• Governor como SPOF — único punto de fallo para políticas"),
            r.c.drawString(MARGIN, r.h - MARGIN - 260, "• Latencia P99 objetivo no benchmarkada"),
            r.c.drawString(MARGIN, r.h - MARGIN - 290, "• Consistencia eventual vs. fuerte: trade-off no resuelto"),
            r.c.drawString(MARGIN, r.h - MARGIN - 320, "• 9 tipos de agente: ¿completos? ¿mínimos? ¿ortogonales?"),
            r.rule_h(r.h - MARGIN - 360, color=AMBER),
            r.c.setFont(SANS_FAMILY, 16), r.c.setFillColor(INK),
            r.c.drawString(MARGIN, r.h - MARGIN - 400, "Valor de la especificación: pensamiento riguroso antes de código"),
            r.c.setFont(SANS_FAMILY, 16), r.c.setFillColor(FAINT),
            r.c.drawString(MARGIN, r.h - MARGIN - 440, "Riesgo: especificación hermética que no sobrevive a la implementación"),
            r.footer(23, 45, "HERMES LÍMITES")
        ),
        speaker_notes="HERMES es SPECULATIVO. Cero código ejecutable. drift_semántico definido pero sin ground truth — no sabemos medirlo realmente. Intervención automática no probada — riesgo de cascada de correcciones. Governor es SPOF (single point of failure) para políticas. Latencia P99 objetivo no benchmarkada. Consistencia eventual vs fuerte: trade-off no resuelto. 9 tipos: ¿completos? ¿mínimos? ¿ortogonales? Valor: pensamiento riguroso antes de código. Riesgo: especificación hermética que no sobrevive a la implementación. Lo presento porque el diseño enseña; lo marco como SPECULATIVO porque no he escrito la primera línea.",
        qa=["¿Por qué no implementar un subconjunto mínimo?", "¿Cómo validarías drift_semántico?", "¿Qué harías distinto si empezaras hoy?"]
    ))

    slides.append(Slide(
        num=24, title="Showcase — 4 reconstrucciones nivel 1",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(INDIGO),
            r.c.drawString(MARGIN, r.h - MARGIN, "23 — SHOWCASE: 4 RECONSTRUCCIONES NIVEL 1"),
            r.c.setFont(SANS_BOLD, 24), r.c.setFillColor(INK),
            r.c.drawString(MARGIN, r.h - MARGIN - 80, "Cuatro reconstrucciones, misma disciplina — fidelidad declarada"),
            r.c.setFont(MONO_FAMILY, 13), r.c.setFillColor(MUTED),
            r.c.drawString(MARGIN, r.h - MARGIN - 130, "1. Wi-Fi Time Machine — Reconstrucción historial inalámbrico"),
            r.c.drawString(MARGIN, r.h - MARGIN - 160, "   Entrada: volcado iw/nmcli · Regla: deduplicar BSSID, freq→canal, AKM→WPA"),
            r.c.drawString(MARGIN, r.h - MARGIN - 190, "   Salida: mapa calor tiempo × red · Fidelidad: NIVEL 1 (reproducción directa)"),
            r.c.drawString(MARGIN, r.h - MARGIN - 230, "2. BLE Radar — Presencia Bluetooth sin hardware"),
            r.c.drawString(MARGIN, r.h - MARGIN - 260, "   Entrada: observaciones sintéticas · Regla: EMA α=0.4, ventanas 15/30s"),
            r.c.drawString(MARGIN, r.h - MARGIN - 290, "   Salida: radar, ciclo de vida, repetición · Fidelidad: NIVEL 1"),
            r.c.drawString(MARGIN, r.h - MARGIN - 330, "3. Process Ecosystem Monitor — Árbol de procesos Linux como ecosistema"),
            r.c.drawString(MARGIN, r.h - MARGIN - 360, "   Entrada: snapshots /proc · Regla: jiffies→CPU%, identidad (pid, starttime)"),
            r.c.drawString(MARGIN, r.h - MARGIN - 390, "   Salida: árbol, eventos, métricas · Fidelidad: NIVEL 1"),
            r.c.drawString(MARGIN, r.h - MARGIN - 430, "4. Terminal Generative Engine — Arte determinista desde semilla"),
            r.c.drawString(MARGIN, r.h - MARGIN - 460, "   Entrada: semilla + modo · Regla: splitmix64 sin estado, campo ángulos analítico"),
            r.c.drawString(MARGIN, r.h - MARGIN - 490, "   Salida: fotograma O(1) + huella mundo · Fidelidad: NIVEL 1"),
            r.footer(24, 45, "SHOWCASE")
        ),
        speaker_notes="Showcase: cuatro reconstrucciones, todas nivel 1 (reproducción directa). 1) Wi-Fi Time Machine: entrada volcado iw/nmcli, regla deduplicar BSSID + freq→canal + AKM→WPA, salida mapa calor tiempo×red. 2) BLE Radar: entrada observaciones sintéticas, regla EMA α=0.4 ventanas 15/30s, salida radar + ciclo vida + repetición. 3) Process Ecosystem Monitor: entrada snapshots /proc, regla jiffies→CPU% + identidad (pid,starttime), salida árbol + eventos + métricas. 4) Terminal Generative Engine: entrada semilla+modo, regla splitmix64 sin estado + campo ángulos analítico, salida fotograma O(1) + huella mundo. 182 tests, 160.69 kB JS, zero runtime deps. Deployed: thorrijadev.github.io/showcase.",
        qa=["¿Por qué 'sin hardware' en BLE Radar?", "¿Qué significa O(1) en TGE?", "¿Cómo validas nivel 1?"]
    ))

    slides.append(Slide(
        num=25, title="Showcase — Arquitectura y despliegue",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(INDIGO),
            r.c.drawString(MARGIN, r.h - MARGIN, "24 — SHOWCASE: ARQUITECTURA Y DESPLIEGUE"),
            r.c.setFont(SANS_BOLD, 24), r.c.setFillColor(INK),
            r.c.drawString(MARGIN, r.h - MARGIN - 80, "Vite + TypeScript · Worker proxy · Zero runtime deps"),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(MUTED),
            r.c.drawString(MARGIN, r.h - MARGIN - 140, "• src/sections/: 4 modelos como módulos ES independientes"),
            r.c.drawString(MARGIN, r.h - MARGIN - 170, "• proxy/worker.js: Cloudflare Worker para CORS + rate limit"),
            r.c.drawString(MARGIN, r.h - MARGIN - 200, "• build: tsc --noEmit clean · vite build → 160.69 kB JS + 12.3 kB CSS"),
            r.c.drawString(MARGIN, r.h - MARGIN - 230, "• 182 tests: vitest · pruebas de propiedad · regresión visual"),
            r.c.drawString(MARGIN, r.h - MARGIN - 260, "• Deploy: GitHub Pages (docs/) · HTTPS · headers de seguridad"),
            r.c.drawString(MARGIN, r.h - MARGIN - 290, "• Verificación semanal: npm test && npm run build && curl -I live URL"),
            r.rule_h(r.h - MARGIN - 330, color=AMBER),
            r.c.setFont(SANS_FAMILY, 16), r.c.setFillColor(INK),
            r.c.drawString(MARGIN, r.h - MARGIN - 370, "Cada modelo: entrada tipada → reglas puras → salida tipada → tests de propiedad"),
            r.c.setFont(SANS_FAMILY, 16), r.c.setFillColor(FAINT),
            r.c.drawString(MARGIN, r.h - MARGIN - 410, "Sin React, sin framework UI, sin estado global — solo funciones puras"),
            r.footer(25, 45, "SHOWCASE DEPLOY")
        ),
        speaker_notes="Arquitectura Showcase: Vite + TypeScript. 4 modelos en src/sections/ como módulos ES independientes. proxy/worker.js es Cloudflare Worker para CORS + rate limit. Build limpio: tsc --noEmit + vite build = 160.69 kB JS + 12.3 kB CSS. 182 tests con vitest: pruebas de propiedad + regresión visual. Deploy en GitHub Pages (carpeta docs/), HTTPS, headers de seguridad. Verificación semanal automatizada: test + build + curl a URL live. Cada modelo: entrada tipada → reglas puras → salida tipada → tests de propiedad. Sin React, sin framework UI, sin estado global — solo funciones puras. Esto no es minimalismo por estética; es para que la verificación sea trivial.",
        qa=["¿Por qué Cloudflare Worker y no backend propio?", "¿Zero runtime deps incluye TypeScript runtime?", "¿Cómo haces regresión visual sin framework?"]
    ))

    slides.append(Slide(
        num=26, title="Transición → Síntesis",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(AMBER),
            r.c.drawString(MARGIN, r.h - MARGIN, "25 — ACTO 5: SÍNTESIS"),
            r.rule_h(r.h - MARGIN - 50, color=AMBER),
            r.c.setFont(SANS_BOLD, 42), r.c.setFillColor(INK),
            r.c.drawString(MARGIN, r.h - MARGIN - 150, "Tres sustratos, una filosofía"),
            r.c.setFont(SANS_FAMILY, 20), r.c.setFillColor(MUTED),
            r.c.drawString(MARGIN, r.h - MARGIN - 220, "The Box · SINGULARITY/ORACLE · HERMES"),
            r.c.drawString(MARGIN, r.h - MARGIN - 260, "Verificación independiente · Fidelidad declarada · Resultados negativos · Defectos documentados"),
            r.footer(26, 45, "SÍNTESIS")
        ),
        speaker_notes="Acto 5: síntesis. Tres sustratos, una filosofía. The Box (sustrato generativo mínimo), SINGULARITY/ORACLE (multi-agente + verificación), HERMES (orquestación operacional). Hilo común: verificación independiente (nunca confiar en auto-reportes), fidelidad declarada (cada claim lleva su nivel), resultados negativos publicados (E1, The Box sin descubrimiento), defectos documentados (since_inflow, Rule.to_dict, drift_semántico no validado). Esto no es una lista de proyectos; es un sistema de pensamiento.",
        qa=["¿Por qué tres y no uno unificado?", "¿Qué proyectos descartaste?", "¿Cuál es el sustrato más prometedor?"]
    ))

    slides.append(Slide(
        num=27, title="Tres sustratos, una filosofía",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(AMBER),
            r.c.drawString(MARGIN, r.h - MARGIN, "26 — TRES SUSTRATOS, UNA FILOSOFÍA"),
            r.image(MARGIN, r.h - MARGIN - 60, os.path.join(ASSETS_DIR, "slide_37_synthesis.png"), max_w=r.w - 2*MARGIN),
            r.footer(27, 45, "SÍNTESIS")
        ),
        diagram="slide_37_synthesis.png",
        speaker_notes="Tarjetas comparativas. The Box: sustrato generativo mínimo, reglas R1–R6 → identidad/linaje/comunidad, nivel 3 (TS), mecanismo explicado. SINGULARITY/ORACLE: sistema multi-agente con verificación, 5 agentes + verificador independiente, E1 resultado negativo verificado. HERMES: orquestación operacional, 9 agentes + governor + intervención automática, especulación. Hilo común en ámbar abajo: verificación independiente, fidelidad declarada, resultados negativos publicados, defectos documentados. Cada sustrato ataca una pregunta central distinta, pero todos usan la misma disciplina epistémica.",
        qa=["¿Podrían fusionarse The Box y SINGULARITY?", "¿Por qué HERMES no usa el Verifier de ORACLE?", "¿Qué sustrato tiene más deuda técnica?"]
    ))

    slides.append(Slide(
        num=28, title="Primitiva de verificación",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(AMBER),
            r.c.drawString(MARGIN, r.h - MARGIN, "27 — PRIMITIVA DE VERIFICACIÓN"),
            r.c.setFont(SANS_BOLD, 28), r.c.setFillColor(INK),
            r.c.drawString(MARGIN, r.h - MARGIN - 100, "Verificación como primitiva transversal, no paso posterior"),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(MUTED),
            r.c.drawString(MARGIN, r.h - MARGIN - 160, "1. Especificación ejecutable: contratos tipados (TypeScript/Rust)"),
            r.c.drawString(MARGIN, r.h - MARGIN - 190, "2. Pruebas de propiedad: proptest (Rust) / fast-check (TS) — generan inputs, validan invariantes"),
            r.c.drawString(MARGIN, r.h - MARGIN - 220, "3. Verificador independiente: proceso separado que nunca confía en auto-reportes"),
            r.c.drawString(MARGIN, r.h - MARGIN - 250, "4. Reproducibilidad: semillas fijas + hash de traza + bootstrap estadístico"),
            r.c.drawString(MARGIN, r.h - MARGIN - 280, "5. Fidelidad declarada: cada claim lleva su nivel (1–4) escrito al lado"),
            r.c.drawString(MARGIN, r.h - MARGIN - 310, "6. Resultados negativos: si el experimento contradice la hipótesis, se publica"),
            r.c.drawString(MARGIN, r.h - MARGIN - 340, "7. Defectos documentados: since_inflow, Rule.to_dict, drift_semántico, etc."),
            r.rule_h(r.h - MARGIN - 380, color=AMBER),
            r.c.setFont(SANS_FAMILY, 16), r.c.setFillColor(INK),
            r.c.drawString(MARGIN, r.h - MARGIN - 420, "Esta primitiva se aplica a The Box, ORACLE, Showcase, y se especifica en HERMES"),
            r.c.setFont(SANS_FAMILY, 16), r.c.setFillColor(FAINT),
            r.c.drawString(MARGIN, r.h - MARGIN - 460, "No es una checklist; es la forma en que escribo código que no me miente"),
            r.footer(28, 45, "VERIFICACIÓN")
        ),
        speaker_notes="Verificación como primitiva transversal, no paso posterior. Siete capas: 1) Especificación ejecutable (contratos tipados). 2) Pruebas de propiedad (proptest/fast-check). 3) Verificador independiente (proceso separado, cero confianza en auto-reportes). 4) Reproducibilidad (semillas fijas + hash traza + bootstrap). 5) Fidelidad declarada (cada claim lleva nivel 1-4). 6) Resultados negativos publicados. 7) Defectos documentados. Esto se aplica a The Box, ORACLE, Showcase, y se especifica en HERMES. No es checklist; es la forma en que escribo código que no me miente.",
        qa=["¿Cómo integras verificación en CI/CD?", "¿Qué pasa si el verificador independiente tiene bugs?", "¿Por qué no usar verificación formal (Coq, Lean)?"]
    ))

    slides.append(Slide(
        num=29, title="Resultados negativos como conocimiento",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(AMBER),
            r.c.drawString(MARGIN, r.h - MARGIN, "28 — RESULTADOS NEGATIVOS"),
            r.c.setFont(SANS_BOLD, 28), r.c.setFillColor(INK),
            r.c.drawString(MARGIN, r.h - MARGIN - 100, "Publicar lo que no funciona evita que otros pierdan tiempo"),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(MUTED),
            r.c.drawString(MARGIN, r.h - MARGIN - 160, "ORACLE E1: Δ = -0.16, p < 0.001, δ = -0.47"),
            r.c.drawString(MARGIN, r.h - MARGIN - 190, "   Colaboración perjudica en gridworld con este protocolo"),
            r.c.drawString(MARGIN, r.h - MARGIN - 220, "The Box: mecanismo explicado, sin descubrimiento"),
            r.c.drawString(MARGIN, r.h - MARGIN - 250, "   Identidad/linaje/comunidad emergen, pero no hay fenómeno nuevo"),
            r.c.drawString(MARGIN, r.h - MARGIN - 280, "Defectos estructurales: since_inflow, Rule.to_dict, drift_semántico"),
            r.c.drawString(MARGIN, r.h - MARGIN - 310, "   Bloquean generalidad — documentados para no repetir"),
            r.rule_h(r.h - MARGIN - 340, color=AMBER),
            r.c.setFont(SANS_FAMILY, 16), r.c.setFillColor(INK),
            r.c.drawString(MARGIN, r.h - MARGIN - 380, "Resultado negativo ≠ fracaso. Resultado negativo = conocimiento acotado"),
            r.c.setFont(SANS_FAMILY, 16), r.c.setFillColor(FAINT),
            r.c.drawString(MARGIN, r.h - MARGIN - 420, "La literatura de IA entierra resultados negativos. Yo los versiono."),
            r.footer(29, 45, "NEGATIVOS")
        ),
        speaker_notes="Resultados negativos como conocimiento. ORACLE E1: colaboración perjudica (Δ=-0.16, p<0.001, δ=-0.47). The Box: mecanismo explicado, sin descubrimiento — identidad/linaje/comunidad emergen pero no hay fenómeno nuevo. Defectos estructurales: since_inflow, Rule.to_dict, drift_semántico — bloquean generalidad, documentados para no repetir. Resultado negativo ≠ fracaso. Resultado negativo = conocimiento acotado. La literatura de IA entierra resultados negativos; yo los versiono. Esto cambia la economía de la investigación: si sabes que este protocolo de colaboración en este dominio tiene overhead neto negativo, no pierdes 6 meses probando variantes.",
        qa=["¿Has tenido presión para no publicar negativos?", "¿Cómo enmarcas un negativo en un paper?", "¿Qué negativo te dolió más publicar?"]
    ))

    slides.append(Slide(
        num=30, title="Mapa de limitaciones — Heatmap",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(AMBER),
            r.c.drawString(MARGIN, r.h - MARGIN, "29 — MAPA DE LIMITACIONES"),
            r.image(MARGIN, r.h - MARGIN - 60, os.path.join(ASSETS_DIR, "slide_40_limitations_heatmap.png"), max_w=r.w - 2*MARGIN),
            r.footer(30, 45, "HEATMAP")
        ),
        diagram="slide_40_limitations_heatmap.png",
        speaker_notes="Heatmap de limitaciones. 8 filas × 3 sustratos. Rojo = bloquea generalidad. Ámbar = reduce alcance. Gris = documentado. Blanco = no aplica. The Box: defectos estructurales (rojo), sin hardware (rojo), sin aprendizaje (rojo), sin baseline externo (rojo), serialización incompleta (rojo), verificación no exhaustiva (gris). ORACLE: sin hardware (ámbar), sin aprendizaje (gris), sin baseline (ámbar), verificación no exhaustiva (ámbar). HERMES: spec no implementada (rojo), drift no validado (ámbar), verificación no exhaustiva (ámbar), intervención no probada (ámbar), Governor SPOF (ámbar), consistencia no resuelta (ámbar), 9 tipos ortogonales (ámbar). Este mapa dice: 'aquí no vayas sin resolver esto primero'.",
        qa=["¿Por qué heatmap y no lista?", "¿Qué limitación resolverías primero?", "¿Cómo priorizas deuda técnica vs features?"]
    ))

    slides.append(Slide(
        num=31, title="Problemas abiertos — Líneas de investigación",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(AMBER),
            r.c.drawString(MARGIN, r.h - MARGIN, "30 — PROBLEMAS ABIERTOS"),
            r.image(MARGIN, r.h - MARGIN - 60, os.path.join(ASSETS_DIR, "slide_41_open_problems.png"), max_w=r.w - 2*MARGIN),
            r.footer(31, 45, "OPEN PROBLEMS")
        ),
        diagram="slide_41_open_problems.png",
        speaker_notes="Seis problemas abiertos que guían lo siguiente. P1: Generalidad del sustrato The Box — resolver since_inflow + Rule.to_dict → ¿permite composición recursiva arbitraria? P2: Colaboración efectiva en multi-agente — E1 muestra overhead > ganancia; ¿qué topologías/contratos invierten la desigualdad? P3: Verificación de propiedades emergentes — hoy verificación estructural; mañana verificación semántica de identidad/linaje. P4: Puente simulación → hardware — The Box es puro software; ¿qué mínima interfaz sensor/actuador preserva determinismo? P5: Métricas de deriva en HERMES — drift semántico definido pero no validado empíricamente; ¿cómo medir sin ground truth? P6: Reproducibilidad cross-language — Rust ↔ TS estructura OK, hashes divergen; ¿nivel 2 alcanzable sin serialización binaria? Estos no son 'futuro trabajo' genérico; son preguntas concretas con criterio de falsificación.",
        qa=["¿Cuál es el más tractable?", "¿P3 requiere verificación formal?", "¿P4 implica robótica?"]
    ))

    slides.append(Slide(
        num=32, title="Reproducibilidad — Artefactos",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(AMBER),
            r.c.drawString(MARGIN, r.h - MARGIN, "31 — REPRODUCIBILIDAD"),
            r.image(MARGIN, r.h - MARGIN - 60, os.path.join(ASSETS_DIR, "slide_43_repro.png"), max_w=r.w - 2*MARGIN),
            r.footer(32, 45, "REPRO")
        ),
        diagram="slide_43_repro.png",
        speaker_notes="Cada claim en esta presentación es reproducible con estos comandos exactos. The Box (Rust): cargo test --package the-box -- --nocapture; cargo run --example r1_descend -- --seeds 10000; cargo run --example r5_perturb -- --seeds 10000. The Box (TypeScript): cd the-box-ts && npm test; npm run verify:structure -- --compare-rust. ORACLE E1: cd oracle && python -m pytest experiments/e1_negative.py -v; python -m pytest experiments/e1_negative.py --bootstrap 10000. Showcase: cd showcase && npm run test && npm run build (182 tests, 160.69 kB JS, zero runtime deps). SINGULARITY: cd singularity && cargo test --workspace; cargo run --example orchestrator_demo. HERMES: cat hermes/SPEC.md (especificación completa, no implementada). Repositorio: github.com/ThorrijaDEV. Todos los experimentos versionados con semillas fijas.",
        qa=["¿Por qué semillas fijas y no aleatorias?", "¿Cómo garantizas mismo entorno (OS, deps)?", "¿Qué pasa si un test flaky?"]
    ))

    slides.append(Slide(
        num=33, title="Contrato social — Qué traigo",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(AMBER),
            r.c.drawString(MARGIN, r.h - MARGIN, "32 — CONTRATO SOCIAL"),
            r.rule_h(r.h - MARGIN - 50, color=AMBER),
            r.c.setFont(SANS_BOLD, 28), r.c.setFillColor(INK),
            r.c.drawString(MARGIN, r.h - MARGIN - 120, "Lo que traigo es esto:"),
            r.c.setFont(SANS_FAMILY, 20), r.c.setFillColor(MUTED),
            r.c.drawString(MARGIN, r.h - MARGIN - 180, "• Veinticuatro proyectos construidos, documentados, verificables"),
            r.c.drawString(MARGIN, r.h - MARGIN - 220, "• Una disciplina: afirmación → evidencia → veredicto"),
            r.c.drawString(MARGIN, r.h - MARGIN - 260, "• Tres sustratos experimentales con preguntas concretas"),
            r.c.drawString(MARGIN, r.h - MARGIN - 300, "• Resultados negativos versionados, defectos documentados"),
            r.c.drawString(MARGIN, r.h - MARGIN - 340, "• Fidelidad declarada en cada claim (niveles 1–4)"),
            r.c.drawString(MARGIN, r.h - MARGIN - 380, "• Reproducibilidad: comandos exactos, semillas fijas, hashes"),
            r.rule_h(r.h - MARGIN - 420, color=AMBER),
            r.c.setFont(SANS_BOLD, 20), r.c.setFillColor(INK),
            r.c.drawString(MARGIN, r.h - MARGIN - 460, "Lo que pido: gente que exija más rigor del que yo tengo hoy"),
            r.c.setFont(SANS_FAMILY, 16), r.c.setFillColor(FAINT),
            r.c.drawString(MARGIN, r.h - MARGIN - 500, "Lo que NO traigo: credenciales inventadas, métricas infladas, promesas de AGI"),
            r.footer(33, 45, "CONTRATO")
        ),
        speaker_notes="Contrato social. Lo que traigo: 24 proyectos construidos/documentados/verificables. Una disciplina: afirmación→evidencia→veredicto. 3 sustratos experimentales con preguntas concretas. Resultados negativos versionados, defectos documentados. Fidelidad declarada (niveles 1-4). Reproducibilidad: comandos exactos, semillas fijas, hashes. Lo que pido: gente que exija más rigor del que yo tengo hoy. Lo que NO traigo: credenciales inventadas, métricas infladas, promesas de AGI. Si buscas alguien que te diga que su sistema 'casi resuelve AGI', no soy yo. Si buscas alguien que construya instrumentos, los mida, documente lo que falla, y los ponga a disposición para que otros los rompan — ese soy yo.",
        qa=["¿Qué significa 'exijan más rigor del que tengo'?", "¿Cómo manejas feedback que desacuerda con tu enfoque?", "¿Qué harías si el equipo usa metodologías distintas?"]
    ))

    slides.append(Slide(
        num=34, title="Llamada a la acción",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(AMBER),
            r.c.drawString(MARGIN, r.h - MARGIN, "33 — LLAMADA A LA ACCIÓN"),
            r.c.setFont(SANS_BOLD, 32), r.c.setFillColor(INK),
            r.c.drawString(MARGIN, r.h - MARGIN - 120, "Tres formas de trabajar juntos:"),
            r.c.setFont(MONO_FAMILY, 18), r.c.setFillColor(INDIGO),
            r.c.drawString(MARGIN, r.h - MARGIN - 190, "1. Resolver P1 (The Box): since_inflow + Rule.to_dict → generalidad"),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(MUTED),
            r.c.drawString(MARGIN + 20, r.h - MARGIN - 220, "→ Requiere: theory of programming languages, type systems, formal verification"),
            r.c.setFont(MONO_FAMILY, 18), r.c.setFillColor(TEAL),
            r.c.drawString(MARGIN, r.h - MARGIN - 260, "2. Invertir E1 (ORACLE): topologías/contratos donde colaboración > aislamiento"),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(MUTED),
            r.c.drawString(MARGIN + 20, r.h - MARGIN - 290, "→ Requiere: multi-agent systems, communication protocols, experimental design"),
            r.c.setFont(MONO_FAMILY, 18), r.c.setFillColor(AMBER),
            r.c.drawString(MARGIN, r.h - MARGIN - 330, "3. Implementar HERMES: de SPECULATIVO a VERIFIED"),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(MUTED),
            r.c.drawString(MARGIN + 20, r.h - MARGIN - 360, "→ Requiere: distributed systems, observability, correctness-by-construction"),
            r.rule_h(r.h - MARGIN - 400, color=AMBER),
            r.c.setFont(SANS_BOLD, 20), r.c.setFillColor(INK),
            r.c.drawString(MARGIN, r.h - MARGIN - 440, "Cada uno tiene criterio de falsificación. Ninguno es 'investigar a ver qué sale'."),
            r.footer(34, 45, "CTA")
        ),
        speaker_notes="Tres formas concretas de trabajar juntos. 1) Resolver P1 (The Box): since_inflow + Rule.to_dict → generalidad. Requiere theory of PL, type systems, formal verification. 2) Invertir E1 (ORACLE): topologías/contratos donde colaboración > aislamiento. Requiere multi-agent systems, communication protocols, experimental design. 3) Implementar HERMES: de SPECULATIVO a VERIFIED. Requiere distributed systems, observability, correctness-by-construction. Cada uno tiene criterio de falsificación. Ninguno es 'investigar a ver qué sale'. Si el equipo tiene expertise en alguna de estas áreas, la conversación técnica empieza ya. Si no, los artefactos están en github.com/ThorrijaDEV para que los evalúen sin mi presencia.",
        qa=["¿Por qué solo tres?", "¿Qué pasa si el equipo no tiene esa expertise?", "¿Cuál priorizarías tú?"]
    ))

    slides.append(Slide(
        num=35, title="Cierre",
        content_fn=lambda r: (
            r.bg(),
            r.c.setFont(SANS_BOLD, 60), r.c.setFillColor(INK),
            r.c.drawCentredString(r.w/2, r.h*0.55, "THORRIJA"),
            r.c.setFont(MONO_FAMILY, 22), r.c.setFillColor(INDIGO),
            r.c.drawCentredString(r.w/2, r.h*0.45, "Gracias."),
            r.rule_h(r.h*0.4, x0=r.w*0.3, x1=r.w*0.7, color=AMBER, w=2),
            r.c.setFont(MONO_FAMILY, 14), r.c.setFillColor(MUTED),
            r.c.drawCentredString(r.w/2, r.h*0.35, "github.com/ThorrijaDEV"),
            r.c.drawCentredString(r.w/2, r.h*0.31, "thorrijadev.github.io/showcase"),
            r.c.drawCentredString(r.w/2, r.h*0.27, "thorrija.contact@gmail.com"),
            r.footer(35, 45, "CIERRE")
        ),
        speaker_notes="Cierre. No '¿preguntas?' genérico. 'El PDF está en github.com/ThorrijaDEV/research-presentation. Los artefactos de reproducibilidad están en cada repo. Los claims tienen su evidencia. Los defectos su documentación. Si algo no se reproduce, abrid un issue. Si algo se reproduce y contradice lo que dije, mejor aún — he aprendido algo. Gracias.'",
        qa=[]
    ))

    # ─── APPENDIX SLIDES (36-45) ───
    appendix_slides = [
        (36, "Apéndice A: The Box — Código kernel (Rust)", """
// the-box/src/kernel.rs
pub struct ArcIncidenceGraph {
    arcs: Vec<Arc>,
    incidence: Vec<Vec<usize>>,  // arco -> [arcos incidentes]
}

pub struct Arc {
    id: ArcId,
    label: Label,           // ι: etiqueta de identidad
    lineage: Label,         // λ: etiqueta de linaje
    seed: Seed,             // σ: splitmix64 state
    payload: Payload,
    since_inflow: Option<usize>,  // DEFECTO: semántica ambigua
}

impl ArcIncidenceGraph {
    pub fn transform(&mut self, arc_id: ArcId) -> ArcId {
        // R1: transformación produce arco nuevo
        // R2: nuevo arco lleva etiqueta
        // R3: etiqueta se copia (o se pierde)
        // R4/R5: match + bind por etiqueta compartida
    }
}

pub trait Rule {
    fn to_dict(&self) -> Dict;  // DEFECTO: omitido en implementación
}
"""),
        (37, "Apéndice B: ORACLE E1 — Script estadístico", """
# oracle/experiments/e1_negative.py
import numpy as np
from scipy.stats import mannwhitneyu
from scipy import bootstrap

def run_e1(n_seeds=500):
    protocol_a = [run_protocol_a(seed) for seed in seeds]
    protocol_b = [run_protocol_b(seed) for seed in seeds]

    # Mann-Whitney U (no paramétrico)
    stat, p = mannwhitneyu(protocol_a, protocol_b, alternative='two-sided')

    # Cliff's delta (tamaño de efecto robusto)
    delta = cliffs_delta(protocol_a, protocol_b)

    # Bootstrap CI 95%
    ci = bootstrap((protocol_a, protocol_b), np.mean_diff, n_resamples=10000)

    return {
        "mean_a": np.mean(protocol_a), "mean_b": np.mean(protocol_b),
        "delta": delta, "p": p, "ci": ci.confidence_interval,
        "power": post_hoc_power(delta, n_seeds, alpha=0.05)
    }

# Resultado verificado:
# mean_a=0.78, mean_b=0.62, delta=-0.16, p<0.001, δ=-0.47, power=0.99
"""),
        (38, "Apéndice C: SINGULARITY — Contrato de agente", """
// singularity/contracts/agent.ts
interface AgentContract {
    role: AgentRole;
    input_schema: JSONSchema;
    output_schema: JSONSchema;
    invariants: Invariant[];           // pruebas de propiedad
    autonomy_level: AutonomyLevel;     // READ_ONLY | PROPOSE | EXECUTE
    drift_threshold?: number;          // para VALIDATOR/CORRECTOR
}

interface VerificationResult {
    passed: boolean;
    property_violations: PropertyViolation[];
    trace_hash: string;                // blake3 de traza completa
    reproducibility: ReproducibilityReport;
}

class IndependentVerifier {
    async verify(agent: Agent, contract: AgentContract, seed: Seed): VerificationResult {
        // 1. Ejecuta agente con semilla fija
        // 2. Genera inputs via fast-check / proptest
        // 3. Valida invariantes contra output
        // 4. Compara trace_hash con expected
        // 5. NUNCA confía en agent.self_report()
    }
}
"""),
        (39, "Apéndice D: Showcase — Modelo Wi-Fi Time Machine", """
// showcase/src/models/wifi-time-machine.ts
interface WiFiScan {
    bssid: string;
    ssid: string;
    frequency: number;    // MHz
    level: number;        // dBm
    capabilities: string; // WPA2-PSK-CCMP, etc.
    timestamp: number;    // ms since epoch
}

function deduplicate(scans: WiFiScan[]): WiFiScan[] {
    const byBSSID = new Map<string, WiFiScan[]>();
    for (const s of scans) {
        const key = s.bssid;
        if (!byBSSID.has(key)) byBSSID.set(key, []);
        byBSSID.get(key)!.push(s);
    }
    return Array.from(byBSSID.values()).map(arr =>
        arr.reduce((best, cur) => cur.level > best.level ? cur : best)
    );
}

function frequencyToChannel(freq: number): number {
    if (freq === 2484) return 14;
    if (freq >= 2412 && freq <= 2472) return Math.round((freq - 2412) / 5) + 1;
    if (freq >= 5180 && freq <= 5825) return Math.round((freq - 5180) / 5) + 36;
    return -1;
}

function akmToWPA(caps: string): string {
    if (caps.includes("WPA3")) return "WPA3";
    if (caps.includes("WPA2")) return "WPA2";
    if (caps.includes("WPA")) return "WPA";
    return "OPEN";
}

// Fidelidad NIVEL 1: misma entrada → misma salida determinista
// Tests de propiedad: proptest genera scans aleatorios, valida invariantes
"""),
        (40, "Apéndice E: HERMES — Especificación de drift", """
# hermes/SPEC.md — Extracto: Drift Semántico

## Definición
drift_semántico(agente, ventana) = distancia(intención_declarada, efecto_observado)

### Intención declarada
- Para PLANNER: plan emitido (JSON Schema validado)
- Para EXECUTOR: contrato aceptado
- Para CORRECTOR: acción de reparación propuesta

### Efecto observado
- Estado del sistema post-ejecución (snapshot inmutable)
- Métricas: latencia, throughput, error_rate, consistencia

### Función de distancia
D = w₁·L₁(intención.acciones, efecto.acciones_ejecutadas) +
    w₂·KL(intención.distribución_esperada, efecto.distribución_observada) +
    w₃·indicador(intención.invariantes_violadas)

Pesos: w₁=0.5, w₂=0.3, w₃=0.2 (configurables por GOVERNOR)

## Estado: NO VALIDADO EMPÍRICAMENTE
- No hay ground truth para 'intención real' vs 'intención declarada'
- Riesgo: agente malicioso/errático declara intención A, ejecuta B
- Mitigación: ARCHIVIST registra todo; VALIDATOR cross-checkea
"""),
        (41, "Apéndice F: Glosario de términos", """
TÉRMINOS CLAVE (definidos operacionalmente)

• Afirmación → Evidencia → Veredicto: orden epistémico inmutable.
• Fidelidad (niveles 1–4): ver § Marco de Fidelidad.
• Reproducción directa (N1): mismas ops, mismas constantes, mismo orden.
• Reconstrucción fiel (N2): comportamiento reproducido, pieza sustituida declarada.
• Reconstrucción parcial (N3): lo entendido reproducido, resto documentado ausente.
• Modelo conceptual (N4): idea reproducida, no mecánica.
• Verificador independiente: proceso que nunca confía en auto-reportes.
• Traza completa: secuencia determinista de estados + hash (blake3).
• Semilla fija: splitmix64 state versionado en repo.
• Resultado negativo: experimento contradice hipótesis; se publica.
• Defecto estructural: bug de diseño que bloquea generalidad (no bug de código).
• Since_inflow: campo en The Box con semántica ambigua en emparejamiento.
• Rule.to_dict(): serialización completa omitida en implementación.
• Drift semántico: distancia(intención_declarada, efecto_observado) — NO VALIDADO.
• SPECULATIVO: especificación completa, cero código ejecutable.
• VERIFIED: reproducible, pre-registrado, bootstrap confirmado.
• ESPECULATIVO (sistema): arquitectura diseñada, no validada en producción.
"""),
        (42, "Apéndice G: Comandos de verificación completa", """
# VERIFICACIÓN COMPLETA — EJECUTAR EN ORDEN

## The Box (Rust)
cd the-box
cargo test --workspace -- --nocapture
cargo run --example r1_descend -- --seeds 10000
cargo run --example r5_perturb -- --seeds 10000
cargo run --example r6_seed -- --seeds 1000

## The Box (TypeScript)
cd the-box-ts
npm test
npm run verify:structure -- --compare-rust

## ORACLE E1
cd oracle
python -m pytest experiments/e1_negative.py -v
python -m pytest experiments/e1_negative.py --bootstrap 10000

## SINGULARITY
cd singularity
cargo test --workspace
cargo run --example orchestrator_demo -- --seeds 100

## Showcase
cd showcase
npm run test
npm run build
# Verificar: 182 tests pass, dist/ size < 200 kB JS
curl -I https://thorrijadev.github.io/showcase/  # 200 OK

## HERMES (solo spec)
cat hermes/SPEC.md

## All repos
github.com/ThorrijaDEV
"""),
        (43, "Apéndice H: Q&A — Preguntas frecuentes de investigadores", """
PREGUNTAS QUE SUELEN HACER LOS INVESTIGADORES
(Con respuestas basadas en evidencia — ver QA_INDEX.md para 180+)

P: ¿Cuál es tu background académico?
R: No relevante para la evaluación técnica. Los artefactos hablan.

P: ¿Por qué no publicas en conferencias?
R: Los resultados negativos y defectos estructurales no encajan en formatos estándar.
   Los versiono en repositorios con semillas fijas y bootstrap.

P: ¿Esto es investigación o ingeniería?
R: Es ingeniería con disciplina experimental. La distinción es falsa.

P: ¿Cómo comparas con [paper famoso X]?
R: No comparo con papers. Comparo mis implementaciones con sus especificaciones.
   Si X no tiene código reproducible, no es comparable.

P: ¿Planeas hacer un PhD?
R: Planeo resolver P1, P2, P3. El formato (PhD, lab, startup, independiente)
   es secundario al criterio de falsificación.

P: ¿Por qué Rust y no Python para The Box?
R: Determinismo, ownership, zero-cost abstractions, proptest nativo.
   Python añade GC no determinista y overhead de verificación.

P: ¿Qué métricas usas para 'calidad de código'?
R: Tests de propiedad que fallan si el comportamiento cambia.
   Coverage es ruido; invariantes son señal.

P: ¿Cómo financias esto?
R: No es relevante para la evaluación técnica de los artefactos.
"""),
        (44, "Apéndice I: Referencias cruzadas — Claims ↔ Evidencia", """
MAPEO CLAIM ↔ EVIDENCIA (extracto — ver EVIDENCE_REGISTRY.json)

CL-0001: The Box kernel = arc-incidence multi-digraph → the-box/src/kernel.rs
CL-0002: R1–R6 definen transform/label/copy/match/bind/close → the-box/src/rules.rs
CL-0003: Identidad = clase equivalencia por ι compartida → the-box/src/identity.rs
CL-0004: R1: mean_depth sobrevive gate (p=0.00111) → the-box/experiments/r1.rs
CL-0005: R5: sin perturbación→FIXED_POINT, con→never settles → the-box/experiments/r5.rs
CL-0006: Defectos: since_inflow + Rule.to_dict → the-box/src/defects.md
CL-0007: Puerto TS: estructura idéntica, hashes divergentes → the-box-ts/src/
CL-0008: Fidelidad TS = Nivel 3 → the-box-ts/FIDELITY.md
CL-0009: ORACLE E1: colaboración perjudica (Δ=-0.16, p<0.001) → oracle/experiments/e1_negative.py
CL-0010: Verificador independiente nunca confía en auto-reportes → singularity/verifier/
CL-0011: Protocolo A vs B pre-registrado → oracle/experimental_design.md
CL-0012: Mann-Whitney U + Cliff's δ + bootstrap 10k → oracle/stats.py
CL-0013: SINGULARITY: 5 agentes + orquestador + verificador → singularity/src/
CL-0014: HERMES: 9 tipos + governor + intervención → hermes/SPEC.md
CL-0015: Drift semántico definido, no validado → hermes/SPEC.md#drift
CL-0016: Showcase: 4 modelos N1, 182 tests, 160.69 kB → showcase/src/
CL-0017: Showcase deploy: GitHub Pages, HTTPS, headers → showcase/.github/workflows/
CL-0018: Verificación semanal automatizada → showcase/verify_weekly.sh
CL-0019: HERMES estado = SPECULATIVO → hermes/STATUS.md
CL-0020: Governor SPOF documentado → hermes/SPEC.md#governor
CL-0021: 9 tipos: completos/mínimos/ortogonales? → hermes/OPEN_QUESTIONS.md
CL-0022: P1–P6 problemas abiertos → research/OPEN_PROBLEMS.md
CL-0023: Reproducibilidad: comandos exactos, semillas, hashes → THIS PRESENTATION
CL-0024: Contrato social: rigor > credenciales → SLIDE 33
CL-0025: Cross-lang validation: estructura OK, hashes divergen → the-box-ts/verify/
CL-0026: Zero runtime deps en Showcase → showcase/package.json
CL-0027: Splitmix64 portado Rust↔TS determinista → the-box/src/rng.rs + the-box-ts/src/rng.ts
"""),
        (45, "Apéndice J: Contacto y siguientes pasos", """
CONTACTO Y PRÓXIMOS PASOS

Repositorio de esta presentación:
github.com/ThorrijaDEV/research-presentation

Artefactos por sustrato:
• The Box:        github.com/ThorrijaDEV/the-box
• The Box (TS):   github.com/ThorrijaDEV/the-box-ts
• ORACLE:         github.com/ThorrijaDEV/oracle
• SINGULARITY:    github.com/ThorrijaDEV/singularity
• HERMES (spec):  github.com/ThorrijaDEV/hermes
• Showcase:       github.com/ThorrijaDEV/showcase (live: thorrijadev.github.io/showcase)

Verificación semanal:
• Todos los lunes: CI ejecuta test suites completas
• Resultados en: github.com/ThorrijaDEV/*/actions

Para evaluación técnica:
1. Clona cualquier repo
2. Ejecuta comandos de reproducción (Apéndice G)
3. Verifica que claims ↔ evidencia (Apéndice I)
4. Abre issue si algo no reproduce

Contacto directo:
thorrija.contact@gmail.com
github.com/ThorrijaDEV

"No me creas. Ejecuta el código."
"""),
    ]

    for num, title, code in appendix_slides:
        slides.append(Slide(
            num=num, title=title,
            content_fn=lambda r, c=code, t=title, n=num: (
                r.bg(),
                r.c.setFont(MONO_FAMILY, 12), r.c.setFillColor(FAINT),
                r.c.drawString(MARGIN, r.h - MARGIN, f"{n:02d} — {t}"),
                r.rule_h(r.h - MARGIN - 20, color=EDGE),
                render_wrapped_code(r, c, MARGIN, r.h - MARGIN - 40, r.w - 2*MARGIN),
                r.footer(n, 45, "APÉNDICE")
            ),
            speaker_notes=f"Apéndice técnico: {title}. Disponible para consulta durante Q&A. No se presenta linealmente; se salta si no hay preguntas.",
            qa=[]
        ))

    return slides


# ──────────────────────────────────────────────────────────────────────────────
# MAIN BUILD
# ──────────────────────────────────────────────────────────────────────────────

def build_pdf():
    print("=" * 60)
    print("THORRIJA — Research Presentation Builder")
    print("=" * 60)

    print("\n[1/3] Generating diagrams...")
    generate_all_diagrams()

    print("\n[2/3] Building slides...")
    slides = make_slides()

    output_path = "/home/thorrija/research-presentation/Thorrija_Research_Presentation.pdf"
    c = canvas.Canvas(output_path, pagesize=(PAGE_W, PAGE_H))
    renderer = SlideRenderer(c)

    for slide in slides:
        print(f"  Slide {slide.num:2d}/45: {slide.title}")
        c.setFillColor(BG)
        c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        slide.content_fn(renderer)
        c.showPage()

    c.save()
    print(f"\n[3/3] PDF saved to: {output_path}")

    import subprocess
    result = subprocess.run(["pdfinfo", output_path], capture_output=True, text=True)
    for line in result.stdout.split("\n"):
        if any(k in line for k in ["Pages", "Page size", "File size", "Title"]):
            print(f"  {line.strip()}")

    print("\n✅ Build complete.")


if __name__ == "__main__":
    build_pdf()
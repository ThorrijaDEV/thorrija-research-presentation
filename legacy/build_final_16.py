#!/usr/bin/env python3
"""
THORRIJA — Research Presentation (16 páginas premium)
Rubén Núñez Sierra — 15 años — Para equipo de investigación IA

Generado con Python/ReportLab + matplotlib: control visual total.
Estética: Dark minimal lab + "handwritten" touches.
"""

from __future__ import annotations

import os
import qrcode
from dataclasses import dataclass
from typing import List, Callable, Optional

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
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle, Circle
from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextPath
import matplotlib.font_manager as fm

# ──────────────────────────────────────────────────────────────────────────────
# CONSTANTS & PALETTE
# ──────────────────────────────────────────────────────────────────────────────

PAGE_W, PAGE_H = landscape((1920, 1080))
MARGIN = 72

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
ORANGE_HEX = "#d49b4a"
CYAN_HEX = "#4ec9b0"

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
ORANGE = HexColor(ORANGE_HEX)
CYAN = HexColor(CYAN_HEX)

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
# QR CODE
# ──────────────────────────────────────────────────────────────────────────────

def generate_qr(data: str, path: str, size: int = 400):
    qr = qrcode.QRCode(
        version=3, error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10, border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#f2f0eb", back_color="#0b0b0d")
    img = img.resize((size, size))
    img.save(path)


# ──────────────────────────────────────────────────────────────────────────────
# DIAGRAM GENERATORS
# ──────────────────────────────────────────────────────────────────────────────

ASSETS_DIR = "/home/thorrija/research-presentation/assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

def diag_slide_02_thesis_fidelity():
    f, ax = canvas_fig(12, 4.5)
    st = Stack(ax, 0.03, 0.94, 0.95, 12, 4.5)
    st.text("TESIS + FIDELIDAD", fs=8, color=FAINT_HEX, mono=True, pad=0.006)
    st.text("Tres pilares, una disciplina, cuatro niveles de honestidad", fs=16, color=INK_HEX, weight="bold", pad=0.03)
    cols = [
        ("AFIRMACIÓN → EVIDENCIA → VEREDICTO", INDIGO_HEX,
         "Nada se afirma sin instrumento.\nNada se mide sin trazabilidad.\nNada se concluye sin intento de refutación."),
        ("FIDELIDAD DECLARADA (1–4)", TEAL_HEX,
         "1 = reproducción directa\n2 = reconstrucción fiel\n3 = parcial documentada\n4 = modelo conceptual"),
        ("RESULTADOS NEGATIVOS PUBLICADOS", AMBER_HEX,
         "ORACLE E1: Δ=-0.16, p<0.001\nThe Box: mecanismo explicado\nDefectos: since_inflow, Rule.to_dict"),
    ]
    y = st.y
    w, gap = 0.30, 0.02
    for i, (title, color, body) in enumerate(cols):
        x = 0.03 + i * (w + gap)
        ax.add_patch(FancyBboxPatch((x, y - 0.55), w, 0.55,
                                    boxstyle="round,pad=0,rounding_size=0.006",
                                    linewidth=1, edgecolor=EDGE_HEX, facecolor=PANEL_HEX, zorder=2))
        ax.add_patch(Rectangle((x, y - 0.55), w, 0.005, facecolor=color, edgecolor="none", zorder=3))
        ax.text(x + 0.015, y - 0.03, title, fontsize=10, color=color, weight="bold",
                family="DejaVu Sans Mono", va="top", zorder=6)
        ax.text(x + 0.015, y - 0.10, body, fontsize=9, color=MUTED_HEX, va="top", zorder=6, linespacing=1.5)
    ax.text(0.03, 0.04, "instrumento → cifra → veredicto. Cada claim lleva su nivel.",
            fontsize=8.5, color=FAINT_HEX, style="italic")
    save_fig(f, os.path.join(ASSETS_DIR, "slide_02_thesis_fidelity.png"))

def diag_slide_03_questions_substrates():
    f, ax = canvas_fig(12, 5)
    st = Stack(ax, 0.02, 0.96, 0.96, 12, 5)
    st.text("PREGUNTAS + SUSTRATOS", fs=8, color=FAINT_HEX, mono=True, pad=0.006)
    st.text("Cinco preguntas que guían tres sustratos experimentales", fs=16, color=INK_HEX, weight="bold", pad=0.03)
    qs = [
        "1. ¿Cómo verificas sin confiar en ti mismo?",
        "2. ¿Qué minimalismo genera estructura?",
        "3. ¿Cuándo la colaboración perjudica?",
        "4. ¿Cómo mides deriva semántica sin ground truth?",
        "5. ¿Qué defectos bloquean la generalidad?",
    ]
    y = 0.80
    for q in qs:
        ax.text(0.03, y, q, fontsize=12, color=INK_HEX, weight="bold", va="top", family="DejaVu Sans")
        y -= 0.10
    cards = [
        ("THE BOX", "Sustrato generativo\nmínimo", "6 reglas → identidad,\nlinaje, comunidad", "Rust + TS\nNivel 3 (TS)\nMecanismo explicado", INDIGO_HEX),
        ("SINGULARITY/\nORACLE", "Multi-agente +\nverificación", "5 agentes + Verifier\nindependiente", "E1: VERIFIED\nΔ=-0.16, δ=-0.47\np<0.001", TEAL_HEX),
        ("HERMES", "Orquestación\noperacional", "9 tipos + Governor\n+ intervención auto", "SPECULATIVO\n(spec only)\nDrift sin validar", AMBER_HEX),
    ]
    for i, (name, desc, mech, fidelity, color) in enumerate(cards):
        x = 0.55 + i * 0.15
        ax.add_patch(FancyBboxPatch((x, 0.15), 0.13, 0.65,
                                    boxstyle="round,pad=0,rounding_size=0.008",
                                    linewidth=1, edgecolor=color, facecolor=PANEL_HEX, zorder=2))
        ax.add_patch(Rectangle((x, 0.15), 0.003, 0.65, facecolor=color, edgecolor="none", zorder=3))
        ax.text(x + 0.065, 0.75, name, fontsize=10, color=color, weight="bold", ha="center", va="top", family="DejaVu Sans Mono")
        ax.text(x + 0.065, 0.62, desc, fontsize=8.5, color=MUTED_HEX, ha="center", va="top", linespacing=1.3)
        ax.text(x + 0.065, 0.45, mech, fontsize=8.5, color=INK_HEX, ha="center", va="top", linespacing=1.3)
        ax.add_patch(FancyBboxPatch((x + 0.01, 0.22), 0.11, 0.18,
                                    boxstyle="round,pad=0,rounding_size=0.006",
                                    linewidth=1, edgecolor=color, facecolor=PANEL_2_HEX, zorder=3))
        ax.text(x + 0.065, 0.35, fidelity, fontsize=8, color=color, weight="bold", ha="center", va="center", linespacing=1.2)
    ax.text(0.02, 0.04, "HILO COMÚN: verificación independiente · fidelidad declarada · negativos publicados · defectos documentados",
            fontsize=9, color=AMBER_HEX, weight="bold", family="DejaVu Sans Mono")
    save_fig(f, os.path.join(ASSETS_DIR, "slide_03_questions_substrates.png"))

def diag_slide_04_box_kernel():
    f, ax = canvas_fig(12, 5)
    st = Stack(ax, 0.02, 0.96, 0.96, 12, 5)
    st.text("THE BOX — KERNEL", fs=8, color=FAINT_HEX, mono=True, pad=0.006)
    st.text("Multigrafo de incidencia arco-arco con espacio de IDs compartido", fs=14, color=INK_HEX, weight="bold", pad=0.02)
    ax.text(0.03, 0.75, "G = (V, E, ι, λ, σ)", fontsize=22, color=INK_HEX, weight="bold", family="DejaVu Sans Mono", va="top")
    defs = [
        "V  :  arcos (no nodos) — cada arco ES identidad + payload",
        "E  ⊆ V × V  :  incidencia dirigida (arco apunta a arco)",
        "ι  :  V → Label  :  etiqueta de identidad (copia/pérdida por R3)",
        "λ  :  V → Label  :  etiqueta de linaje (origen)",
        "σ  :  V → {0,1}^k  :  semilla determinista (splitmix64)",
    ]
    y = 0.68
    for d in defs:
        ax.text(0.03, y, d, fontsize=11.5, color=MUTED_HEX, family="DejaVu Sans Mono", va="top")
        y -= 0.055
    arc_positions = [
        (0.65, 0.65, "Arco A\nι=α, λ=∅"),
        (0.80, 0.50, "Arco B\nι=α, λ=A"),
        (0.65, 0.35, "Arco C\nι=β, λ=A"),
    ]
    for i, (x, y, label) in enumerate(arc_positions):
        ax.add_patch(FancyBboxPatch((x - 0.07, y - 0.06), 0.14, 0.12,
                                    boxstyle="round,pad=0,rounding_size=0.01",
                                    linewidth=1.5, edgecolor=INDIGO_HEX, facecolor=PANEL_HEX, zorder=3))
        ax.text(x, y + 0.01, label, fontsize=9, color=INK_HEX, ha="center", va="center", zorder=5, linespacing=1.3, family="DejaVu Sans Mono")
    arrow(ax, (0.65, 0.59), (0.73, 0.50), color=TEAL_HEX, lw=1.5)
    arrow(ax, (0.65, 0.59), (0.58, 0.41), color=TEAL_HEX, lw=1.5, rad=-0.3)
    ax.plot([0.50, 0.50], [0.78, 0.15], color=EDGE_HEX, linewidth=0.8)
    ax.text(0.55, 0.75, "LO QUE SE DERIVA", fontsize=10, color=FAINT_HEX, family="DejaVu Sans Mono", va="top")
    derived = [
        ("identidad", "clase de equivalencia\npor ι compartida", INDIGO_HEX),
        ("linaje", "de qué arco nació,\ny de cuál nació ése", TEAL_HEX),
        ("comunidad", "quién comparte\netiqueta con quién", AMBER_HEX),
    ]
    for i, (name, gloss, color) in enumerate(derived):
        yy = 0.60 - i * 0.16
        ax.add_patch(FancyBboxPatch((0.53, yy - 0.09), 0.44, 0.14,
                                    boxstyle="round,pad=0,rounding_size=0.006",
                                    linewidth=0.9, edgecolor=EDGE_HEX, facecolor=PANEL_HEX, zorder=2))
        ax.add_patch(Rectangle((0.53, yy - 0.09), 0.003, 0.14, facecolor=color, edgecolor="none", zorder=3))
        ax.text(0.55, yy, name, fontsize=10.5, color=INK_HEX, weight="bold", va="top", zorder=6, family="DejaVu Sans Mono")
        ax.text(0.55, yy - 0.04, gloss, fontsize=9, color=MUTED_HEX, va="top", zorder=6)
    ax.text(0.03, 0.05, "Los arcos SON las identidades. No hay nodos separados. Medible: contar arcos con ι idéntica.",
            fontsize=9, color=FAINT_HEX, style="italic")
    save_fig(f, os.path.join(ASSETS_DIR, "slide_04_box_kernel.png"))

def diag_slide_05_box_rules():
    f, ax = canvas_fig(12, 5)
    st = Stack(ax, 0.02, 0.96, 0.96, 12, 5)
    st.text("THE BOX — 6 REGLAS", fs=8, color=FAINT_HEX, mono=True, pad=0.006)
    st.text("Ninguna menciona identidad, linaje o comunidad. Emergen.", fs=14, color=INK_HEX, weight="bold", pad=0.02)
    rules = [
        ("R1", "transform", "Una transformación produce arcos"),
        ("R2", "label", "Cada arco lleva una etiqueta"),
        ("R3", "copy", "Las etiquetas se copian o se pierden"),
        ("R4", "match", "Los arcos se emparejan por etiqueta"),
        ("R5", "bind", "El emparejamiento crea un arco nuevo"),
        ("R6", "close", "Nada más está programado"),
    ]
    y = 0.78
    for i, (code, name, desc) in enumerate(rules):
        yy = y - i * 0.10
        ax.add_patch(Rectangle((0.02, yy - 0.08), 0.0035, 0.06, facecolor=INDIGO_HEX, edgecolor="none", zorder=3))
        ax.text(0.038, yy - 0.01, f"{code}: {name}", fontsize=11.5, color=INK_HEX, weight="bold", va="top", zorder=6, family="DejaVu Sans Mono")
        ax.text(0.038, yy - 0.045, desc, fontsize=10, color=MUTED_HEX, va="top", zorder=6)
        if i < len(rules) - 1:
            ax.plot([0.02, 0.48], [yy - 0.085, yy - 0.085], color=EDGE_HEX, linewidth=0.5, zorder=2)
    ax.plot([0.50, 0.50], [0.80, 0.12], color=EDGE_HEX, linewidth=0.8)
    ax.text(0.55, 0.78, "DERIVADO", fontsize=10, color=FAINT_HEX, family="DejaVu Sans Mono", va="top")
    derived = [
        ("identidad", "historia de ι compartida", INDIGO_HEX),
        ("linaje", "origen recursivo", TEAL_HEX),
        ("comunidad", "ι compartida entre arcos", AMBER_HEX),
    ]
    for i, (name, gloss, color) in enumerate(derived):
        yy = 0.60 - i * 0.15
        ax.add_patch(FancyBboxPatch((0.53, yy - 0.08), 0.44, 0.12,
                                    boxstyle="round,pad=0,rounding_size=0.006",
                                    linewidth=0.9, edgecolor=EDGE_HEX, facecolor=PANEL_HEX, zorder=2))
        ax.add_patch(Rectangle((0.53, yy - 0.08), 0.003, 0.12, facecolor=color, edgecolor="none", zorder=3))
        ax.text(0.55, yy, name, fontsize=11, color=INK_HEX, weight="bold", va="top", zorder=6, family="DejaVu Sans Mono")
        ax.text(0.55, yy - 0.035, gloss, fontsize=9.5, color=MUTED_HEX, va="top", zorder=6)
    ax.text(0.03, 0.04, "R1+R2+R3+R4 → identidad. R5 → linaje. R3+R4 → comunidad. Nada de esto está escrito en las reglas.",
            fontsize=9, color=FAINT_HEX, style="italic")
    save_fig(f, os.path.join(ASSETS_DIR, "slide_05_box_rules.png"))

def diag_slide_06_box_experiments():
    f, ax = canvas_fig(12, 5)
    st = Stack(ax, 0.02, 0.96, 0.96, 12, 5)
    st.text("THE BOX — EXPERIMENTOS + TS + LÍMITES", fs=8, color=FAINT_HEX, mono=True, pad=0.006)
    st.text("Tres experimentos, un hallazgo admitido, puerto TS Nivel 3, seis límites honestos", fs=13, color=INK_HEX, weight="bold", pad=0.025)
    ax.add_patch(FancyBboxPatch((0.02, 0.70), 0.96, 0.22,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=AMBER_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.text(0.04, 0.88, "EMERGENCIA DE IDENTIDAD", fontsize=11, color=AMBER_HEX, weight="bold", family="DejaVu Sans Mono")
    ax.text(0.04, 0.82, "t=0  Arco A (ι=α nueva)  →  t=1  transform(A)→B (ι=α copiada por R3)  →  t=2  transform(B)→C (ι=α copiada)  →  t=3  match(A,C) por ι=α → Arco D (R5)",
            fontsize=9.5, color=MUTED_HEX, va="top", linespacing=1.4)
    ax.text(0.04, 0.74, "Identidad = clase de equivalencia por ι compartida.  Medible: contar arcos con ι idéntica.  Reproducible: misma semilla → misma traza completa.",
            fontsize=9, color=FAINT_HEX, style="italic")
    exps = [
        ("R1: DESCEND gate", INDIGO_HEX,
         "mean_depth sobrevive perturbación periódica\np=0.00111, n=10k semillas\nMecanismo: inyección entropía controlada"),
        ("R5: Perturbación periódica", TEAL_HEX,
         "Sin perturbación → FIXED_POINT (absorbido)\nCon perturbación → never settles (vivo)\nEstructura se sostiene por interrupción externa"),
        ("R6: Semilla → determinismo", AMBER_HEX,
         "splitmix64: misma semilla → misma traza completa\nHash de traza verificable (blake3)"),
    ]
    for i, (title, color, body) in enumerate(exps):
        x = 0.02 + i * 0.325
        ax.add_patch(FancyBboxPatch((x, 0.40), 0.30, 0.28,
                                    boxstyle="round,pad=0,rounding_size=0.008",
                                    linewidth=1, edgecolor=color, facecolor=PANEL_HEX, zorder=2))
        ax.add_patch(Rectangle((x, 0.40), 0.003, 0.28, facecolor=color, edgecolor="none", zorder=3))
        ax.text(x + 0.015, 0.64, title, fontsize=10.5, color=color, weight="bold", va="top", family="DejaVu Sans Mono")
        ax.text(x + 0.015, 0.55, body, fontsize=9, color=MUTED_HEX, va="top", linespacing=1.4)
    ax.add_patch(FancyBboxPatch((0.02, 0.08), 0.47, 0.30,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=TEAL_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.add_patch(Rectangle((0.02, 0.08), 0.003, 0.30, facecolor=TEAL_HEX, edgecolor="none", zorder=3))
    ax.text(0.04, 0.34, "PUERTO TYPESCRIPT — NIVEL 3", fontsize=10.5, color=TEAL_HEX, weight="bold", family="DejaVu Sans Mono")
    ax.text(0.04, 0.28, "Estructura idéntica, hashes divergentes.  since_inflow: semántica ambigua.  Rule.to_dict(): AUSENTE.  No afirmo equivalencia cross-language.",
            fontsize=9, color=MUTED_HEX, linespacing=1.4)
    limits = [
        "① Sin generalidad (2 defectos bloquean)",
        "② Sin hardware (simulación pura)",
        "③ Sin aprendizaje (estructura fija R1–R6)",
        "④ Una métrica admitida (mean_depth, explicada)",
        "⑤ Sin baseline externo",
        "⑥ Puerto TS = nivel 3",
    ]
    ax.add_patch(FancyBboxPatch((0.51, 0.08), 0.47, 0.30,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=RED_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.add_patch(Rectangle((0.51, 0.08), 0.003, 0.30, facecolor=RED_HEX, edgecolor="none", zorder=3))
    ax.text(0.53, 0.34, "LÍMITES HONESTOS — Veredicto: «mecanismo explicado, sin descubrimiento»", fontsize=10, color=RED_HEX, weight="bold", family="DejaVu Sans Mono")
    y = 0.27
    for lim in limits:
        ax.text(0.53, y, lim, fontsize=9, color=MUTED_HEX)
        y -= 0.042
    save_fig(f, os.path.join(ASSETS_DIR, "slide_06_box_experiments.png"))

def diag_slide_07_nox():
    f, ax = canvas_fig(12, 5)
    st = Stack(ax, 0.02, 0.96, 0.96, 12, 5)
    st.text("NOX", fs=8, color=FAINT_HEX, mono=True, pad=0.006)
    st.text("Persistent Autonomous Cognitive Runtime", fs=16, color=INK_HEX, weight="bold", pad=0.02)
    ax.add_patch(FancyBboxPatch((0.02, 0.55), 0.47, 0.38,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=INDIGO_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.add_patch(Rectangle((0.02, 0.55), 0.0035, 0.38, facecolor=INDIGO_HEX, edgecolor="none", zorder=3))
    ax.text(0.04, 0.88, "ARQUITECTURA PERSISTENTE", fontsize=11, color=INDIGO_HEX, weight="bold", family="DejaVu Sans Mono")
    nox_items = [
        "• Loop cognitivo: percibir → razonar → actuar → consolidar",
        "• Memoria episódica: SQLite + vector store (embeddings locales)",
        "• Herramientas: código, web, terminal, sistema de archivos",
        "• Modelos: 20 GB (GGUF quantizados, ejecución local via Ollama)",
        "• Verificación: property tests + trace hashing + replay determinista",
        "• Estado: ACTIVO · repo: nox-cognitive-runtime · 2.4 GB código+datos",
    ]
    y = 0.81
    for item in nox_items:
        ax.text(0.04, y, item, fontsize=9.5, color=MUTED_HEX, linespacing=1.3)
        y -= 0.05
    ax.add_patch(FancyBboxPatch((0.51, 0.55), 0.47, 0.38,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=CYAN_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.add_patch(Rectangle((0.51, 0.55), 0.0035, 0.38, facecolor=CYAN_HEX, edgecolor="none", zorder=3))
    ax.text(0.53, 0.88, "CICLO COGNITIVO", fontsize=11, color=CYAN_HEX, weight="bold", family="DejaVu Sans Mono")
    cycle = [
        ("PERCEIVE", "observación\nentorno + estado", INDIGO_HEX),
        ("REASON", "planificación +\nbúsqueda", TEAL_HEX),
        ("ACT", "ejecución\nherramientas", AMBER_HEX),
        ("CONSOLIDATE", "memoria +\naprendizaje", PLUM_HEX),
    ]
    for i, (name, desc, color) in enumerate(cycle):
        x = 0.54 + i * 0.115
        ax.add_patch(FancyBboxPatch((x, 0.60), 0.105, 0.28,
                                    boxstyle="round,pad=0,rounding_size=0.006",
                                    linewidth=1.5, edgecolor=color, facecolor=PANEL_HEX, zorder=2))
        ax.add_patch(Rectangle((x, 0.60), 0.003, 0.28, facecolor=color, edgecolor="none", zorder=3))
        ax.text(x + 0.0525, 0.82, name, fontsize=9, color=color, weight="bold", ha="center", va="top", family="DejaVu Sans Mono")
        ax.text(x + 0.0525, 0.72, desc, fontsize=7.5, color=MUTED_HEX, ha="center", va="top", linespacing=1.2)
        if i < 3:
            arrow(ax, (x + 0.105, 0.74), (x + 0.115, 0.74), color=FAINT_HEX, lw=1)
    ax.add_patch(FancyBboxPatch((0.02, 0.10), 0.96, 0.42,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=GREEN_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.add_patch(Rectangle((0.02, 0.10), 0.0035, 0.42, facecolor=GREEN_HEX, edgecolor="none", zorder=3))
    ax.text(0.04, 0.48, "DIFERENCIADORES CLAVE", fontsize=11, color=GREEN_HEX, weight="bold", family="DejaVu Sans Mono")
    diffs = [
        "✓ Persistencia real: el estado sobrevive reinicios (SQLite + vector store)",
        "✓ Verificación integrada: property tests en cada ciclo, trace hashing (blake3)",
        "✓ Modelos locales: zero API calls, zero telemetría, ejecución en hardware propio",
        "✓ Herramientas composables: cada tool es función pura con contrato tipado (JSON Schema)",
        "✓ Reproducibilidad: semillas fijas + hash de traza completa + replay determinista",
        "✓ Sin 'AGI' marketing: ingeniería honesta, limitaciones documentadas, fidelidad declarada",
    ]
    y = 0.41
    for d in diffs:
        ax.text(0.04, y, d, fontsize=9.5, color=MUTED_HEX, linespacing=1.3)
        y -= 0.055
    save_fig(f, os.path.join(ASSETS_DIR, "slide_07_nox.png"))

def diag_slide_08_echo():
    f, ax = canvas_fig(12, 5)
    st = Stack(ax, 0.02, 0.96, 0.96, 12, 5)
    st.text("ECHO", fs=8, color=FAINT_HEX, mono=True, pad=0.006)
    st.text("Autonomous Cognitive Organism", fs=16, color=INK_HEX, weight="bold", pad=0.02)
    ax.add_patch(FancyBboxPatch((0.02, 0.55), 0.47, 0.38,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=PLUM_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.add_patch(Rectangle((0.02, 0.55), 0.0035, 0.38, facecolor=PLUM_HEX, edgecolor="none", zorder=3))
    ax.text(0.04, 0.88, "ESPECIFICACIÓN TÉCNICA", fontsize=11, color=PLUM_HEX, weight="bold", family="DejaVu Sans Mono")
    echo_items = [
        "• Stack: FastAPI + React + WebSockets + Ollama (local LLM)",
        "• Memoria: 26 GB (modelos GGUF merged + safetensors + datasets)",
        "• Herramientas: código, web, terminal, FS, planificador, sintetizador",
        "• Ciclo de vida: spawn → plan → execute → verify → consolidate → sleep",
        "• Autonomía: 9 tipos de agente (Observer → Governor) con reglas por diseño",
        "• Estado: IN RESEARCH · repo: echo-cognitive-organism · project_life/echo",
    ]
    y = 0.81
    for item in echo_items:
        ax.text(0.04, y, item, fontsize=9.5, color=MUTED_HEX, linespacing=1.3)
        y -= 0.05
    ax.add_patch(FancyBboxPatch((0.51, 0.55), 0.47, 0.38,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=AMBER_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.add_patch(Rectangle((0.51, 0.55), 0.0035, 0.38, facecolor=AMBER_HEX, edgecolor="none", zorder=3))
    ax.text(0.53, 0.88, "9 TIPOS DE AGENTE (grid 3×3)", fontsize=11, color=AMBER_HEX, weight="bold", family="DejaVu Sans Mono")
    agents = [
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
    for i, (name, desc, color) in enumerate(agents):
        row, col = i // 3, i % 3
        x = 0.52 + col * 0.15
        y = 0.78 - row * 0.115
        ax.add_patch(FancyBboxPatch((x, y), 0.135, 0.095,
                                    boxstyle="round,pad=0,rounding_size=0.006",
                                    linewidth=1, edgecolor=color, facecolor=PANEL_HEX, zorder=2))
        ax.add_patch(Rectangle((x, y), 0.003, 0.095, facecolor=color, edgecolor="none", zorder=3))
        ax.text(x + 0.0675, y + 0.065, name, fontsize=8, color=color, weight="bold", ha="center", va="top", family="DejaVu Sans Mono")
        ax.text(x + 0.0675, y + 0.02, desc, fontsize=6.5, color=MUTED_HEX, ha="center", va="top", linespacing=1.1)
    ax.add_patch(FancyBboxPatch((0.02, 0.10), 0.96, 0.42,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=ORANGE_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.add_patch(Rectangle((0.02, 0.10), 0.0035, 0.42, facecolor=ORANGE_HEX, edgecolor="none", zorder=3))
    ax.text(0.04, 0.48, "ESTADO: SPECULATIVO (spec completa, 0 código ejecutable)  ·  Drift semántico NO validado empíricamente", fontsize=10.5, color=ORANGE_HEX, weight="bold", family="DejaVu Sans Mono")
    insights = [
        "✓ Autonomía por diseño: cada tipo tiene nivel de autonomía explícito (READ_ONLY → EXECUTE)",
        "✓ Intervención automática: drift_semántico > θ → CORRECTOR despachado (definido, no validado)",
        "✓ Governor = SPOF documentado (única autoridad para θ y políticas)",
        "✓ Valor: pensamiento riguroso antes de código. Riesgo: spec hermética que no sobrevive implementación",
        "✓ Repo: echo-cognitive-organism · 26 GB modelos · FastAPI/React/Ollama stack",
    ]
    y = 0.41
    for d in insights:
        ax.text(0.04, y, d, fontsize=9.5, color=MUTED_HEX, linespacing=1.3)
        y -= 0.055
    save_fig(f, os.path.join(ASSETS_DIR, "slide_08_echo.png"))

def diag_slide_09_singularity():
    f, ax = canvas_fig(12, 5)
    st = Stack(ax, 0.02, 0.96, 0.96, 12, 5)
    st.text("SINGULARITY / ORACLE", fs=8, color=FAINT_HEX, mono=True, pad=0.006)
    st.text("Multi-Agente + Verificación Independiente  ·  E1: Colaboración Perjudica", fs=13, color=INK_HEX, weight="bold", pad=0.02)
    ax.add_patch(FancyBboxPatch((0.35, 0.65), 0.30, 0.18,
                                boxstyle="round,pad=0,rounding_size=0.01",
                                linewidth=1.5, edgecolor=INDIGO_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.text(0.5, 0.77, "ORCHESTRATOR", fontsize=11, color=INDIGO_HEX, weight="bold", ha="center", va="center", family="DejaVu Sans Mono")
    ax.text(0.5, 0.69, "routing · lifecycle · contracts", fontsize=8.5, color=MUTED_HEX, ha="center", va="center")
    agents = [
        (0.05, 0.72, "NAVIGATOR", "exploración", INDIGO_HEX),
        (0.05, 0.42, "MAPPER", "construcción mapa", TEAL_HEX),
        (0.55, 0.72, "PLANNER", "política óptima", AMBER_HEX),
        (0.55, 0.42, "EXECUTOR", "ejecución det.", PLUM_HEX),
        (0.92, 0.57, "VERIFIER", "validación indep.", GREEN_HEX),
    ]
    for x, y, name, desc, color in agents:
        ax.add_patch(FancyBboxPatch((x, y), 0.20, 0.25,
                                    boxstyle="round,pad=0,rounding_size=0.008",
                                    linewidth=1, edgecolor=color, facecolor=PANEL_HEX, zorder=2))
        ax.add_patch(Rectangle((x, y), 0.003, 0.25, facecolor=color, edgecolor="none", zorder=3))
        ax.text(x + 0.1, y + 0.18, name, fontsize=10, color=INK_HEX, weight="bold", ha="center", va="center", family="DejaVu Sans Mono")
        ax.text(x + 0.1, y + 0.08, desc, fontsize=8, color=MUTED_HEX, ha="center", va="center", linespacing=1.3)
        if name == "NAVIGATOR":
            arrow(ax, (x + 0.20, y + 0.12), (0.35, 0.70), color=FAINT_HEX, lw=1, rad=-0.2)
        elif name == "MAPPER":
            arrow(ax, (x + 0.20, y + 0.12), (0.35, 0.65), color=FAINT_HEX, lw=1, rad=0.2)
        elif name == "PLANNER":
            arrow(ax, (x - 0.02, y + 0.12), (0.65, 0.70), color=FAINT_HEX, lw=1, rad=0.2)
        elif name == "EXECUTOR":
            arrow(ax, (x - 0.02, y + 0.12), (0.65, 0.65), color=FAINT_HEX, lw=1, rad=-0.2)
        elif name == "VERIFIER":
            arrow(ax, (x - 0.02, y + 0.12), (0.65, 0.68), color=FAINT_HEX, lw=1)
    ax.add_patch(FancyBboxPatch((0.02, 0.10), 0.96, 0.12,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=GREEN_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.text(0.5, 0.17, "VERIFICADOR INDEPENDIENTE — Nunca confía en auto-reportes  ·  Property tests  ·  Trace comparison  ·  Contract validation  ·  Reject if not reproducible",
            fontsize=10, color=GREEN_HEX, weight="bold", ha="center", va="center")
    ax.add_patch(FancyBboxPatch((0.02, 0.28), 0.47, 0.30,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=RED_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.add_patch(Rectangle((0.02, 0.28), 0.0035, 0.30, facecolor=RED_HEX, edgecolor="none", zorder=3))
    ax.text(0.04, 0.53, "E1 RESULTADO NEGATIVO VERIFICADO", fontsize=11, color=RED_HEX, weight="bold", family="DejaVu Sans Mono")
    ax.text(0.04, 0.46, "Protocolo A (aislamiento): 0.78 [0.74, 0.82]", fontsize=9.5, color=INK_HEX)
    ax.text(0.04, 0.40, "Protocolo B (colaboración): 0.62 [0.57, 0.67]", fontsize=9.5, color=INK_HEX)
    ax.text(0.04, 0.34, "Δ = -0.16  ·  IC 95% [-0.21, -0.11]  ·  p < 0.001  ·  Cliff's δ = -0.47  ·  Power = 0.99  ·  Bootstrap 10k", fontsize=9, color=AMBER_HEX, weight="bold")
    ax.text(0.04, 0.28, "Conclusión: overhead de coordinación > ganancia de información compartida (gridworld).", fontsize=9, color=FAINT_HEX, style="italic")
    ax.add_patch(FancyBboxPatch((0.51, 0.28), 0.47, 0.30,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=INDIGO_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.text(0.53, 0.53, "PROTOCOLO A: AISLAMIENTO", fontsize=10.5, color=INDIGO_HEX, weight="bold", family="DejaVu Sans Mono")
    ax.text(0.53, 0.46, "Cada agente ejecuta su rol sin comunicación.  Verificador valida salida individual.", fontsize=9, color=MUTED_HEX)
    ax.text(0.53, 0.40, "Hipótesis: baseline rendimiento individual", fontsize=8.5, color=FAINT_HEX, style="italic")
    ax.add_patch(FancyBboxPatch((0.51, 0.10), 0.47, 0.15,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=AMBER_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.text(0.53, 0.21, "PROTOCOLO B: COLABORACIÓN  ·  Mensajes estructurados  ·  Orquestador coordina plan-ejecutar-verificar  ·  Hipótesis: colaboración mejora (FALSA en E1)", fontsize=9, color=AMBER_HEX, weight="bold")
    ax.add_patch(FancyBboxPatch((0.02, 0.02), 0.96, 0.06,
                                boxstyle="round,pad=0,rounding_size=0.006",
                                linewidth=1, edgecolor=FAINT_HEX, facecolor=PANEL_2_HEX, zorder=2))
    ax.text(0.5, 0.05, "LIMITACIONES: un dominio (gridworld)  ·  un protocolo colaboración  ·  verificador solo estructural  ·  sin learning online  ·  HERMES no implementado  ·  Claim E1: VERIFIED  ·  SINGULARITY general: ESPECULATIVO",
            fontsize=8.5, color=MUTED_HEX, ha="center", va="center")
    save_fig(f, os.path.join(ASSETS_DIR, "slide_09_singularity.png"))

def diag_slide_10_hermes():
    f, ax = canvas_fig(12, 5)
    st = Stack(ax, 0.02, 0.96, 0.96, 12, 5)
    st.text("HERMES", fs=8, color=FAINT_HEX, mono=True, pad=0.006)
    st.text("9 Tipos de Agente  ·  Autonomía por Diseño  ·  Estado: SPECULATIVO", fs=13, color=INK_HEX, weight="bold", pad=0.02)
    agents = [
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
    for i, (name, desc, color) in enumerate(agents):
        row, col = i // 3, i % 3
        x, y = 0.03 + col * 0.32, 0.72 - row * 0.18
        ax.add_patch(FancyBboxPatch((x, y), 0.30, 0.16,
                                    boxstyle="round,pad=0,rounding_size=0.006",
                                    linewidth=0.8, edgecolor=color, facecolor=PANEL_HEX, zorder=2))
        ax.add_patch(Rectangle((x, y), 0.003, 0.16, facecolor=color, edgecolor="none", zorder=3))
        ax.text(x + 0.01, y + 0.10, name, fontsize=8.5, color=color, weight="bold", va="top", family="DejaVu Sans Mono")
        ax.text(x + 0.01, y + 0.03, desc, fontsize=7.5, color=MUTED_HEX, va="top", linespacing=1.2)
    ax.add_patch(FancyBboxPatch((0.03, 0.18), 0.94, 0.16,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1.5, edgecolor=GREEN_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.text(0.5, 0.30, "ORQUESTADOR: routing por contrato  ·  ciclo de vida  ·  reglas de autonomía  ·  intervenciones automáticas (drift > θ)", fontsize=10, color=GREEN_HEX, weight="bold", ha="center", va="center")
    ax.text(0.5, 0.22, "Métricas: latencia P99  ·  tasa intervención  ·  deriva semántica  ·  reproducibilidad de traza", fontsize=9, color=MUTED_HEX, ha="center", va="center")
    ax.add_patch(FancyBboxPatch((0.02, 0.02), 0.96, 0.14,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=AMBER_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.text(0.5, 0.11, "AUTONOMÍA: Observer/Analyzer (READ_ONLY) → Planner (PROPOSE) → Executor (EXECUTE) → Validator/Corrector (INTERVENE si drift>θ) → Governor (AUTHORITY θ)", fontsize=9.5, color=AMBER_HEX, weight="bold", ha="center", va="center", family="DejaVu Sans Mono")
    ax.text(0.5, 0.05, "drift_semántico = distancia(intención_declarada, efecto_observado)  ·  NO VALIDADO EMPÍRICAMENTE  ·  Estado: SPECULATIVO (spec only)  ·  Governor SPOF documentado", fontsize=8.5, color=FAINT_HEX, ha="center", va="center")
    save_fig(f, os.path.join(ASSETS_DIR, "slide_10_hermes.png"))

def diag_slide_11_showcase():
    f, ax = canvas_fig(12, 4.5)
    st = Stack(ax, 0.02, 0.96, 0.96, 12, 4.5)
    st.text("SHOWCASE", fs=8, color=FAINT_HEX, mono=True, pad=0.006)
    st.text("4 Reconstrucciones  ·  Fidelidad Nivel 1 (reproducción directa)  ·  182 tests", fs=13, color=INK_HEX, weight="bold", pad=0.02)
    models = [
        ("1. Wi-Fi Time Machine", INDIGO_HEX,
         "Entrada: volcado iw/nmcli\nRegla: deduplicar BSSID, freq→canal, AKM→WPA\nSalida: mapa calor tiempo × red"),
        ("2. BLE Radar", TEAL_HEX,
         "Entrada: observaciones sintéticas\nRegla: EMA α=0.4, ventanas 15/30s\nSalida: radar, ciclo vida, repetición"),
        ("3. Process Ecosystem Monitor", AMBER_HEX,
         "Entrada: snapshots /proc\nRegla: jiffies→CPU%, identidad (pid,starttime)\nSalida: árbol, eventos, métricas"),
        ("4. Terminal Generative Engine", PLUM_HEX,
         "Entrada: semilla + modo\nRegla: splitmix64 sin estado, campo ángulos analítico\nSalida: fotograma O(1) + huella mundo"),
    ]
    for i, (title, color, body) in enumerate(models):
        x = 0.02 + i * 0.245
        ax.add_patch(FancyBboxPatch((x, 0.15), 0.225, 0.75,
                                    boxstyle="round,pad=0,rounding_size=0.008",
                                    linewidth=1, edgecolor=color, facecolor=PANEL_HEX, zorder=2))
        ax.add_patch(Rectangle((x, 0.15), 0.0035, 0.75, facecolor=color, edgecolor="none", zorder=3))
        ax.text(x + 0.01, 0.85, title, fontsize=10, color=color, weight="bold", va="top", family="DejaVu Sans Mono")
        ax.text(x + 0.01, 0.75, "NIVEL 1", fontsize=9, color=color, weight="bold", va="top", family="DejaVu Sans Mono")
        ax.text(x + 0.01, 0.68, body, fontsize=8.5, color=MUTED_HEX, va="top", linespacing=1.4)
        ax.text(x + 0.01, 0.30, "FIDELIDAD NIVEL 1", fontsize=8, color=color, weight="bold", va="top", family="DejaVu Sans Mono")
    ax.add_patch(FancyBboxPatch((0.02, 0.02), 0.96, 0.10,
                                boxstyle="round,pad=0,rounding_size=0.006",
                                linewidth=1, edgecolor=AMBER_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.text(0.5, 0.07, "Vite + TS  ·  Cloudflare Worker (CORS+rate limit)  ·  182 tests (vitest, property, visual regression)  ·  160.69 kB JS  ·  Zero runtime deps  ·  GitHub Pages  ·  Live: thorrijadev.github.io/showcase",
            fontsize=9, color=AMBER_HEX, weight="bold", ha="center", va="center", family="DejaVu Sans Mono")
    save_fig(f, os.path.join(ASSETS_DIR, "slide_11_showcase.png"))

def diag_slide_12_synthesis():
    f, ax = canvas_fig(12, 4.5)
    st = Stack(ax, 0.02, 0.96, 0.96, 12, 4.5)
    st.text("SÍNTESIS", fs=8, color=FAINT_HEX, mono=True, pad=0.006)
    st.text("5 Sustratos  ·  1 Primitiva de Verificación  ·  Negativos = Conocimiento", fs=13, color=INK_HEX, weight="bold", pad=0.02)
    substrates = [
        ("THE BOX", INDIGO_HEX, "Sustrato generativo\nmínimo", "Reglas R1–R6", "Nivel 3 (TS)", "Mecanismo explicado"),
        ("NOX", CYAN_HEX, "Runtime cognitivo\npersistente", "Loop P-R-A-C", "VERIFIED", "20 GB local"),
        ("ECHO", PLUM_HEX, "Organismo cognitivo\nautónomo", "9 agentes + Gov", "SPECULATIVO", "26 GB / FastAPI"),
        ("SINGULARITY/\nORACLE", TEAL_HEX, "Multi-agente +\nverificación", "5 + Verifier", "E1 VERIFIED", "Δ=-0.16"),
        ("HERMES", AMBER_HEX, "Orquestación\noperacional", "9 + Governor", "SPECULATIVO", "Drift sin validar"),
    ]
    for i, (name, color, desc, mech, fidelity, detail) in enumerate(substrates):
        x = 0.02 + i * 0.195
        ax.add_patch(FancyBboxPatch((x, 0.15), 0.18, 0.75,
                                    boxstyle="round,pad=0,rounding_size=0.008",
                                    linewidth=1, edgecolor=color, facecolor=PANEL_HEX, zorder=2))
        ax.add_patch(Rectangle((x, 0.15), 0.003, 0.75, facecolor=color, edgecolor="none", zorder=3))
        ax.text(x + 0.09, 0.85, name, fontsize=10, color=color, weight="bold", ha="center", va="top", family="DejaVu Sans Mono")
        ax.text(x + 0.09, 0.75, desc, fontsize=8.5, color=MUTED_HEX, ha="center", va="top", linespacing=1.3)
        ax.text(x + 0.09, 0.60, mech, fontsize=8.5, color=INK_HEX, ha="center", va="top", linespacing=1.3)
        ax.add_patch(FancyBboxPatch((x + 0.01, 0.40), 0.16, 0.14,
                                    boxstyle="round,pad=0,rounding_size=0.006",
                                    linewidth=1, edgecolor=color, facecolor=PANEL_2_HEX, zorder=3))
        ax.text(x + 0.09, 0.48, fidelity, fontsize=9, color=color, weight="bold", ha="center", va="center", linespacing=1.2)
        ax.text(x + 0.09, 0.28, detail, fontsize=8, color=MUTED_HEX, ha="center", va="top", linespacing=1.2)
    ax.add_patch(FancyBboxPatch((0.02, 0.02), 0.96, 0.10,
                                boxstyle="round,pad=0,rounding_size=0.006",
                                linewidth=1, edgecolor=AMBER_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.text(0.5, 0.07, "PRIMITIVA DE VERIFICACIÓN (7 capas):  Spec ejecutable  ·  Property tests  ·  Verificador independiente  ·  Reproducibilidad (semillas+hash+bootstrap)  ·  Fidelidad declarada  ·  Negativos publicados  ·  Defectos documentados",
            fontsize=9, color=AMBER_HEX, weight="bold", ha="center", va="center", family="DejaVu Sans Mono")
    save_fig(f, os.path.join(ASSETS_DIR, "slide_12_synthesis.png"))

def diag_slide_13_heatmap():
    f, ax = canvas_fig(12, 4.5)
    st = Stack(ax, 0.02, 0.96, 0.96, 12, 4.5)
    st.text("HEATMAP LÍMITES + 6 PROBLEMAS ABIERTOS", fs=8, color=FAINT_HEX, mono=True, pad=0.006)
    st.text("Rojo = bloquea generalidad  ·  Ámbar = reduce alcance  ·  Gris = documentado", fs=12, color=INK_HEX, weight="bold", pad=0.02)
    rows = [
        "Defectos estructurales",
        "Sin hardware / entorno real",
        "Sin aprendizaje / plasticidad",
        "Sin baseline externo",
        "Serialización incompleta",
        "Verificación no exhaustiva",
        "Spec no implementada",
        "Métricas deriva no validadas",
    ]
    cols = ["The Box", "NOX", "ECHO", "SINGULARITY", "HERMES"]
    severity = [
        [3, 1, 1, 1, 0],
        [3, 2, 3, 2, 2],
        [3, 1, 2, 1, 1],
        [3, 1, 2, 2, 2],
        [3, 0, 1, 1, 0],
        [1, 2, 2, 2, 2],
        [0, 0, 3, 0, 3],
        [0, 1, 2, 2, 2],
    ]
    cell_w, cell_h = 0.17, 0.095
    start_x, start_y = 0.15, 0.82
    sev_colors = {0: BG_HEX, 1: FAINT_HEX, 2: AMBER_HEX, 3: RED_HEX}
    for j, col in enumerate(cols):
        x = start_x + j * cell_w
        ax.text(x + cell_w/2, start_y + 0.03, col, fontsize=9.5, color=INK_HEX, weight="bold", ha="center", va="bottom", family="DejaVu Sans Mono")
    for i, row in enumerate(rows):
        y = start_y - i * cell_h
        ax.text(start_x - 0.01, y + cell_h/2, row, fontsize=8.5, color=MUTED_HEX, ha="right", va="center")
        for j in range(5):
            x = start_x + j * cell_w
            s = severity[i][j]
            fc = sev_colors[s]
            ax.add_patch(Rectangle((x, y), cell_w, cell_h, facecolor=fc, edgecolor=EDGE_HEX, linewidth=0.5, zorder=2))
            if s > 0:
                labels = {1: "doc", 2: "alcance", 3: "bloquea"}
                ax.text(x + cell_w/2, y + cell_h/2, labels[s], fontsize=7, color=INK_HEX if s<3 else BG_HEX, weight="bold", ha="center", va="center")
    ax.text(0.02, 0.52, "PROBLEMAS ABIERTOS (con criterio de falsificación):", fontsize=11, color=AMBER_HEX, weight="bold", family="DejaVu Sans Mono")
    problems = [
        ("P1", "Generalidad The Box", "Resolver since_inflow + Rule.to_dict → ¿composición recursiva arbitraria?", INDIGO_HEX),
        ("P2", "Colaboración efectiva", "E1: overhead > ganancia → ¿topologías/contratos que inviertan la desigualdad?", TEAL_HEX),
        ("P3", "Verificación emergente", "Hoy estructural → mañana semántica (identidad/linaje)", AMBER_HEX),
        ("P4", "Sim→Hardware", "The Box puro software → ¿mínima interfaz sensor/actuador preserve determinismo?", PLUM_HEX),
        ("P5", "Métricas deriva HERMES", "drift definido sin ground truth → ¿cómo medir?", RED_HEX),
        ("P6", "Cross-language repro", "Rust↔TS estructura OK, hashes divergen → ¿nivel 2 sin serialización binaria?", FAINT_HEX),
    ]
    y = 0.48
    for code, title, question, color in problems:
        ax.add_patch(Rectangle((0.02, y - 0.055), 0.0035, 0.04, facecolor=color, edgecolor="none", zorder=3))
        ax.text(0.038, y - 0.005, f"{code}: {title}", fontsize=10.5, color=INK_HEX, weight="bold", va="top")
        ax.text(0.038, y - 0.04, question, fontsize=9, color=MUTED_HEX, va="top", linespacing=1.3)
        y -= 0.065
    save_fig(f, os.path.join(ASSETS_DIR, "slide_13_heatmap.png"))

def diag_slide_14_repro_cta():
    f, ax = canvas_fig(12, 4.5)
    st = Stack(ax, 0.02, 0.96, 0.96, 12, 4.5)
    st.text("REPRODUCIBILIDAD + CONTRATO + CTA", fs=8, color=FAINT_HEX, mono=True, pad=0.006)
    st.text("Comandos exactos  ·  Lo que traigo / no traigo  ·  3 formas de trabajar juntos", fs=12, color=INK_HEX, weight="bold", pad=0.02)
    ax.add_patch(FancyBboxPatch((0.02, 0.55), 0.47, 0.40,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=INDIGO_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.add_patch(Rectangle((0.02, 0.55), 0.0035, 0.40, facecolor=INDIGO_HEX, edgecolor="none", zorder=3))
    ax.text(0.04, 0.90, "COMANDOS PARA VERIFICAR TODO", fontsize=10.5, color=INDIGO_HEX, weight="bold", family="DejaVu Sans Mono")
    cmds = [
        "The Box (Rust):     cargo test --package the-box && cargo run --example r1_descend -- --seeds 10000",
        "The Box (TS):       cd the-box-ts && npm test && npm run verify:structure -- --compare-rust",
        "NOX:                cd nox && cargo test --workspace",
        "ECHO (spec):        cat echo/SPEC.md",
        "ORACLE E1:          cd oracle && python -m pytest experiments/e1_negative.py --bootstrap 10000",
        "SINGULARITY:        cd singularity && cargo test --workspace",
        "Showcase:           cd showcase && npm test && npm run build  # 182 tests",
        "HERMES (spec):      cat hermes/SPEC.md",
    ]
    y = 0.83
    for c in cmds:
        ax.text(0.04, y, c, fontsize=8.5, color=MUTED_HEX, family="DejaVu Sans Mono", linespacing=1.3)
        y -= 0.045
    ax.add_patch(FancyBboxPatch((0.51, 0.55), 0.47, 0.40,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=AMBER_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.add_patch(Rectangle((0.51, 0.55), 0.0035, 0.40, facecolor=AMBER_HEX, edgecolor="none", zorder=3))
    ax.text(0.53, 0.90, "CONTRATO SOCIAL", fontsize=10.5, color=AMBER_HEX, weight="bold", family="DejaVu Sans Mono")
    ax.text(0.53, 0.83, "LO QUE TRAIGO:", fontsize=10, color=INK_HEX, weight="bold")
    brings = [
        "• 24 proyectos construidos, documentados, verificables",
        "• Disciplina: afirmación → evidencia → veredicto",
        "• 5 sustratos experimentales con preguntas concretas",
        "• Negativos versionados, defectos documentados",
        "• Fidelidad declarada (niveles 1–4) en cada claim",
        "• Reproducibilidad: comandos, semillas, hashes",
    ]
    y = 0.76
    for b in brings:
        ax.text(0.53, y, b, fontsize=9, color=MUTED_HEX)
        y -= 0.042
    ax.text(0.53, 0.48, "LO QUE PIDO: gente que exija más rigor del que yo tengo hoy", fontsize=10, color=INK_HEX, weight="bold")
    ax.text(0.53, 0.42, "LO QUE NO TRAIGO: credenciales inventadas, métricas infladas, promesas de AGI", fontsize=9, color=FAINT_HEX, style="italic")
    ax.add_patch(FancyBboxPatch((0.02, 0.10), 0.96, 0.42,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=GREEN_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.add_patch(Rectangle((0.02, 0.10), 0.0035, 0.42, facecolor=GREEN_HEX, edgecolor="none", zorder=3))
    ax.text(0.04, 0.48, "TRES FORMAS DE TRABAJAR JUNTOS (cada una con criterio de falsificación):", fontsize=10.5, color=GREEN_HEX, weight="bold", family="DejaVu Sans Mono")
    ctas = [
        "1. Resolver P1 (The Box): since_inflow + Rule.to_dict → generalidad  ·  Requiere: PL theory, type systems, formal verification",
        "2. Invertir E1 (ORACLE): topologías/contratos donde colaboración > aislamiento  ·  Requiere: multi-agent, comm protocols, exp design",
        "3. Implementar HERMES: de SPECULATIVO a VERIFIED  ·  Requiere: distributed systems, observability, correctness-by-construction",
        "4. Puente NOX/ECHO: memoria episódica compartida + verificación cruzada  ·  Requiere: memory systems, formal methods",
    ]
    y = 0.40
    for c in ctas:
        ax.text(0.04, y, c, fontsize=9.5, color=MUTED_HEX, linespacing=1.3)
        y -= 0.06
    ax.text(0.04, 0.15, "Cada una tiene criterio de falsificación.  Ninguna es 'investigar a ver qué sale'.", fontsize=9, color=FAINT_HEX, style="italic")
    save_fig(f, os.path.join(ASSETS_DIR, "slide_14_repro_cta.png"))

def diag_slide_15_appendix():
    f, ax = canvas_fig(12, 4.5)
    st = Stack(ax, 0.02, 0.96, 0.96, 12, 4.5)
    st.text("APÉNDICE TÉCNICO", fs=8, color=FAINT_HEX, mono=True, pad=0.006)
    st.text("The Box Kernel (Rust)  ·  ORACLE E1 Stats (Python)  ·  SINGULARITY Contract (TS)", fs=12, color=INK_HEX, weight="bold", pad=0.02)
    ax.add_patch(FancyBboxPatch((0.02, 0.55), 0.47, 0.40,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=INDIGO_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.add_patch(Rectangle((0.02, 0.55), 0.0035, 0.40, facecolor=INDIGO_HEX, edgecolor="none", zorder=3))
    ax.text(0.04, 0.90, "THE BOX KERNEL (Rust)", fontsize=10.5, color=INDIGO_HEX, weight="bold", family="DejaVu Sans Mono")
    kernel_code = """// the-box/src/kernel.rs
pub struct ArcIncidenceGraph {
    arcs: Vec<Arc>,
    incidence: Vec<Vec<usize>>,
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
pub trait Rule { fn to_dict(&self) -> Dict; }  // DEFECTO: omitido"""
    ax.text(0.04, 0.83, kernel_code, fontsize=7.5, color=MUTED_HEX, family="DejaVu Sans Mono", linespacing=1.2)
    ax.add_patch(FancyBboxPatch((0.51, 0.55), 0.47, 0.40,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=TEAL_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.add_patch(Rectangle((0.51, 0.55), 0.0035, 0.40, facecolor=TEAL_HEX, edgecolor="none", zorder=3))
    ax.text(0.53, 0.90, "ORACLE E1 STATS (Python)", fontsize=10.5, color=TEAL_HEX, weight="bold", family="DejaVu Sans Mono")
    stats_code = """# oracle/experiments/e1_negative.py
import numpy as np
from scipy.stats import mannwhitneyu
from scipy import bootstrap

def run_e1(n_seeds=500):
    protocol_a = [run_protocol_a(s) for s in seeds]
    protocol_b = [run_protocol_b(s) for s in seeds]
    stat, p = mannwhitneyu(protocol_a, protocol_b, alternative='two-sided')
    delta = cliffs_delta(protocol_a, protocol_b)
    ci = bootstrap((protocol_a, protocol_b), np.mean_diff, n_resamples=10000)
    return {"mean_a": np.mean(protocol_a), "mean_b": np.mean(protocol_b),
            "delta": delta, "p": p, "ci": ci.confidence_interval,
            "power": post_hoc_power(delta, n_seeds, alpha=0.05)}
# Verificado: mean_a=0.78, mean_b=0.62, Δ=-0.16, p<0.001, δ=-0.47, power=0.99"""
    ax.text(0.53, 0.83, stats_code, fontsize=7.5, color=MUTED_HEX, family="DejaVu Sans Mono", linespacing=1.2)
    ax.add_patch(FancyBboxPatch((0.02, 0.10), 0.96, 0.42,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=AMBER_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.add_patch(Rectangle((0.02, 0.10), 0.0035, 0.42, facecolor=AMBER_HEX, edgecolor="none", zorder=3))
    ax.text(0.04, 0.48, "SINGULARITY CONTRACT (TypeScript)", fontsize=10.5, color=AMBER_HEX, weight="bold", family="DejaVu Sans Mono")
    contract_code = """// singularity/contracts/agent.ts
interface AgentContract {
    role: AgentRole;
    input_schema: JSONSchema;
    output_schema: JSONSchema;
    invariants: Invariant[];           // property tests
    autonomy_level: AutonomyLevel;     // READ_ONLY | PROPOSE | EXECUTE
    drift_threshold?: number;          // for VALIDATOR/CORRECTOR
}
interface VerificationResult {
    passed: boolean;
    property_violations: PropertyViolation[];
    trace_hash: string;                // blake3 full trace
    reproducibility: ReproducibilityReport;
}
class IndependentVerifier {
    async verify(agent, contract, seed): VerificationResult {
        // 1. Run agent with fixed seed
        // 2. Generate inputs via fast-check / proptest
        // 3. Validate invariants vs output
        // 4. Compare trace_hash with expected
        // 5. NEVER trust agent.self_report()
    }
}"""
    ax.text(0.04, 0.41, contract_code, fontsize=7.5, color=MUTED_HEX, family="DejaVu Sans Mono", linespacing=1.2)
    save_fig(f, os.path.join(ASSETS_DIR, "slide_15_appendix.png"))

def diag_slide_16_personal():
    f, ax = canvas_fig(12, 5)
    st = Stack(ax, 0.02, 0.96, 0.96, 12, 5)
    ax.add_patch(FancyBboxPatch((0.02, 0.10), 0.47, 0.85,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=AMBER_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.add_patch(Rectangle((0.02, 0.10), 0.0035, 0.85, facecolor=AMBER_HEX, edgecolor="none", zorder=3))
    ax.text(0.04, 0.90, "Rubén Núñez Sierra", fontsize=18, color=INK_HEX, weight="bold", family="DejaVu Sans")
    ax.text(0.04, 0.84, "15 años", fontsize=14, color=AMBER_HEX, weight="bold", family="DejaVu Sans")
    handwritten = (
        "No destaco por mis notas.\n"
        "No soy popular.\n\n"
        "Simplemente me considero un adolescente\n"
        "bastante ambicioso que quiere aprender\n"
        "de mucha gente.\n\n"
        "Lo que ves aquí — The Box, NOX, ECHO,\n"
        "SINGULARITY, HERMES, el Showcase —\n"
        "no es 'deberes'. Es lo que construyo\n"
        "cuando nadie me obliga.\n\n"
        "Mi disciplina es simple:\n"
        "si no se puede ejecutar, medir y repetir,\n"
        "no existe.\n\n"
        "Los defectos los documento.\n"
        "Los negativos los publico.\n"
        "La fidelidad la declaro.\n\n"
        "Busco gente que exija más rigor\n"
        "del que yo tengo hoy.\n\n"
        "Gracias por leer hasta aquí."
    )
    ax.text(0.04, 0.72, handwritten, fontsize=12, color=INK_HEX, linespacing=1.5, family="DejaVu Sans")
    ax.add_patch(FancyBboxPatch((0.51, 0.10), 0.47, 0.85,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=1, edgecolor=INDIGO_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.add_patch(Rectangle((0.51, 0.10), 0.0035, 0.85, facecolor=INDIGO_HEX, edgecolor="none", zorder=3))
    ax.text(0.53, 0.90, "CONTACTO + ARTEFACTOS", fontsize=14, color=INDIGO_HEX, weight="bold", family="DejaVu Sans Mono")
    ax.add_patch(Rectangle((0.60, 0.60), 0.30, 0.30, facecolor=PANEL_2_HEX, edgecolor=EDGE_HEX, linewidth=1, zorder=3))
    ax.text(0.75, 0.55, "[ QR: github.com/ThorrijaDEV ]", fontsize=10, color=MUTED_HEX, ha="center", va="center", family="DejaVu Sans Mono")
    ax.text(0.75, 0.50, "Escanea para portfolio", fontsize=8, color=FAINT_HEX, ha="center", va="center")
    links = ["github.com/ThorrijaDEV", "thorrijadev.github.io/showcase", "thorrija.contact@gmail.com"]
    y = 0.45
    for link in links:
        ax.text(0.53, y, link, fontsize=11, color=INK_HEX, family="DejaVu Sans Mono")
        y -= 0.05
    ax.text(0.53, 0.30, "24 proyectos  ·  5 sustratos  ·  182 tests  ·  0 deps runtime  ·  1 disciplina", fontsize=10, color=AMBER_HEX, weight="bold", ha="center", va="center", family="DejaVu Sans Mono")
    ax.add_patch(FancyBboxPatch((0.02, 0.02), 0.96, 0.06,
                                boxstyle="round,pad=0,rounding_size=0.006",
                                linewidth=1, edgecolor=AMBER_HEX, facecolor=PANEL_HEX, zorder=2))
    ax.text(0.5, 0.05, "\"No me creas. Ejecuta el código.\"  ·  Fidelidad declarada  ·  Defectos documentados  ·  Negativos versionados",
            fontsize=9, color=AMBER_HEX, weight="bold", ha="center", va="center", family="DejaVu Sans Mono")
    save_fig(f, os.path.join(ASSETS_DIR, "slide_16_personal.png"))

def generate_all_diagrams():
    print("Generating 15 diagrams...")
    diag_slide_02_thesis_fidelity(); print("  02_thesis_fidelity")
    diag_slide_03_questions_substrates(); print("  03_questions_substrates")
    diag_slide_04_box_kernel(); print("  04_box_kernel")
    diag_slide_05_box_rules(); print("  05_box_rules")
    diag_slide_06_box_experiments(); print("  06_box_experiments")
    diag_slide_07_nox(); print("  07_nox")
    diag_slide_08_echo(); print("  08_echo")
    diag_slide_09_singularity(); print("  09_singularity")
    diag_slide_10_hermes(); print("  10_hermes")
    diag_slide_11_showcase(); print("  11_showcase")
    diag_slide_12_synthesis(); print("  12_synthesis")
    diag_slide_13_heatmap(); print("  13_heatmap")
    diag_slide_14_repro_cta(); print("  14_repro_cta")
    diag_slide_15_appendix(); print("  15_appendix")
    diag_slide_16_personal(); print("  16_personal")
    print("All diagrams generated.")

# ──────────────────────────────────────────────────────────────────────────────
# QR CODE
# ──────────────────────────────────────────────────────────────────────────────

QR_PATH = os.path.join(ASSETS_DIR, "qr_portfolio.png")
generate_qr("https://github.com/ThorrijaDEV", QR_PATH, size=400)


# ──────────────────────────────────────────────────────────────────────────────
# SLIDE RENDERER
# ──────────────────────────────────────────────────────────────────────────────

class SlideRenderer:
    def __init__(self, c: canvas.Canvas):
        self.c = c
        self.w, self.h = PAGE_W, PAGE_H

    def bg(self):
        self.c.setFillColor(BG)
        self.c.rect(0, 0, self.w, self.h, fill=1, stroke=0)

    def rule_h(self, y, x0=MARGIN, x1=None, color=EDGE, w=0.8):
        if x1 is None: x1 = self.w - MARGIN
        self.c.setStrokeColor(color); self.c.setLineWidth(w)
        self.c.line(x0, y, x1, y)

    def image(self, x, y, img_path, max_w=None, max_h=None):
        from PIL import Image
        im = Image.open(img_path)
        iw, ih = im.size
        if max_w and iw > max_w:
            scale = max_w / iw; iw, ih = max_w, ih * scale
        if max_h and ih > max_h:
            scale = max_h / ih; iw, ih = iw * scale, max_h
        self.c.drawImage(img_path, x, y - ih, width=iw, height=ih, preserveAspectRatio=True, mask='auto')
        return iw, ih

    def footer(self, slide_num: int, total: int, tag: str = ""):
        self.c.setFont(MONO_FAMILY, 9); self.c.setFillColor(FAINT)
        left = f"{slide_num}/{total}"; right = tag
        self.c.drawString(MARGIN, MARGIN/2, left)
        tw = self.c.stringWidth(right, MONO_FAMILY, 9)
        self.c.drawString(self.w - MARGIN - tw, MARGIN/2, right)

    def mono(self, x, y, text, fs=14, color=INK):
        self.c.setFont(MONO_FAMILY, fs); self.c.setFillColor(color)
        self.c.drawString(x, y, text)

    def handwritten_block(self, x, y, lines, fs=12, color=INK, line_h=18):
        self.c.setFont(SANS_FAMILY, fs); self.c.setFillColor(color)
        for line in lines:
            self.c.drawString(x, y, line)
            y -= line_h
        return y


# ──────────────────────────────────────────────────────────────────────────────
# SLIDE DEFINITIONS
# ──────────────────────────────────────────────────────────────────────────────

def draw_slide_1(r):
    r.bg()
    r.c.setFont(SANS_BOLD, 72); r.c.setFillColor(INK)
    r.c.drawCentredString(r.w/2, r.h*0.55, "THORRIJA")
    r.c.setFont(SANS_FAMILY, 22); r.c.setFillColor(MUTED)
    r.c.drawCentredString(r.w/2, r.h*0.45, "Presentación para equipo de investigación IA")
    r.c.setFont(MONO_FAMILY, 14); r.c.setFillColor(FAINT)
    r.c.drawCentredString(r.w/2, r.h*0.35, "Noviembre 2026  ·  Rubén Núñez Sierra")
    r.rule_h(r.h*0.3, x0=r.w*0.25, x1=r.w*0.75, color=AMBER, w=2)
    r.c.setFont(MONO_FAMILY, 12); r.c.setFillColor(AMBER)
    r.c.drawCentredString(r.w/2, r.h*0.25, "github.com/ThorrijaDEV  ·  thorrijadev.github.io/showcase")
    r.footer(1, 16, "THORRIJA")

def draw_slide_2(r):
    r.bg()
    r.mono(MARGIN, r.h - MARGIN, "01 — TESIS + FIDELIDAD", 14, INDIGO)
    r.image(MARGIN, r.h - MARGIN - 60, os.path.join(ASSETS_DIR, "slide_02_thesis_fidelity.png"), max_w=r.w - 2*MARGIN)
    r.footer(2, 16, "TESIS")

def draw_slide_3(r):
    r.bg()
    r.mono(MARGIN, r.h - MARGIN, "02 — PREGUNTAS + SUSTRATOS", 14, INDIGO)
    r.image(MARGIN, r.h - MARGIN - 60, os.path.join(ASSETS_DIR, "slide_03_questions_substrates.png"), max_w=r.w - 2*MARGIN)
    r.footer(3, 16, "PREGUNTAS")

def draw_slide_4(r):
    r.bg()
    r.mono(MARGIN, r.h - MARGIN, "03 — THE BOX: KERNEL", 14, INDIGO)
    r.image(MARGIN, r.h - MARGIN - 60, os.path.join(ASSETS_DIR, "slide_04_box_kernel.png"), max_w=r.w - 2*MARGIN)
    r.footer(4, 16, "KERNEL")

def draw_slide_5(r):
    r.bg()
    r.mono(MARGIN, r.h - MARGIN, "04 — THE BOX: 6 REGLAS", 14, INDIGO)
    r.image(MARGIN, r.h - MARGIN - 60, os.path.join(ASSETS_DIR, "slide_05_box_rules.png"), max_w=r.w - 2*MARGIN)
    r.footer(5, 16, "REGLAS")

def draw_slide_6(r):
    r.bg()
    r.mono(MARGIN, r.h - MARGIN, "05 — THE BOX: EXP + TS + LÍMITES", 14, INDIGO)
    r.image(MARGIN, r.h - MARGIN - 60, os.path.join(ASSETS_DIR, "slide_06_box_experiments.png"), max_w=r.w - 2*MARGIN)
    r.footer(6, 16, "EXP + TS")

def draw_slide_7(r):
    r.bg()
    r.mono(MARGIN, r.h - MARGIN, "06 — NOX: COGNITIVE RUNTIME", 14, INDIGO)
    r.image(MARGIN, r.h - MARGIN - 60, os.path.join(ASSETS_DIR, "slide_07_nox.png"), max_w=r.w - 2*MARGIN)
    r.footer(7, 16, "NOX")

def draw_slide_8(r):
    r.bg()
    r.mono(MARGIN, r.h - MARGIN, "07 — ECHO: COGNITIVE ORGANISM", 14, INDIGO)
    r.image(MARGIN, r.h - MARGIN - 60, os.path.join(ASSETS_DIR, "slide_08_echo.png"), max_w=r.w - 2*MARGIN)
    r.footer(8, 16, "ECHO")

def draw_slide_9(r):
    r.bg()
    r.mono(MARGIN, r.h - MARGIN, "08 — SINGULARITY / ORACLE", 14, INDIGO)
    r.image(MARGIN, r.h - MARGIN - 60, os.path.join(ASSETS_DIR, "slide_09_singularity.png"), max_w=r.w - 2*MARGIN)
    r.footer(9, 16, "ORACLE")

def draw_slide_10(r):
    r.bg()
    r.mono(MARGIN, r.h - MARGIN, "09 — HERMES", 14, INDIGO)
    r.image(MARGIN, r.h - MARGIN - 60, os.path.join(ASSETS_DIR, "slide_10_hermes.png"), max_w=r.w - 2*MARGIN)
    r.footer(10, 16, "HERMES")

def draw_slide_11(r):
    r.bg()
    r.mono(MARGIN, r.h - MARGIN, "10 — SHOWCASE: 4 MODELOS N1", 14, INDIGO)
    r.image(MARGIN, r.h - MARGIN - 60, os.path.join(ASSETS_DIR, "slide_11_showcase.png"), max_w=r.w - 2*MARGIN)
    r.footer(11, 16, "SHOWCASE")

def draw_slide_12(r):
    r.bg()
    r.mono(MARGIN, r.h - MARGIN, "11 — SÍNTESIS: 5 SUSTRATOS", 14, INDIGO)
    r.image(MARGIN, r.h - MARGIN - 60, os.path.join(ASSETS_DIR, "slide_12_synthesis.png"), max_w=r.w - 2*MARGIN)
    r.footer(12, 16, "SÍNTESIS")

def draw_slide_13(r):
    r.bg()
    r.mono(MARGIN, r.h - MARGIN, "12 — HEATMAP + PROBLEMAS ABIERTOS", 14, INDIGO)
    r.image(MARGIN, r.h - MARGIN - 60, os.path.join(ASSETS_DIR, "slide_13_heatmap.png"), max_w=r.w - 2*MARGIN)
    r.footer(13, 16, "HEATMAP")

def draw_slide_14(r):
    r.bg()
    r.mono(MARGIN, r.h - MARGIN, "13 — REPRODUCIBILIDAD + CTA", 14, INDIGO)
    r.image(MARGIN, r.h - MARGIN - 60, os.path.join(ASSETS_DIR, "slide_14_repro_cta.png"), max_w=r.w - 2*MARGIN)
    r.footer(14, 16, "REPRO + CTA")

def draw_slide_15(r):
    r.bg()
    r.mono(MARGIN, r.h - MARGIN, "14 — APÉNDICE: CÓDIGO + STATS", 14, INDIGO)
    r.image(MARGIN, r.h - MARGIN - 60, os.path.join(ASSETS_DIR, "slide_15_appendix.png"), max_w=r.w - 2*MARGIN)
    r.footer(15, 16, "APÉNDICE")

def draw_slide_16(r):
    r.bg()
    left_w = r.w * 0.48
    right_x = MARGIN + left_w + 20  # 20px gap so the panels never overlap
    right_w = r.w - right_x - MARGIN

    # ── LEFT PANEL (Rubén, handwritten) ─────────────────────────────────────
    r.c.setFillColor(PANEL); r.c.setStrokeColor(AMBER); r.c.setLineWidth(1)
    r.c.roundRect(MARGIN, MARGIN + 20, left_w, r.h - 2*MARGIN - 40, 8, fill=1, stroke=1)
    r.c.setFillColor(AMBER); r.c.rect(MARGIN, MARGIN + 20, 3, r.h - 2*MARGIN - 40, fill=1, stroke=0)

    # Header
    r.c.setFont(SANS_BOLD, 20); r.c.setFillColor(INK)
    r.c.drawString(MARGIN + 20, r.h - MARGIN - 80, "Rubén Núñez Sierra")
    r.c.setFont(SANS_FAMILY, 16); r.c.setFillColor(AMBER)
    r.c.drawString(MARGIN + 20, r.h - MARGIN - 110, "15 años")

    # Handwritten narrative — occupies the BOTTOM of the left panel, spanning
    # roughly y∈[450, 860]. The QR lives in the right panel at y∈[260, 440],
    # so the two regions are vertically offset with a ~210px vertical gap
    # (y=440..450) AND at completely different x — nothing can overlap.
    handwritten = [
        "No destaco por mis notas.",
        "No soy popular.",
        "",
        "Simplemente me considero un adolescente",
        "bastante ambicioso que quiere aprender",
        "de mucha gente.",
        "",
        "Lo que ves aquí — The Box, NOX, ECHO,",
        "SINGULARITY, HERMES, el Showcase —",
        "no es 'deberes'. Es lo que construyo",
        "cuando nadie me obliga.",
        "",
        "Mi disciplina es simple:",
        "si no se puede ejecutar, medir y repetir,",
        "no existe.",
        "",
        "Los defectos los documento.",
        "Los negativos los publico.",
        "La fidelidad la declaro.",
        "",
        "Busco gente que exija más rigor",
        "del que yo tengo hoy.",
        "",
        "Gracias por leer hasta aquí.",
    ]
    y = 860.0  # 23 lines * 18.5 ≈ 425px tall → spans ~[435, 860]
    r.c.setFont(SANS_FAMILY, 12); r.c.setFillColor(INK)
    for line in handwritten:
        r.c.drawString(MARGIN + 20, y, line)
        y -= 18.5

    # ── RIGHT PANEL (QR + links + summary) ───────────────────────────────────
    r.c.setFillColor(PANEL); r.c.setStrokeColor(INDIGO); r.c.setLineWidth(1)
    r.c.roundRect(right_x, MARGIN + 20, right_w, r.h - 2*MARGIN - 40, 8, fill=1, stroke=1)
    r.c.setFillColor(INDIGO); r.c.rect(right_x, MARGIN + 20, 3, r.h - 2*MARGIN - 40, fill=1, stroke=0)

    rx = right_x + 30
    qr_size = 180
    qr_y = 300
    qr_x = rx + (right_w - qr_size) / 2

    # Title at top of the right panel
    r.c.setFont(SANS_BOLD, 16); r.c.setFillColor(INDIGO)
    r.c.drawString(rx, r.h - MARGIN - 40, "CONTACTO + ARTEFACTOS")

    # QR code
    r.c.drawImage(QR_PATH, qr_x, qr_y, width=qr_size, height=qr_size, mask='auto')
    r.c.setFont(MONO_FAMILY, 9); r.c.setFillColor(FAINT)
    r.c.drawCentredString(qr_x + qr_size / 2, qr_y + qr_size + 8,
                          "Escanea → github.com/ThorrijaDEV")

    # Links below QR
    links = ["github.com/ThorrijaDEV", "thorrijadev.github.io/showcase",
             "thorrija.contact@gmail.com"]
    r.c.setFont(MONO_FAMILY, 11); r.c.setFillColor(INK)
    for i, link in enumerate(links):
        r.c.drawString(rx, qr_y + qr_size + 40 + i * 20, link)

    # Summary — below the last link (y≈620 for the 6th link at i=5 → links reach ~620)
    r.c.setFont(MONO_FAMILY, 10); r.c.setFillColor(AMBER)
    r.c.drawCentredString(rx + (right_w - 60) / 2, qr_y + qr_size + 145,
        "24 proyectos  ·  5 sustratos  ·  182 tests  ·  0 deps runtime  ·  1 disciplina")

    # Bottom bar
    r.c.setFillColor(PANEL); r.c.setStrokeColor(AMBER); r.c.setLineWidth(1.5)
    r.c.roundRect(MARGIN, MARGIN/2, r.w - 2*MARGIN, 30, 4, fill=1, stroke=1)
    r.c.setFont(MONO_FAMILY, 10); r.c.setFillColor(AMBER)
    r.c.drawCentredString(r.w/2, MARGIN/2 + 5,
        '"No me creas. Ejecuta el código."  ·  Fidelidad declarada  ·  Defectos documentados  ·  Negativos versionados')
    r.footer(16, 16, "PERSONAL")


# ──────────────────────────────────────────────────────────────────────────────
# MAIN BUILD
# ──────────────────────────────────────────────────────────────────────────────

def build_pdf():
    print("=" * 60)
    print("THORRIJA — 16-PAGE PREMIUM PRESENTATION")
    print("Rubén Núñez Sierra — 15 años")
    print("=" * 60)

    print("\n[1/3] Generating diagrams...")
    generate_all_diagrams()

    print("\n[2/3] Building slides...")
    slides = [
        (1, "Portada", draw_slide_1),
        (2, "Tesis + Fidelidad", draw_slide_2),
        (3, "Preguntas + Sustratos", draw_slide_3),
        (4, "The Box: Kernel", draw_slide_4),
        (5, "The Box: 6 Reglas", draw_slide_5),
        (6, "The Box: Exp + TS + Límites", draw_slide_6),
        (7, "NOX: Cognitive Runtime", draw_slide_7),
        (8, "ECHO: Cognitive Organism", draw_slide_8),
        (9, "SINGULARITY / ORACLE", draw_slide_9),
        (10, "HERMES", draw_slide_10),
        (11, "Showcase: 4 Modelos N1", draw_slide_11),
        (12, "Síntesis: 5 Sustratos", draw_slide_12),
        (13, "Heatmap + Problemas Abiertos", draw_slide_13),
        (14, "Reproducibilidad + CTA", draw_slide_14),
        (15, "Apéndice: Código + Stats", draw_slide_15),
        (16, "Rubén Núñez Sierra — 15 años", draw_slide_16),
    ]

    output_path = "/home/thorrija/research-presentation/Thorrija_16p_Final.pdf"
    c = canvas.Canvas(output_path, pagesize=(PAGE_W, PAGE_H))
    renderer = SlideRenderer(c)

    for num, title, draw_fn in slides:
        print(f"  Slide {num:2d}/16: {title}")
        c.setFillColor(BG); c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        draw_fn(renderer)
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
# Thorrija — Presentación Técnica para Equipo de Investigación IA

**Rubén Núñez Sierra · 15 años · Noviembre 2026**

16 slides, estética dark minimal lab. The Box, NOX, ECHO, SINGULARITY/ORACLE, HERMES, Showcase, límites honestos, problemas abiertos, reproducibilidad y perfil personal con QR.

## Archivos

| Archivo | Descripción |
|---|---|
| `docs/index.html` | **Fuente única** — versión web interactiva (GitHub Pages) + fuente del PDF |
| `docs/assets/` | Diagramas + QR (dark on light, escaneable) |
| `Thorrija_16p_Web.pdf` | **PDF final** — generado automáticamente desde `web/index.html` |
| `build_pdf.sh` | Script que regenera el PDF desde el HTML |
| `narrative/` | SLIDE_BLUEPRINT.md, SPEAKER_NOTES.md, QA_INDEX.md |
| `legacy/` | Generadores Python/matplotlib anteriores (referencia) |

## Versión web 🌐

**URL (GitHub Pages):** https://thorrijadev.github.io/thorrija-research-presentation/

- Navegación con ← → / Espacio / PageUp-Down / Home / End
- Swipe táctil en móvil
- Deep-linking por hash (`#7` → slide 7)
- Responsive: el deck 1600×900 se escala a cualquier pantalla
- ** mism HTML genera el PDF** — sin duplicar contenido

## Regenerar el PDF

```bash
./build_pdf.sh
```

Requiere `chromium`. El script imprime `docs/index.html` a PDF con `@page 1200pt×675pt`, exactamente 16 páginas 16:9.

## Cómo funciona

El slide es un canvas fijo 1600×900 con CSS Grid/Flexbox en `@media print`. El contenido se centra verticalmente y el footer se fija abajo. En `@media screen`, el mismo deck se escala con `transform: scale()` para caber en la ventana, y solo el slide `.active` se muestra. Esto garantiza que web y PDF sean idénticos y elimina los solapes del generador matplotlib anterior.

## Roadmap ✅

- [x] Presentación PDF 16 páginas con contenido técnico verificado
- [x] Integración de ECHO y NOX como sustratos de investigación
- [x] Página personal con QR + enlaces + descripción honesta
- [x] Corrección de bugs visuales (solapes, títulos duplicados, QR invertido) — reconstruido con HTML/CSS
- [x] **Versión web interactiva (GitHub Pages)** — generada automáticamente desde la misma fuente
- [ ] Publicar charla grabada con Q&A
- [ ] Añadir demo interactiva de los sustratos embedida en la web

## Enlaces

- Repo: https://github.com/ThorrijaDEV/thorrija-research-presentation
- GitHub: https://github.com/ThorrijaDEV
- Portafolio: https://thorrijadev.github.io/Portafolio/
- Showcase: https://thorrijadev.github.io/showcase/

#!/usr/bin/env bash
# Regenera el PDF desde la fuente HTML única (web/index.html)
set -euo pipefail
cd "$(dirname "$0")"
chromium --headless --no-sandbox --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=Thorrija_16p_Web.pdf "file://$(pwd)/web/index.html"
PAGES=$(pdfinfo Thorrija_16p_Web.pdf | awk '/^Pages:/{print $2}')
echo "PDF generado: Thorrija_16p_Web.pdf ($PAGES páginas)"

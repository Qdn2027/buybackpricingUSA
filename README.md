# buybackpricingUSA
iPhone Buyback Radar USA (QDN). Netlify serves `index.html`.
- `data.py` – scraped prices (updated weekly)
- `template.html` – original page (text/layout); never edited by the build
- `build.py` – `python3 build.py` regenerates `index.html` from template + data

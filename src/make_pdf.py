"""Gera Victor-Maksud-Carneiro-Resume.pdf a partir de src/resume.html.

Requer: pip install playwright && playwright install chromium
Uso:    python3 src/make_pdf.py
"""
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "src" / "resume.html"
OUTPUT = ROOT / "Victor-Maksud-Carneiro-Resume.pdf"


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(SOURCE.as_uri())
        page.wait_for_load_state("networkidle")
        page.pdf(path=str(OUTPUT), format="A4", print_background=True,
                 margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
                 prefer_css_page_size=True)
        browser.close()
    print(f"ok: {OUTPUT.name}")


if __name__ == "__main__":
    main()

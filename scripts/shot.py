"""Снимок страницы браузером Chromium: python shot.py URL out.png"""
import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1000, "height": 620})
    pg.goto(sys.argv[1], timeout=30000)
    pg.wait_for_timeout(500)
    pg.screenshot(path=sys.argv[2])
    b.close()

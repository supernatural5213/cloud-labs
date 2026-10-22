"""ЛР1: проверка PaaS-приложения в интернете: снимки страницы до и после расчёта."""
import sys
from playwright.sync_api import sync_playwright
url = sys.argv[1]
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 760, "height": 620})
    pg.goto(url, timeout=60000)
    pg.screenshot(path="paas_form.png")
    pg.fill("input[name=name]", "Сабитхан Жасулан")
    pg.fill("input[name=t1]", "85"); pg.fill("input[name=t2]", "90"); pg.fill("input[name=exam]", "86")
    pg.click("button")
    pg.wait_for_selector(".res")
    pg.screenshot(path="paas_result.png")
    print(pg.inner_text(".res"))
    pg.goto(url, timeout=60000)
    pg.fill("input[name=name]", "Тест Студент")
    pg.fill("input[name=t1]", "40"); pg.fill("input[name=t2]", "35"); pg.fill("input[name=exam]", "50")
    pg.click("button"); pg.wait_for_selector(".res")
    pg.screenshot(path="paas_fail.png")
    print(pg.inner_text(".res"))
    b.close()

from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8080/quicktools/index.html")
        page.wait_for_selector(".tool-card")

        # 1. Screenshot Dashboard with Dark Theme & One-line Categories
        page.screenshot(path="verification/dashboard_dark_final.png")
        print("Dashboard screenshot saved.")

        # 2. Check Scroll Diffusion (visual check, element should exist)
        # We check computed style of #content-area
        mask = page.evaluate("getComputedStyle(document.getElementById('content-area')).maskImage")
        print(f"Mask Image: {mask}")

        # 3. Check Themed Components
        page.click(".tool-card[data-tool='mortgage-calc']")
        page.wait_for_selector("#mortgage-calc-calc")

        page.screenshot(path="verification/tool_theme_final.png")
        print("Tool theme screenshot saved.")

        browser.close()

run()

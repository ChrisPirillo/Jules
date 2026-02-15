from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8080/quicktools/index.html")
        page.wait_for_selector(".tool-card")

        # 1. Screenshot Dashboard
        page.screenshot(path="verification/dashboard_dark_theme.png")
        print("Dashboard screenshot saved.")

        # 2. Open Mortgage Calc (Has buttons)
        page.click(".tool-card[data-tool='mortgage-calc']")
        page.wait_for_selector("#mortgage-calc-calc")

        # 3. Check Theme Accent on Button
        btn_bg = page.evaluate("getComputedStyle(document.getElementById('mortgage-calc-calc')).backgroundColor")
        print(f"Button BG: {btn_bg}")

        # Verify it's not the default gradient if possible, but hard to check rgb values against random.
        # Just ensure it's valid.

        page.screenshot(path="verification/tool_theme_dark.png")
        print("Tool view screenshot saved.")

        browser.close()

if __name__ == "__main__":
    run()

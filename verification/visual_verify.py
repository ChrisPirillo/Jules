from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8080/quicktools/index.html")
        page.wait_for_selector(".tool-card")

        # 1. Screenshot Dashboard with 200+ Badge
        page.screenshot(path="verification/dashboard_final_250.png")
        print("Dashboard screenshot saved.")

        # 2. Open Tool
        page.click(".tool-card[data-tool='mortgage-calc']")
        page.wait_for_selector("#mortgage-calc-p")

        # 3. Check Scroll Mask (Should be removed on tool page)
        mask = page.evaluate("getComputedStyle(document.getElementById('content-area')).maskImage")
        print(f"Tool Mask: {mask}")

        page.screenshot(path="verification/tool_page_clean.png")

        browser.close()

run()

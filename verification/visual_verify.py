from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8080/quicktools/index.html")
        page.wait_for_selector(".tool-card")

        # 1. Screenshot Dashboard
        page.screenshot(path="verification/dashboard_final_280.png")
        print("Dashboard screenshot saved.")

        # 2. Open Tool
        page.click(".tool-card[data-tool='mortgage-calc']")
        page.wait_for_selector("#mortgage-calc-p")

        # 3. Check Header Alignment (Visual)
        # Screenshot Top Area
        page.screenshot(path="verification/tool_header_align.png", clip={"x":0,"y":0,"width":1000,"height":100})
        print("Header alignment screenshot saved.")

        browser.close()

run()

from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8080/quicktools/index.html")
        page.wait_for_selector(".tool-card")

        # 1. Screenshot Dashboard with Count & Tabs
        page.screenshot(path="verification/dashboard_batch7.png")
        print("Dashboard screenshot saved.")

        # 2. Open Mortgage Calc (Finance)
        page.click(".tool-card[data-tool='mortgage-calc']")
        page.wait_for_selector("#mortgage-calc-p")

        # Take screenshot of Tool View (Inputs should be white text on dark bg)
        page.screenshot(path="verification/tool_inputs.png")
        print("Tool inputs screenshot saved.")

        browser.close()

run()

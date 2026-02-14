from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8080/quicktools/index.html")
        page.wait_for_selector(".tool-card")

        # 1. Screenshot Dashboard with Count & Tabs (No horizontal scroll logic check visually)
        page.screenshot(path="verification/dashboard_single.png")
        print("Dashboard screenshot saved.")

        # 2. Open Regex Tool
        page.click(".tool-card[data-tool='regex-real']")
        page.wait_for_selector("#rx-pattern")

        # Take screenshot of Tool View (Inputs should have same height as buttons)
        page.screenshot(path="verification/tool_ui_single.png")
        print("Tool UI screenshot saved.")

        browser.close()

run()

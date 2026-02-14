from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8080/quicktools/index.html")
        page.wait_for_selector(".tool-card")

        # Take screenshot of Dashboard with Category Tabs
        page.screenshot(path="verification/dashboard_final.png")
        print("Dashboard screenshot saved.")

        # Open a tool (BMR)
        page.click(".tool-card[data-tool='bmr-calc']")
        page.wait_for_selector("#bmr-calc-w")

        # Take screenshot of Tool View (No Tabs)
        page.screenshot(path="verification/tool_view_final.png")
        print("Tool view screenshot saved.")

        browser.close()

run()

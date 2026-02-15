from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8080/quicktools/index.html")
        page.wait_for_selector(".tool-card")

        # 1. Screenshot Dashboard
        page.screenshot(path="verification/dashboard_final_v2.png")

        # 2. Open Tool (Regex)
        page.click(".tool-card[data-tool='regex-real']")
        page.wait_for_selector("#rx-pattern")

        # 3. Check Nav Alignment
        # Screenshot tool view top part
        page.screenshot(path="verification/tool_nav_align.png", clip={"x":0,"y":0,"width":1000,"height":150})

        # 4. Check Logo Link (again)
        page.click("h1")
        # Wait for dashboard
        try:
            page.wait_for_selector("#dashboard", state="visible", timeout=2000)
            print("PASS: Logo link returned to dashboard.")
        except:
            print("FAIL: Logo link did not return to dashboard.")

        browser.close()

run()

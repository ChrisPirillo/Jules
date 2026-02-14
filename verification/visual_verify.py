from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8080/quicktools/index.html")
        page.wait_for_selector(".tool-card")

        # 1. Screenshot Dashboard with Count
        page.screenshot(path="verification/dashboard_count.png")
        print("Dashboard screenshot saved.")

        # 2. Open a colored tool (Math -> Purple)
        page.click(".tool-card[data-tool='prime-check']")
        page.wait_for_selector("#prime-check-n")

        # Check background color class
        bg_class = page.locator("#app").get_attribute("class")
        print(f"App classes: {bg_class}")
        if "theme-red" in bg_class or "theme-purple" in bg_class: # Math maps to purple/red depending on logic
             print("PASS: Theme applied.")
        else:
             print("FAIL: Theme not applied.")

        page.screenshot(path="verification/tool_theme.png")
        print("Tool theme screenshot saved.")

        browser.close()

run()

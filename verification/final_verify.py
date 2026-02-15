from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8080/quicktools/index.html")
        page.wait_for_selector(".tool-card")

        # 1. Screenshot Dashboard
        page.screenshot(path="verification/dashboard_final_250.png")

        # 2. Help Modal
        page.click("#help-btn")
        page.wait_for_selector("#help-modal")
        page.screenshot(path="verification/help_modal.png")

        page.click("#help-close")
        page.wait_for_selector("#help-modal", state="hidden")

        # 3. Logo Link
        page.evaluate("window.location.hash = '#mortgage-calc'")
        page.wait_for_selector("#mortgage-calc-p")

        # Click Logo
        page.click("h1")
        time.sleep(0.5) # Wait for hashchange

        # Check URL
        if "#" not in page.url or page.url.endswith("#"):
            print("PASS: Logo cleared hash.")
        else:
            print(f"FAIL: Hash not cleared: {page.url}")

        if page.locator("#dashboard").is_visible():
            print("PASS: Dashboard visible.")
        else:
            print("FAIL: Dashboard hidden.")

        browser.close()

run()

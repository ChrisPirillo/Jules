from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Listen for console logs
        page.on("console", lambda msg: print(f"Browser Console: {msg.text}"))

        # 1. Load Dashboard
        print("Loading Dashboard...")
        page.goto("http://localhost:8080/index.html")
        page.wait_for_selector(".tool-card")

        # Count tools
        count = page.locator(".tool-card").count()
        print(f"Total tools loaded: {count}")

        if count < 50:
            print("WARNING: Less than 50 tools loaded!")

        page.screenshot(path="verification/dashboard_100.png")
        print("Dashboard screenshot saved.")

        # 2. Test a generic text tool (e.g., Uppercase)
        print("Testing Uppercase tool...")
        page.click(".tool-card[data-tool='uppercase']")
        page.wait_for_selector("#uppercase-input")

        page.fill("#uppercase-input", "hello world")
        page.click("#uppercase-action")

        output = page.input_value("#uppercase-output")
        print(f"Uppercase Output: {output}")

        if output == "HELLO WORLD":
            print("PASS: Uppercase tool working.")
        else:
            print("FAIL: Uppercase tool failed.")

        page.screenshot(path="verification/uppercase.png")

        # 3. Go back
        page.click("#back-btn")

        # 4. Test a math factory tool (e.g., BMI)
        print("Testing BMI Calculator...")
        page.fill("#search-input", "BMI")
        page.wait_for_selector(".tool-card[data-tool='bmi-calc']:visible")
        page.click(".tool-card[data-tool='bmi-calc']")

        page.wait_for_selector("#bmi-calc-w")
        page.fill("#bmi-calc-w", "70")
        page.fill("#bmi-calc-h", "1.75")
        page.click("#bmi-calc-calc")

        bmi = page.text_content("#bmi-calc-result")
        print(f"BMI Result: {bmi}")

        if bmi == "22.86":
            print("PASS: BMI Calculator working.")
        else:
            print("FAIL: BMI Calculator failed.")

        page.screenshot(path="verification/bmi.png")

        browser.close()

if __name__ == "__main__":
    run()

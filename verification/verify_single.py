from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Loading index.html...")
        page.goto("http://localhost:8080/quicktools/index.html")
        page.wait_for_selector(".tool-card")

        badge = page.locator("#tool-count-badge").text_content()
        print(f"Badge: {badge}")

        # Test Real Tool (Regex)
        print("Testing Regex Tool...")
        page.evaluate("window.location.hash = '#regex-real'")
        page.wait_for_selector("#rx-pattern")

        # Test: Global match
        page.fill("#rx-pattern", "\\d+")  # Escaped backslash for python string
        page.fill("#rx-flags", "g")         # Set global flag
        page.fill("#rx-text", "abc 123 def 456")
        page.click("#rx-btn")

        res = page.locator("#rx-result").text_content()
        print(f"Regex Result: {res}")
        if "123" in res and "456" in res:
            print("PASS: Regex tool works.")
        else:
            print("FAIL: Regex tool failed.")

        page.screenshot(path="verification/single_spa_fixed.png")
        browser.close()

if __name__ == "__main__":
    run()

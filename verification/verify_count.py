from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8080/quicktools/index.html")
        page.wait_for_selector(".tool-card")

        # Check badge
        badge = page.locator("#tool-count-badge")
        if badge.is_visible():
            text = badge.text_content()
            print(f"Badge Text: {text}")
            count = int(text.split(' ')[0])
            if count > 120:
                print("PASS: Tool count updated (>120).")
            else:
                print(f"FAIL: Tool count too low ({count}).")
        else:
            print("FAIL: Badge not visible.")

        browser.close()

if __name__ == "__main__":
    run()

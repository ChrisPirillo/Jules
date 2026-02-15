from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8080/quicktools/index.html")
        page.wait_for_selector(".tool-card")

        badge = page.locator("#tool-count-badge").text_content()
        print(f"Badge: {badge}")

        count = int(badge.split(' ')[0])
        if count > 180:
            print("PASS: Tool count > 180.")
        else:
            print(f"FAIL: Tool count {count} is low.")

        browser.close()

if __name__ == "__main__":
    run()

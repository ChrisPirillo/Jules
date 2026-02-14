from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. Load Dashboard
        print("Loading Dashboard...")
        page.goto("http://localhost:8080/quicktools/index.html")
        page.wait_for_selector(".tool-card")

        # Check Meta Tags
        desc = page.locator('meta[name="description"]').get_attribute("content")
        print(f"Meta Description: {desc}")
        if "100+ free online web tools" in desc:
            print("PASS: Meta Description found.")
        else:
            print("FAIL: Meta Description incorrect.")

        # Check Category Tabs visible
        if page.locator("#category-tabs").is_visible():
            print("PASS: Category Tabs visible on Dashboard.")
        else:
            print("FAIL: Category Tabs hidden on Dashboard.")

        # 2. Test Routing & Title
        print("Clicking 'BMR Calculator'...")
        # We need to find the card. Use search to find it quickly.
        page.fill("#search-input", "BMR")
        page.wait_for_selector(".tool-card[data-tool='bmr-calc']:visible")
        page.click(".tool-card[data-tool='bmr-calc']")

        # Check Hash
        # Wait for hash update
        page.wait_for_timeout(500)
        url = page.url
        print(f"URL: {url}")
        if "#bmr-calc" in url:
            print("PASS: URL Hash updated.")
        else:
            print("FAIL: URL Hash NOT updated.")

        # Check Title
        title = page.title()
        print(f"Page Title: {title}")
        if "BMR Calculator" in title:
            print("PASS: Document Title updated.")
        else:
            print("FAIL: Document Title NOT updated.")

        # Check Category Tabs hidden
        if not page.locator("#category-tabs").is_visible():
            print("PASS: Category Tabs hidden on Tool View.")
        else:
            print("FAIL: Category Tabs visible on Tool View.")

        # 3. Test Back Button
        print("Clicking Back...")
        page.click("#back-btn")
        page.wait_for_timeout(500)

        # Check URL (should be empty hash or removed)
        url = page.url
        print(f"URL after back: {url}")
        if "#" not in url or url.endswith("#"):
            print("PASS: URL Hash cleared.")
        else:
            print("FAIL: URL Hash NOT cleared.")

        # Check Title reset
        title = page.title()
        if "The Glassomorphic Web Utility Hub" in title:
            print("PASS: Document Title reset.")
        else:
            print("FAIL: Document Title NOT reset.")

        browser.close()

if __name__ == "__main__":
    run()

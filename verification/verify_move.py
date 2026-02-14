from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. Load Dashboard from new location
        print("Loading Dashboard from quicktools/index.html...")
        page.goto("http://localhost:8080/quicktools/index.html")
        page.wait_for_selector(".tool-card")

        # Check if styles loaded (background should be gradient)
        bg = page.evaluate("getComputedStyle(document.body).backgroundImage")
        print(f"Background: {bg}")

        if "linear-gradient" in bg:
            print("PASS: Styles loaded.")
        else:
            print("FAIL: Styles not loaded.")

        page.screenshot(path="verification/quicktools_move.png")
        browser.close()

if __name__ == "__main__":
    run()

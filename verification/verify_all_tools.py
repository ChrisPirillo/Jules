from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Capture errors
        errors = []
        page.on("pageerror", lambda err: errors.append(f"JS Error: {err.message}"))
        page.on("console", lambda msg: errors.append(f"Console Error: {msg.text}") if msg.type == "error" else None)

        print("Loading Dashboard...")
        page.goto("http://localhost:8080/quicktools/index.html")
        page.wait_for_selector(".tool-card")

        # Get all tool IDs
        tool_cards = page.locator(".tool-card")
        count = tool_cards.count()
        print(f"Found {count} tools.")

        tool_ids = []
        for i in range(count):
            tool_ids.append(tool_cards.nth(i).get_attribute("data-tool"))

        print(f"Validating {len(tool_ids)} tools...")

        failed_tools = []

        for i, tool_id in enumerate(tool_ids):
            try:
                # print(f"Testing {tool_id} ({i+1}/{count})...")

                # Navigate via Hash to be faster and test routing
                page.evaluate(f"window.location.hash = '#{tool_id}'")

                # Wait for tool content
                # We expect #tool-content to have children
                page.wait_for_function("document.getElementById('tool-content').children.length > 0", timeout=2000)

                # Check for errors in this iteration
                if errors:
                    print(f"❌ Errors found for {tool_id}: {errors}")
                    failed_tools.append(tool_id)
                    errors = [] # Reset

            except Exception as e:
                print(f"❌ Exception for {tool_id}: {e}")
                failed_tools.append(tool_id)

        if failed_tools:
            print(f"FAILED TOOLS ({len(failed_tools)}): {failed_tools}")
        else:
            print("✅ All tools rendered successfully.")

        browser.close()

if __name__ == "__main__":
    run()

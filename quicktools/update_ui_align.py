import re

with open('quicktools/index.html', 'r') as f:
    content = f.read()

# 1. Extract tool-header HTML
tool_header_regex = r'<div class="tool-header">[\s\S]*?</div>'
match = re.search(tool_header_regex, content)
if not match:
    print("Error: tool-header not found")
    # It might be because of regex limitation on large files?
    # Or previous script already moved it?
    # Let's search string.
    start = content.find('<div class="tool-header">')
    if start != -1:
        end = content.find('</div>', start)
        tool_header_html = content[start:end+6]
    else:
        print("Really not found")
        exit(1)
else:
    tool_header_html = match.group(0)

# Remove it from tool-view
content = content.replace(tool_header_html, '')

# Prepare new header with ID and styling to match tabs
# Tabs style: padding: 0 20px 10px 20px; (inline style in <head>) or CSS class?
# <nav class="category-tabs" ...>
# CSS: padding: 0 10px 10px 10px; (from `update_css_layout.py` override)
# Let's match it.
new_header = tool_header_html.replace('<div class="tool-header">', '<div class="tool-header" id="tool-nav" style="display: none; padding: 0 10px 10px 10px; margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between;">')

# Insert before main-container
content = content.replace('<div class="main-container">', new_header + '\n        <div class="main-container">')

# 2. Update JS Logic
# showDashboard
content = content.replace("if(categoryTabs) categoryTabs.style.display = 'flex';",
                          "if(categoryTabs) categoryTabs.style.display = 'flex';\n        const toolNav = document.getElementById('tool-nav');\n        if(toolNav) toolNav.style.display = 'none';")

# showTool
content = content.replace("if(categoryTabs) categoryTabs.style.display = 'none';",
                          "if(categoryTabs) categoryTabs.style.display = 'none';\n            const toolNav = document.getElementById('tool-nav');\n            if(toolNav) toolNav.style.display = 'flex';")

with open('quicktools/index.html', 'w') as f:
    f.write(content)

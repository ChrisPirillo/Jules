import re

with open('quicktools/index.html', 'r') as f:
    content = f.read()

# 1. Header Cleanup (Remove HR)
content = re.sub(r'border-bottom: 1px solid.*?;', 'border-bottom: none;', content)

# 2. Tool Header Layout
style_old = 'padding: 0 10px 10px 10px; margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between;'
style_new = 'padding: 0 10px 5px 10px; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between;'
content = content.replace(style_old, style_new)

# Update Title style
content = content.replace('<h2 id="tool-title">', '<h2 id="tool-title" style="flex: 1; text-align: center; margin: 0;">')

# 3. Modal Contrast
content = content.replace('style="width: 90%; max-width: 500px; position: relative;"', 'style="width: 90%; max-width: 500px; position: relative; color: white; background: rgba(30, 30, 30, 0.85);"')

with open('quicktools/index.html', 'w') as f:
    f.write(content)

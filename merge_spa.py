import os

with open('quicktools/index.html', 'r') as f:
    html = f.read()

with open('quicktools/styles.css', 'r') as f:
    css = f.read()

with open('quicktools/script.js', 'r') as f:
    js = f.read()

# Remove external links
html = html.replace('<link rel="stylesheet" href="styles.css">', '')
html = html.replace('<script src="script.js"></script>', '')

# Inject CSS
style_tag = f"<style>\n{css}\n</style>"
html = html.replace('</head>', f"{style_tag}\n</head>")

# Inject JS
script_tag = f"<script>\n{js}\n</script>"
html = html.replace('</body>', f"{script_tag}\n</body>")

with open('quicktools/index.html', 'w') as f:
    f.write(html)

print("Merged successfully.")

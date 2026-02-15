import re

with open('quicktools/index.html', 'r') as f:
    content = f.read()

# 1. Update Body Alignment & App Height
content = content.replace('align-items: flex-start;', 'align-items: center;')
content = content.replace('padding: 20px;', 'padding: 30px;') # slightly more breathing room
content = re.sub(r'height: 90vh;', 'height: calc(100vh - 60px);', content)

# 2. Update Scroll Mask (Top & Bottom)
mask_css = """mask-image: linear-gradient(to bottom, transparent 0%, black 20px, black calc(100% - 20px), transparent 100%);
    -webkit-mask-image: linear-gradient(to bottom, transparent 0%, black 20px, black calc(100% - 20px), transparent 100%);"""
content = re.sub(r'mask-image:.*?;', mask_css, content, flags=re.DOTALL)
content = re.sub(r'-webkit-mask-image:.*?;', '', content, flags=re.DOTALL) # remove duplicate if regex matched roughly

# 3. Update Glow (Box Shadow) to use variable
# Find #app style
content = content.replace('box-shadow: var(--glass-shadow);', 'box-shadow: 0 8px 32px 0 var(--theme-shadow, rgba(31, 38, 135, 0.37)); border-color: var(--theme-border, rgba(255, 255, 255, 0.18));')

# 4. Rename Category
content = content.replace('data-cat="Game">Random/Game<', 'data-cat="Random">Random<')

# 5. Rename App
content = content.replace('Crystal Tools', 'Tooltimate')

with open('quicktools/index.html', 'w') as f:
    f.write(content)

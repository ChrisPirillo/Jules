import re

with open('quicktools/index.html', 'r') as f:
    content = f.read()

# 1. CSS Fix
css_fix = """
#content-area {
    height: 100%;
    overflow-y: auto;
    scrollbar-width: thin;
    padding-right: 10px;
}

#content-area.masked-scroll {
    mask-image: linear-gradient(to bottom, transparent 0%, black 20px, black calc(100% - 20px), transparent 100%);
    -webkit-mask-image: linear-gradient(to bottom, transparent 0%, black 20px, black calc(100% - 20px), transparent 100%);
    padding-top: 10px;
}
"""

# Remove old block (it had mask-image inside #content-area)
content = re.sub(r'#content-area\s*\{[^}]*mask-image[^}]*\}', '', content, flags=re.DOTALL)
content = content.replace('/* Scroll Diffusion */', css_fix)

# 2. JS Fix
# Inject class toggle
if "masked-scroll" not in content:
    content = content.replace("if(categoryTabs) categoryTabs.style.display = 'flex';", "if(categoryTabs) categoryTabs.style.display = 'flex';\n        document.getElementById('content-area').classList.add('masked-scroll');")
    content = content.replace("if(categoryTabs) categoryTabs.style.display = 'none';", "if(categoryTabs) categoryTabs.style.display = 'none';\n            document.getElementById('content-area').classList.remove('masked-scroll');")
    # Initial state (renderDashboard calls showDashboard? No, it just renders)
    # But init logic calls `renderDashboard()`. We should ensure mask is added on init.
    content = content.replace("renderDashboard();", "document.getElementById('content-area').classList.add('masked-scroll');\n    renderDashboard();")

with open('quicktools/index.html', 'w') as f:
    f.write(content)

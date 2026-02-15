import re

with open('quicktools/index.html', 'r') as f:
    content = f.read()

# 1. Update setRandomTheme to set --theme-shadow
new_theme_logic = r"""    function setRandomTheme() {
        const hue = Math.floor(Math.random() * 360);
        const sat = Math.floor(Math.random() * 20) + 60;
        const light = Math.floor(Math.random() * 20) + 10;

        const primaryColor = `hsl(${hue}, ${sat}%, ${light}%)`;
        const accentColor = `hsl(${hue}, ${sat}%, ${light + 40}%)`;
        const bgInput = `hsla(${hue}, 30%, 10%, 0.6)`;
        const border = `hsla(${hue}, 50%, 50%, 0.3)`;
        const shadow = `hsla(${hue}, ${sat}%, ${light + 10}%, 0.3)`;

        const root = document.documentElement;
        root.style.setProperty('--primary-color', primaryColor);

        const hue2 = (hue + 40) % 360;
        const bgGradient = `linear-gradient(135deg, hsl(${hue}, 60%, 20%) 0%, hsl(${hue2}, 60%, 10%) 100%)`;
        root.style.setProperty('--bg-gradient', bgGradient);

        root.style.setProperty('--theme-accent', accentColor);
        root.style.setProperty('--theme-accent-hover', `hsl(${hue}, ${sat}%, ${light + 50}%)`);
        root.style.setProperty('--theme-bg-input', bgInput);
        root.style.setProperty('--theme-border', border);
        root.style.setProperty('--theme-shadow', shadow);
        root.style.setProperty('--theme-bg-hover', `hsla(${hue}, ${sat}%, 25%, 0.4)`);
    }"""

content = re.sub(r"function setRandomTheme\(\) \{.*?\}", new_theme_logic, content, flags=re.DOTALL)

# 2. Update Tool Page UI to include Category Badge
content = content.replace('<h2 id="tool-title">Tool Name</h2>', '<h2 id="tool-title">Tool Name</h2> <span id="tool-category-badge" style="margin-left: auto; background: rgba(255,255,255,0.1); padding: 4px 12px; border-radius: 15px; font-size: 0.8rem; border: 1px solid rgba(255,255,255,0.2);">Category</span>')

# Update `showTool` to populate badge
show_tool_logic = r"""
            toolTitle.textContent = tool.name;
            const catBadge = document.getElementById('tool-category-badge');
            if(catBadge) catBadge.textContent = tool.category || 'Tool';
            toolContent.innerHTML = '';
"""
content = content.replace('toolTitle.textContent = tool.name;', show_tool_logic)

# 3. Update Title Logic (Tooltimate)
content = content.replace('document.title = tool.name + \' - Crystal Tools\';', 'document.title = tool.name + \' - Tooltimate\';')
content = content.replace('document.title = \'Crystal Tools - The Glassomorphic Web Utility Hub\';', 'document.title = \'Tooltimate - The Glassomorphic Web Utility Hub\';')

with open('quicktools/index.html', 'w') as f:
    f.write(content)

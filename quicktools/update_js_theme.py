import re

with open('quicktools/index.html', 'r') as f:
    content = f.read()

# Replace setRandomTheme function
new_theme_logic = r"""    function setRandomTheme() {
        const hue = Math.floor(Math.random() * 360);
        // Darker Theme: Saturation 60-80%, Lightness 10-30%
        const sat = Math.floor(Math.random() * 20) + 60;
        const light = Math.floor(Math.random() * 20) + 10;

        const primaryColor = `hsl(${hue}, ${sat}%, ${light}%)`;
        const accentColor = `hsl(${hue}, ${sat}%, ${light + 40}%)`;
        const bgInput = `hsla(${hue}, 30%, 10%, 0.6)`;
        const border = `hsla(${hue}, 50%, 50%, 0.3)`;

        const root = document.documentElement;
        root.style.setProperty('--primary-color', primaryColor);

        const hue2 = (hue + 40) % 360;
        const bgGradient = `linear-gradient(135deg, hsl(${hue}, 60%, 20%) 0%, hsl(${hue2}, 60%, 10%) 100%)`;
        root.style.setProperty('--bg-gradient', bgGradient);

        root.style.setProperty('--theme-accent', accentColor);
        root.style.setProperty('--theme-accent-hover', `hsl(${hue}, ${sat}%, ${light + 50}%)`);
        root.style.setProperty('--theme-bg-input', bgInput);
        root.style.setProperty('--theme-border', border);
        root.style.setProperty('--theme-bg-hover', `hsla(${hue}, ${sat}%, 25%, 0.4)`);
    }"""

content = re.sub(r"function setRandomTheme\(\) \{[\s\S]*?root\.style\.setProperty\('--bg-gradient', bgGradient\);\s+}", new_theme_logic, content)

with open('quicktools/index.html', 'w') as f:
    f.write(content)

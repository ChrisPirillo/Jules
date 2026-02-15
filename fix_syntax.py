import re

with open('quicktools/index.html', 'r') as f:
    content = f.read()

# Find the broken line
# `const primaryColor = ;`
content = content.replace('const primaryColor = ;', 'const primaryColor = `hsl(${hue}, ${sat}%, ${light}%)`;')

# Check other broken lines
# `const accentColor = ;` ?
# `const bgInput = ;` ?
# `const border = ;` ?

content = content.replace('const accentColor = ;', 'const accentColor = `hsl(${hue}, ${sat}%, ${light + 40}%)`;')
content = content.replace('const bgInput = ;', 'const bgInput = `hsla(${hue}, 30%, 10%, 0.6)`;')
content = content.replace('const border = ;', 'const border = `hsla(${hue}, 50%, 50%, 0.3)`;')
content = content.replace('const bgGradient = ;', 'const bgGradient = `linear-gradient(135deg, hsl(${hue}, 60%, 20%) 0%, hsl(${hue2}, 60%, 10%) 100%)`;')
content = content.replace('root.style.setProperty(\'--theme-accent-hover\', );', 'root.style.setProperty(\'--theme-accent-hover\', `hsl(${hue}, ${sat}%, ${light + 50}%)`);')
content = content.replace('root.style.setProperty(\'--theme-bg-hover\', );', 'root.style.setProperty(\'--theme-bg-hover\', `hsla(${hue}, ${sat}%, 25%, 0.4)`);')

with open('quicktools/index.html', 'w') as f:
    f.write(content)

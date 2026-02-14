import re

with open('quicktools/script.js', 'r') as f:
    content = f.read()

# 1. Update registerTool to accept theme or category mapping
# We already have 'category'. We can map category to theme color in showTool.

# 2. Update showTool to apply theme
# Find 'function showTool(toolId) {'
# It ends with 'if (window.location.hash...'

# We need to inject the theme logic inside showTool.
# Logic:
# const category = tool.category || 'Default';
# const themeMap = { Text: 'blue', Math: 'purple', Dev: 'green', Converter: 'orange', Game: 'pink', Health: 'red', Security: 'green', Color: 'pink' };
# const theme = themeMap[category] || 'default';
# document.getElementById('app').className = ''; // Reset
# document.getElementById('app').classList.add('theme-' + theme.toLowerCase());

# Also update showDashboard to reset theme.

# Let's rewrite the functions using regex replacement.

show_tool_replacement = r"""    function showTool(toolId) {
        const tool = toolRegistry[toolId];
        if (tool) {
            dashboard.style.display = 'none';
            toolView.style.display = 'flex';
            if(categoryTabs) categoryTabs.style.display = 'none';
            toolTitle.textContent = tool.name;
            toolContent.innerHTML = '';

            // Dynamic Theme
            const app = document.getElementById('app');
            app.className = ''; // Reset
            const cat = tool.category;
            let theme = 'default';
            if (cat === 'Text') theme = 'blue';
            else if (cat === 'Math' || cat === 'Finance') theme = 'purple';
            else if (cat === 'Dev') theme = 'green';
            else if (cat === 'Converter') theme = 'orange';
            else if (cat === 'Game' || cat === 'Color') theme = 'pink';
            else if (cat === 'Health' || cat === 'Science') theme = 'red';
            else if (cat === 'Security') theme = 'green';

            app.classList.add('theme-' + theme);

            tool.render(toolContent);
            document.title = tool.name + ' - Crystal Tools';

            if (window.location.hash !== '#' + toolId) {
                history.pushState(null, null, '#' + toolId);
            }
        }
    }"""

show_dashboard_replacement = r"""    function showDashboard() {
        toolView.style.display = 'none';
        dashboard.style.display = 'grid';
        if(categoryTabs) categoryTabs.style.display = 'flex';
        toolContent.innerHTML = '';
        searchInput.value = '';

        // Reset Theme
        const app = document.getElementById('app');
        app.className = ''; // Reset

        document.title = 'Crystal Tools - The Glassomorphic Web Utility Hub';
        history.pushState(null, null, ' ');
    }"""

# Replace showTool
content = re.sub(r"function showTool\(toolId\) \{.*?^\s\s\s\s\}", show_tool_replacement, content, flags=re.DOTALL | re.MULTILINE)

# Replace showDashboard
content = re.sub(r"function showDashboard\(\) \{.*?^\s\s\s\s\}", show_dashboard_replacement, content, flags=re.DOTALL | re.MULTILINE)

# Write back
with open('quicktools/script.js', 'w') as f:
    f.write(content)

import re

with open('quicktools/script.js', 'r') as f:
    content = f.read()

# Extract the tool definitions (between factory and render)
# Factory starts at line ~10
# We want to keep everything from "const toolRegistry = {};" up to before "renderDashboard();"
# Then we will rewrite the init/navigation logic.

# Let's find the tool definitions block
start_marker = "// --- Tool Factory ---"
end_marker = "// --- Render Dashboard ---"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Error: Could not find markers")
    exit(1)

tool_defs = content[start_idx:end_idx]

# We also need the batch 4 tools which might be after renderDashboard in previous appends?
# Let's check the end of the file.
# Ah, I see I appended Batch 4 *after* the initial file creation.
# The file structure is:
# 1. Setup (vars)
# 2. Factory
# 3. Batch 1
# 4. Render Dashboard (initial call)
# 5. Event Listeners
# 6. Batch 2
# 7. Batch 3
# 8. Batch 4
# 9. Render Dashboard (second call)

# This is messy. Let's extract *all* lines that look like tool creations.
# createSimpleTextTool, createMathTool, createGeneratorTool, registerTool (calculator)

lines = content.split('\n')
tool_lines = []
factory_lines = []

for line in lines:
    if "const toolRegistry = {};" in line:
        factory_lines.append(line)
    elif "function registerTool" in line or "function createSimpleTextTool" in line or "function createMathTool" in line or "function createGeneratorTool" in line:
        factory_lines.append(line)
    # Collect the body of factory functions... this is hard with line-by-line.

# Better approach:
# Keep the file as is, but REPLACE the beginning (setup) and end (navigation/init).
# The middle part (tool definitions) is what we want to preserve.

# The file starts with:
# document.addEventListener('DOMContentLoaded', () => {
#    const dashboard ...

# And ends with:
# });

# I want to inject the new tools and routing logic.

new_setup = """document.addEventListener('DOMContentLoaded', () => {
    const dashboard = document.getElementById('dashboard');
    const toolView = document.getElementById('tool-view');
    const toolTitle = document.getElementById('tool-title');
    const toolContent = document.getElementById('tool-content');
    const backBtn = document.getElementById('back-btn');
    const searchInput = document.getElementById('search-input');
    const categoryTabs = document.getElementById('category-tabs'); // NEW

    // --- Tool Factory ---
    const toolRegistry = {};

    function registerTool(id, name, category, description, icon, renderFn) {
        toolRegistry[id] = { name, category, description, icon, render: renderFn };
    }
"""

# We need the factory functions. They are in the original file.
# Let's regex to find them.

# Actually, I can just use the previous file content, but I need to be careful about the structure.
# Let's just append the new tools to the existing file, and then
# append a block that *overrides* the navigation logic?
# No, that's sloppy.

# Let's write a new script.js that contains EVERYTHING cleanly.
# I will output the *entire* content here in the python script.

# ... This is too large for one tool call.

# Plan B:
# 1. Read existing script.js.
# 2. Identify the part that defines tools.
# 3. Write a new header (variables, routing logic).
# 4. Write the tool definitions.
# 5. Write the new tools.
# 6. Write the init/render logic.

# Let's find the start of tool definitions.
# It starts after "const searchInput = ...;" usually.
# But I can just look for "const toolRegistry = {};"

parts = content.split("const toolRegistry = {};")
if len(parts) < 2:
    print("Error splitting")
    exit(1)

header = parts[0] # This contains the old setup variables
body = "const toolRegistry = {};" + parts[1] # This contains everything else

# Remove the last line "});"
body = body.strip()
if body.endswith("});"):
    body = body[:-3]

# Now I have the body of tool definitions (and some old event listeners).
# I want to strip out the old event listeners if possible, or just overwrite them.
# The old event listeners are:
# dashboard.addEventListener...
# backBtn.addEventListener...
# searchInput.addEventListener...

# I can just append new event listeners that do what I want.
# But for "backBtn", adding another listener might not clear the old one.
# However, "backBtn" is a button. I can set  to override? No, addEventListener accumulates.
# But I can clone the node to clear listeners!

new_logic = """
    // --- Routing & UI Logic (Overrides) ---

    function updateTitle(toolName) {
        if (toolName) {
            document.title = `${toolName} - Crystal Tools`;
        } else {
            document.title = 'Crystal Tools - The Glassomorphic Web Utility Hub';
        }
    }

    function showDashboard() {
        toolView.style.display = 'none';
        dashboard.style.display = 'grid';
        categoryTabs.style.display = 'flex'; // Show tabs
        toolContent.innerHTML = '';
        searchInput.value = '';
        updateTitle(null);
        history.pushState(null, null, ' '); // Clear hash
    }

    function showTool(toolId) {
        const tool = toolRegistry[toolId];
        if (tool) {
            dashboard.style.display = 'none';
            toolView.style.display = 'flex';
            categoryTabs.style.display = 'none'; // Hide tabs
            toolTitle.textContent = tool.name;
            toolContent.innerHTML = '';
            tool.render(toolContent);
            updateTitle(tool.name);
            // Update URL hash without reloading
            if (window.location.hash !== '#' + toolId) {
                history.pushState(null, null, '#' + toolId);
            }
        }
    }

    // Override Navigation
    // Clone elements to remove old event listeners
    const newBackBtn = backBtn.cloneNode(true);
    backBtn.parentNode.replaceChild(newBackBtn, backBtn);
    newBackBtn.addEventListener('click', () => {
        showDashboard();
    });

    // We don't need to clone dashboard, but we should ensure the click handler uses the new showTool
    // The old click handler calls 'showTool' which is closure-bound.
    // Wait, the old 'showTool' is defined in the previous closure scope?
    // No, it's in the same scope 'DOMContentLoaded'.
    // If I redefine 'showTool' function at the end, does it overwrite the previous one?
    // In JS, function declarations are hoisted, but function expressions (const showTool = ...) are not.
    // The previous one was .
    // If I declare  again, it might throw or override depending on strict mode/block.
    // But we are in a huge arrow function .
    // Redefining a function inside a block usually works or throws.

    // Actually, simply assigning  won't help inside the closure.

    // Let's just use a router based approach.

    function handleHash() {
        const hash = window.location.hash.substring(1);
        if (hash && toolRegistry[hash]) {
            showTool(hash);
        } else {
            showDashboard();
        }
    }

    window.addEventListener('hashchange', handleHash);

    // Handle initial load
    if (window.location.hash) {
        handleHash();
    }

    // Update dashboard click to set hash
    dashboard.addEventListener('click', (e) => {
        const card = e.target.closest('.tool-card');
        if (card) {
            const toolId = card.getAttribute('data-tool');
            // Instead of calling showTool directly, we set hash and let handler do it
            window.location.hash = toolId;
        }
    });

"""

# Now handle the "Add More Tools" part.
new_tools = """
    // --- Batch 5: SEO & More Tools ---

    // Health
    createMathTool('bmr-calc', 'BMR Calculator', 'Health', 'Basal Metabolic Rate.',
        [{key:'w', label:'Weight (kg)'}, {key:'h', label:'Height (cm)'}, {key:'a', label:'Age'}],
        (v) => (10 * v.w + 6.25 * v.h - 5 * v.a + 5).toFixed(0) + ' kcal (M) / ' + (10 * v.w + 6.25 * v.h - 5 * v.a - 161).toFixed(0) + ' kcal (F)');

    createMathTool('water-intake', 'Water Intake', 'Health', 'Daily water need (L).',
        [{key:'w', label:'Weight (kg)'}],
        (v) => (v.w * 0.033).toFixed(2) + ' Liters');

    createMathTool('target-heart-rate', 'Target Heart Rate', 'Health', 'Zone 2 (60-70%).',
        [{key:'age', label:'Age'}],
        (v) => {
            const max = 220 - v.age;
            return Math.floor(max * 0.6) + ' - ' + Math.floor(max * 0.7) + ' bpm';
        });

    // Education
    createMathTool('gpa-calc', 'GPA Calculator (4.0)', 'Science', 'Simple Avg GPA.',
        [{key:'g1', label:'Grade 1'}, {key:'g2', label:'Grade 2'}, {key:'g3', label:'Grade 3'}, {key:'g4', label:'Grade 4'}],
        (v) => ((v.g1 + v.g2 + v.g3 + v.g4) / 4).toFixed(2));

    createMathTool('grade-pct', 'Grade Percentage', 'Science', 'Score / Total.',
        [{key:'s', label:'Score'}, {key:'t', label:'Total'}],
        (v) => ((v.s / v.t) * 100).toFixed(2) + '%');

    // Dev
    createSimpleTextTool('html-minifier', 'HTML Minifier', 'Dev', 'Remove whitespace.', (text) => text.replace(/\s+/g, ' ').replace(/> </g, '><'));
    createSimpleTextTool('hashtag-gen', 'Hashtag Generator', 'Social', 'Generate tags from text.', (text) => text.split(' ').map(w => '#' + w).join(' '));
    createSimpleTextTool('tweet-link', 'Tweet Link Gen', 'Social', 'Create intent link.', (text) => 'https://twitter.com/intent/tweet?text=' + encodeURIComponent(text));

    createSimpleTextTool('binary-to-hex', 'Binary to Hex', 'Dev', 'Convert Bin to Hex.', (text) => parseInt(text.replace(/[^01]/g, ''), 2).toString(16).toUpperCase());
    createSimpleTextTool('hex-to-binary', 'Hex to Binary', 'Dev', 'Convert Hex to Bin.', (text) => parseInt(text, 16).toString(2));

    // Finance (Mock)
    createMathTool('currency-usd-eur', 'USD to EUR (Mock)', 'Finance', 'Est. rate 0.92', [{key:'usd', label:'USD'}], (v) => (v.usd * 0.92).toFixed(2));
    createMathTool('currency-eur-usd', 'EUR to USD (Mock)', 'Finance', 'Est. rate 1.09', [{key:'eur', label:'EUR'}], (v) => (v.eur * 1.09).toFixed(2));

    // Refresh dashboard one last time
    renderDashboard();

    // Initial Hash Check
    if (window.location.hash) {
        handleHash();
    }

    // Update search to search new tools
    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        const cards = document.querySelectorAll('.tool-card');
        cards.forEach(card => {
            const name = card.querySelector('h3').textContent.toLowerCase();
            const desc = card.querySelector('p').textContent.toLowerCase();
            if (name.includes(query) || desc.includes(query)) {
                card.style.display = 'flex';
            } else {
                card.style.display = 'none';
            }
        });
    });

"""

final_content = new_setup + body + new_logic + new_tools + "});"

with open('quicktools/script.js', 'w') as f:
    f.write(final_content)

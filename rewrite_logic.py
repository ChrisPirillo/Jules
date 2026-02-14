import re

# Read original file
with open('quicktools/script.js.bak', 'r') as f:
    content = f.read()

# We want to preserve the tool factory and definitions
# They are between "const toolRegistry = {};" and the end of the file
# But the end of the file has event listeners we want to replace.

# Let's find where the tool definitions end.
# They end before "renderDashboard();" usually.
# But I added more batches.

# Strategy:
# 1. Keep everything from "const toolRegistry = {};" until the end of the file.
# 2. Prepend the new header (with categoryTabs).
# 3. Append the new tools and routing logic at the end (before the final closing brace).

# Find start of body
start_marker = "const toolRegistry = {};"
idx = content.find(start_marker)
if idx == -1:
    print("Error: Start marker not found")
    exit(1)

body = content[idx:]

# Remove the existing event listeners and init logic at the end
# The existing file ends with:
# renderDashboard();
# ... event listeners ...
# });

# We want to keep the tool definitions (createSimpleTextTool calls).
# Let's split by "renderDashboard();" - the FIRST one.
parts = body.split("renderDashboard();")

# The first part contains toolRegistry + Batch 1 + Factory.
# The subsequent parts contain Batch 2, 3, 4 tools + more renderDashboard calls.

# Let's reconstruct.
# We will just take the whole file content, strip the header and footer wrapper.

inner_content = content.replace("document.addEventListener('DOMContentLoaded', () => {", "").strip()
if inner_content.endswith("});"):
    inner_content = inner_content[:-3]

# Now we have the inner content.
# We need to replace the *initial* variable declarations to include categoryTabs.
# And we need to replace the *navigation* logic.

# Regex to replace variable declarations
new_vars = """    const dashboard = document.getElementById('dashboard');
    const toolView = document.getElementById('tool-view');
    const toolTitle = document.getElementById('tool-title');
    const toolContent = document.getElementById('tool-content');
    const backBtn = document.getElementById('back-btn');
    const searchInput = document.getElementById('search-input');
    const categoryTabs = document.getElementById('category-tabs');"""

# Replace the old vars block
inner_content = re.sub(r"const dashboard = .*?const searchInput = .*?;", new_vars, inner_content, flags=re.DOTALL)

# Now, we need to remove the OLD navigation logic so we don't have duplicates.
# Old logic:
# dashboard.addEventListener('click', ...
# backBtn.addEventListener('click', ...
# function showTool ...
# function showDashboard ...
# searchInput.addEventListener ...

# It's hard to regex remove them cleanly.
# However, we can just append the NEW logic which will define NEW functions/listeners.
# If we define  again in the same scope, it might crash if it's let/const, but functions are hoisted/overwritable in loose mode.
# But we are in strict mode module? No, standard script.
# Actually, inside , functions are block-scoped.
# Redefining  will throw SyntaxError: Identifier 'showTool' has already been declared.

# So we MUST remove the old function definitions.
# Let's just strip everything after the LAST  call?
# No,  needs to be kept or re-added.

# Let's try to remove known blocks.
inner_content = re.sub(r"function showTool\(.*?\n    }", "", inner_content, flags=re.DOTALL)
inner_content = re.sub(r"function showDashboard\(.*?\n    }", "", inner_content, flags=re.DOTALL)
# The above regex is too simple, won't match multiline bodies well.

# Fallback: Just rename the new functions and use them in the new event listeners.
# , .
# And we clone the buttons to remove old listeners.

new_logic = """
    // --- Routing & SEO Logic ---

    function showDashboardWithTabs() {
        toolView.style.display = 'none';
        dashboard.style.display = 'grid';
        categoryTabs.style.display = 'flex';
        toolContent.innerHTML = '';
        searchInput.value = '';
        document.title = 'Crystal Tools - The Glassomorphic Web Utility Hub';
        history.pushState(null, null, ' ');
    }

    function showToolWithSEO(toolId) {
        const tool = toolRegistry[toolId];
        if (tool) {
            dashboard.style.display = 'none';
            toolView.style.display = 'flex';
            categoryTabs.style.display = 'none';
            toolTitle.textContent = tool.name;
            toolContent.innerHTML = '';
            tool.render(toolContent);
            document.title = tool.name + ' - Crystal Tools';
        }
    }

    function handleRouting() {
        const hash = window.location.hash.substring(1);
        if (hash && toolRegistry[hash]) {
            showToolWithSEO(hash);
        } else {
            showDashboardWithTabs();
        }
    }

    window.addEventListener('hashchange', handleRouting);

    // Initial Load
    if (window.location.hash) {
        handleRouting();
    }

    // Override Dashboard Navigation
    // We can't easily remove the old listener on dashboard, but we can add a new one that stops prop?
    // No, the old one sets .
    // The old  sets display but doesn't handle hash/tabs/title.
    // We need to STOP the old one from working or make it irrelevant.

    // If we replace the dashboard element clone, we lose all children (cards).
    // But  repopulates it!
    // So yes, we can clone dashboard to clear listeners.

    const newDashboard = dashboard.cloneNode(false); // shallow clone
    dashboard.parentNode.replaceChild(newDashboard, dashboard);

    // We need to re-render dashboard because we wiped it.
    // But  function uses the  variable which now points to the DETACHED element.
    // We need to update the  variable ref? We can't, it's const.

    // Okay, this patching approach is getting messy.
    // It is better to write a CLEAN file.

"""

# Let's accept that we need to write a clean file.
# I will use the  +  calls from the file, but wrap them in my own clean setup.

# 1. Extract all  and  calls.
tool_calls = []
for line in content.splitlines():
    if "registerTool(" in line or "createSimpleTextTool(" in line or "createMathTool(" in line or "createGeneratorTool(" in line:
        tool_calls.append(line)

# This misses multi-line calls.
# Most of my calls were one-liners, but some (like calculator) were multi-line.
# The calculator was:

# Okay, I will just append the NEW tools to the END of the file,
# and I will use  instead of  in the new file so I can override it? No.

# Let's go with the "Append and Patch" strategy but be smart.
# I will append code that:
# 1. Defines  and .
# 2. Re-implements  to use the global  (which is populated).
# 3. Re-attaches event listeners to use the new functions.
# 4. Triggers routing.

# The only issue is the old event listeners.
#  is attached to the DOM element.
#  is attached to the DOM element.

# I can clear them by cloning the element, as long as I have a reference to it.
#  holds the reference.
# If I do
# Then  has no listeners.
# But the  variable still points to the old (now removed) element.
# So if I call  (which uses  var), it renders to the removed element.

# So I MUST NOT remove the element if the variable is const and closed over.
# I MUST edit the source code of .

# I will verify the file content and use python to simply delete the lines I don't want.

# Lines to delete:
# - The initial variables block (replace with new one including tabs)
# - The  function
# - The  function
# - The event listeners for dashboard and backBtn.

# I will read the file, filter out these lines, and write back.

lines = content.splitlines()
new_lines = []
skip_mode = False

for line in lines:
    stripped = line.strip()

    # Replace variables
    if "const dashboard =" in line:
        new_lines.append("    const dashboard = document.getElementById('dashboard');")
        new_lines.append("    const toolView = document.getElementById('tool-view');")
        new_lines.append("    const toolTitle = document.getElementById('tool-title');")
        new_lines.append("    const toolContent = document.getElementById('tool-content');")
        new_lines.append("    const backBtn = document.getElementById('back-btn');")
        new_lines.append("    const searchInput = document.getElementById('search-input');")
        new_lines.append("    const categoryTabs = document.getElementById('category-tabs');")
        # Skip original vars
        continue
    if "const toolView =" in line or "const toolTitle =" in line or "const toolContent =" in line or "const backBtn =" in line or "const searchInput =" in line:
        continue

    # Skip old functions
    if "function showTool(" in line:
        skip_mode = True
    if "function showDashboard(" in line:
        skip_mode = True

    # Skip old listeners
    if "dashboard.addEventListener('click'" in line:
        skip_mode = True
    if "backBtn.addEventListener('click'" in line:
        skip_mode = True

    if skip_mode:
        # Detect end of block? strictly indentation based or '}'
        if line.strip() == "}" or line.strip() == "});":
            skip_mode = False
            # Don't add the closing brace of the function yet
        continue

    new_lines.append(line)

# Remove the last line "});"
if new_lines[-1].strip() == "});":
    new_lines.pop()

# Now append the new logic
new_code = """
    // --- Optimized Navigation & SEO ---

    function showDashboard() {
        toolView.style.display = 'none';
        dashboard.style.display = 'grid';
        if(categoryTabs) categoryTabs.style.display = 'flex';
        toolContent.innerHTML = '';
        searchInput.value = '';
        document.title = 'Crystal Tools - The Glassomorphic Web Utility Hub';
        history.pushState(null, null, ' ');
    }

    function showTool(toolId) {
        const tool = toolRegistry[toolId];
        if (tool) {
            dashboard.style.display = 'none';
            toolView.style.display = 'flex';
            if(categoryTabs) categoryTabs.style.display = 'none';
            toolTitle.textContent = tool.name;
            toolContent.innerHTML = '';
            tool.render(toolContent);
            document.title = tool.name + ' - Crystal Tools';

            if (window.location.hash !== '#' + toolId) {
                history.pushState(null, null, '#' + toolId);
            }
        }
    }

    function handleRouting() {
        const hash = window.location.hash.substring(1);
        if (hash && toolRegistry[hash]) {
            showTool(hash);
        } else {
            showDashboard();
        }
    }

    window.addEventListener('hashchange', handleRouting);

    // Listeners
    dashboard.addEventListener('click', (e) => {
        const card = e.target.closest('.tool-card');
        if (card) {
            const toolId = card.getAttribute('data-tool');
            window.location.hash = toolId;
        }
    });

    backBtn.addEventListener('click', () => {
        window.location.hash = ''; // This triggers hashchange -> handleRouting -> showDashboard
    });

    // Initial Route
    if (window.location.hash) {
        handleRouting();
    }

    // --- Batch 5 Tools (Health, Science, etc) ---
    // (Injecting them here)
"""

# Append Batch 5 tools
batch5 = """
    createMathTool('bmr-calc', 'BMR Calculator', 'Health', 'Basal Metabolic Rate.', [{key:'w', label:'Weight (kg)'}, {key:'h', label:'Height (cm)'}, {key:'a', label:'Age'}], (v) => (10 * v.w + 6.25 * v.h - 5 * v.a + 5).toFixed(0));
    createMathTool('water-intake', 'Water Intake', 'Health', 'Daily water need (L).', [{key:'w', label:'Weight (kg)'}], (v) => (v.w * 0.033).toFixed(2) + ' L');
    createMathTool('target-hr', 'Target Heart Rate', 'Health', 'Zone 2 (60-70%).', [{key:'age', label:'Age'}], (v) => Math.floor((220 - v.age) * 0.6) + '-' + Math.floor((220 - v.age) * 0.7));
    createMathTool('gpa-calc', 'GPA Calculator', 'Science', 'Simple Avg.', [{key:'g1', label:'G1'}, {key:'g2', label:'G2'}, {key:'g3', label:'G3'}, {key:'g4', label:'G4'}], (v) => ((v.g1+v.g2+v.g3+v.g4)/4).toFixed(2));
    createSimpleTextTool('html-minifier', 'HTML Minifier', 'Dev', 'Minify HTML.', (text) => text.replace(/\s+/g, ' ').replace(/> </g, '><'));
    createSimpleTextTool('hashtag-gen', 'Hashtag Generator', 'Social', 'Create tags.', (text) => text.split(' ').map(w => '#' + w).join(' '));
    createSimpleTextTool('bin-hex', 'Bin to Hex', 'Dev', 'Binary to Hex.', (text) => parseInt(text, 2).toString(16).toUpperCase());
    createSimpleTextTool('hex-bin', 'Hex to Bin', 'Dev', 'Hex to Binary.', (text) => parseInt(text, 16).toString(2));

    // Refresh
    renderDashboard();

});
"""

# Combine
final_output = "\n".join(new_lines) + new_logic + batch5

with open('quicktools/script.js', 'w') as f:
    f.write(final_output)

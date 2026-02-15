import re

with open('quicktools/index.html', 'r') as f:
    content = f.read()

# Define the modal JS block to remove
modal_js_pattern = r"""\s+// --- Help Modal ---\s+const helpBtn = document.getElementById\('help-btn'\);[\s\S]*?if\(e.key === 'Escape'\) toggleHelp\(false\);\s+    \}\);"""

# Remove all occurrences
content = re.sub(modal_js_pattern, "", content)

# Now add it back ONCE at the end of the script (before closing `});`)
modal_js = r"""
    // --- Help Modal ---
    const helpBtn = document.getElementById('help-btn');
    const helpModal = document.getElementById('help-modal');
    const helpClose = document.getElementById('help-close');

    function toggleHelp(show) {
        if(helpModal) helpModal.style.display = show ? 'flex' : 'none';
    }

    if(helpBtn) helpBtn.addEventListener('click', () => toggleHelp(true));
    if(helpClose) helpClose.addEventListener('click', () => toggleHelp(false));
    if(helpModal) helpModal.addEventListener('click', (e) => {
        if(e.target === helpModal) toggleHelp(false);
    });

    document.addEventListener('keydown', (e) => {
        if(e.key === 'Escape') toggleHelp(false);
    });
"""

# Find the last `});` and insert before it
last_brace = content.rfind('});')
if last_brace != -1:
    content = content[:last_brace] + modal_js + "\n" + content[last_brace:]
else:
    # If not found, append to end of script?
    # Script tag end?
    script_end = content.rfind('</script>')
    content = content[:script_end] + modal_js + "\n});\n" + content[script_end:]

with open('quicktools/index.html', 'w') as f:
    f.write(content)

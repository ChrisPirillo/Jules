import re

with open('quicktools/index.html', 'r') as f:
    content = f.read()

# 1. Logo Link
content = content.replace('<h1>Tooltimate</h1>', '<h1 onclick="window.location.hash=\'\'" style="cursor: pointer;">Tooltimate</h1>')

# 2. Navigation Logic (Tabs & Filtering)
tabs_logic = r"""
    // --- Navigation Logic ---
    function filterByCategory(category) {
        const cards = document.querySelectorAll('.tool-card');
        cards.forEach(card => {
            const cardCat = card.getAttribute('data-category');
            if (category === 'All' || cardCat === category || (!cardCat && category === 'All')) {
                card.style.display = 'flex';
            } else {
                card.style.display = 'none';
            }
        });

        // Update Active Tab
        const tabs = document.querySelectorAll('.category-tab');
        tabs.forEach(t => {
            if(t.getAttribute('data-cat') === category) t.classList.add('active');
            else t.classList.remove('active');
        });
    }

    const tabs = document.querySelectorAll('.category-tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            filterByCategory(tab.getAttribute('data-cat'));
        });
    });
"""

# Inject before `renderDashboard();`
if "filterByCategory" not in content:
    content = content.replace('renderDashboard();', tabs_logic + '\n    renderDashboard();', 1)

# 3. Badge Link Logic
badge_logic = r"""
            const catBadge = document.getElementById('tool-category-badge');
            if(catBadge) {
                catBadge.textContent = tool.category || 'Tool';
                catBadge.style.cursor = 'pointer';
                catBadge.onclick = (e) => {
                    e.stopPropagation();
                    window.location.hash = '';
                    setTimeout(() => filterByCategory(tool.category), 50);
                };
            }
"""
content = re.sub(r"const catBadge = document.getElementById\('tool-category-badge'\);\s+if\(catBadge\) catBadge.textContent = tool.category \|\| 'Tool';", badge_logic, content)

# 4. Help Modal HTML
modal_html = """
    <div id="help-btn" style="position: fixed; bottom: 20px; right: 20px; width: 40px; height: 40px; background: var(--theme-accent, #4f46e5); color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; cursor: pointer; box-shadow: 0 4px 10px rgba(0,0,0,0.3); z-index: 1000;">?</div>

    <div id="help-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); backdrop-filter: blur(5px); z-index: 2000; align-items: center; justify-content: center;">
        <div class="glass-panel" style="width: 90%; max-width: 500px; position: relative;">
            <button id="help-close" style="position: absolute; top: 15px; right: 15px; background: transparent; border: none; color: white; font-size: 1.5rem; cursor: pointer;">&times;</button>
            <h2 style="margin-bottom: 15px;">About Tooltimate</h2>
            <p style="margin-bottom: 20px;">Tooltimate is a collection of 200+ free, privacy-focused web utilities running entirely in your browser.</p>
            <div style="display: flex; flex-direction: column; gap: 10px;">
                <a href="https://pirillo.com/arcade/" target="_blank" class="glass-btn" style="justify-content: center;">More Apps</a>
                <a href="https://chris.pirillo.com/" target="_blank" class="glass-btn" style="justify-content: center;">Follow Chris</a>
                <a href="https://ctrlaltcreate.live/" target="_blank" class="glass-btn" style="justify-content: center;">Learn More</a>
            </div>
            <div style="margin-top: 20px; font-size: 0.8rem; opacity: 0.7; text-align: center;">Press ESC to close</div>
        </div>
    </div>
"""
if "help-modal" not in content:
    content = content.replace('</body>', modal_html + '\n</body>')

# 5. Help Modal JS
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
if "toggleHelp" not in content:
    # Append to script before end
    script_end = content.rfind('</script>')
    # Assuming script structure ends with `});` before `</script>`
    # But checking for `});` might be fragile if multiple.
    # Just look for the last `});`
    last_brace = content.rfind('});')
    if last_brace != -1:
        content = content[:last_brace] + modal_js + "\n" + content[last_brace:]

with open('quicktools/index.html', 'w') as f:
    f.write(content)

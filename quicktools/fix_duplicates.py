import re

with open('quicktools/index.html', 'r') as f:
    content = f.read()

# Find tool-header
start = content.find('<div class="tool-header">')
end = content.find('</div>', start)

if start != -1:
    header_content = content[start:end]
    # Count badges
    count = header_content.count('id="tool-category-badge"')
    print(f"Found {count} badges in header.")

    if count > 1:
        # Reconstruct header cleanly
        clean_header = r"""<div class="tool-header">
                        <button id="back-btn" class="glass-btn" aria-label="Back to Dashboard">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
                            Back
                        </button>
                        <h2 id="tool-title">Tool Name</h2> <span id="tool-category-badge" style="margin-left: auto; background: rgba(255,255,255,0.1); padding: 4px 12px; border-radius: 15px; font-size: 0.8rem; border: 1px solid rgba(255,255,255,0.2);">Category</span>"""

        new_content = content[:start] + clean_header + content[end:]
        with open('quicktools/index.html', 'w') as f:
            f.write(new_content)
        print("Fixed duplicates.")

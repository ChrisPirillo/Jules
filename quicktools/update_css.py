import re

with open('quicktools/index.html', 'r') as f:
    content = f.read()

# 1. Update CSS
# We need to find the <style> block and update rules.
# It's easier to just append new overrides at the end of the <style> block.

new_css = """
/* --- Enhancements --- */

/* Scroll Diffusion */
#content-area {
    /* Mask to fade out content at the top as it scrolls */
    mask-image: linear-gradient(to bottom, transparent 0%, black 30px, black 100%);
    -webkit-mask-image: linear-gradient(to bottom, transparent 0%, black 30px, black 100%);
    padding-top: 10px; /* Space for the fade */
}

/* One-Line Categories (Desktop) */
@media (min-width: 768px) {
    .category-tabs {
        flex-wrap: nowrap !important;
        overflow-x: hidden !important; /* No scroll */
        justify-content: space-between;
        gap: 5px;
        padding: 0 10px 10px 10px;
    }
    .category-tab {
        flex: 1;
        text-align: center;
        padding: 8px 4px !important; /* Reduced padding */
        font-size: 0.8rem !important; /* Reduced font */
        min-width: 0; /* Allow shrinking below content size */
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
}

/* Themed Components */
.glass-btn-primary {
    background: var(--theme-accent, linear-gradient(135deg, #667eea 0%, #764ba2 100%)) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    color: var(--theme-text, white) !important;
}

.glass-input, .glass-select, .glass-textarea {
    background: var(--theme-bg-input, rgba(0,0,0,0.4)) !important;
    border-color: var(--theme-border, rgba(255,255,255,0.3)) !important;
}

.glass-btn:hover {
    background: var(--theme-accent-hover, rgba(255,255,255,0.35)) !important;
}

/* Tool Card Theme Support */
.tool-card {
    border-color: var(--theme-border, rgba(255,255,255,0.2)) !important;
}
.tool-card:hover {
    background: var(--theme-bg-hover, rgba(255,255,255,0.35)) !important;
    border-color: var(--theme-accent, white) !important;
}
.tool-card .icon {
    color: var(--theme-accent, #4f46e5) !important;
}
"""

content = content.replace('</style>', new_css + '\n</style>')

with open('quicktools/index.html', 'w') as f:
    f.write(content)

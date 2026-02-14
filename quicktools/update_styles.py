import re

with open('quicktools/index.html', 'r') as f:
    content = f.read()

# 1. Uniform Height Fix
# Add CSS rule for inputs and buttons to have same height
uniform_css = """
/* Uniform Height & UI Fixes */
.glass-input, .glass-select, .glass-btn, .glass-btn-primary {
    height: 44px !important;
    min-height: 44px;
    box-sizing: border-box;
    display: inline-flex;
    align-items: center;
    vertical-align: middle;
    margin: 0; /* Reset margins for alignment */
}

/* Ensure buttons in flex containers align with inputs */
.input-group {
    display: flex;
    flex-direction: column;
}

/* Category Tabs - No scroll on Desktop */
@media (min-width: 768px) {
    .category-tabs {
        flex-wrap: wrap;
        overflow-x: visible;
        justify-content: center;
    }
    .category-tab {
        flex: 0 1 auto; /* Allow shrinking if absolutely needed, but prefer wrap */
        font-size: 0.9rem;
        padding: 6px 12px;
    }
}

/* Mobile: Keep scrolling */
@media (max-width: 767px) {
    .category-tabs {
        justify-content: flex-start;
    }
}
"""

# Inject before closing style tag
content = content.replace('</style>', uniform_css + '\n</style>')

with open('quicktools/index.html', 'w') as f:
    f.write(content)

import os

with open('all_tools_extracted.js', 'r') as f:
    tools_code = f.read()

# Escape backslashes in tools_code for python string if needed?
# No, we will just concatenate.

code = r"""document.addEventListener('DOMContentLoaded', () => {
    const dashboard = document.getElementById('dashboard');
    const toolView = document.getElementById('tool-view');
    const toolTitle = document.getElementById('tool-title');
    const toolContent = document.getElementById('tool-content');
    const backBtn = document.getElementById('back-btn');
    const searchInput = document.getElementById('search-input');
    const categoryTabs = document.getElementById('category-tabs');

    // --- Tool Factory ---
    const toolRegistry = {};

    function registerTool(id, name, category, description, icon, renderFn) {
        toolRegistry[id] = { name, category, description, icon, render: renderFn };
    }

    function createSimpleTextTool(id, name, category, description, transformFn) {
        registerTool(id, name, category, description,
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>',
            (container) => {
                const html = `
                    <div class="glass-panel" style="max-width: 800px;">
                        <textarea id="${id}-input" class="glass-textarea" placeholder="Enter text..."></textarea>
                        <div style="display: flex; gap: 10px; margin-bottom: 20px;">
                            <button id="${id}-action" class="glass-btn-primary" style="flex: 1;">${name}</button>
                            <button id="${id}-copy" class="glass-btn" style="flex: 1;">Copy Result</button>
                        </div>
                        <textarea id="${id}-output" class="glass-textarea" readonly placeholder="Result..."></textarea>
                    </div>
                `;
                container.innerHTML = html;

                const input = document.getElementById(`${id}-input`);
                const output = document.getElementById(`${id}-output`);
                const actionBtn = document.getElementById(`${id}-action`);
                const copyBtn = document.getElementById(`${id}-copy`);

                actionBtn.addEventListener('click', () => {
                    try {
                        output.value = transformFn(input.value);
                    } catch (e) {
                        output.value = "Error: " + e.message;
                    }
                });

                copyBtn.addEventListener('click', () => {
                    if(output.value) {
                        navigator.clipboard.writeText(output.value);
                        const original = copyBtn.textContent;
                        copyBtn.textContent = 'Copied!';
                        setTimeout(() => copyBtn.textContent = original, 1000);
                    }
                });
            }
        );
    }

    function createMathTool(id, name, category, description, inputs, calcFn) {
        registerTool(id, name, category, description,
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 21h10a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2z"/><line x1="9" y1="7" x2="15" y2="7"/><line x1="9" y1="11" x2="15" y2="11"/><line x1="9" y1="15" x2="15" y2="15"/></svg>',
            (container) => {
                let inputsHtml = '';
                inputs.forEach(inp => {
                    inputsHtml += `<div class="input-group"><label>${inp.label}</label><input type="number" id="${id}-${inp.key}" class="glass-input" placeholder="${inp.placeholder || '0'}" step="any"></div>`;
                });

                const html = `
                    <div class="glass-panel" style="max-width: 500px;">
                        ${inputsHtml}
                        <button id="${id}-calc" class="glass-btn-primary" style="margin-top: 10px;">Calculate</button>
                        <div style="margin-top: 20px; text-align: center;">
                            <label style="color:white; font-size: 0.9rem;">Result</label>
                            <div id="${id}-result" style="font-size: 2rem; color: white; font-weight: bold;">-</div>
                        </div>
                    </div>
                `;
                container.innerHTML = html;

                document.getElementById(`${id}-calc`).addEventListener('click', () => {
                    const values = {};
                    inputs.forEach(inp => {
                        values[inp.key] = parseFloat(document.getElementById(`${id}-${inp.key}`).value) || 0;
                    });
                    const result = calcFn(values);
                    document.getElementById(`${id}-result`).textContent = result;
                });
            }
        );
    }

    function createGeneratorTool(id, name, category, description, actionName, genFn) {
        registerTool(id, name, category, description,
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg>',
            (container) => {
                const html = `
                    <div class="glass-panel" style="max-width: 500px; text-align: center;">
                        <button id="${id}-action" class="glass-btn-primary">${actionName}</button>
                        <div id="${id}-result" class="glass-textarea" style="margin-top: 20px; min-height: 100px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem;"></div>
                        <button id="${id}-copy" class="glass-btn" style="margin-top: 10px; width: 100%;">Copy Result</button>
                    </div>
                `;
                container.innerHTML = html;

                const resDiv = document.getElementById(`${id}-result`);

                document.getElementById(`${id}-action`).addEventListener('click', () => {
                    resDiv.textContent = genFn();
                });

                document.getElementById(`${id}-copy`).addEventListener('click', () => {
                     navigator.clipboard.writeText(resDiv.textContent);
                });
            }
        );
    }

    // --- Tools ---
""" + "\n" + tools_code + "\n" + r"""

    // --- Render & Navigation ---
    function renderDashboard() {
        dashboard.innerHTML = '';
        const sortedTools = Object.keys(toolRegistry).sort();
        sortedTools.forEach(key => {
            const tool = toolRegistry[key];
            const card = document.createElement('div');
            card.className = 'tool-card';
            card.setAttribute('data-tool', key);
            card.setAttribute('data-category', tool.category);
            card.innerHTML = `
                <div class="icon">${tool.icon}</div>
                <h3>${tool.name}</h3>
                <p>${tool.description}</p>
            `;
            dashboard.appendChild(card);
        });
    }

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

    renderDashboard();

    // Listeners
    window.addEventListener('hashchange', handleRouting);
    if (window.location.hash) handleRouting();

    dashboard.addEventListener('click', (e) => {
        const card = e.target.closest('.tool-card');
        if (card) {
            const toolId = card.getAttribute('data-tool');
            window.location.hash = toolId;
        }
    });

    backBtn.addEventListener('click', () => {
        window.location.hash = '';
    });

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

});
"""

with open('quicktools/script.js', 'w') as f:
    f.write(code)

import os

code = r"""document.addEventListener('DOMContentLoaded', () => {
    const dashboard = document.getElementById('dashboard');
    const toolView = document.getElementById('tool-view');
    const toolTitle = document.getElementById('tool-title');
    const toolContent = document.getElementById('tool-content');
    const backBtn = document.getElementById('back-btn');
    const searchInput = document.getElementById('search-input');
    const categoryTabs = document.getElementById('category-tabs');

    // --- Random Theming ---
    function setRandomTheme() {
        const hue = Math.floor(Math.random() * 360);
        const sat = Math.floor(Math.random() * 20) + 60; // 60-80%
        const light = Math.floor(Math.random() * 20) + 40; // 40-60%
        const primaryColor = `hsl(${hue}, ${sat}%, ${light}%)`;

        const root = document.documentElement;
        root.style.setProperty('--primary-color', primaryColor);

        const hue2 = (hue + 40) % 360;
        const bgGradient = `linear-gradient(135deg, hsl(${hue}, 70%, 60%) 0%, hsl(${hue2}, 70%, 40%) 100%)`;
        root.style.setProperty('--bg-gradient', bgGradient);
    }

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

    // --- Real Tools (Batch 7+8 Impl) ---
    registerTool('speed-test', 'Internet Speed', 'Misc', 'Download Speed Test.',
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 12h20"/><path d="M12 2v20"/><path d="M4.93 4.93l14.14 14.14"/></svg>',
        (container) => {
            container.innerHTML = `
                <div class="glass-panel" style="text-align: center;">
                    <h3 id="st-status">Ready</h3>
                    <div style="font-size: 3rem; font-weight: bold; margin: 20px 0;" id="st-val">0.0</div>
                    <div style="color: rgba(255,255,255,0.7);">Mbps</div>
                    <button id="st-btn" class="glass-btn-primary" style="margin-top: 20px;">Start Test</button>
                </div>
            `;
            document.getElementById('st-btn').addEventListener('click', () => {
                const val = document.getElementById('st-val');
                const status = document.getElementById('st-status');
                status.textContent = 'Testing...';
                val.textContent = '0.0';

                const imageAddr = "https://upload.wikimedia.org/wikipedia/commons/2/2d/Snake_River_%285mb%29.jpg";
                const downloadSize = 5245329;
                const startTime = (new Date()).getTime();
                const cacheBuster = "?nnn=" + startTime;

                const download = new Image();
                download.onload = function () {
                    const endTime = (new Date()).getTime();
                    const duration = (endTime - startTime) / 1000;
                    const bitsLoaded = downloadSize * 8;
                    const speedBps = bitsLoaded / duration;
                    const speedMbps = (speedBps / 1024 / 1024).toFixed(2);
                    status.textContent = 'Done';
                    val.textContent = speedMbps;
                }
                download.onerror = function (err, msg) {
                    status.textContent = 'Error';
                    val.textContent = '0.0';
                }
                download.src = imageAddr + cacheBuster;
            });
        }
    );

    registerTool('ip-address', 'Public IP', 'Dev', 'Get your public IP.',
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
        (container) => {
            container.innerHTML = `
                <div class="glass-panel" style="text-align: center;">
                    <div id="ip-result" style="font-size: 2rem; font-weight: bold; margin: 20px 0;">---.---.---.---</div>
                    <button id="ip-btn" class="glass-btn-primary">Fetch IP</button>
                </div>
            `;
            document.getElementById('ip-btn').addEventListener('click', () => {
                const resDiv = document.getElementById('ip-result');
                resDiv.textContent = 'Fetching...';
                fetch('https://api.ipify.org?format=json')
                    .then(res => res.json())
                    .then(data => resDiv.textContent = data.ip)
                    .catch(e => resDiv.textContent = 'Error');
            });
        }
    );

    registerTool('sha256', 'SHA-256 Hash', 'Security', 'Generate SHA-256 hash.',
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
        (container) => {
             container.innerHTML = `
                <div class="glass-panel" style="max-width: 800px;">
                    <textarea id="sha-input" class="glass-textarea" placeholder="Enter text..."></textarea>
                    <button id="sha-btn" class="glass-btn-primary" style="width: 100%; margin-bottom: 10px;">Generate Hash</button>
                    <textarea id="sha-output" class="glass-textarea" readonly placeholder="Hash..."></textarea>
                </div>
            `;
            document.getElementById('sha-btn').addEventListener('click', async () => {
                const text = document.getElementById('sha-input').value;
                const msgBuffer = new TextEncoder().encode(text);
                const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
                const hashArray = Array.from(new Uint8Array(hashBuffer));
                const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
                document.getElementById('sha-output').value = hashHex;
            });
        }
    );

    registerTool('regex-real', 'Regex Tester', 'Dev', 'Test Regular Expressions.',
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 22h14a2 2 0 0 0 2-2V7.5L14.5 2H6a2 2 0 0 0-2 2v4"/><polyline points="14 2 14 8 20 8"/><path d="M2 15h10"/><path d="M9 18l3-3-3-3"/></svg>',
        (container) => {
            container.innerHTML = `
                <div class="glass-panel" style="max-width: 800px;">
                    <div class="input-group">
                        <label>Pattern (e.g. \\d+)</label>
                        <input type="text" id="rx-pattern" class="glass-input" placeholder="\\w+">
                    </div>
                    <div class="input-group">
                        <label>Flags (e.g. gi)</label>
                        <input type="text" id="rx-flags" class="glass-input" placeholder="g">
                    </div>
                    <label>Test String</label>
                    <textarea id="rx-text" class="glass-textarea" placeholder="Text to match..."></textarea>
                    <button id="rx-btn" class="glass-btn-primary" style="margin-bottom: 10px;">Test Regex</button>
                    <label>Matches</label>
                    <div id="rx-result" class="glass-textarea" style="white-space: pre-wrap;"></div>
                </div>
            `;
            document.getElementById('rx-btn').addEventListener('click', () => {
                const pat = document.getElementById('rx-pattern').value;
                const flags = document.getElementById('rx-flags').value;
                const text = document.getElementById('rx-text').value;
                const resDiv = document.getElementById('rx-result');

                try {
                    const regex = new RegExp(pat, flags);
                    const matches = text.match(regex);
                    if(matches) {
                        resDiv.textContent = JSON.stringify(matches, null, 2);
                        resDiv.style.color = 'white';
                    } else {
                        resDiv.textContent = 'No matches found.';
                        resDiv.style.color = '#ffaaaa';
                    }
                } catch(e) {
                    resDiv.textContent = 'Error: ' + e.message;
                    resDiv.style.color = '#ff6b6b';
                }
            });
        }
    );

    // --- Standard Tools ---
    createSimpleTextTool('uppercase', 'Uppercase', 'Text', 'Convert text to uppercase.', (text) => text.toUpperCase());
    createSimpleTextTool('lowercase', 'Lowercase', 'Text', 'Convert text to lowercase.', (text) => text.toLowerCase());
    createSimpleTextTool('slugify', 'Slug Generator', 'Text', 'Convert text to URL slug.', (text) => text.toLowerCase().replace(/[^\w ]+/g, '').replace(/ +/g, '-'));
    createSimpleTextTool('word-count', 'Word Count', 'Text', 'Count words.', (text) => `Words: ${text.trim().split(/\s+/).length}`);
    createSimpleTextTool('char-count', 'Char Count', 'Text', 'Count characters.', (text) => `Characters: ${text.length}`);
    createSimpleTextTool('html-minifier', 'HTML Minifier', 'Dev', 'Minify HTML.', (text) => text.replace(/\s+/g, ' ').replace(/> </g, '><'));
    createSimpleTextTool('hashtag-gen', 'Hashtag Generator', 'Social', 'Create tags.', (text) => text.split(' ').map(w => '#' + w).join(' '));
    createSimpleTextTool('base64-encode', 'Base64 Encode', 'Dev', 'Encode text to Base64.', (text) => btoa(text));
    createSimpleTextTool('base64-decode', 'Base64 Decode', 'Dev', 'Decode Base64 to text.', (text) => atob(text));
    createSimpleTextTool('json-minify', 'JSON Minifier', 'Dev', 'Remove whitespace from JSON.', (text) => JSON.stringify(JSON.parse(text)));
    createSimpleTextTool('list-random', 'Randomize List', 'Text', 'Shuffle list items.', (text) => text.split('\n').sort(() => 0.5 - Math.random()).join('\n'));
    createSimpleTextTool('list-sort', 'Sort List (Numeric)', 'Text', 'Sort numbers.', (text) => text.split('\n').sort((a,b) => parseFloat(a)-parseFloat(b)).join('\n'));

    createMathTool('bmi-calc', 'BMI Calculator', 'Health', 'Basal Metabolic Rate.', [{key:'w', label:'Weight (kg)'}, {key:'h', label:'Height (m)'}], (v) => (v.w / (v.h * v.h)).toFixed(2));
    createMathTool('water-intake', 'Water Intake', 'Health', 'Daily water need (L).', [{key:'w', label:'Weight (kg)'}], (v) => (v.w * 0.033).toFixed(2) + ' L');
    createMathTool('target-hr', 'Target Heart Rate', 'Health', 'Zone 2 (60-70%).', [{key:'age', label:'Age'}], (v) => Math.floor((220 - v.age) * 0.6) + '-' + Math.floor((220 - v.age) * 0.7));
    createMathTool('tip-calc', 'Tip Calculator', 'Finance', 'Calculate tip amount.', [{key:'bill', label:'Bill Amount'}, {key:'tip', label:'Tip %'}], (v) => (v.bill * (v.tip / 100)).toFixed(2));
    createMathTool('prime-factor', 'Prime Factorization', 'Math', 'Find prime factors.', [{key:'n', label:'Number'}], (v) => { let n = parseInt(v.n); const f = []; let d = 2; while (d * d <= n) { while (n % d === 0) { f.push(d); n = Math.floor(n / d); } d++; } if (n > 1) f.push(n); return f.join(' × '); });

    createGeneratorTool('uuid', 'UUID Generator', 'Dev', 'Generate UUID v4.', 'Generate UUID', () => 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) { var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8); return v.toString(16); }));
    createGeneratorTool('random-number', 'Random Number', 'Math', 'Random number 1-100.', 'Roll (1-100)', () => Math.floor(Math.random() * 100) + 1);
    createGeneratorTool('random-quote', 'Random Quote', 'Game', 'Get a random quote.', 'Get Quote', () => ["The only way to do great work is to love what you do. - Steve Jobs", "Simplicity is the soul of efficiency. - Austin Freeman"].sort(() => 0.5 - Math.random())[0]);

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

        // Update Count
        const countBadge = document.getElementById('tool-count-badge');
        if (countBadge) {
            const count = sortedTools.length;
            countBadge.textContent = `${count} Tools`;
            countBadge.style.display = 'inline-block';
            document.getElementById('search-input').placeholder = `Search ${count} tools...`;
        }
    }

    function showDashboard() {
        toolView.style.display = 'none';
        dashboard.style.display = 'grid';
        if(categoryTabs) categoryTabs.style.display = 'flex';
        toolContent.innerHTML = '';
        searchInput.value = '';

        // Randomize Theme on Dashboard return
        setRandomTheme();

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

            // Note: We keep the randomized theme active

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

    // Init
    setRandomTheme();
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

# Replace script in index.html
with open('quicktools/index.html', 'r') as f:
    html = f.read()

# Replace content between <script> and </script>
start = html.find('<script src="script.js">')
if start == -1:
    start = html.find('<script>') + 8
    end = html.find('</script>', start)
    html = html[:start] + "\n" + code + "\n" + html[end:]
else:
    # This shouldn't happen if we merged correctly earlier, but let's be safe
    pass

# We already merged styles/script earlier, so we look for <script>...</script>
# But wait, I might have messed up the file with previous failed tool calls.
# Let's check current file state.
with open('quicktools/index.html', 'r') as f:
    current = f.read()

# Just look for the script tag
import re
new_html = re.sub(r'<script>.*?</script>', f'<script>\n{code}\n</script>', current, flags=re.DOTALL)

with open('quicktools/index.html', 'w') as f:
    f.write(new_html)

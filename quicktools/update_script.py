import re

with open('quicktools/index.html', 'r') as f:
    content = f.read()

# 1. Random Theming
theme_logic = r"""
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
"""

if 'function setRandomTheme' not in content:
    content = content.replace("const categoryTabs = document.getElementById('category-tabs');", "const categoryTabs = document.getElementById('category-tabs');" + theme_logic)
    content = content.replace('renderDashboard();', 'setRandomTheme();\n    renderDashboard();')

# Remove old theme logic
content = re.sub(r"// Dynamic Theme.*?app.classList.add\('theme-' \+ theme\);", "// Theme is randomized on load", content, flags=re.DOTALL)

# 2. Real Speed Test
real_speed_test = r"""
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
"""
content = re.sub(r"registerTool\('speed-test'.*?\);", real_speed_test, content, flags=re.DOTALL)

# 3. Real IP
custom_ip = r"""
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
"""
# Assuming the old IP tool was removed or we just append this one
content = content.replace("// --- Batch 7: High Volume & Complex Tools ---", "// --- Batch 7: High Volume & Complex Tools ---\n" + custom_ip)

# 4. Real SHA-256
sha_func = r"""
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
"""
content = re.sub(r"createSimpleTextTool\('md5-mock'.*?\);", "", content)
content = content.replace("// --- Batch 7: High Volume & Complex Tools ---", "// --- Batch 7: High Volume & Complex Tools ---\n" + sha_func)

# 5. Batch 8 Tools
batch8 = r"""
    // --- Batch 8: More Real Tools ---

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

    createMathTool('prime-factor', 'Prime Factorization', 'Math', 'Find prime factors.', [{key:'n', label:'Number'}], (v) => {
        let n = parseInt(v.n);
        const factors = [];
        let d = 2;
        while (d * d <= n) {
            while (n % d === 0) {
                factors.push(d);
                n = Math.floor(n / d);
            }
            d++;
        }
        if (n > 1) factors.push(n);
        return factors.join(' × ');
    });

    createSimpleTextTool('list-random', 'Randomize List', 'Text', 'Shuffle list items.', (text) => text.split('\n').sort(() => 0.5 - Math.random()).join('\n'));
    createSimpleTextTool('list-sort', 'Sort List (Numeric)', 'Text', 'Sort numbers.', (text) => text.split('\n').sort((a,b) => parseFloat(a)-parseFloat(b)).join('\n'));
    createSimpleTextTool('json-minify', 'JSON Minifier', 'Dev', 'Remove whitespace from JSON.', (text) => JSON.stringify(JSON.parse(text)));
"""

if 'Regex Tester' not in content:
    content = content.replace("if (countBadge) {", batch8 + "\n    if (countBadge) {")

with open('quicktools/index.html', 'w') as f:
    f.write(content)

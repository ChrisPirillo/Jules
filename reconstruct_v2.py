import os

# 1. Theme Logic
theme_js = r"""    // --- Random Theming ---
    function setRandomTheme() {
        const hue = Math.floor(Math.random() * 360);
        const sat = Math.floor(Math.random() * 20) + 60;
        const light = Math.floor(Math.random() * 20) + 10;

        const primaryColor = `hsl(${hue}, ${sat}%, ${light}%)`;
        const accentColor = `hsl(${hue}, ${sat}%, ${light + 40}%)`;
        const bgInput = `hsla(${hue}, 30%, 10%, 0.6)`;
        const border = `hsla(${hue}, 50%, 50%, 0.3)`;
        const shadow = `hsla(${hue}, ${sat}%, ${light + 10}%, 0.3)`;

        const root = document.documentElement;
        root.style.setProperty('--primary-color', primaryColor);

        const hue2 = (hue + 40) % 360;
        const bgGradient = `linear-gradient(135deg, hsl(${hue}, 60%, 20%) 0%, hsl(${hue2}, 60%, 10%) 100%)`;
        root.style.setProperty('--bg-gradient', bgGradient);

        root.style.setProperty('--theme-accent', accentColor);
        root.style.setProperty('--theme-accent-hover', `hsl(${hue}, ${sat}%, ${light + 50}%)`);
        root.style.setProperty('--theme-bg-input', bgInput);
        root.style.setProperty('--theme-border', border);
        root.style.setProperty('--theme-shadow', shadow);
        root.style.setProperty('--theme-bg-hover', `hsla(${hue}, ${sat}%, 25%, 0.4)`);
    }"""

# 2. Tools
# Read tools from `all_tools_extracted.js` which has Batch 1-7
with open('all_tools_extracted.js', 'r') as f:
    tools_code = f.read()

# Add Batch 8 (Regex, Prime, List)
batch8 = r"""
    // --- Batch 8 ---
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
                    if(matches) { resDiv.textContent = JSON.stringify(matches, null, 2); resDiv.style.color = 'white'; }
                    else { resDiv.textContent = 'No matches found.'; resDiv.style.color = '#ffaaaa'; }
                } catch(e) { resDiv.textContent = 'Error: ' + e.message; resDiv.style.color = '#ff6b6b'; }
            });
        }
    );
    createMathTool('prime-factor', 'Prime Factorization', 'Math', 'Find prime factors.', [{key:'n', label:'Number'}], (v) => { let n = parseInt(v.n); const f = []; let d = 2; while (d * d <= n) { while (n % d === 0) { f.push(d); n = Math.floor(n / d); } d++; } if (n > 1) f.push(n); return f.join(' × '); });
    createSimpleTextTool('list-random', 'Randomize List', 'Text', 'Shuffle list items.', (text) => text.split('\n').sort(() => 0.5 - Math.random()).join('\n'));
    createSimpleTextTool('list-sort', 'Sort List (Numeric)', 'Text', 'Sort numbers.', (text) => text.split('\n').sort((a,b) => parseFloat(a)-parseFloat(b)).join('\n'));
    createSimpleTextTool('json-minify', 'JSON Minifier', 'Dev', 'Remove whitespace from JSON.', (text) => JSON.stringify(JSON.parse(text)));
"""

# Add Batch 9 (GCD, Text Diff, URL Parser, Curl, Contrast)
batch9 = r"""
    // --- Batch 9 ---
    createMathTool('gcd-lcm', 'GCD & LCM', 'Math', 'Greatest Common Divisor.', [{key:'a', label:'Number A'}, {key:'b', label:'Number B'}], (v) => {
        const gcd = (a, b) => !b ? a : gcd(b, a % b);
        const lcm = (a, b) => (a * b) / gcd(a, b);
        const g = gcd(v.a, v.b);
        const l = lcm(v.a, v.b);
        return 'GCD: ' + g + ' | LCM: ' + l;
    });
    createMathTool('pct-diff', 'Percentage Difference', 'Math', 'Diff between two values.', [{key:'v1', label:'Value 1'}, {key:'v2', label:'Value 2'}], (v) => {
        const avg = (v.v1 + v.v2) / 2;
        return (Math.abs(v.v1 - v.v2) / avg * 100).toFixed(2) + '%';
    });
    createSimpleTextTool('text-diff', 'Text Diff (Lines)', 'Text', 'Show added/removed lines.', (text) => {
        const parts = text.split('\n---\n');
        if(parts.length < 2) return "Enter two text blocks separated by a line containing only '---'";
        const lines1 = parts[0].split('\n');
        const lines2 = parts[1].split('\n');
        const added = lines2.filter(x => !lines1.includes(x));
        const removed = lines1.filter(x => !lines2.includes(x));
        return 'Added:\n' + added.join('\n') + '\n\nRemoved:\n' + removed.join('\n');
    });
    createSimpleTextTool('remove-dup-lines', 'Remove Duplicates', 'Text', 'Unique lines only.', (text) => [...new Set(text.split('\n'))].join('\n'));
    createSimpleTextTool('url-parser', 'URL Parser', 'Dev', 'Parse URL parts.', (text) => { try { const u = new URL(text); return JSON.stringify({ protocol: u.protocol, host: u.host, pathname: u.pathname, search: u.search, hash: u.hash }, null, 2); } catch(e) { return "Invalid URL"; } });
    createSimpleTextTool('curl-gen', 'Curl Generator', 'Dev', 'GET request curl.', (text) => 'curl -X GET "' + text + '"');

    registerTool('contrast-check', 'Contrast Checker', 'Color', 'Check text contrast.',
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
        (container) => {
            container.innerHTML = `
                <div class="glass-panel" style="max-width: 500px;">
                    <div class="input-group">
                        <label>Foreground (Hex)</label>
                        <input type="color" id="cc-fg" class="glass-input" value="#ffffff" style="height:50px;">
                    </div>
                    <div class="input-group">
                        <label>Background (Hex)</label>
                        <input type="color" id="cc-bg" class="glass-input" value="#000000" style="height:50px;">
                    </div>
                    <div id="cc-preview" style="padding: 20px; border-radius: 8px; text-align: center; margin: 20px 0; border: 1px solid rgba(255,255,255,0.2);">Preview Text</div>
                    <div id="cc-result" style="text-align: center; font-weight: bold; font-size: 1.2rem;">Ratio: 21.00 (AAA)</div>
                </div>`;
            function getLum(hex) {
                const r = parseInt(hex.substr(1,2),16)/255;
                const g = parseInt(hex.substr(3,2),16)/255;
                const b = parseInt(hex.substr(5,2),16)/255;
                const a = [r,g,b].map(v => v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4));
                return a[0]*0.2126 + a[1]*0.7152 + a[2]*0.0722;
            }
            function check() {
                const fg = document.getElementById('cc-fg').value;
                const bg = document.getElementById('cc-bg').value;
                document.getElementById('cc-preview').style.color = fg;
                document.getElementById('cc-preview').style.backgroundColor = bg;
                const l1 = getLum(fg);
                const l2 = getLum(bg);
                const ratio = (Math.max(l1,l2)+0.05)/(Math.min(l1,l2)+0.05);
                let rating = '';
                if(ratio >= 7) rating = '(AAA)';
                else if(ratio >= 4.5) rating = '(AA)';
                else rating = '(Fail)';
                document.getElementById('cc-result').textContent = 'Ratio: ' + ratio.toFixed(2) + ' ' + rating;
            }
            document.getElementById('cc-fg').addEventListener('input', check);
            document.getElementById('cc-bg').addEventListener('input', check);
            check();
        }
    );
"""

# Add Batch 10 (Mass Tools)
batch10 = r"""
    // --- Batch 10: The Road to 200 ---
    // Math
    createMathTool('factorial', 'Factorial', 'Math', 'N!', [{key:'n', label:'N'}], (v) => { let r=1; for(let i=2; i<=v.n; i++) r*=i; return r; });
    createMathTool('fibonacci', 'Fibonacci', 'Math', 'Nth number.', [{key:'n', label:'N'}], (v) => { let a=0, b=1, t; for(let i=2; i<=v.n; i++){t=a+b; a=b; b=t;} return v.n<1?0:b; });
    createMathTool('sqrt', 'Square Root', 'Math', 'Sqrt(x)', [{key:'x', label:'X'}], (v) => Math.sqrt(v.x).toFixed(4));
    createMathTool('cbrt', 'Cube Root', 'Math', 'Cbrt(x)', [{key:'x', label:'X'}], (v) => Math.cbrt(v.x).toFixed(4));
    createMathTool('log10', 'Log Base 10', 'Math', 'Log10(x)', [{key:'x', label:'X'}], (v) => Math.log10(v.x).toFixed(4));
    createMathTool('ln', 'Natural Log', 'Math', 'Ln(x)', [{key:'x', label:'X'}], (v) => Math.log(v.x).toFixed(4));
    createMathTool('sin', 'Sine', 'Math', 'Sin(x deg)', [{key:'x', label:'Degrees'}], (v) => Math.sin(v.x * Math.PI / 180).toFixed(4));
    createMathTool('cos', 'Cosine', 'Math', 'Cos(x deg)', [{key:'x', label:'Degrees'}], (v) => Math.cos(v.x * Math.PI / 180).toFixed(4));
    createMathTool('tan', 'Tangent', 'Math', 'Tan(x deg)', [{key:'x', label:'Degrees'}], (v) => Math.tan(v.x * Math.PI / 180).toFixed(4));
    createMathTool('deg-rad', 'Deg to Rad', 'Math', 'Degrees to Radians.', [{key:'d', label:'Degrees'}], (v) => (v.d * Math.PI / 180).toFixed(4));
    createMathTool('rad-deg', 'Rad to Deg', 'Math', 'Radians to Degrees.', [{key:'r', label:'Radians'}], (v) => (v.r * 180 / Math.PI).toFixed(4));

    // Statistics
    createSimpleTextTool('stats-mean', 'Mean Calculator', 'Math', 'Average of list.', (text) => { const n = text.match(/-?[\d\.]+/g).map(Number); return (n.reduce((a,b)=>a+b,0)/n.length).toFixed(4); });
    createSimpleTextTool('stats-median', 'Median Calculator', 'Math', 'Median of list.', (text) => { const n = text.match(/-?[\d\.]+/g).map(Number).sort((a,b)=>a-b); const m = Math.floor(n.length/2); return (n.length%2!==0 ? n[m] : (n[m-1]+n[m])/2).toFixed(4); });
    createSimpleTextTool('stats-range', 'Range Calculator', 'Math', 'Range (Max-Min).', (text) => { const n = text.match(/-?[\d\.]+/g).map(Number); return (Math.max(...n) - Math.min(...n)).toFixed(4); });

    // Text
    createSimpleTextTool('repeat-string', 'Repeat String', 'Text', 'Repeat text N times (use line1 for N).', (text) => { const lines = text.split('\n'); const n = parseInt(lines[0]) || 1; return lines.slice(1).join('\n').repeat(n); });
    createSimpleTextTool('pad-start', 'Pad Start', 'Text', 'Pad text start.', (text) => text.split('\n').map(l => l.padStart(20, ' ')).join('\n'));
    createSimpleTextTool('pad-end', 'Pad End', 'Text', 'Pad text end.', (text) => text.split('\n').map(l => l.padEnd(20, ' ')).join('\n'));
    createSimpleTextTool('center-text', 'Center Text', 'Text', 'Center align text (mock).', (text) => text.split('\n').map(l => l.padStart((40 + l.length)/2).padEnd(40)).join('\n'));
    createSimpleTextTool('leet-speak', 'Leet Speak', 'Text', '1337 5p34k.', (text) => text.replace(/[aA]/g,'4').replace(/[eE]/g,'3').replace(/[iI]/g,'1').replace(/[oO]/g,'0').replace(/[sS]/g,'5').replace(/[tT]/g,'7'));
    createSimpleTextTool('obfuscate', 'Obfuscate Text', 'Text', 'Base64 + Reverse.', (text) => btoa(text).split('').reverse().join(''));

    // Dev
    createSimpleTextTool('chmod-calc', 'Chmod Calculator', 'Dev', 'Octal to Symbol (e.g. 755).', (text) => {
        const p = ['---','--x','-w-','-wx','r--','r-x','rw-','rwx'];
        return text.split('').map(c => p[parseInt(c)] || '').join('');
    });
    createSimpleTextTool('http-status', 'HTTP Status', 'Dev', 'Lookup Code.', (text) => {
        const codes = {200:'OK', 201:'Created', 400:'Bad Request', 401:'Unauthorized', 403:'Forbidden', 404:'Not Found', 500:'Server Error', 502:'Bad Gateway'};
        return codes[text] || 'Unknown';
    });

    // Health
    createMathTool('body-fat', 'Body Fat (Navy)', 'Health', 'Est. Body Fat %.', [{key:'w', label:'Waist (cm)'}, {key:'n', label:'Neck (cm)'}, {key:'h', label:'Height (cm)'}], (v) => (495 / (1.0324 - 0.19077 * Math.log10(v.w - v.n) + 0.15456 * Math.log10(v.h)) - 450).toFixed(2) + '%');
    createMathTool('ideal-weight', 'Ideal Weight (Devine)', 'Health', 'Ideal Weight (kg).', [{key:'h', label:'Height (in)'}], (v) => (50 + 2.3 * (v.h - 60)).toFixed(2) + ' kg');

    // Finance
    createMathTool('rule-72', 'Rule of 72', 'Finance', 'Years to double inv.', [{key:'r', label:'Rate %'}], (v) => (72 / v.r).toFixed(2) + ' Years');
    createMathTool('vat-calc', 'VAT Calculator', 'Finance', 'Add VAT.', [{key:'p', label:'Price'}, {key:'v', label:'VAT %'}], (v) => (v.p * (1 + v.v/100)).toFixed(2));
    createMathTool('markup-calc', 'Markup Calculator', 'Finance', 'Price + Markup.', [{key:'c', label:'Cost'}, {key:'m', label:'Markup %'}], (v) => (v.c * (1 + v.m/100)).toFixed(2));
    createMathTool('margin-calc', 'Margin Calculator', 'Finance', 'Find Margin.', [{key:'c', label:'Cost'}, {key:'p', label:'Price'}], (v) => ((v.p - v.c) / v.p * 100).toFixed(2) + '%');

    // Science / Units
    function createConverter(id, name, cat, desc, unit1, unit2, factor) {
        createMathTool(id, name, cat, desc, [{key:'v', label:unit1}], (v) => (v.v * factor).toFixed(4) + ' ' + unit2);
        createMathTool(id + '-rev', name + ' (Rev)', cat, desc, [{key:'v', label:unit2}], (v) => (v.v / factor).toFixed(4) + ' ' + unit1);
    }

    createConverter('pres-bar-psi', 'Bar to PSI', 'Science', 'Pressure.', 'Bar', 'PSI', 14.5038);
    createConverter('ener-j-wh', 'Joules to Wh', 'Science', 'Energy.', 'Joules', 'Wh', 0.000277778);
    createConverter('force-n-lbf', 'Newton to lbf', 'Science', 'Force.', 'Newton', 'lbf', 0.224809);
    createConverter('angle-deg-grad', 'Deg to Grad', 'Science', 'Angle.', 'Deg', 'Grad', 1.11111);
    createConverter('data-tb-gb', 'TB to GB', 'Science', 'Data.', 'TB', 'GB', 1024);

    // Random
    createGeneratorTool('random-bool', 'True/False', 'Random', 'Random boolean.', 'Flip', () => Math.random() < 0.5 ? 'True' : 'False');
    createGeneratorTool('random-date', 'Random Date', 'Random', 'Past 50 years.', 'Generate', () => new Date(Date.now() - Math.random() * 1000000000000).toLocaleDateString());
    createGeneratorTool('random-time', 'Random Time', 'Random', '24h format.', 'Generate', () => Math.floor(Math.random()*24).toString().padStart(2,'0') + ':' + Math.floor(Math.random()*60).toString().padStart(2,'0'));
"""

# Re-add Batch 7 (Real Tools) because they might be missing from extracted or partial
batch7_real = r"""
    // --- Batch 7: Real Tools ---
    // Mortgage
    createMathTool('mortgage-calc', 'Mortgage Calculator', 'Finance', 'Monthly payment (est).',
        [{key:'p', label:'Loan Amount'}, {key:'r', label:'Annual Rate %'}, {key:'y', label:'Years'}],
        (v) => {
            const r = v.r / 100 / 12;
            const n = v.y * 12;
            return (v.p * r * Math.pow(1 + r, n) / (Math.pow(1 + r, n) - 1)).toFixed(2);
        });
    createMathTool('roi-calc', 'ROI Calculator', 'Finance', 'Return on Investment.', [{key:'inv', label:'Investment'}, {key:'ret', label:'Return Amount'}], (v) => (((v.ret - v.inv) / v.inv) * 100).toFixed(2) + '%');
    createMathTool('salary-calc', 'Salary Converter', 'Finance', 'Annual to Monthly/Hourly.', [{key:'annual', label:'Annual Salary'}], (v) => `Monthly: ${(v.annual/12).toFixed(2)}\nHourly (2080h): ${(v.annual/2080).toFixed(2)}`);
    createSimpleTextTool('xml-format', 'XML Formatter', 'Dev', 'Simple XML Indent.', (text) => { let formatted = '', indent= ''; text.split(/>\s*</).forEach(node => { if (node.match( /^\/\w/ )) indent = indent.substring(2); formatted += indent + '<' + node + '>\r\n'; if (node.match( /^<?\w[^>]*[^\/]$/ )) indent += '  '; }); return formatted.substring(1, formatted.length-3); });
    createSimpleTextTool('sql-minify', 'SQL Minifier', 'Dev', 'Remove whitespace from SQL.', (text) => text.replace(/\s+/g, ' ').trim());

    // Image
    function registerImageTool(id, name, desc, actionName, processFn) {
        registerTool(id, name, 'Image', description,
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>',
            (container) => {
                container.innerHTML = `
                    <div class="glass-panel" style="text-align: center;">
                        <input type="file" id="${id}-file" accept="image/*" style="display: none;">
                        <button id="${id}-upload" class="glass-btn" style="width: 100%; margin-bottom: 10px;">Upload Image</button>
                        <canvas id="${id}-canvas" style="max-width: 100%; max-height: 300px; display: none; border: 1px solid rgba(255,255,255,0.2);"></canvas>
                        <div id="${id}-controls" style="margin-top: 10px; display: none;">
                            <button id="${id}-process" class="glass-btn-primary">${actionName}</button>
                            <a id="${id}-download" class="glass-btn" style="margin-top: 5px; display: inline-flex; justify-content: center; text-decoration: none;">Download</a>
                        </div>
                    </div>
                `;
                const fileInput = document.getElementById(`${id}-file`);
                const uploadBtn = document.getElementById(`${id}-upload`);
                const canvas = document.getElementById(`${id}-canvas`);
                const ctx = canvas.getContext('2d');
                const controls = document.getElementById(`${id}-controls`);
                const processBtn = document.getElementById(`${id}-process`);
                const downloadLink = document.getElementById(`${id}-download`);
                let img = new Image();
                uploadBtn.addEventListener('click', () => fileInput.click());
                fileInput.addEventListener('change', (e) => {
                    const file = e.target.files[0];
                    if(file) {
                        const reader = new FileReader();
                        reader.onload = (event) => {
                            img.onload = () => {
                                canvas.width = img.width;
                                canvas.height = img.height;
                                ctx.drawImage(img, 0, 0);
                                canvas.style.display = 'block';
                                controls.style.display = 'block';
                            }
                            img.src = event.target.result;
                        }
                        reader.readAsDataURL(file);
                    }
                });
                processBtn.addEventListener('click', () => {
                    processFn(ctx, canvas.width, canvas.height);
                    downloadLink.href = canvas.toDataURL();
                    downloadLink.download = `${id}-result.png`;
                });
            }
        );
    }
    registerImageTool('img-grayscale', 'Grayscale Filter', 'Convert to B&W.', 'Apply Grayscale', (ctx, w, h) => { const imgData = ctx.getImageData(0, 0, w, h); const data = imgData.data; for (let i = 0; i < data.length; i += 4) { const avg = (data[i] + data[i + 1] + data[i + 2]) / 3; data[i] = avg; data[i + 1] = avg; data[i + 2] = avg; } ctx.putImageData(imgData, 0, 0); });
    registerImageTool('img-invert', 'Invert Colors', 'Invert colors.', 'Invert', (ctx, w, h) => { const imgData = ctx.getImageData(0, 0, w, h); const data = imgData.data; for (let i = 0; i < data.length; i += 4) { data[i] = 255 - data[i]; data[i + 1] = 255 - data[i + 1]; data[i + 2] = 255 - data[i + 2]; } ctx.putImageData(imgData, 0, 0); });

    // QR & IP & SHA were added in reconstruct_full.py already or need to be here?
    // They are in reconstruct_full.py hardcoded.
"""

# Boilerplate for Factory Functions
factory = r"""
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
                actionBtn.addEventListener('click', () => { try { output.value = transformFn(input.value); } catch (e) { output.value = "Error: " + e.message; } });
                copyBtn.addEventListener('click', () => { if(output.value) { navigator.clipboard.writeText(output.value); const original = copyBtn.textContent; copyBtn.textContent = 'Copied!'; setTimeout(() => copyBtn.textContent = original, 1000); } });
            }
        );
    }
    function createMathTool(id, name, category, description, inputs, calcFn) {
        registerTool(id, name, category, description,
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 21h10a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2z"/><line x1="9" y1="7" x2="15" y2="7"/><line x1="9" y1="11" x2="15" y2="11"/><line x1="9" y1="15" x2="15" y2="15"/></svg>',
            (container) => {
                let inputsHtml = '';
                inputs.forEach(inp => { inputsHtml += `<div class="input-group"><label>${inp.label}</label><input type="number" id="${id}-${inp.key}" class="glass-input" placeholder="${inp.placeholder || '0'}" step="any"></div>`; });
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
                    inputs.forEach(inp => { values[inp.key] = parseFloat(document.getElementById(`${id}-${inp.key}`).value) || 0; });
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
                document.getElementById(`${id}-action`).addEventListener('click', () => { resDiv.textContent = genFn(); });
                document.getElementById(`${id}-copy`).addEventListener('click', () => { navigator.clipboard.writeText(resDiv.textContent); });
            }
        );
    }
"""

logic = r"""
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
        setRandomTheme();
        document.title = 'Tooltimate - The Glassomorphic Web Utility Hub';
        history.pushState(null, null, ' ');
    }

    function showTool(toolId) {
        const tool = toolRegistry[toolId];
        if (tool) {
            dashboard.style.display = 'none';
            toolView.style.display = 'flex';
            if(categoryTabs) categoryTabs.style.display = 'none';
            toolTitle.textContent = tool.name;
            const catBadge = document.getElementById('tool-category-badge');
            if(catBadge) catBadge.textContent = tool.category || 'Tool';
            toolContent.innerHTML = '';
            tool.render(toolContent);
            document.title = tool.name + ' - Tooltimate';
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

    setRandomTheme();
    renderDashboard();

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

# Combine everything
# Structure: Header > Theme > Factory > Tools (Original + Batch 7 + Batch 8 + Batch 9 + Batch 10) > Logic
# Note: `tools_code` variable contains Batch 1-6 but lacks the new factories (Batch 7+ was manual).
# I will just concatenate all tool definitions I have.

full_script = r"""document.addEventListener('DOMContentLoaded', () => {
    const dashboard = document.getElementById('dashboard');
    const toolView = document.getElementById('tool-view');
    const toolTitle = document.getElementById('tool-title');
    const toolContent = document.getElementById('tool-content');
    const backBtn = document.getElementById('back-btn');
    const searchInput = document.getElementById('search-input');
    const categoryTabs = document.getElementById('category-tabs');
""" + theme_js + factory + tools_code + batch7_real + batch8 + batch9 + batch10 + logic

# Write to file
with open('quicktools/index.html', 'r') as f:
    content = f.read()

import re
start_tag = '<script>'
end_tag = '</script>'
start_idx = content.rfind(start_tag)
end_idx = content.find(end_tag, start_idx)

if start_idx != -1 and end_idx != -1:
    new_content = content[:start_idx + len(start_tag)] + "\n" + full_script + "\n" + content[end_idx:]
    with open('quicktools/index.html', 'w') as f:
        f.write(new_content)
else:
    print("Script tag not found")

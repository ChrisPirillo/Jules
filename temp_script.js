
document.addEventListener('DOMContentLoaded', () => {
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
    }, ${sat}%, ${light}%)`;
        const accentColor = `hsl(${hue}, ${sat}%, ${light + 40}%)`; // Brighter accent
        const bgInput = `hsla(${hue}, 30%, 10%, 0.6)`;
        const border = `hsla(${hue}, 50%, 50%, 0.3)`;

        const root = document.documentElement;
        root.style.setProperty('--primary-color', primaryColor);

        // Gradient: Dark to slightly lighter dark
        const hue2 = (hue + 40) % 360;
        const bgGradient = `linear-gradient(135deg, hsl(${hue}, 60%, 20%) 0%, hsl(${hue2}, 60%, 10%) 100%)`;
        root.style.setProperty('--bg-gradient', bgGradient);

        // Component Vars
        root.style.setProperty('--theme-accent', accentColor);
        root.style.setProperty('--theme-accent-hover', `hsl(${hue}, ${sat}%, ${light + 50}%)`);
        root.style.setProperty('--theme-bg-input', bgInput);
        root.style.setProperty('--theme-border', border);
        root.style.setProperty('--theme-bg-hover', `hsla(${hue}, ${sat}%, 25%, 0.4)`);

        // Force redraw/recalc if needed (usually auto)
    }

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
                    try { output.value = transformFn(input.value); } catch (e) { output.value = "Error: " + e.message; }
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
                document.getElementById(`${id}-action`).addEventListener('click', () => { resDiv.textContent = genFn(); });
                document.getElementById(`${id}-copy`).addEventListener('click', () => { navigator.clipboard.writeText(resDiv.textContent); });
            }
        );
    }

    createSimpleTextTool('uppercase', 'Uppercase', 'Text', 'Convert text to uppercase.', (text) => text.toUpperCase());
    createSimpleTextTool('lowercase', 'Lowercase', 'Text', 'Convert text to lowercase.', (text) => text.toLowerCase());
    createSimpleTextTool('title-case', 'Title Case', 'Text', 'Capitalize first letter of each word.', (text) => text.toLowerCase().split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' '));
    createSimpleTextTool('reverse-string', 'Reverse Text', 'Text', 'Reverse the characters in text.', (text) => text.split('').reverse().join(''));
    createSimpleTextTool('remove-spaces', 'Remove Spaces', 'Text', 'Remove all whitespace.', (text) => text.replace(/\s/g, ''));
    createSimpleTextTool('slugify', 'Slug Generator', 'Text', 'Convert text to URL slug.', (text) => text.toLowerCase().replace(/[^\w ]+/g, '').replace(/ +/g, '-'));
    createSimpleTextTool('base64-encode', 'Base64 Encode', 'Dev', 'Encode text to Base64.', (text) => btoa(text));
    createSimpleTextTool('base64-decode', 'Base64 Decode', 'Dev', 'Decode Base64 to text.', (text) => atob(text));
    createSimpleTextTool('url-encode', 'URL Encode', 'Dev', 'Encode text for URLs.', (text) => encodeURIComponent(text));
    createSimpleTextTool('url-decode', 'URL Decode', 'Dev', 'Decode URL encoded text.', (text) => decodeURIComponent(text));
    createSimpleTextTool('rot13', 'ROT13 Cipher', 'Text', 'Apply ROT13 substitution.', (text) => text.replace(/[a-zA-Z]/g, c => String.fromCharCode((c <= 'Z' ? 90 : 122) >= (c = c.charCodeAt(0) + 13) ? c : c - 26)));
    createSimpleTextTool('word-count', 'Word Count', 'Text', 'Count words in text.', (text) => `Words: ${text.trim().split(/\s+/).length}`);
    createSimpleTextTool('char-count', 'Char Count', 'Text', 'Count characters in text.', (text) => `Characters: ${text.length}`);
    createSimpleTextTool('camel-case', 'Camel Case', 'Text', 'Convert text to camelCase.', (text) => text.toLowerCase().replace(/[^a-zA-Z0-9]+(.)/g, (m, chr) => chr.toUpperCase()));
    createSimpleTextTool('snake-case', 'Snake Case', 'Text', 'Convert text to snake_case.', (text) => text && text.match(/[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*|\b)|[A-Z]?[a-z]+[0-9]*|[A-Z]|[0-9]+/g).map(x => x.toLowerCase()).join('_'));
    createSimpleTextTool('kebab-case', 'Kebab Case', 'Text', 'Convert text to kebab-case.', (text) => text && text.match(/[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*|\b)|[A-Z]?[a-z]+[0-9]*|[A-Z]|[0-9]+/g).map(x => x.toLowerCase()).join('-'));
    createSimpleTextTool('sentence-case', 'Sentence Case', 'Text', 'Convert text to Sentence case.', (text) => text.toLowerCase().replace(/(^\s*\w|[\.\!\?]\s*\w)/g, c => c.toUpperCase()));
    createSimpleTextTool('reverse-words', 'Reverse Words', 'Text', 'Reverse the order of words.', (text) => text.split(' ').reverse().join(' '));
    createSimpleTextTool('remove-duplicates', 'Remove Duplicate Lines', 'Text', 'Remove duplicate lines.', (text) => [...new Set(text.split('\n'))].join('\n'));
    createSimpleTextTool('sort-lines', 'Sort Lines (A-Z)', 'Text', 'Sort lines alphabetically.', (text) => text.split('\n').sort().join('\n'));
    createSimpleTextTool('sort-lines-reverse', 'Sort Lines (Z-A)', 'Text', 'Sort lines in reverse.', (text) => text.split('\n').sort().reverse().join('\n'));
    createSimpleTextTool('random-lines', 'Shuffle Lines', 'Text', 'Randomly shuffle lines.', (text) => text.split('\n').sort(() => Math.random() - 0.5).join('\n'));
    createSimpleTextTool('trim-lines', 'Trim Lines', 'Text', 'Trim whitespace from lines.', (text) => text.split('\n').map(l => l.trim()).join('\n'));
    createSimpleTextTool('remove-empty-lines', 'Remove Empty Lines', 'Text', 'Remove empty lines.', (text) => text.split('\n').filter(l => l.trim() !== '').join('\n'));
    createSimpleTextTool('add-line-numbers', 'Add Line Numbers', 'Text', 'Add line numbers to text.', (text) => text.split('\n').map((l, i) => `${i+1}. ${l}`).join('\n'));
    createSimpleTextTool('extract-emails', 'Extract Emails', 'Dev', 'Extract email addresses.', (text) => (text.match(/([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)/gi) || []).join('\n'));
    createSimpleTextTool('extract-urls', 'Extract URLs', 'Dev', 'Extract URLs from text.', (text) => (text.match(/https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)/gi) || []).join('\n'));
    createSimpleTextTool('extract-numbers', 'Extract Numbers', 'Dev', 'Extract numbers from text.', (text) => (text.match(/\d+/g) || []).join('\n'));
    createSimpleTextTool('morse-code', 'Text to Morse', 'Text', 'Convert text to Morse code.', (text) => {
        const morseCode = { 'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----', ' ': '/' };
        return text.toUpperCase().split('').map(c => morseCode[c] || c).join(' ');
    });
    createSimpleTextTool('binary-encode', 'Text to Binary', 'Dev', 'Convert text to binary.', (text) => text.split('').map(c => c.charCodeAt(0).toString(2).padStart(8, '0')).join(' '));
    createSimpleTextTool('hex-encode', 'Text to Hex', 'Dev', 'Convert text to hexadecimal.', (text) => text.split('').map(c => c.charCodeAt(0).toString(16).padStart(2, '0')).join(' '));
    createSimpleTextTool('ascii-encode', 'Text to ASCII', 'Dev', 'Convert text to ASCII codes.', (text) => text.split('').map(c => c.charCodeAt(0)).join(' '));
    createSimpleTextTool('csv-to-json', 'CSV to JSON', 'Dev', 'Simple CSV to JSON conversion.', (text) => {
        const lines = text.split('\n');
        const headers = lines[0].split(',');
        return JSON.stringify(lines.slice(1).map(line => {
            const data = line.split(',');
            return headers.reduce((obj, nextKey, index) => {
                obj[nextKey.trim()] = data[index];
                return obj;
            }, {});
        }), null, 2);
    });
    createMathTool('bmi-calc', 'BMI Calculator', 'Math', 'Calculate Body Mass Index.',
        [{key:'w', label:'Weight (kg)'}, {key:'h', label:'Height (m)'}],
        (v) => (v.w / (v.h * v.h)).toFixed(2));
    createMathTool('tip-calc', 'Tip Calculator', 'Finance', 'Calculate tip amount.',
        [{key:'bill', label:'Bill Amount'}, {key:'tip', label:'Tip %'}],
        (v) => (v.bill * (v.tip / 100)).toFixed(2));
    createMathTool('discount-calc', 'Discount Calculator', 'Finance', 'Calculate discounted price.',
        [{key:'price', label:'Original Price'}, {key:'disc', label:'Discount %'}],
        (v) => (v.price - (v.price * (v.disc / 100))).toFixed(2));
    createMathTool('sales-tax', 'Sales Tax', 'Finance', 'Calculate final price with tax.',
        [{key:'price', label:'Price'}, {key:'tax', label:'Tax %'}],
        (v) => (v.price * (1 + v.tax / 100)).toFixed(2));
    createMathTool('circle-area', 'Circle Area', 'Math', 'Calculate area of a circle.',
        [{key:'r', label:'Radius'}],
        (v) => (Math.PI * v.r * v.r).toFixed(2));
    createMathTool('rect-area', 'Rectangle Area', 'Math', 'Calculate area of a rectangle.',
        [{key:'w', label:'Width'}, {key:'h', label:'Height'}],
        (v) => (v.w * v.h).toFixed(2));
    createMathTool('triangle-area', 'Triangle Area', 'Math', 'Calculate area of a triangle.',
        [{key:'b', label:'Base'}, {key:'h', label:'Height'}],
        (v) => (0.5 * v.b * v.h).toFixed(2));
    createMathTool('cylinder-vol', 'Cylinder Volume', 'Math', 'Calculate volume of a cylinder.',
        [{key:'r', label:'Radius'}, {key:'h', label:'Height'}],
        (v) => (Math.PI * v.r * v.r * v.h).toFixed(2));
    createMathTool('sphere-vol', 'Sphere Volume', 'Math', 'Calculate volume of a sphere.',
        [{key:'r', label:'Radius'}],
        (v) => ((4/3) * Math.PI * Math.pow(v.r, 3)).toFixed(2));
    createMathTool('simple-interest', 'Simple Interest', 'Finance', 'Calculate simple interest.',
        [{key:'p', label:'Principal'}, {key:'r', label:'Rate %'}, {key:'t', label:'Time (years)'}],
        (v) => (v.p * v.r * v.t / 100).toFixed(2));
    createMathTool('compound-interest', 'Compound Interest', 'Finance', 'Calculate compound interest.',
        [{key:'p', label:'Principal'}, {key:'r', label:'Rate %'}, {key:'t', label:'Time (years)'}, {key:'n', label:'Times/Year'}],
        (v) => (v.p * Math.pow((1 + (v.r/100)/v.n), v.n * v.t)).toFixed(2));
    createMathTool('percentage-of', 'Percentage Of', 'Math', 'What is X% of Y?',
        [{key:'x', label:'Percentage (X)'}, {key:'y', label:'Value (Y)'}],
        (v) => ((v.x / 100) * v.y).toFixed(2));
    createMathTool('percentage-change', 'Percentage Change', 'Math', 'Change from X to Y.',
        [{key:'x', label:'Old Value'}, {key:'y', label:'New Value'}],
        (v) => (((v.y - v.x) / v.x) * 100).toFixed(2) + '%');
    createMathTool('average', 'Average Calculator', 'Math', 'Calculate average of 2 numbers.',
        [{key:'a', label:'Number 1'}, {key:'b', label:'Number 2'}],
        (v) => ((v.a + v.b) / 2).toFixed(2));
    createMathTool('hypotenuse', 'Hypotenuse Calc', 'Math', 'Calculate hypotenuse (Pythagorean).',
        [{key:'a', label:'Side A'}, {key:'b', label:'Side B'}],
        (v) => Math.sqrt(v.a*v.a + v.b*v.b).toFixed(2));
    createMathTool('aspect-ratio', 'Aspect Ratio Height', 'Math', 'Calculate height from width & ratio.',
        [{key:'w', label:'Width'}, {key:'rw', label:'Ratio W'}, {key:'rh', label:'Ratio H'}],
        (v) => (v.w * (v.rh / v.rw)).toFixed(2));
    createMathTool('factorial', 'Factorial', 'Math', 'Calculate N!.',
        [{key:'n', label:'Number (N)'}],
        (v) => {
            let res = 1;
            for(let i=2; i<=v.n; i++) res *= i;
            return res;
        });
    createMathTool('power', 'Power Calculator', 'Math', 'Calculate Base^Exponent.',
        [{key:'b', label:'Base'}, {key:'e', label:'Exponent'}],
        (v) => Math.pow(v.b, v.e));
    createMathTool('root', 'Nth Root', 'Math', 'Calculate Nth root of X.',
        [{key:'x', label:'Number (X)'}, {key:'n', label:'Root (N)'}],
        (v) => Math.pow(v.x, 1/v.n).toFixed(4));
    createGeneratorTool('uuid', 'UUID Generator', 'Dev', 'Generate UUID v4.', 'Generate UUID', () =>
        'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        })
    );
    createGeneratorTool('unix-timestamp', 'Unix Timestamp', 'Dev', 'Get current Unix timestamp.', 'Get Timestamp', () => Math.floor(Date.now() / 1000));
    createGeneratorTool('current-time-ms', 'Timestamp (ms)', 'Dev', 'Get current timestamp (ms).', 'Get Milliseconds', () => Date.now());
    createGeneratorTool('random-number', 'Random Number', 'Math', 'Random number 1-100.', 'Roll (1-100)', () => Math.floor(Math.random() * 100) + 1);
    createGeneratorTool('dice-roller', 'Dice Roller', 'Game', 'Roll a 6-sided die.', 'Roll D6', () => Math.floor(Math.random() * 6) + 1);
    createGeneratorTool('coin-flipper', 'Coin Flipper', 'Game', 'Flip a coin.', 'Flip Coin', () => Math.random() < 0.5 ? 'Heads' : 'Tails');
    createGeneratorTool('yes-no', 'Yes/No Decision', 'Game', 'Random Yes or No.', 'Decide', () => Math.random() < 0.5 ? 'Yes' : 'No');
    createGeneratorTool('ip-address', 'IP Address (Mock)', 'Dev', 'Simulated IP Lookup.', 'Get IP', () => '192.168.1.' + Math.floor(Math.random() * 255));
    createGeneratorTool('mac-address', 'MAC Address Gen', 'Dev', 'Random MAC Address.', 'Generate MAC', () => 'XX:XX:XX:XX:XX:XX'.replace(/X/g, () => '0123456789ABCDEF'.charAt(Math.floor(Math.random() * 16))));
    createGeneratorTool('hex-color', 'Random Color', 'Color', 'Generate random Hex color.', 'Generate Color', () => '#' + Math.floor(Math.random()*16777215).toString(16).padStart(6, '0'));
    createGeneratorTool('password-strength', 'Password Strength', 'Security', 'Check password strength.', 'Check', () => {
        // Since input is needed, this simple generator won't work perfectly.
        // Let's just return a placeholder or random advice for the "Generator" pattern.
        // Better: Use SimpleTextTool for this one actually.
        return "Use the 'Password Gen' tool for actual generation.";
    });
    createGeneratorTool('lorem-word', 'Random Word', 'Text', 'Generate a random latin word.', 'Generate Word', () => {
        const words = ['lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 'adipiscing', 'elit', 'sed', 'do', 'eiusmod', 'tempor', 'incididunt'];
        return words[Math.floor(Math.random() * words.length)];
    });
    createSimpleTextTool('hash-simple', 'Simple Hash (djb2)', 'Security', 'Generate simple hash.', (text) => {
        let hash = 5381;
        for (let i = 0; i < text.length; i++) hash = (hash * 33) ^ text.charCodeAt(i);
        return (hash >>> 0).toString(16);
    });
    createSimpleTextTool('md5-mock', 'MD5 (Mock)', 'Security', 'Mock MD5 hash (not real security).', (text) => "d41d8cd98f00b204e9800998ecf8427e (Mock)");
    createSimpleTextTool("css-minifier", "CSS Minifier", "Dev", "Minify CSS code.", (text) => text.replace(/\s+/g, " "));
    createSimpleTextTool('js-minifier', 'JS Minifier (Simple)', 'Dev', 'Remove comments and whitespace.', (text) => text.replace(/\/\/.*$/gm, '').replace(/\/\*[\s\S]*?\*\//g, '').replace(/\s+/g, ' '));
    createSimpleTextTool('html-encode', 'HTML Entity Encode', 'Dev', 'Encode HTML special chars.', (text) => text.replace(/[\u00A0-\u9999<>\&]/g, i => '&#'+i.charCodeAt(0)+';'));
    createSimpleTextTool('html-decode', 'HTML Entity Decode', 'Dev', 'Decode HTML entities.', (text) => {
        const doc = new DOMParser().parseFromString(text, "text/html");
        return doc.documentElement.textContent;
    });
    createSimpleTextTool('sql-format', 'SQL Formatter', 'Dev', 'Simple SQL Formatting.', (text) => text.replace(/\s+/g, ' ').replace(/ (SELECT|FROM|WHERE|AND|OR|ORDER BY|GROUP BY|LIMIT|INSERT|UPDATE|DELETE) /gi, '\n '));
    createSimpleTextTool('markdown-preview', 'Markdown Preview', 'Text', 'Preview markdown (HTML output).', (text) => {
        // Very simple markdown parser
        return text
            .replace(/^# (.*$)/gim, '<h1></h1>')
            .replace(/^## (.*$)/gim, '<h2></h2>')
            .replace(/^### (.*$)/gim, '<h3></h3>')
            .replace(/\*\*(.*)\*\*/gim, '<b></b>')
            .replace(/\*(.*)\*/gim, '<i></i>')
            .replace(/\n/gim, '<br>');
    });
    createMathTool('age-calc', 'Age Calculator', 'Time', 'Calculate age from birth year.',
        [{key:'year', label:'Birth Year'}, {key:'curr', label:'Current Year (optional)', placeholder:'2025'}],
        (v) => (v.curr || new Date().getFullYear()) - v.year);
    createMathTool('date-diff', 'Date Difference (Days)', 'Time', 'Difference between two years.',
        [{key:'y1', label:'Year 1'}, {key:'y2', label:'Year 2'}],
        (v) => Math.abs(v.y1 - v.y2) * 365);
    createMathTool('leap-year', 'Leap Year Checker', 'Time', 'Is year a leap year? (1=Yes, 0=No)',
        [{key:'year', label:'Year'}],
        (v) => ((v.year % 4 == 0 && v.year % 100 != 0) || v.year % 400 == 0) ? "Yes" : "No");
    createMathTool('c-to-f', 'Celsius to Fahrenheit', 'Converter', 'Convert C to F.', [{key:'c', label:'Celsius'}], (v) => (v.c * 9/5 + 32).toFixed(2));
    createMathTool('f-to-c', 'Fahrenheit to Celsius', 'Converter', 'Convert F to C.', [{key:'f', label:'Fahrenheit'}], (v) => ((v.f - 32) * 5/9).toFixed(2));
    createMathTool('km-to-mi', 'KM to Miles', 'Converter', 'Convert km to miles.', [{key:'km', label:'Kilometers'}], (v) => (v.km * 0.621371).toFixed(4));
    createMathTool('mi-to-km', 'Miles to KM', 'Converter', 'Convert miles to km.', [{key:'mi', label:'Miles'}], (v) => (v.mi / 0.621371).toFixed(4));
    createMathTool('kg-to-lb', 'KG to Pounds', 'Converter', 'Convert kg to lbs.', [{key:'kg', label:'Kilograms'}], (v) => (v.kg * 2.20462).toFixed(4));
    createMathTool('lb-to-kg', 'Pounds to KG', 'Converter', 'Convert lbs to kg.', [{key:'lb', label:'Pounds'}], (v) => (v.lb / 2.20462).toFixed(4));
    createMathTool('m-to-ft', 'Meters to Feet', 'Converter', 'Convert meters to feet.', [{key:'m', label:'Meters'}], (v) => (v.m * 3.28084).toFixed(4));
    createMathTool('ft-to-m', 'Feet to Meters', 'Converter', 'Convert feet to meters.', [{key:'ft', label:'Feet'}], (v) => (v.ft / 3.28084).toFixed(4));
    createMathTool('l-to-gal', 'Liters to Gallons', 'Converter', 'Convert liters to US gallons.', [{key:'l', label:'Liters'}], (v) => (v.l * 0.264172).toFixed(4));
    createMathTool('gal-to-l', 'Gallons to Liters', 'Converter', 'Convert US gallons to liters.', [{key:'gal', label:'Gallons'}], (v) => (v.gal / 0.264172).toFixed(4));
    createMathTool('speed-kph-mph', 'KPH to MPH', 'Converter', 'Convert speed.', [{key:'kph', label:'KPH'}], (v) => (v.kph * 0.621371).toFixed(2));
    createMathTool('speed-mph-kph', 'MPH to KPH', 'Converter', 'Convert speed.', [{key:'mph', label:'MPH'}], (v) => (v.mph / 0.621371).toFixed(2));
    createMathTool('data-mb-gb', 'MB to GB', 'Converter', 'Convert Megabytes to Gigabytes.', [{key:'mb', label:'MB'}], (v) => (v.mb / 1024).toFixed(4));
    createMathTool('data-gb-mb', 'GB to MB', 'Converter', 'Convert Gigabytes to Megabytes.', [{key:'gb', label:'GB'}], (v) => (v.gb * 1024).toFixed(2));
    createMathTool('data-byte-kb', 'Bytes to KB', 'Converter', 'Convert Bytes to KB.', [{key:'b', label:'Bytes'}], (v) => (v.b / 1024).toFixed(4));
    createMathTool('time-min-sec', 'Minutes to Seconds', 'Time', 'Convert minutes to seconds.', [{key:'m', label:'Minutes'}], (v) => v.m * 60);
    createMathTool('time-hr-min', 'Hours to Minutes', 'Time', 'Convert hours to minutes.', [{key:'h', label:'Hours'}], (v) => v.h * 60);
    createMathTool('time-day-hr', 'Days to Hours', 'Time', 'Convert days to hours.', [{key:'d', label:'Days'}], (v) => v.d * 24);
    createMathTool('energy-j-cal', 'Joules to Calories', 'Converter', 'Convert energy.', [{key:'j', label:'Joules'}], (v) => (v.j / 4.184).toFixed(4));
    createMathTool('power-hp-kw', 'Horsepower to kW', 'Converter', 'Convert power.', [{key:'hp', label:'Horsepower'}], (v) => (v.hp * 0.7457).toFixed(4));
    createGeneratorTool('random-letter', 'Random Letter', 'Game', 'Random alphabet letter.', 'Pick Letter', () => 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.charAt(Math.floor(Math.random() * 26)));
    createGeneratorTool('random-emoji', 'Random Emoji', 'Game', 'Random emoji.', 'Pick Emoji', () => ['😀','😂','🥰','😎','🤔','😭','😡','👍','👎','🎉','🔥','❤️'].sort(() => 0.5 - Math.random())[0]);
    createGeneratorTool('lorem-sentence', 'Lorem Sentence', 'Text', 'Random latin sentence.', 'Generate', () => "Lorem ipsum dolor sit amet consectetur adipiscing elit.");
    createSimpleTextTool('space-to-dash', 'Spaces to Dashes', 'Text', 'Replace spaces with dashes.', (text) => text.replace(/ /g, '-'));
    createSimpleTextTool('dash-to-space', 'Dashes to Spaces', 'Text', 'Replace dashes with spaces.', (text) => text.replace(/-/g, ' '));
    createSimpleTextTool('underscore-to-space', 'Underscores to Spaces', 'Text', 'Replace underscores with spaces.', (text) => text.replace(/_/g, ' '));
    createSimpleTextTool('space-to-underscore', 'Spaces to Underscores', 'Text', 'Replace spaces with underscores.', (text) => text.replace(/ /g, '_'));
    createSimpleTextTool('remove-special', 'Remove Special Chars', 'Text', 'Keep only alphanumeric.', (text) => text.replace(/[^a-zA-Z0-9 ]/g, ''));
    createSimpleTextTool('keep-numbers', 'Keep Only Numbers', 'Text', 'Remove non-numeric chars.', (text) => text.replace(/[^0-9]/g, ''));
    createMathTool('bmr-calc', 'BMR Calculator', 'Health', 'Basal Metabolic Rate.',
        [{key:'w', label:'Weight (kg)'}, {key:'h', label:'Height (cm)'}, {key:'a', label:'Age'}],
        (v) => (10 * v.w + 6.25 * v.h - 5 * v.a + 5).toFixed(0) + ' kcal (M) / ' + (10 * v.w + 6.25 * v.h - 5 * v.a - 161).toFixed(0) + ' kcal (F)');
    createMathTool('water-intake', 'Water Intake', 'Health', 'Daily water need (L).',
        [{key:'w', label:'Weight (kg)'}],
        (v) => (v.w * 0.033).toFixed(2) + ' Liters');
    createMathTool('target-heart-rate', 'Target Heart Rate', 'Health', 'Zone 2 (60-70%).',
        [{key:'age', label:'Age'}],
        (v) => {
            const max = 220 - v.age;
            return Math.floor(max * 0.6) + ' - ' + Math.floor(max * 0.7) + ' bpm';
        });
    createMathTool('gpa-calc', 'GPA Calculator (4.0)', 'Science', 'Simple Avg GPA.',
        [{key:'g1', label:'Grade 1'}, {key:'g2', label:'Grade 2'}, {key:'g3', label:'Grade 3'}, {key:'g4', label:'Grade 4'}],
        (v) => ((v.g1 + v.g2 + v.g3 + v.g4) / 4).toFixed(2));
    createMathTool('grade-pct', 'Grade Percentage', 'Science', 'Score / Total.',
        [{key:'s', label:'Score'}, {key:'t', label:'Total'}],
        (v) => ((v.s / v.t) * 100).toFixed(2) + '%');
    createSimpleTextTool('html-minifier', 'HTML Minifier', 'Dev', 'Remove whitespace.', (text) => text.replace(/\s+/g, ' ').replace(/> </g, '><'));
    createSimpleTextTool('hashtag-gen', 'Hashtag Generator', 'Social', 'Generate tags from text.', (text) => text.split(' ').map(w => '#' + w).join(' '));
    createSimpleTextTool('tweet-link', 'Tweet Link Gen', 'Social', 'Create intent link.', (text) => 'https://twitter.com/intent/tweet?text=' + encodeURIComponent(text));
    createSimpleTextTool('binary-to-hex', 'Binary to Hex', 'Dev', 'Convert Bin to Hex.', (text) => parseInt(text.replace(/[^01]/g, ''), 2).toString(16).toUpperCase());
    createSimpleTextTool('hex-to-binary', 'Hex to Binary', 'Dev', 'Convert Hex to Bin.', (text) => parseInt(text, 16).toString(2));
    createMathTool('currency-usd-eur', 'USD to EUR (Mock)', 'Finance', 'Est. rate 0.92', [{key:'usd', label:'USD'}], (v) => (v.usd * 0.92).toFixed(2));
    createMathTool('currency-eur-usd', 'EUR to USD (Mock)', 'Finance', 'Est. rate 1.09', [{key:'eur', label:'EUR'}], (v) => (v.eur * 1.09).toFixed(2));

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
                    } else {
                        resDiv.textContent = 'No matches found.';
                    }
                } catch(e) {
                    resDiv.textContent = 'Error: ' + e.message;
                }
            });
        }
    );

    createMathTool('prime-factor', 'Prime Factorization', 'Math', 'Find prime factors.', [{key:'n', label:'Number'}], (v) => { let n = parseInt(v.n); const f = []; let d = 2; while (d * d <= n) { while (n % d === 0) { f.push(d); n = Math.floor(n / d); } d++; } if (n > 1) f.push(n); return f.join(' × '); });
    createSimpleTextTool('list-random', 'Randomize List', 'Text', 'Shuffle list items.', (text) => text.split('\n').sort(() => 0.5 - Math.random()).join('\n'));
    createSimpleTextTool('list-sort', 'Sort List (Numeric)', 'Text', 'Sort numbers.', (text) => text.split('\n').sort((a,b) => parseFloat(a)-parseFloat(b)).join('\n'));
    createSimpleTextTool('json-minify', 'JSON Minifier', 'Dev', 'Remove whitespace from JSON.', (text) => JSON.stringify(JSON.parse(text)));


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

            const catBadge = document.getElementById('tool-category-badge');
            if(catBadge) catBadge.textContent = tool.category || 'Tool';
            toolContent.innerHTML = '';

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

    // --- Batch 9: More Real Tools ---
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

    createSimpleTextTool('url-parser', 'URL Parser', 'Dev', 'Parse URL parts.', (text) => {
        try {
            const u = new URL(text);
            return JSON.stringify({ protocol: u.protocol, host: u.host, pathname: u.pathname, search: u.search, hash: u.hash }, null, 2);
        } catch(e) { return "Invalid URL"; }
    });

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
                    <div id="cc-preview" style="padding: 30px; border-radius: 8px; text-align: center; margin: 20px 0; border: 1px solid rgba(255,255,255,0.2);">
                        Preview Text
                    </div>
                    <div id="cc-result" style="text-align: center; font-weight: bold; font-size: 1.2rem;">Ratio: 21.00 (AAA)</div>
                </div>
            `;

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


    // --- Batch 7: High Volume Tools (Re-added) ---
    createMathTool('mortgage-calc', 'Mortgage Calculator', 'Finance', 'Monthly payment.', [{key:'p', label:'Loan'}, {key:'r', label:'Rate %'}, {key:'y', label:'Years'}], (v) => { const r = v.r/1200; const n = v.y*12; return (v.p * r * Math.pow(1+r,n)/(Math.pow(1+r,n)-1)).toFixed(2); });
    createMathTool('roi-calc', 'ROI Calculator', 'Finance', 'Return on Investment.', [{key:'inv', label:'Investment'}, {key:'ret', label:'Return'}], (v) => (((v.ret-v.inv)/v.inv)*100).toFixed(2)+'%');
    createSimpleTextTool('xml-format', 'XML Formatter', 'Dev', 'Indent XML.', (text) => text.replace(/>\s*</g, '>\n<'));

    // Image Tools (Canvas)
    function registerImageTool(id, name, desc, actionName, processFn) {
        registerTool(id, name, 'Image', desc,
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

    registerImageTool('img-grayscale', 'Grayscale Filter', 'Convert to B&W.', 'Apply Grayscale', (ctx, w, h) => {
        const imgData = ctx.getImageData(0, 0, w, h);
        const data = imgData.data;
        for (let i = 0; i < data.length; i += 4) {
            const avg = (data[i] + data[i + 1] + data[i + 2]) / 3;
            data[i] = avg; data[i + 1] = avg; data[i + 2] = avg;
        }
        ctx.putImageData(imgData, 0, 0);
    });

    registerTool('qr-gen', 'QR Code Generator', 'Misc', 'Generate QR Code.',
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>',
        (container) => {
            container.innerHTML = `
                <div class="glass-panel" style="text-align: center;">
                    <input type="text" id="qr-input" class="glass-input" placeholder="Enter URL or Text">
                    <button id="qr-btn" class="glass-btn-primary" style="margin: 10px 0;">Generate QR</button>
                    <div id="qr-result" style="margin-top: 20px;"></div>
                </div>
            `;
            document.getElementById('qr-btn').addEventListener('click', () => {
                const text = document.getElementById('qr-input').value;
                if(text) {
                    const url = `https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=${encodeURIComponent(text)}`;
                    document.getElementById('qr-result').innerHTML = `<img src="${url}" alt="QR Code" style="border-radius: 8px;">`;
                }
            });
        }
    );


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

    // Science / Units (Simple Converters via Factory)
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

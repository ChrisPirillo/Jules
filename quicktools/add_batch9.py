import re

with open('quicktools/index.html', 'r') as f:
    content = f.read()

batch9 = r"""
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
                    <div id="cc-preview" style="padding: 20px; border-radius: 8px; text-align: center; margin: 20px 0; border: 1px solid rgba(255,255,255,0.2);">
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
"""

# Replace only the FIRST occurrence of renderDashboard(); to avoid nested duplication loops
if "Contrast Checker" not in content:
    content = content.replace("renderDashboard();", batch9 + "\n    renderDashboard();", 1)

with open('quicktools/index.html', 'w') as f:
    f.write(content)

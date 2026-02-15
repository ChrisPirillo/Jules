import re

with open('quicktools/index.html', 'r') as f:
    content = f.read()

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

"""

content = content.replace("renderDashboard();", batch10 + "\n    renderDashboard();", 1)

with open('quicktools/index.html', 'w') as f:
    f.write(content)

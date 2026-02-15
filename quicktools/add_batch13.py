import re

with open('quicktools/index.html', 'r') as f:
    content = f.read()

batch13 = r"""
    // --- Batch 13: Goal 250+ (Finance, Health, Science, Dev) ---
    // Finance
    createMathTool('loan-afford', 'Loan Affordability', 'Finance', 'How much can I borrow?', [{key:'inc', label:'Monthly Income'}, {key:'exp', label:'Monthly Debt'}, {key:'r', label:'Rate %'}, {key:'y', label:'Years'}], (v) => {
        const r = v.r/1200; const n = v.y*12; const maxPay = (v.inc - v.exp) * 0.36; // 36% rule
        return (maxPay * (Math.pow(1+r,n)-1) / (r * Math.pow(1+r,n))).toFixed(2);
    });
    createMathTool('cd-calc', 'CD Calculator', 'Finance', 'Certificate of Deposit.', [{key:'p', label:'Deposit'}, {key:'r', label:'Rate %'}, {key:'y', label:'Years'}], (v) => (v.p * Math.pow(1+v.r/100, v.y)).toFixed(2));
    createMathTool('net-worth', 'Net Worth', 'Finance', 'Assets - Liabilities.', [{key:'a', label:'Assets'}, {key:'l', label:'Liabilities'}], (v) => (v.a - v.l).toFixed(2));
    createMathTool('debt-ratio', 'Debt-to-Income', 'Finance', 'Debt / Income.', [{key:'d', label:'Monthly Debt'}, {key:'i', label:'Monthly Income'}], (v) => ((v.d/v.i)*100).toFixed(2) + '%');
    createMathTool('expense-ratio', 'Expense Ratio', 'Finance', 'Cost of fund.', [{key:'c', label:'Cost'}, {key:'inv', label:'Investment'}], (v) => ((v.c/v.inv)*100).toFixed(2) + '%');

    // Health
    createMathTool('bmi-prime', 'BMI Prime', 'Health', 'Ratio to upper limit (25).', [{key:'bmi', label:'BMI'}], (v) => (v.bmi / 25).toFixed(2));
    createMathTool('lean-body-mass', 'Lean Body Mass (Boer)', 'Health', 'LBM Estimate.', [{key:'w', label:'Weight (kg)'}, {key:'h', label:'Height (cm)'}, {key:'g', label:'Gender (1=M, 0=F)'}], (v) => v.g==1 ? (0.407*v.w + 0.267*v.h - 19.2).toFixed(1) : (0.252*v.w + 0.473*v.h - 48.3).toFixed(1));
    createMathTool('water-hardness', 'Water Hardness', 'Health', 'ppm to GPG.', [{key:'ppm', label:'ppm'}], (v) => (v.ppm / 17.1).toFixed(2) + ' gpg');
    createMathTool('sleep-cycle', 'Sleep Cycle Wake', 'Health', 'Wake times (90m cycles).', [{key:'h', label:'Sleep Hour (24)'}, {key:'m', label:'Sleep Min'}], (v) => {
        const d = new Date(); d.setHours(v.h); d.setMinutes(v.m);
        let res = ''; for(let i=3; i<=6; i++) { d.setMinutes(d.getMinutes()+90); res += d.toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'}) + ' '; }
        return res;
    });

    // Science
    createMathTool('sound-speed', 'Speed of Sound', 'Science', 'In air at T (°C).', [{key:'t', label:'Temp °C'}], (v) => (331.3 + 0.606 * v.t).toFixed(2) + ' m/s');
    createMathTool('mach-num', 'Mach Number', 'Science', 'Velocity / Sound Speed.', [{key:'v', label:'Velocity'}, {key:'c', label:'Speed of Sound'}], (v) => (v.v / v.c).toFixed(2));
    createMathTool('ohms-law-v', 'Ohm\'s Law (V)', 'Science', 'V = I * R', [{key:'i', label:'Current (I)'}, {key:'r', label:'Resistance (R)'}], (v) => (v.i * v.r).toFixed(2) + ' V');
    createMathTool('ohms-law-i', 'Ohm\'s Law (I)', 'Science', 'I = V / R', [{key:'v', label:'Voltage (V)'}, {key:'r', label:'Resistance (R)'}], (v) => (v.v / v.r).toFixed(2) + ' A');
    createMathTool('ohms-law-r', 'Ohm\'s Law (R)', 'Science', 'R = V / I', [{key:'v', label:'Voltage (V)'}, {key:'i', label:'Current (I)'}], (v) => (v.v / v.i).toFixed(2) + ' Ω');
    createMathTool('cap-energy', 'Capacitor Energy', 'Science', '0.5 * C * V^2', [{key:'c', label:'Capacitance (F)'}, {key:'v', label:'Voltage (V)'}], (v) => (0.5 * v.c * v.v * v.v).toFixed(4) + ' J');
    createMathTool('res-parallel', 'Parallel Resistors', 'Science', 'R1 || R2', [{key:'r1', label:'R1'}, {key:'r2', label:'R2'}], (v) => ((v.r1*v.r2)/(v.r1+v.r2)).toFixed(2) + ' Ω');

    // Color
    createSimpleTextTool('color-shade', 'Lighten/Darken Hex', 'Color', 'Adjust brightness (e.g. #336699 20).', (text) => {
        const [hex, percent] = text.split(' ');
        const num = parseInt(hex.replace('#',''), 16), amt = Math.round(2.55 * parseInt(percent));
        const R = (num >> 16) + amt, G = (num >> 8 & 0x00FF) + amt, B = (num & 0x0000FF) + amt;
        return '#' + (0x1000000 + (R<255?R<1?0:R:255)*0x10000 + (G<255?G<1?0:G:255)*0x100 + (B<255?B<1?0:B:255)).toString(16).slice(1);
    });
    createSimpleTextTool('color-blend', 'Blend Two Colors', 'Color', 'Average RGB.', (text) => {
        const [c1, c2] = text.split(' ');
        const n1 = parseInt(c1.replace('#',''), 16), n2 = parseInt(c2.replace('#',''), 16);
        const r = Math.round(((n1>>16) + (n2>>16))/2);
        const g = Math.round(((n1>>8&0xFF) + (n2>>8&0xFF))/2);
        const b = Math.round(((n1&0xFF) + (n2&0xFF))/2);
        return '#' + (0x1000000 + r*0x10000 + g*0x100 + b).toString(16).slice(1);
    });

    // Text
    createSimpleTextTool('text-cleaner', 'Text Cleaner', 'Text', 'Remove non-ASCII.', (text) => text.replace(/[^\x00-\x7F]/g, ''));
    createSimpleTextTool('random-pass', 'Random Password', 'Security', 'Strong random string.', (text) => Array(16).fill(0).map(()=>'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*'.charAt(Math.floor(Math.random()*70))).join(''));
    createSimpleTextTool('string-stats', 'String Stats', 'Text', 'Entropy & details.', (text) => `Length: ${text.length}\nUnique Chars: ${new Set(text).size}\nDigits: ${(text.match(/\d/g)||[]).length}\nAlpha: ${(text.match(/[a-z]/gi)||[]).length}`);

    // Dev
    createSimpleTextTool('cron-gen', 'Cron Generator', 'Dev', 'Mock UI (Simple).', (text) => {
        // Simple parser
        if(text === 'daily') return '0 0 * * *';
        if(text === 'weekly') return '0 0 * * 0';
        return 'Enter "daily" or "weekly"';
    });
    createSimpleTextTool('sql-format-v2', 'SQL Formatter (Adv)', 'Dev', 'Better regex.', (text) => text.replace(/\b(SELECT|FROM|WHERE|AND|OR|ORDER BY|GROUP BY|LIMIT|INSERT|UPDATE|DELETE|JOIN|LEFT JOIN|RIGHT JOIN|INNER JOIN)\b/gi, '\n$1'));
"""

content = content.replace("renderDashboard();", batch13 + "\n    renderDashboard();", 1)

with open('quicktools/index.html', 'w') as f:
    f.write(content)

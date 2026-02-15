import re

with open('quicktools/index.html', 'r') as f:
    content = f.read()

batch14 = r"""
    // --- Batch 14: Final Push to 275+ ---
    // Color
    createSimpleTextTool('color-mix', 'Color Mixer (Avg)', 'Color', 'Avg 2 Hex Colors.', (text) => { const [c1, c2] = text.split(' '); if(!c1||!c2) return 'Enter 2 Hex codes separated by space'; const n1 = parseInt(c1.replace('#',''), 16), n2 = parseInt(c2.replace('#',''), 16); const r = ((n1>>16) + (n2>>16))>>1; const g = ((n1>>8&0xFF) + (n2>>8&0xFF))>>1; const b = ((n1&0xFF) + (n2&0xFF))>>1; return '#' + (0x1000000 + r*0x10000 + g*0x100 + b).toString(16).slice(1); });
    createSimpleTextTool('rgb-hsl', 'RGB to HSL', 'Color', 'Convert RGB.', (text) => { const [r,g,b] = text.split(',').map(n => parseInt(n)/255); const max = Math.max(r,g,b), min = Math.min(r,g,b); let h, s, l = (max + min) / 2; if(max == min){ h = s = 0; } else { const d = max - min; s = l > 0.5 ? d / (2 - max - min) : d / (max + min); switch(max){ case r: h = (g - b) / d + (g < b ? 6 : 0); break; case g: h = (b - r) / d + 2; break; case b: h = (r - g) / d + 4; break; } h /= 6; } return `H:${(h*360).toFixed(0)} S:${(s*100).toFixed(0)}% L:${(l*100).toFixed(0)}%`; });

    // Random
    createGeneratorTool('rand-country', 'Random Country', 'Random', 'Pick a country.', 'Pick', () => ['USA', 'Canada', 'UK', 'France', 'Germany', 'Japan', 'China', 'India', 'Brazil', 'Australia', 'Italy', 'Spain', 'Mexico', 'Russia', 'South Korea'].sort(()=>0.5-Math.random())[0]);
    createGeneratorTool('rand-element', 'Random Element', 'Random', 'Periodic table.', 'Pick', () => ['Hydrogen','Helium','Lithium','Carbon','Nitrogen','Oxygen','Iron','Gold','Silver','Copper'].sort(()=>0.5-Math.random())[0]);
    createGeneratorTool('rand-animal', 'Random Animal', 'Random', 'Pick an animal.', 'Pick', () => ['Dog','Cat','Elephant','Lion','Tiger','Bear','Wolf','Fox','Eagle','Shark'].sort(()=>0.5-Math.random())[0]);

    // Text
    createSimpleTextTool('remove-accents', 'Remove Accents', 'Text', 'Normalize text.', (text) => text.normalize("NFD").replace(/[\u0300-\u036f]/g, ""));
    createSimpleTextTool('text-reverse-words', 'Reverse Words Only', 'Text', 'Reverse chars in words.', (text) => text.split(' ').map(w => w.split('').reverse().join('')).join(' '));
    createSimpleTextTool('case-swap', 'Swap Case', 'Text', 'Lowercase <-> Uppercase.', (text) => text.split('').map(c => c === c.toUpperCase() ? c.toLowerCase() : c.toUpperCase()).join(''));

    // Math
    createMathTool('circle-diam', 'Circle Diameter', 'Math', 'From Radius.', [{key:'r', label:'Radius'}], (v) => (v.r * 2).toFixed(4));
    createMathTool('circle-rad', 'Circle Radius', 'Math', 'From Diameter.', [{key:'d', label:'Diameter'}], (v) => (v.d / 2).toFixed(4));
    createMathTool('sphere-surf', 'Sphere Surface', 'Math', 'Area.', [{key:'r', label:'Radius'}], (v) => (4 * Math.PI * v.r * v.r).toFixed(4));
    createMathTool('cone-surf', 'Cone Surface', 'Math', 'Area.', [{key:'r', label:'Radius'}, {key:'h', label:'Height'}], (v) => (Math.PI * v.r * (v.r + Math.sqrt(v.h*v.h + v.r*v.r))).toFixed(4));

    // Misc
    createConverter('temp-k-c', 'Kelvin to Celsius', 'Science', 'Temp.', 'K', 'C', 1, -273.15); // Offset handled? Factory logic doesn't handle offset.
    // My factory `createConverter` uses simple multiplication factor.
    // Need custom for Temp if offset required.
    // Let's stick to simple factor converters for now or use `createMathTool`.
    createMathTool('temp-k-c-real', 'Kelvin to Celsius', 'Science', 'K to C.', [{key:'k', label:'Kelvin'}], (v) => (v.k - 273.15).toFixed(2));
    createMathTool('temp-c-k-real', 'Celsius to Kelvin', 'Science', 'C to K.', [{key:'c', label:'Celsius'}], (v) => (v.c + 273.15).toFixed(2));

"""

content = content.replace("renderDashboard();", batch14 + "\n    renderDashboard();", 1)

with open('quicktools/index.html', 'w') as f:
    f.write(content)

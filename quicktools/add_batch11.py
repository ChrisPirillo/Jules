import re

with open('quicktools/index.html', 'r') as f:
    content = f.read()

batch11 = r"""
    // --- Batch 11: Final Push to 200 ---
    // More Converters
    createConverter('area-sqm-sqft', 'Sq Meters to Sq Feet', 'Science', 'Area.', 'm²', 'ft²', 10.7639);
    createConverter('area-sqkm-sqmi', 'Sq KM to Sq Miles', 'Science', 'Area.', 'km²', 'mi²', 0.386102);
    createConverter('vol-l-ml', 'Liters to ML', 'Science', 'Volume.', 'L', 'mL', 1000);
    createConverter('vol-gal-qt', 'Gallons to Quarts', 'Science', 'Volume.', 'Gal', 'Qt', 4);
    createConverter('vol-qt-pt', 'Quarts to Pints', 'Science', 'Volume.', 'Qt', 'Pt', 2);
    createConverter('vol-pt-cup', 'Pints to Cups', 'Science', 'Volume.', 'Pt', 'Cup', 2);
    createConverter('len-cm-in', 'CM to Inches', 'Science', 'Length.', 'cm', 'in', 0.393701);
    createConverter('len-mm-in', 'MM to Inches', 'Science', 'Length.', 'mm', 'in', 0.0393701);
    createConverter('len-yd-m', 'Yards to Meters', 'Science', 'Length.', 'yd', 'm', 0.9144);
    createConverter('mass-oz-g', 'Ounces to Grams', 'Science', 'Mass.', 'oz', 'g', 28.3495);
    createConverter('mass-t-kg', 'Tons to KG', 'Science', 'Mass.', 't', 'kg', 1000);
    createConverter('time-wk-d', 'Weeks to Days', 'Time', 'Time.', 'Wk', 'Day', 7);
    createConverter('time-yr-d', 'Years to Days', 'Time', 'Time.', 'Yr', 'Day', 365.25);
    createConverter('time-dec-yr', 'Decades to Years', 'Time', 'Time.', 'Dec', 'Yr', 10);
    createConverter('data-kb-b', 'KB to Bytes', 'Dev', 'Data.', 'KB', 'B', 1024);
    createConverter('data-pb-tb', 'PB to TB', 'Dev', 'Data.', 'PB', 'TB', 1024);

    // Simple Math
    createMathTool('circle-circum', 'Circle Circumference', 'Math', '2*pi*r', [{key:'r', label:'Radius'}], (v) => (2 * Math.PI * v.r).toFixed(2));
    createMathTool('sphere-area', 'Sphere Area', 'Math', '4*pi*r^2', [{key:'r', label:'Radius'}], (v) => (4 * Math.PI * v.r * v.r).toFixed(2));
    createMathTool('cone-vol', 'Cone Volume', 'Math', 'Volume.', [{key:'r', label:'Radius'}, {key:'h', label:'Height'}], (v) => (Math.PI * v.r * v.r * v.h / 3).toFixed(2));
    createMathTool('box-vol', 'Box Volume', 'Math', 'L*W*H', [{key:'l', label:'L'}, {key:'w', label:'W'}, {key:'h', label:'H'}], (v) => (v.l*v.w*v.h).toFixed(2));
    createMathTool('mod', 'Modulo Calculator', 'Math', 'A % B', [{key:'a', label:'A'}, {key:'b', label:'B'}], (v) => v.a % v.b);

    // Misc
    createSimpleTextTool('reverse-lines', 'Reverse Lines', 'Text', 'Flip line order.', (text) => text.split('\n').reverse().join('\n'));
    createSimpleTextTool('sort-length', 'Sort by Length', 'Text', 'Sort lines by length.', (text) => text.split('\n').sort((a,b) => a.length - b.length).join('\n'));
    createGeneratorTool('random-digit', 'Random Digit', 'Random', '0-9', 'Pick', () => Math.floor(Math.random()*10));
    createGeneratorTool('random-char', 'Random Char', 'Random', 'A-Z, 0-9', 'Pick', () => 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'.charAt(Math.floor(Math.random()*36)));
"""

content = content.replace("renderDashboard();", batch11 + "\n    renderDashboard();", 1)

with open('quicktools/index.html', 'w') as f:
    f.write(content)

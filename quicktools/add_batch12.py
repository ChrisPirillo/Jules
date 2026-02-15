import re

with open('quicktools/index.html', 'r') as f:
    content = f.read()

batch12 = r"""
    // --- Batch 12: Goal 250 (Health, Science, Finance, Color) ---

    // Health (Anemic)
    createMathTool('preg-due', 'Pregnancy Due Date', 'Health', 'Based on LMP.', [{key:'d', label:'Day'}, {key:'m', label:'Month'}, {key:'y', label:'Year'}], (v) => { const d = new Date(v.y, v.m-1, v.d); d.setDate(d.getDate() + 280); return d.toLocaleDateString(); });
    createMathTool('ovul-calc', 'Ovulation Calculator', 'Health', 'Next fertile window.', [{key:'d', label:'LMP Day'}, {key:'m', label:'LMP Month'}, {key:'y', label:'LMP Year'}, {key:'c', label:'Cycle Days'}], (v) => { const d = new Date(v.y, v.m-1, v.d); d.setDate(d.getDate() + (v.c || 28) - 14); return d.toLocaleDateString(); });
    createMathTool('cal-burned', 'Calories Burned', 'Health', 'Estimate by MET.', [{key:'w', label:'Weight (kg)'}, {key:'t', label:'Time (min)'}, {key:'met', label:'MET Value'}], (v) => (v.met * 3.5 * v.w / 200 * v.t).toFixed(0) + ' kcal');
    createMathTool('one-rep-max', 'One Rep Max', 'Health', 'Epley Formula.', [{key:'w', label:'Weight'}, {key:'r', label:'Reps'}], (v) => (v.w * (1 + v.r/30)).toFixed(1));
    createMathTool('protein-intake', 'Protein Intake', 'Health', 'Daily need (1.6g/kg).', [{key:'w', label:'Weight (kg)'}], (v) => (v.w * 1.6).toFixed(1) + ' g');
    createMathTool('tdee-calc', 'TDEE Calculator', 'Health', 'Daily Energy Expenditure.', [{key:'bmr', label:'BMR'}, {key:'act', label:'Activity Level (1.2-1.9)'}], (v) => (v.bmr * v.act).toFixed(0) + ' kcal');
    createMathTool('bac-est', 'BAC Estimate', 'Health', 'Widmark Formula.', [{key:'alc', label:'Alcohol (g)'}, {key:'w', label:'Weight (kg)'}, {key:'r', label:'r (0.7 M, 0.6 F)'}, {key:'t', label:'Hours'}], (v) => ((v.alc / (v.w * v.r)) * 100 - (0.015 * v.t)).toFixed(3) + '%');

    // Science (Anemic)
    createMathTool('molar-mass', 'Molar Mass (Approx)', 'Science', 'Sum of parts.', [{key:'n', label:'Num Atoms'}, {key:'w', label:'Atomic Weight'}], (v) => (v.n * v.w).toFixed(4) + ' g/mol');
    createMathTool('density-calc', 'Density Calculator', 'Science', 'Mass/Volume.', [{key:'m', label:'Mass'}, {key:'v', label:'Volume'}], (v) => (v.m / v.v).toFixed(4));
    createMathTool('velocity-calc', 'Velocity Calculator', 'Science', 'Dist/Time.', [{key:'d', label:'Distance'}, {key:'t', label:'Time'}], (v) => (v.d / v.t).toFixed(4));
    createMathTool('accel-calc', 'Acceleration Calc', 'Science', 'Delta V / Time.', [{key:'v', label:'Change in Vel'}, {key:'t', label:'Time'}], (v) => (v.v / v.t).toFixed(4));
    createMathTool('momentum-calc', 'Momentum Calculator', 'Science', 'Mass * Vel.', [{key:'m', label:'Mass'}, {key:'v', label:'Velocity'}], (v) => (v.m * v.v).toFixed(4));
    createMathTool('kin-energy', 'Kinetic Energy', 'Science', '0.5 * m * v^2', [{key:'m', label:'Mass'}, {key:'v', label:'Velocity'}], (v) => (0.5 * v.m * v.v * v.v).toFixed(4) + ' J');
    createMathTool('pot-energy', 'Potential Energy', 'Science', 'm * g * h', [{key:'m', label:'Mass'}, {key:'h', label:'Height'}], (v) => (v.m * 9.8 * v.h).toFixed(4) + ' J');
    createMathTool('torque-calc', 'Torque Calculator', 'Science', 'Force * Radius.', [{key:'f', label:'Force'}, {key:'r', label:'Radius'}], (v) => (v.f * v.r).toFixed(4) + ' Nm');
    createMathTool('power-phys', 'Power (Physics)', 'Science', 'Work / Time.', [{key:'w', label:'Work'}, {key:'t', label:'Time'}], (v) => (v.w / v.t).toFixed(4) + ' W');
    createSimpleTextTool('element-lookup', 'Element Lookup', 'Science', 'Get symbol.', (text) => { const e = {Hydrogen:'H',Helium:'He',Lithium:'Li',Carbon:'C',Nitrogen:'N',Oxygen:'O',Sodium:'Na',Magnesium:'Mg'}; return e[text] || 'Unknown (Mock DB)'; });

    // Finance (Anemic)
    createMathTool('inflation-calc', 'Inflation (Est)', 'Finance', 'Future Value.', [{key:'p', label:'Amount'}, {key:'r', label:'Rate %'}, {key:'y', label:'Years'}], (v) => (v.p * Math.pow(1+v.r/100, v.y)).toFixed(2));
    createMathTool('savings-goal', 'Savings Goal', 'Finance', 'Monthly needed.', [{key:'g', label:'Goal'}, {key:'c', label:'Current'}, {key:'m', label:'Months'}], (v) => ((v.g - v.c) / v.m).toFixed(2));
    createMathTool('rule-50-30-20', '50/30/20 Rule', 'Finance', 'Budget Split.', [{key:'inc', label:'Income'}], (v) => `Needs: ${(v.inc*0.5).toFixed(2)}\nWants: ${(v.inc*0.3).toFixed(2)}\nSave: ${(v.inc*0.2).toFixed(2)}`);
    createMathTool('cagr-calc', 'CAGR Calculator', 'Finance', 'Growth Rate.', [{key:'ev', label:'End Val'}, {key:'bv', label:'Begin Val'}, {key:'n', label:'Years'}], (v) => ((Math.pow(v.ev/v.bv, 1/v.n) - 1) * 100).toFixed(2) + '%');
    createMathTool('breakeven', 'Break Even Point', 'Finance', 'Units to sell.', [{key:'fc', label:'Fixed Cost'}, {key:'p', label:'Price'}, {key:'vc', label:'Var Cost'}], (v) => (v.fc / (v.p - v.vc)).toFixed(0));

    // Color
    createSimpleTextTool('rgb-cmyk', 'RGB to CMYK', 'Color', 'Convert RGB.', (text) => { const [r,g,b] = text.split(',').map(Number); const k = 1-Math.max(r/255,g/255,b/255); return `C:${((1-r/255-k)/(1-k)).toFixed(2)} M:${((1-g/255-k)/(1-k)).toFixed(2)} Y:${((1-b/255-k)/(1-k)).toFixed(2)} K:${k.toFixed(2)}`; });
    createSimpleTextTool('hex-rgb', 'Hex to RGB', 'Color', 'Convert Hex.', (text) => { const r=parseInt(text.substr(1,2),16), g=parseInt(text.substr(3,2),16), b=parseInt(text.substr(5,2),16); return `${r},${g},${b}`; });

    // Dev
    createSimpleTextTool('unix-date', 'Unix to Date', 'Dev', 'Timestamp to ISO.', (text) => new Date(text*1000).toISOString());
    createSimpleTextTool('date-unix', 'Date to Unix', 'Dev', 'ISO to Timestamp.', (text) => Math.floor(new Date(text).getTime()/1000));
    createSimpleTextTool('url-encode-batch', 'Batch URL Encode', 'Dev', 'Line by line.', (text) => text.split('\n').map(encodeURIComponent).join('\n'));
    createSimpleTextTool('jwt-decode', 'JWT Decode', 'Dev', 'Decode payload.', (text) => { try { return atob(text.split('.')[1]); } catch(e) { return "Invalid JWT"; } });
    createSimpleTextTool('json-xml', 'JSON to XML', 'Dev', 'Simple converter.', (text) => { const o = JSON.parse(text); return Object.keys(o).map(k => `<${k}>${o[k]}</${k}>`).join('\n'); });

"""

content = content.replace("renderDashboard();", batch12 + "\n    renderDashboard();", 1)

with open('quicktools/index.html', 'w') as f:
    f.write(content)

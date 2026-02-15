import re

with open('quicktools/index.html', 'r') as f:
    content = f.read()

# Batch 7 Tools definition
batch7 = r"""
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
"""

# Insert before "renderDashboard();"
content = content.replace("renderDashboard();", batch7 + "\n    renderDashboard();", 1)

with open('quicktools/index.html', 'w') as f:
    f.write(content)

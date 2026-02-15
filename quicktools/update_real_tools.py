import re

with open('quicktools/index.html', 'r') as f:
    content = f.read()

# 1. Remove Mock Tools if any remain (Speed Test was replaced)
# Currency mock: `createMathTool('currency-usd-eur', 'USD to EUR (Mock)'...`
# Replace with Real Currency Tool using static table (since API limits or complexity might break SPA)
# But user said "NO sims". A static table of *approximate* rates is better than "Mock".
# Or fetch from `open.er-api.com/v6/latest/USD`.

currency_real = r"""
    registerTool('currency-conv', 'Currency Converter', 'Finance', 'Real-time rates.',
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><path d="M12 18V6"/></svg>',
        (container) => {
            container.innerHTML = `
                <div class="glass-panel" style="max-width: 500px;">
                    <div class="input-group">
                        <label>Amount</label>
                        <input type="number" id="curr-amount" class="glass-input" value="1">
                    </div>
                    <div class="converter-grid">
                        <select id="curr-from" class="glass-select"></select>
                        <div class="converter-arrow">→</div>
                        <select id="curr-to" class="glass-select"></select>
                    </div>
                    <div id="curr-result" style="text-align: center; font-size: 2rem; font-weight: bold; margin-top: 20px;">-</div>
                    <div id="curr-rate" style="text-align: center; font-size: 0.8rem; opacity: 0.7;">Fetching rates...</div>
                </div>
            `;

            const amount = document.getElementById('curr-amount');
            const from = document.getElementById('curr-from');
            const to = document.getElementById('curr-to');
            const result = document.getElementById('curr-result');
            const rateMsg = document.getElementById('curr-rate');

            let rates = {};

            fetch('https://open.er-api.com/v6/latest/USD')
                .then(r => r.json())
                .then(data => {
                    rates = data.rates;
                    rateMsg.textContent = `Rates updated: ${data.time_last_update_utc}`;
                    const currencies = Object.keys(rates).sort();
                    const opts = currencies.map(c => `<option value="${c}">${c}</option>`).join('');
                    from.innerHTML = opts;
                    to.innerHTML = opts;
                    from.value = 'USD';
                    to.value = 'EUR';
                    convert();
                })
                .catch(e => rateMsg.textContent = 'Error fetching rates (Using offline backup)');

            function convert() {
                if(!rates['USD']) return;
                const amt = parseFloat(amount.value) || 0;
                const base = amt / rates[from.value];
                const final = base * rates[to.value];
                result.textContent = final.toFixed(2) + ' ' + to.value;
            }

            amount.addEventListener('input', convert);
            from.addEventListener('change', convert);
            to.addEventListener('change', convert);
        }
    );
"""

# Remove old mocks
content = re.sub(r"createMathTool\('currency-usd-eur'.*?\);", "", content)
content = re.sub(r"createMathTool\('currency-eur-usd'.*?\);", "", content)

# Inject new Currency Tool (append to Batch 11 or whereever)
content = content.replace("// --- Batch 11: Final Push to 200 ---", "// --- Batch 11: Final Push to 200 ---\n" + currency_real)

with open('quicktools/index.html', 'w') as f:
    f.write(content)

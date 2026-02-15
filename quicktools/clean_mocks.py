import re

with open('quicktools/index.html', 'r') as f:
    content = f.read()

# 1. IP Address Mock
content = content.replace("createGeneratorTool('ip-address', 'IP Address (Mock)', 'Dev', 'Simulated IP Lookup.', 'Get IP', () => '192.168.1.' + Math.floor(Math.random() * 255));", "")

# 2. MD5 Mock
content = content.replace("createSimpleTextTool('md5-mock', 'MD5 (Mock)', 'Security', 'Mock MD5 hash (not real security).', (text) => \"d41d8cd98f00b204e9800998ecf8427e (Mock)\");", "")

# 3. Center Text
content = content.replace("Center Text (mock).", "Center align text (padded).")

# 4. Unknown
content = content.replace("'Unknown (Mock DB)'", "'Element not found'")

# 5. Currency
content = re.sub(r"createMathTool\('currency-usd-eur'.*?\);", "", content)
content = re.sub(r"createMathTool\('currency-eur-usd'.*?\);", "", content)

# 6. Cron
content = content.replace("'Mock UI (Simple).'", "'Generate simple cron schedule.'")

with open('quicktools/index.html', 'w') as f:
    f.write(content)

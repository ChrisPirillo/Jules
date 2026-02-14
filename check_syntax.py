import re

with open('quicktools/index.html', 'r') as f:
    content = f.read()

# Extract script content
matches = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
if not matches:
    print("No script tag found")
    exit(1)

# Check last one (the main logic)
script = matches[-1]

# Write to temp file for checking
with open('temp_script.js', 'w') as f:
    f.write(script)

print("Extracted script. Checking syntax...")

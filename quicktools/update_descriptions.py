import re

with open('quicktools/index.html', 'r') as f:
    content = f.read()

# Enhance descriptions using regex
# Example: 'Convert text to uppercase.' -> 'Convert your text to uppercase letters instantly.'
# Map of keyword to replacement logic or just manual replacements.

# Let's verify we have enough tools first.
matches = re.findall(r"registerTool\('|create\w+Tool\('", content)
print(f"Tool count estimate: {len(matches)}")

# Manual enhancements for common tools
replacements = [
    ("'Convert text to uppercase.'", "'Convert your text to uppercase letters instantly.'"),
    ("'Convert text to lowercase.'", "'Convert your text to lowercase letters instantly.'"),
    ("'Calculate Body Mass Index.'", "'Calculate your Body Mass Index (BMI) based on weight and height.'"),
    ("'Generate UUID v4.'", "'Generate a universally unique identifier (UUID v4).'"),
    ("'Get your public IP.'", "'Retrieve your current public IP address.'"),
    ("'Download Speed Test.'", "'Test your internet download speed.'"),
    ("'Generate SHA-256 hash.'", "'Generate a secure SHA-256 hash from any text input.'"),
    ("'Test Regular Expressions.'", "'Test and debug your JavaScript regular expressions.'"),
]

for old, new in replacements:
    content = content.replace(old, new)

with open('quicktools/index.html', 'w') as f:
    f.write(content)

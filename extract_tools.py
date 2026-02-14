import re

with open('quicktools/script.js.bak', 'r') as f:
    content = f.read()

# Regex to find tool calls
# Matches create...Tool(...) until the closing );
# This is tricky with nested parenthesis, but my tools are simple.
# They end with  usually on a new line or same line.

tools = []
# Split by lines
lines = content.splitlines()
buffer = ""
in_tool = False

for line in lines:
    stripped = line.strip()
    if stripped.startswith("createSimpleTextTool(") or stripped.startswith("createMathTool(") or stripped.startswith("createGeneratorTool("):
        in_tool = True
        buffer = line
    elif in_tool:
        buffer += "\n" + line

    if in_tool:
        # Check for end
        # Count parens?
        # My specific format always ends with ?
        if line.strip().endswith(");"):
            # Check balance roughly
            if buffer.count('(') == buffer.count(')'):
                tools.append(buffer)
                in_tool = False
            # else continue

# Remove duplicates
unique_tools = []
seen = set()
for tool in tools:
    # Use the first line (tool id/name) as key
    key = tool.split(',')[0]
    if key not in seen:
        seen.add(key)
        unique_tools.append(tool)

print(f"Found {len(unique_tools)} tools.")
with open('all_tools_extracted.js', 'w') as f:
    f.write('\n'.join(unique_tools))

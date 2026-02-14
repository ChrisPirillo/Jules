import re

with open('quicktools/index.html', 'r') as f:
    content = f.read()

# I know lines 861+ are garbage from the previous grep.
# They are a duplicate partial fragment.
# I will just remove the fragment.

fragment = r'">Mbps</div>'
idx = content.find(fragment)

if idx != -1:
    # Find the next "registerTool" or "create" to know where garbage ends.
    # Or find the end of the script tag?

    next_tool = content.find("registerTool('ip-address'", idx)
    if next_tool == -1:
        # Maybe next is something else
        next_tool = content.find("createGeneratorTool", idx)

    if next_tool != -1:
        # Removing from idx to next_tool
        print(f"Removing garbage from {idx} to {next_tool}")
        new_content = content[:idx] + content[next_tool:]

        # Check if we broke syntax (missing brace/paren from the PREVIOUS valid tool?)
        # The previous valid tool was the NEW speed test.
        # It ends with .
        # The fragment starts with .
        # We need to ensure the previous tool is closed.

        # Let's inspect the text right before idx.
        print("Context before garbage:")
        print(content[idx-50:idx])

        with open('quicktools/index.html', 'w') as f:
            f.write(new_content)
    else:
        print("Could not find end of garbage.")
else:
    print("Garbage not found (maybe fixed?)")

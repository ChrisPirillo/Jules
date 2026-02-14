def check_file(filename):
    with open(filename, 'r') as f:
        content = f.read()

    stack = []

    for i, char in enumerate(content):
        if char == '{':
            stack.append(i)
        elif char == '}':
            if not stack:
                print(f"Extra '}}' at index {i}")
                start = max(0, i - 50)
                end = min(len(content), i + 50)
                print(f"Context: ...{content[start:end]}...")
                return
            stack.pop()

    if stack:
        idx = stack[-1]
        print(f"Unclosed '{{' at index {idx}")
        # Show context
        start = max(0, idx - 50)
        end = min(len(content), idx + 50)
        print(f"Context: ...{content[start:end]}...")
    else:
        print("Braces balanced.")

check_file('script.js')

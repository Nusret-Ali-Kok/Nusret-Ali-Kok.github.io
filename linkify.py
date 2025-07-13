import re

def linkify_response(text):
    # Regex to find "/experience/any-valid-id"
    pattern = r"(/experience/[a-zA-Z0-9-_]+)"
    # Replace with clickable HTML links, open in new tab
    return re.sub(pattern, r'<a href="\1" target="_blank">\1</a>', text)
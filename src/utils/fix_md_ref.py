import re

def fix_markdown_references(content):
    """
    Fix improperly formatted references in Markdown content.
    Ensures all references are in the form [text](url).
    """
    # Regex pattern to find improperly formatted references
    pattern = r'(\d+\.\s\((.*?)\)\s(.*?)\s)(http[s]?://[^\s]+)'
    matches = re.finditer(pattern, content)

    for match in matches:
        label = match.group(2)  # e.g., Emerson2024SexSpecific
        description = match.group(3).strip()  # e.g., Sex-Specific Response to A1BG Loss...
        url = match.group(4)  # The URL part
        
        # Construct the corrected Markdown link
        corrected = f"[({label}) {description}]({url})"
        
        # Replace the original reference with the corrected one
        content = content.replace(match.group(0), corrected)
    
    return content

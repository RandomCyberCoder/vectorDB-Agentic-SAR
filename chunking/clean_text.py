import ast
import re

def clean_text(text: str) -> str:
    try:
        # First pass: decode escape sequences (e.g. \\n -> \n)
        text = ast.literal_eval(f'"{text}"')
    except Exception:
        pass  # Skip if it's already a properly escaped string

    try:
        # Second pass: decode UTF-8 bytes (e.g. \xe2\x80\x94 -> —)
        text = text.encode('utf-8').decode('unicode_escape').encode('latin1').decode('utf-8')
    except Exception:
        pass  # Skip if not needed

    # Remove characters in the Private Use Area (PUA) - Unicode U+E000 to U+F8FF
    text = re.sub(r'[\uE000-\uF8FF]', '', text)

    # Optional: You can also replace these with a placeholder if you prefer
    # text = re.sub(r'[\uE000-\uF8FF]', '?', text)

    # Remove asterisks (e.g., "**" used for emphasis in Markdown)
    text = text.replace("**", "")
    
    return text
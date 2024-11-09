import markdown

def convert_markdown_to_html(markdown_text):
    """
    Convert Markdown text to HTML.

    Args:
        markdown_text (str): The Markdown content to convert.

    Returns:
        str: The converted HTML content.
    """
    return markdown.markdown(markdown_text)

import re


def remove_urls(text: str) -> str:
    """
    Removes all URLs from the given text.

    Args:
    text (str): The input string from which URLs need to be removed.

    Returns:
    str: The text with all URLs removed.
    """
    # Regex pattern for matching URLs
    url_pattern = r'https?://\S+|www\.\S+'
    return re.sub(url_pattern, '', text)

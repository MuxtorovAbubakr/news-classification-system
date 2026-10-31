import html
import re


def preprocess_text(text: str) -> str:

    text = text.replace("\\", " ")

    while True:
        decoded_text = html.unescape(text)

        if decoded_text == text:
            break

        text = decoded_text

    # Handle remaining HTML artifacts
    text = re.sub(r"#36;", "$", text)
    text = re.sub(r"#39;", "'", text)
    text = re.sub(r"\s+amp;\s*", "&", text)
    text = re.sub(r"\s*quot;\s*", '"', text)

    # Remove common HTML tags
    text = re.sub(
        r"</?(?:strong|em|b|i|p|div|br|span)\b[^>]*>",
        " ",
        text,
        flags=re.IGNORECASE
    )

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text

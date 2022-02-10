EMOJI_LOOKUP = {
    "blocked": "🚫",
    "today": "🚧",
    "yesterday": "⏪",
}


def slack_bold(text):
    return f"*{text}*"


def emojify(name):
    text = EMOJI_LOOKUP.get(name.lower(), "")
    if text:
        text += " "
    return text

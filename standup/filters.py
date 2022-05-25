EMOJI_LOOKUP = {
    "blocked": "🚫",
    "today": "🏗",
    "yesterday": "⏪",
    "announcements": "📣",
}


def slack_bold(text):
    return f"*{text}*"


def emojify(name):
    text = EMOJI_LOOKUP.get(name.lower(), "")
    if text:
        text += " "
    return text


def ensure_list(value):
    if isinstance(value, list):
        return value
    else:
        return [value]

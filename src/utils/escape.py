def telegram_escape(text):
    return text.replace("_", "\\_") \
               .replace("*", "\\*") \
               .replace("[", "\\[") \
               .replace("`", "\\`")

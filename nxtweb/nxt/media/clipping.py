from django.utils.html import strip_tags


def clipping_paragraph(text, word):
    text = strip_tags(text).strip()
    word = word.strip()
    text_lower = text.lower()
    word_lower = word.lower()
    clipping_index = None
    attemps = [
        f' {word_lower} ',
        f' {word_lower},',
        f' {word_lower}.',
        f',{word_lower} ',
        f'.{word_lower} ',
        f'\n{word_lower} ',
        f'\n{word_lower}\n',
        f' {word_lower}\n',
    ]
    for attemp in attemps:
        try:
            clipping_index = text_lower.index(attemp)
        except:
            continue
        break
    if clipping_index is None:
        return None
    words_prev = [word for word in text[:clipping_index].split() if len(word) > 4]
    words_next = [word for word in text[clipping_index:].split() if len(word) > 4]
    if words_prev:
        start_word = words_prev[max(len(words_prev) - 50, 0)]
        start = text.index(start_word)
    else:
        start = 0
    if words_next:
        end_word = words_next[min(50, len(words_next) - 1)]
        end = clipping_index + text[clipping_index:].index(end_word)
    else:
        end = None
    return text[start:end]

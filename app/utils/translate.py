from googletrans import Translator

translator = Translator()


async def translate_text(text: str, dest: str) -> str:
    res = await translator.translate(text, dest=dest)
    return res.text


async def detect_language(text: str) -> str:
    res = await translator.detect(text)
    return res.lang

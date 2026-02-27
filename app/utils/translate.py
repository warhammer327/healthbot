from googletrans import Translator

translator = Translator()


async def translate_text(text: str, dest: str) -> str:
    res = await translator.translate(text, dest=dest)
    return res.text

from googletrans import Translator
import asyncio

async def translate_text(text, dest_lang):
    """Translate text to the specified destination language asynchronously.
    Args:
        text (str): The text to translate.
        dest_lang (str): The target language code (e.g., 'en', 'fr').
    Returns:
        googletrans.Translated: The translated text object.
    """
    async with Translator() as translator:
        result = await translator.translate(text, dest=dest_lang)
        return result

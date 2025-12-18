from googletrans import Translator
import asyncio

async def translate_text(text, dest_lang):
    async with Translator() as translator:
        result = await translator.translate(text, dest=dest_lang)
        return result

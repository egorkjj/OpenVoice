from elevenlabs.client import AsyncElevenLabs, ElevenLabs
from elevenlabs import save
import elevenlabs, string, random, os
from tinytag import TinyTag


async def OpenVoice(filename: str, text): #filename: str, text

    client = AsyncElevenLabs(
        api_key="sk_2dc9bf9826b00d56293e264d9a04540eb59584e84af7f79e" #"sk_9ef1d1a67b8d7c28ddaf1e2515f8a95b67f9ea471d797274", 
    )
    
    voice = await client.clone(name = "Jhon", description="Desc", files=[filename], labels = {})
    if "tg_bot/user_models/" in filename:
        os.remove(filename)

    voices = elevenlabs.Voice(voice_id = voice.voice_id, language='ru', name = "Speaker")

    def generate_random_string(length):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    
    name = generate_random_string(20)

    if not os.path.isdir("tg_bot/voices"):
        os.mkdir("tg_bot/voices")

    async_generator = client.generate(text=text, voice=voices, model = "eleven_multilingual_v2")
    with open(f"tg_bot/voices/{name}.mp3", "wb") as f:
        async for chunk in await async_generator:
            f.write(chunk)
    await client.voices.delete(voice.voice_id)


    tag = TinyTag.get(f"tg_bot/voices/{name}.mp3")
    duration = tag.duration
    return [f"tg_bot/voices/{name}.mp3", duration]


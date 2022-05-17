from pyrogram import filters
from bot import app, data, sudo_users
from bot.helper.utils import add_task
import asyncio
import time

video_mimetype = [
  "video/x-flv",
  "video/mp4",
  "application/x-mpegURL",
  "video/MP2T",
  "video/3gpp",
  "video/quicktime",
  "video/x-msvideo",
  "video/x-ms-wmv",
  "video/x-matroska",
  "video/webm",
  "video/x-m4v",
  "video/quicktime",
  "video/mpeg"
  ]

@app.on_message(filters.user(sudo_users) & filters.command(["start", "help"]))
async def help_message(app, message):
    await message.reply_text(f"Hi {message.from_user.mention()}\n**•I can Encode Telegram files And Send Sample (Especially Movies,Animes), just send me a video.**\n**•This Bot is Developed by @NIRUSAKI_AYEDAEMON**\n**•Simple, Easy and Convenient to use**\n**Thanks**")

@app.on_message(filters.user(sudo_users) & filters.incoming & (filters.video | filters.document))
async def encode_video(app, message):
    if message.document:
      if not message.document.mime_type in video_mimetype:
        await message.reply_text("𝓢𝓔𝓓 𝓛𝓨𝓕 𝓦𝓡𝓞𝓝𝓖 𝓕𝓞𝓡𝓜𝓐𝓣", quote=True)
        return
    await message.reply_text("𝓐𝓭𝓭𝓮𝓭 𝓣𝓸 𝓠𝓾𝓮𝓾𝓮 𝓟𝓵𝓮𝓪𝓼𝓮 𝓦𝓪𝓲𝓽 𝓐 𝓦𝓱𝓲𝓵𝓮 𝓤𝓷𝓽𝓲𝓵 𝓔𝓷𝓬𝓸𝓭𝓲𝓷𝓰 𝓢𝓽𝓪𝓻𝓽𝓼", quote=True)
    data.append(message)
    if len(data) == 1:
     await add_task(message)
     time.sleep(1)

app.run()

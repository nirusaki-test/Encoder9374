import pyrogram
import asyncio
import time
import subprocess
from bot import app, sudo_users, ffmpeg

async def change_ffmpeg(app, message):
  try:
    changeffmpeg = message.text.split(" ", maxsplit=1)[1]
    ffmpeg.insert(0,changeffmpeg)
    await app.reply_text(f"**Successfully Changed The FFMPEG-CODE To**\n```{changeffmpeg}```")
  except Exception as e:
    await app.reply_test(f"Error {e}")
  

import pyrogram
import asyncio
import time
import subprocess
from bot import app, sudo_users, ffmpeg

async def change_ffmpeg(app, message):
  try:
    changeffmpeg = message.text.split(" ", maxsplit=1)[1]
    ffmpeg.insert(0,changeffmpeg)
    await message.reply_text(f"**Successfully Changed The FFMPEG-CODE To**\n```{changeffmpeg}```")
  except Exception as e:
    await message.reply_text(f"Error {e}")
    
  
async def get_ffmpeg(app, message):
  await message.reply_text(f"**The Set Code Is**\n{ffmpeg[0]}")

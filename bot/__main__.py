from pyrogram import filters
from bot import app, data, sudo_users
from bot.helper.utils import add_task, startup
import asyncio
import traceback
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

@app.on_message(filters.incoming & filters.command(["cmds", "cmd", "commands"]))
async def help_message(app, message):
    if message.chat.id not in sudo_users:
      return await message.reply_text("**You Are Not Authorised To Use This Bot Contact @Nirusaki**")
    await message.reply_text(f"Hi {message.from_user.mention()}\n**•The List Of Commands Are As Follows -:**\n•```/start```**- To Start The Bot\n**•```/cmds```**-To Repeat This List**\n•**Maintained By @FIERCE_TOONS**")

@app.on_message(filters.incoming & filters.command(["start", "help"]))
async def help_message(app, message):
    if message.chat.id not in sudo_users:
      return await message.reply_text("**You Are Not Authorised To Use This Bot Contact @Nirusaki**")
    await message.reply_text(f"Hi {message.from_user.mention()}\n**•I can Encode Telegram files And Send Sample (Especially Movies,Animes), just send me a video.**\n**•This Bot is Developed by @NIRUSAKI_AYEDAEMON**\n**•Simple, Easy and Convenient to use**\n**Thanks**")

@app.on_message(filters.incoming & (filters.video | filters.document))
async def encode_video(app, message):
    if message.chat.id not in sudo_users:
      return await message.reply_text("**You Are Not Authorised To Use This Bot Contact @Nirusaki**")
    if message.document:
      if not message.document.mime_type in video_mimetype:
        await message.reply_text("**Send Any Video File**", quote=True)
        return
    a = await message.reply_text("**Added To Queue Please Wait...**", quote=True)
    data.append(message)
    if len(data) == 1:
     await add_task(message, a)
     time.sleep(1.8)

app.run()

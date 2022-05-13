import os
from bot import data, download_dir, app
import asyncio
from pyrogram.types import Message
from pyrogram.errors.exceptions.bad_request_400 import MessageNotModified
from .ffmpeg_utils import encode, get_thumbnail, get_duration, get_width_height 

def on_task_complete():
    del data[0]
    if len(data) > 0:
      add_task(data[0])

def add_task(message: Message):
    try:
      msg = message.reply_text("⬇️ **Downloading Video** ⬇️", quote=True)
      filepath = message.download(file_name=download_dir)
      msg.edit(f"Renaming The File")
      new_file, og = encode(filepath)
      if new_file:
        msg.edit("**⬆️ Starting To Upload**")
        duration = get_duration(new_file)
        thumb = get_thumbnail(new_file)
        width, height = get_width_height(new_file)
        duration2 = get_duration(filepath)
        msg.edit("**⬆️ Uploading Video ⬆️**")
        app.send_video(video=filepath, chat_id=message.chat.id, supports_streaming=True, file_name=og, thumb=thumb, duration=duration2, width=width, height=height, caption=og)
        os.remove(new_file)
        os.remove(filepath)
        os.remove(thumb)
        msg.edit("**File Renamed")
        msg.delete()
      else:
        msg.edit("**Error Contact @NIRUSAKIMARVALE**")
        os.remove(filepath)
    except MessageNotModified:
      pass
    except Exception as e:
      msg.edit(f"```{e}```")
    on_task_complete()

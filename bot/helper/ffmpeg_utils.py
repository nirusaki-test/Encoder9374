import asyncio
import pyrogram
import os
import sys
import json
import anitopy
import time
import logging
from bot import ffmpeg, app, LOG_CHANNEL
from subprocess import call, check_output
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import subprocess
from subprocess import Popen, PIPE

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)


async def run_subprocess(cmd):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    return await process.communicate()

async def encode(filepath):
    basefilepath, extension = os.path.splitext(filepath)
    output_filepath = basefilepath + "R136A1_Encodes" + ".mkv"
    nam = filepath.replace("/home/runner/work/Auto-Renamer-Queue/Auto-Renamer-Queue/downloads/", " ")
    nam = nam.replace("_", " ")
    nam = nam.replace(".mkv", " ")
    nam = nam.replace(".mp4", " ")
    nam = nam.replace(".", " ")
    if "/bot/downloads/" in nam:
      nam = nam.replace("/bot/downloads", " ")
    new_name = anitopy.parse(nam)
    anime_name = new_name["anime_title"]
    joined_string = f"[{anime_name}]"
    if "anime_season" in new_name.keys():
      animes_season = new_name["anime_season"]
      joined_string = f"{joined_string}" + f" [Season {animes_season}]"
    if "episode_number" in new_name.keys():
      episode_no = new_name["episode_number"]
      joined_string = f"{joined_string}" + f" [Episode {episode_no}]"
    og = joined_string + " [@ANIXPO]" + ".mkv"
    og = og.replace("/home/runner/work/Encoder/Encoder/downloads/", "")
    try:
        ffmpeg = f'ffmpeg -i "{filepath}" {ffmpeg[0]} -y "{og}"'
        LOGGER.info(ffmpeg)
        process = await run_subprocess(ffmpeg)
        LOGGER.info(process)
        return og
    except Exception as er:
        return er

async def get_thumbnail(in_filename):
    out_filename = 'thumb1.jpg'
    outfile = 'thumb.jpg'
    try:
        code = f'ffmpeg -hide_banner -loglevel error -i "{in_filename}" -map 0:v -ss 00:20 -frames:v 1 "{out_filename}" -y'
        process = await run_subprocess(code)
        return out_filename
    except Exception as er:
        return LOGGER.info(er)
  
async def get_duration(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata.has("duration"):
      return metadata.get('duration').seconds
    else:
      return 0

async def get_width_height(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata.has("width") and metadata.has("height"):
      return metadata.get("width"), metadata.get("height")
    else:
      return 1280, 720

async def startup():
    LOGGER.info("The Bot Has Started")

    
async def sample_gen(app, message):
  if message.reply_to_message:
     vid = message.reply_to_message.id
     dp = await message.reply_to_message.reply_text("Downloading The Video")
     video = await app.download_media(message=message.reply_to_message)
     await dp.edit("Downloading Finished Starting To Generate Sample")
     output_file = video + 'sample_video.mkv'
     await dp.edit("Generating Sample...This May Take Few Moments")
     file_gen_cmd = f'ffmpeg -ss 00:30 -i "{video}" -map 0 -c:v copy -c:a copy -t 30 "{output_file}" -y'
     output = await run_subprocess(file_gen_cmd)   
     LOGGER.info(output)
     duration = await get_duration(output_file)
     output_thumb = video + 'thumb.jpg'
     thumb_cmd = f'ffmpeg -i {output_file} -map 0:v -ss 00:15 -frames:v 1 -y "{output_thumb}"'
     output = await run_subprocess(thumb_cmd)
  else:
     await message.reply_text('NO FILE DETECTED')
  if os.path.exists(output_file):
     await dp.edit('Uploading The Video')
     chat_id = message.chat.id
     upload = await app.send_video(
        chat_id=message.chat.id,
        video=output_file,
        caption="Sample Generated From 00:30 Of 30 SECONDS",
        supports_streaming=True,
        duration=duration,
        width=1280,
        height=720,
        file_name=output_file,
        thumb=output_thumb,
        reply_to_message_id=vid
     )
     await dp.delete()
     os.remove(video)
     os.remove(output_file)
     os.remove(output_thumb)
  else:
     await dp.edit("Failed To Generate Sample Due To Locked Infrastructure")
     os.remove(video_file)    

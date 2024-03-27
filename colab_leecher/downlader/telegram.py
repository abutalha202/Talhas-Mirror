import logging
import asyncio
from datetime import datetime
from os import path as ospath
import aiohttp
from colab_leecher import colab_bot
from colab_leecher.utility.handler import cancelTask
from colab_leecher.utility.variables import Transfer, Paths, Messages, BotTimes
from colab_leecher.utility.helper import speedETA, getTime, sizeUnit, status_bar

async def media_Identifier(link):
    parts = link.split("/")
    message_id, message = parts[-1], None
    msg_chat_id = "-100" + parts[4]
    message_id, msg_chat_id = int(message_id), int(msg_chat_id)
    try:
        message = await colab_bot.get_messages(msg_chat_id, message_id)
    except Exception as e:
        logging.error(f"Error getting messages {e}")

    media = (
        message.document  # type: ignore
        or message.photo  # type: ignore
        or message.video  # type: ignore
        or message.audio  # type: ignore
        or message.voice  # type: ignore
        or message.video_note  # type: ignore
        or message.sticker  # type: ignore
        or message.animation  # type: ignore
        or None
    )
    if media is None:
        logging.error("Couldn't Download Telegram Message")
        await cancelTask("Couldn't Download Telegram Message")
        return
    return media, message

async def download_chunk(session, url, start, end):
    headers = {'Range': f'bytes={start}-{end}'}
    async with session.get(url, headers=headers) as response:
        chunk = await response.read()
        return chunk

async def download_file(url, file_path):
    async with aiohttp.ClientSession() as session:
        async with session.head(url) as response:
            total_size = int(response.headers['Content-Length'])
        
        chunk_size = 4000 * 4000  # 1 MB chunks
        tasks = []
        with open(file_path, 'wb') as file:
            for start in range(0, total_size, chunk_size):
                end = min(start + chunk_size - 1, total_size - 1)
                task = asyncio.create_task(download_chunk(session, url, start, end))
                tasks.append(task)
            chunks = await asyncio.gather(*tasks)
            for chunk in chunks:
                file.write(chunk)
                Transfer.down_bytes.append(len(chunk))

async def download_progress(current, total):
    speed_string, eta, percentage = speedETA(start_time, current, total)

    await status_bar(
        down_msg=Messages.status_head,
        speed=speed_string,
        percentage=percentage,
        eta=getTime(eta),
        done=sizeUnit(sum(Transfer.down_bytes) + current),
        left=sizeUnit(Transfer.total_down_size),
        engine="Pyrogram 💥",
    )

async def TelegramDownload(link, num):
    global start_time
    media, message = await media_Identifier(link) # type: ignore
    if media is not None:
        name = media.file_name if hasattr(  # type: ignore
            media, "file_name") else "None"
    else:
        logging.error("Couldn't Download Telegram Message")
        await cancelTask("Couldn't Download Telegram Message")
        return

    Messages.status_head = f"<b>📥 DOWNLOADING FROM » </b><i>🔗Link {str(num).zfill(2)}</i>\n\n<code>{name}</code>\n"
    start_time = datetime.now()
    file_path = ospath.join(Paths.down_path, name)
    
    await download_file(link, file_path)

# Start your script here

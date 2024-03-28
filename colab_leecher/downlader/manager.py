import logging
from natsort import natsorted
from datetime import datetime
from asyncio import sleep
from colab_leecher.downlader.mega import megadl
from colab_leecher.utility.handler import cancelTask
from colab_leecher.downlader.ytdl import YTDL_Status, get_YT_Name
from colab_leecher.downlader.aria2 import aria2_Download, get_Aria2c_Name
from colab_leecher.downlader.telegram import TelegramDownload, media_Identifier
from colab_leecher.utility.variables import Gdrive, Transfer, MSG, Messages, Aria2c, BotTimes
from colab_leecher.downlader.gdrive import (
    build_service,
    g_DownLoad,
    get_Gfolder_size,
    getFileMetadata,
    getIDFromURL,
)

async def downloadManager(source, is_ytdl: bool):
    message = "\n<b>Please Wait...</b> ⏳\n<i>Merging YTDL Video...</i> 🐬"
    BotTimes.task_start = datetime.now()
    if is_ytdl:
        for i, link in enumerate(source):
            await YTDL_Status(link, i + 1)
        while not isYtdlComplete():
            await sleep(2)
    else:
        for i, link in enumerate(source):
            try:
                if "drive.google.com" in link:
                    await g_DownLoad(link, i + 1)
                elif "t.me" in link:
                    await TelegramDownload(link, i + 1)
                elif "youtube.com" in link or "youtu.be" in link:
                    await YTDL_Status(link, i + 1)
                    while not isYtdlComplete():
                        await sleep(2)
                elif "mega.nz" in link:
                    await megadl(link, i + 1)
                else:
                    await aria2_Download(link, i + 1)
            except Exception as Error:
                await cancelTask(f"Download Error: {str(Error)}")
                logging.error(f"Error While Downloading: {Error}")
                return

async def calDownSize(sources):
    for link in natsorted(sources):
        if "drive.google.com" in link:
            await build_service()
            id = await getIDFromURL(link)
            try:
                meta = getFileMetadata(id)
            except Exception as e:
                logging.error(f"Error in G-API: {e}")
                await cancelTask("Error in Google API.")
            else:
                if meta.get("mimeType") == "application/vnd.google-apps.folder":
                    Transfer.total_down_size += get_Gfolder_size(id)
                else:
                    Transfer.total_down_size += int(meta["size"])
        elif "t.me" in link:
            media, _ = await media_Identifier(link)
            if media is not None:
                size = media.file_size
                Transfer.total_down_size += size

async def get_d_name(link: str):
    if "drive.google.com" in link:
        id = await getIDFromURL(link)
        meta = getFileMetadata(id)
        Messages.download_name = meta["name"]
    elif "t.me" in link:
        media, _ = await media_Identifier(link)
        Messages.download_name = media.file_name if hasattr(media, "file_name") else "None"
    elif "youtube.com" in link or "youtu.be" in link:
        Messages.download_name = await get_YT_Name(link)
    elif "mega.nz" in link:
        Messages.download_name = "Don't Know 🥲 (Trying)"
    else:
        Messages.download_name = get_Aria2c_Name(link)
            

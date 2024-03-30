from time import time
from datetime import datetime
from pyrogram.types import Message


class BOT:
    SOURCE = []
    TASK = None
    class Setting:
        stream_upload = "Media"
        convert_video = "Yes"
        convert_quality = "High"
        caption = "Monospace"
        prefix = ""
        suffix = ""
        thumbnail = False

    class Options:
        stream_upload = True
        convert_video = True
        convert_quality = True
        caption = "code"
        video_out = "mp4"
        custom_name = ""
        zip_pswd = ""
        unzip_pswd = ""

    class Mode:
        mode = "leech"
        type = "normal"
        ytdl = False

    class State:
        started = False
        task_going = False
        prefix = False
        suffix = False


class YTDL:
    header = ""
    speed = ""
    percentage = 0.0
    eta = ""
    done = ""
    left = ""


class Transfer:
    down_bytes = [0, 0]
    up_bytes = [0, 0]
    total_down_size = 0
    sent_file = []
    sent_file_names = []


class TaskError:
    state = False
    text = ""


class BotTimes:
    current_time = time()
    start_time = datetime.now()
    task_start = datetime.now()


class Paths:
    WORK_PATH = "/content/Talhas-MIRROR/BOT_WORK"
    THMB_PATH = "/content/Talhas-MIRROR/colab_leecher/Thumbnail.jpg"
    VIDEO_FRAME = f"{WORK_PATH}/video_frame.jpg"
    HERO_IMAGE = f"{WORK_PATH}/Hero.jpg"
    DEFAULT_HERO =  "/content/Talhas-MIRROR/custom_thmb.jpg"
    MOUNTED_DRIVE = "/content/drive"
    down_path = f"{WORK_PATH}/Downloads"
    temp_dirleech_path = f"{WORK_PATH}/dir_leech_temp"
    mirror_dir = "//content/drive/MyDrive/Colab Leecher Uploads"
    temp_zpath = f"{WORK_PATH}/Leeched_Files"
    temp_unzip_path = f"{WORK_PATH}/Unzipped_Files"
    temp_files_dir = f"{WORK_PATH}/leech_temp"
    thumbnail_ytdl = f"{WORK_PATH}/ytdl_thumbnails"
    access_token = "/content/token.pickle"


class Messages:
    caution_msg = "\n\n<i>💖 When Talha's bot Doin This, Do Something Else ! <b>Because, Time Is Precious ✨</b></i>"
    download_name = ""
    task_msg = ""
    status_head = f"<b>📥 DOWNLOADING » </b>\n"
    dump_task = ""
    src_link = ""
    link_p = ""


class MSG:
    sent_msg = Message(id=1)
    status_msg = Message(id=2)



class Aria2c:
    link_info = False
    pic_dwn_url = "https://d1qde0807mi10y.cloudfront.net/s24m0w%2Fpreview%2F56921116%2Fmain_large.gif?response-content-disposition=inline%3Bfilename%3D"main_large.gif"%3B&response-content-type=image%2Fgif&Expires=1711836963&Signature=ekNuDmkyFtA-g8N5TOwFEZfRW2ddqxi3GCC1xTtbZ7UgIhfYQpJQvFKi~16zUKsGO1ieRhXhU6rJ-6Bje9XFdjBw4K8fp-RTH8CdY9Pk3jS9qxedm-52OuYLiGzoyv~2yJ2TLj69WjXT2NVtKydCkmdX-BF1X6x6-DKGlE~JElq7DKDamZNsaVkEGAzfCB25gXPv4pKJt-80SHljvEsgyHqEYjbKIEWyESEP-lE8tfCJQrKFFo9E7poJVY2URidD0IAPpcY4AGHmWsW8H5gYHfg~BYFWBWv4GVKyQY-YDCxRaFJOpU-yndNe0DReodh08uSpNbKRxOs~AP5l0Q0P3A__&Key-Pair-Id=APKAJT5WQLLEOADKLHBQ"


class Gdrive:
    service = None

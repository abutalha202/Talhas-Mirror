async def upload_file(file_path, real_name):
    global Transfer, MSG
    BotTimes.task_start = datetime.now()
    caption = f"<{BOT.Options.caption}>{BOT.Setting.prefix} {real_name} {BOT.Setting.suffix}</{BOT.Options.caption}>"
    type_ = fileType(file_path)

    f_type = type_ if BOT.Options.stream_upload else "document"

    try:
        if f_type == "video":
            # For Renaming to mp4
            if not BOT.Options.stream_upload:
                file_path = videoExtFix(file_path)
            # Generate Thumbnail and Get Duration
            thmb_path, seconds = thumbMaintainer(file_path)
            with Image.open(thmb_path) as img:
                width, height = img.size

            MSG.sent_msg = await MSG.sent_msg.reply_video(
                video=file_path,
                supports_streaming=True,
                width=width,
                height=height,
                caption=caption,
                thumb=thmb_path,
                duration=int(seconds),
                progress=progress_bar,
                reply_to_message_id=MSG.sent_msg.id,
                chunk_size=1024 * 512  # Set chunk size to 512KB
            )

        # Other file types handled similarly with appropriate chunk sizes

        Transfer.sent_file.append(MSG.sent_msg)
        Transfer.sent_file_names.append(real_name)

    except FloodWait as e:
        await sleep(5)  # Wait 5 seconds before Trying Again
        await upload_file(file_path, real_name)
    except Exception as e:
        logging.error(f"Error When Uploading : {e}")
        

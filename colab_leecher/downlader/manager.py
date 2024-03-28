async def calDownSize(sources):
    for link in natsorted(sources):
        if "drive.google.com" in link:
            await build_service()
            id = await getIDFromURL(link)
            try:
                meta = getFileMetadata(id)
            except HttpError as e:
                if "File not found" in str(e):
                    err = "The file link you gave either doesn't exist or You don't have access to it!"
                elif "Failed to retrieve" in str(e):
                    err = "Authorization Error with Google! Make sure you have the necessary permissions."
                else:
                    err = f"Error in G-API: {e}"
                logging.error(err)
                await cancelTask(err)
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
                

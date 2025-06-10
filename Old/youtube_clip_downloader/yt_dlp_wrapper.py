import yt_dlp

def list_formats(url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'forcejson': True,
        'simulate': True,
    }

    formats = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        for fmt in info_dict['formats']:
            if fmt.get('vcodec') != 'none':
                formats.append(f"{fmt['format_id']} - Video - {fmt.get('format_note', '')} - {fmt.get('ext')}")
            elif fmt.get('acodec') != 'none':
                formats.append(f"{fmt['format_id']} - Audio - {fmt.get('abr', '')}kbps - {fmt.get('ext')}")
    return formats

def download_clip(url, segments, format_id, output_folder, progress_hook):
    ydl_opts = {
        'format': format_id,
        'download_sections': [f"*{seg}" for seg in segments],  # fixed multi-segment handling
        'outtmpl': f'{output_folder}/%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
        'ignore_playlist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

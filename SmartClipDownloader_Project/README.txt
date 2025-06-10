FULL README CONTENT:

# Smart Clip Downloader (YouTube)

👉 A simple GUI app to download specific clips (with start/end time) from YouTube.
👉 Supports full video/audio quality options.
👉 Allows batch download + parallel downloads + progress bars.
👉 Remembers last used folder.

---------

## Setup

### 1️⃣ Install Python 3.10+ (already done)

### 2️⃣ Install dependencies

---------
pip install -r requirements.txt


### 3️⃣ Run the app

---------

python SmartClipDownloader.pyw


## Features

✅ Select start/end time (HH:MM:SS)  
✅ Select video quality (144p to 8K)  
✅ Select audio quality (up to 320k)  
✅ Pause/Resume downloads  
✅ Batch clip downloads  
✅ Parallel download control  
✅ Progress bar + download history  
✅ Folder selector (auto-remembers)  

## Notes

- Requires ffmpeg for clip cutting (yt-dlp uses this internally).  
- On Windows → easiest way to install ffmpeg:

---------

choco install ffmpeg -y

Or manually download from https://ffmpeg.org/download.html and add it to PATH.

## Known Limitations

- Not all videos are available in every resolution.  
- Parallel download works best for 2–5 concurrent threads.  
- Some videos (age-restricted/private) may not download.

## License

Free to use and modify.  
Built for educational purposes.

## Author

Generated in collaboration with ChatGPT and user Chetan Gadhiya 🙏  
Jay Swaminarayan!

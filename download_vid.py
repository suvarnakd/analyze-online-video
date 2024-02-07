import sys
from pytube import YouTube

def download_video(url):
    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        video.download()
        print("Video downloaded successfully")
    except Exception as e:
        print("An error occurred: ", str(e))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the video URL as a command line argument")
    else:
        video_url = sys.argv[1]
        download_video(video_url)
from tkinter import *
from tkinter import filedialog
# from pytube import YouTube
# from pytube import Playlist
import yt_dlp
# from moviepy.editor import *
import re
import subprocess
import os

window = Tk()
window.geometry("800x600")
window.resizable(0,0)
window.title("Musi Playlist Downloader")
window.configure(bg="#eee")


output_directory = ""
def open_directory():
    global output_directory
    output_directory = filedialog.askdirectory()
    if output_directory:
        selectedFolder.config(text="Selected Folder: " + output_directory)

def convert_to_mp3(input_file, output_file):
    try:
        subprocess.run(['ffmpeg', '-i', input_file, '-vn', '-acodec', 'libmp3lame', '-y', output_file])
        os.remove(input_file)
    except Exception as e:
        print(f"Error converting video to mp3: {e}")

ydl_opts = ""
def download():
    file_path = str(urlInput.get())
    fileType = str(FileClick.get())
    if (fileType == "File Type:"):
        fileType = "Audio"
    quality = str(qualityDefault.get())
    destination = str(selectedFolder.cget("text")).split(": ")[1]

    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    pattern = re.compile(r'<a\s+(?:[^>]*?\s+)?href="(https://youtube\.com[^"]*)"')
    links = pattern.findall(html_content)

    with open('youtube_links.txt', 'w') as output_file:
        for link in links:
            output_file.write(link + '\n')

    def downloadURL(url, videoNum):
        global ydl_opts
        if (fileType == "Audio"):
            if (quality == "High Quality"):
                ydl_opts = {
                    'format': 'bestaudio',
                    # 'merge_output_format': 'mp3',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        # 'preferredquality': '192',  # Quality: 192 kbps
                    }],
                    'outtmpl': f'{output_directory}/{videoNum}. %(title)s.%(ext)s',
                }
            elif (quality == "Low Quality"):
                # global ydl_opts
                ydl_opts = {
                    'format': 'worstaudio',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        # 'preferredquality': '192',  # Quality: 192 kbps
                    }],
                    'outtmpl': f'{output_directory}/{videoNum}. %(title)s.%(ext)s',
                }
        elif (fileType == "Video"):
            if (quality == "High Quality"):
                # global ydl_opts
                ydl_opts = {
                    'format': 'bestvideo',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp4',
                        # 'preferredquality': '192',  # Quality: 192 kbps
                    }],
                    'outtmpl': f'{output_directory}/{videoNum}. %(title)s.%(ext)s',
                }
            elif (quality == "Low Quality"):
                # global ydl_opts
                ydl_opts = {
                    'format': 'worstvideo',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp4',
                        # 'preferredquality': '192',  # Quality: 192 kbps
                    }],
                    'outtmpl': f'{output_directory}/{videoNum}. %(title)s.%(ext)s',
                }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            # info_dict = ydl.extract_info(url, download=False)
            # video_title = info_dict.get('title', None)
            # original_file_path = os.path.join(output_directory, f'{video_title}.mp4')
            # if os.path.exists(original_file_path):
            #     os.remove(original_file_path)

    videoNum = 0
    if (destination != ""):
        for link in links:
            videoNum += 1
            # url = YouTube(link)
            url = link
            downloadURL(url, videoNum)
            # if (videoNum == 15):
            #     break
            # break
            # if (fileType == "Audio"):
                # video_path = outFile
                # mp3_output_path = f"{output_directory}/{videoNum}, {url.title}.mp3"
                # convert_to_mp3(video_path, mp3_output_path)
                # print(output_directory)
                # print(f"{output_directory}/{videoNum}, {url.title}.mp3")
                # break

Label(text="Enter Musi URL:", font=40, fg="black").pack()
Label(text="Click download to start", font=35, fg="black").pack()

urlInput = Entry(window, width=32)
urlInput.pack()

selectedFolder = Label(window, text="Selected Folder: ", font=40, fg="black")
selectedFolder.pack(pady=(10, 0))
openFolder = Button(window, text="Open Folder", command=open_directory, font=30, fg="blue")
openFolder.pack(pady=(0, 10))

fileOptions = ["Audio", "Video"]
FileClick = StringVar()
FileClick.set("File Type:")
FileDrop = OptionMenu(window, FileClick, *fileOptions)
FileDrop.pack()

qualityOptions = ["High Quality", "Low Quality"]
qualityDefault = StringVar()
qualityDefault.set("High Quality")
qualityDrop = OptionMenu(window, qualityDefault, *qualityOptions)
qualityDrop.pack()

Button(text="Download", command=download, width=8, height=2, fg="blue", font="bold").pack(pady=20)

window.mainloop()
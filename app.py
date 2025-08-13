import os
import time
import threading
import customtkinter as ctk
import subprocess
from pytube import YouTube
from tkinter import messagebox
from pathlib import Path

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x400")
        self.title("Link Downloader")
        self.resizable(0, 0)
        
        self.entryPoint()
        
        

    def entryPoint(self):
        self.columnconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)

        self.link_entry=ctk.CTkEntry(self,width=500,height=40,placeholder_text="Paste YouTube link...",fg_color="#101010",border_color="#ff0000",border_width=1)
        self.link_entry.grid(row=0,column=0,sticky="nsew",pady=(10,5),padx=(10,5))

        self.download_button=ctk.CTkButton(self,width=130,height=40,text="Download",command=self.download_audio,fg_color="#101010",border_color="#ff0000",border_width=1,hover_color="#990000")
        self.download_button.grid(row=0,column=1,sticky="nsew",pady=(10,5),padx=(0,10))

        self.console=ctk.CTkTextbox(self,height=300,wrap="word",fg_color="#101010",border_color="#ff0000",border_width=1)
        self.console.grid(row=1,column=0,columnspan=2,sticky="nsew",pady=(0,10),padx=(10,10))
        self.console.insert(0.0,"Ready...\n")

    def log_to_console(self,message):
        self.console.insert("end",f"{message}\n")
        self.console.see("end")

    def download_audio(self):
        print("Hello World!")
        link=self.link_entry.get().strip()
        links=link.split(" ")
        if not links:
            self.log_to_console("ERROR: Please enter a YouTube link.")
            return

        threading.Thread(target=self.start_download, args=(links,)).start()

    def start_download(self, links):
        x=1
        for link in links:
            self.log_to_console(f"STATUS: Starting link {x} of {len(links)}.")
            try:
                # self.log_to_console("Initializing download...")
                downloads_path=str(Path.home() / "Downloads")
                command=[
                    "yt-dlp", "-x", "--audio-format", "mp3",
                    "--ffmpeg-location", "c:/Users/<username>/ffmpeg-full_build/bin",
                    "-o", f"{downloads_path}/%(title)s.%(ext)s", link,
                ]

                yt = YouTube(f'{link}')
                title=yt.title
                ourAudioList=yt.streams.filter(only_audio=True).all()
                ourAudioList[0].download(output_path=f"{downloads_path}",filename=f"{title}")

                process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
                start_time=time.time()

                for line in process.stdout:
                    if "downloaded" in line.lower():
                        self.log_to_console(line.strip())
                    elif "speed" in line.lower():
                        self.log_to_console(line.strip())

                process.wait()
                elapsed_time=time.time()-start_time

                if process.returncode==0:
                    self.log_to_console(f"COMPLETED! Total time: {elapsed_time:.2f} seconds.")
                else:
                    self.log_to_console("Error: Download failed.")

            except Exception as e:
                self.log_to_console(f"Exception: {e}")
            x=+1

if __name__=="__main__":
    app=App()
    app.mainloop()
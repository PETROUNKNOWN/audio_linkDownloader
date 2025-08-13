import os
import time
import threading
import customtkinter as ctk
import subprocess
from pytubefix import YouTube
from tkinter import messagebox
from pathlib import Path
import ffmpeg


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x400")
        self.title("Link Downloader")
        self.resizable(0, 0)
        
        self.createUI()
        
        

    def createUI(self):
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
        link=self.link_entry.get().strip()
        links=link.split(" ")
        if not links:
            self.log_to_console("ERROR: Please enter a YouTube link.")
            return
        self.start_time=0
        self.start_download(links)
        #execution should wait for download completion here!!
        elapsedTime=int(time.time()-self.start_time)
        
        lengthdy=int(elapsedTime/86400)
        lengthhr=int(int(elapsedTime-int(lengthdy*86400))/3600)
        lengthmin=int(int(elapsedTime-int(lengthdy*86400)-int(lengthhr*3600))/60)
        lengthsec=int(elapsedTime-int(lengthdy*86400)-int(lengthhr*3600)-int(lengthmin*60))


        if elapsedTime > 86399: #You never know
            self.log_to_console(f"Download Time: {lengthdy}Days {lengthhr}Hours {lengthmin}Minutes {lengthsec}Seconds.")
        elif elapsedTime > 3599:
            self.log_to_console(f"Download Time: {lengthhr}Hours {lengthmin}Minutes {lengthsec}Seconds.")
        elif elapsedTime > 59:
            self.log_to_console(f"Download Time: {lengthmin}Minutes {lengthsec}Seconds.")
        else:
            self.log_to_console(f"Download Time: {lengthsec}Seconds.")

        # threading.Thread(target=self.start_download, args=(links,)).start()

    def start_download(self, links):
        x=1
        self.start_time=time.time()
        print(links)
        for link in links:
            self.log_to_console(f"STATUS: Starting download {x} of {len(links)}.")
            try:
                # self.log_to_console("Initializing download...")
                downloadsPath=str(Path.home() / "Downloads")
                # command=[
                #     "yt-dlp", "-x", "--audio-format", "mp3",
                #     "--ffmpeg-location", "c:/Users/<username>/ffmpeg-full_build/bin",
                #     "-o", f"{downloadsPath}/%(title)s.%(ext)s", link,
                # ]

                yt = YouTube(url=f"{link}")
                # print(yt)
                title=yt.title
                length=yt.length

                lengthdy=int(length/86400)
                lengthhr=int(int(length-int(lengthdy*86400))/3600)
                lengthmin=int(int(length-int(lengthdy*86400)-int(lengthhr*3600))/60)
                lengthsec=int(length-int(lengthdy*86400)-int(lengthhr*3600)-int(lengthmin*60)) #Works:|

                if lengthsec <= 9:
                    lengthsec=f"0{lengthsec}"
                elif lengthsec > 9:
                    lengthsec=f"{lengthsec}"
                else:
                    lengthsec=f"00" #Works:|

                self.log_to_console(f"\tTitle: {title}")

                if lengthdy == 0:
                    self.log_to_console(f"\tLength: {lengthhr}:{lengthmin}:{lengthsec}.")
                else:
                    self.log_to_console(f"\tLength: {lengthdy}Days {lengthhr}Hours {lengthmin}Minutes {lengthsec}Seconds.")

                
                

                ourAudioList=yt.streams.filter(only_audio=True)
                ourAudioList[0].download(output_path=f"{downloadsPath}",filename=f"{title}")

                # process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
                

                # for line in process.stdout:
                #     if "downloaded" in line.lower():
                #         self.log_to_console(line.strip())
                #     elif "speed" in line.lower():
                #         self.log_to_console(line.strip())

                # process.wait()
                

                # if process.returncode==0:
                #     self.log_to_console(f"COMPLETED! Total time: {elapsed_time:.2f} seconds.")
                # else:
                #     self.log_to_console("Error: Download failed.")

            except Exception as e:
                self.log_to_console(f"Exception: {e}\n")
            x+=1

if __name__=="__main__":
    app=App()
    app.mainloop()
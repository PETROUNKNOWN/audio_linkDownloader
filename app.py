import os
import time
import customtkinter as ctk
import subprocess
from pytubefix import YouTube
from tkinter import messagebox
from pathlib import Path
import ffmpeg

import os
import threading
import glob


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x400")
        self.title("Link Downloader")
        self.resizable(0, 0)
        self.downloadsPath=str(Path.home() / "Downloads")
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
        if not os.path.exists(str(Path.home() / "Downloads/ytDownloads")):
            print("Folder ytDownloads does not exist.")
            self.log_to_console("Folder ytDownloads does not exist.")
            self.log_to_console("Creating the folder user/Downloads/ytDownloads")
            os.makedirs(os.path.join(self.downloadsPath, "ytDownloads"))
            self.repairsPath=str(Path.home() / "Downloads/ytDownloads")
        else:
            self.repairsPath=str(Path.home() / "Downloads/ytDownloads")
            
        link=self.link_entry.get().strip()
        links=link.split(" ")
        if not links:
            self.log_to_console("ERROR: Please enter a YouTube link.")
            return
        self.start_time=0

        x=1
        self.start_time=time.time()
        for link in links:
            self.log_to_console(f"STATUS: Starting download {x} of {len(links)}.")
            time.sleep(1.0)
            self.start_download(link)
            x+=1


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

    

    def start_download(self, link):
        try:
            yt = YouTube(url=f"{link}")
            title=yt.title
            length=yt.length
            
            lengthdy=int(length/86400)
            lengthhr=int(int(length-int(lengthdy*86400))/3600)
            lengthmin=int(int(length-int(lengthdy*86400)-int(lengthhr*3600))/60)
            lengthsec=int(length-int(lengthdy*86400)-int(lengthhr*3600)-int(lengthmin*60)) #Works:|

            # https://www.youtube.com/watch?v=y5DAgBaS53Y

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

            
            
            
            ourAudioList=yt.streams.filter(only_audio=True).first()
            self.fileName=f"{title}.webm"
            ourAudioList.download(output_path=self.downloadsPath,filename=self.fileName)

            input_file=os.path.join(self.downloadsPath,self.fileName)
            output_file=os.path.join(self.repairsPath,f"{title}.mp3")

            ffmpeg.input(input_file).output(output_file,acodec="libmp3lame",audio_bitrate="320k",write_id3v1="1",id3v2_version="3").run(quiet=True)

            if os.path.exists(input_file):
                os.remove(input_file)
                print(f"{input_file} has been deleted.")
            else:
                print(f"{input_file} does not exist.")


        except Exception as e:
            self.log_to_console(f"Exception: {e}\n")
            

if __name__=="__main__":
    app=App()
    app.mainloop()
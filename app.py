import os
import time
import ffmpeg
import threading
from pathlib import Path
import customtkinter as ctk
from pytubefix import YouTube

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x400")
        self.title("Youtube Audio Downloader")
        self.configure(fg_color="#101010")
        self.downloadsPath=str(Path.home() / "Downloads")
        self.createUI()

    def createUI(self):
        self.columnconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)

        self.linkEntry=ctk.CTkEntry(self,width=500,height=40,placeholder_text="Paste YouTube links...",fg_color="#101010",border_color="#ff0000",border_width=1)
        self.linkEntry.grid(row=0,column=0,sticky="nsew",pady=(5,5),padx=(5,5))

        ctk.CTkButton(self,width=130,height=40,text="Download",command=self.download_audio,fg_color="#101010",border_color="#ff0000",border_width=1,hover_color="#990000").grid(row=0,column=1,sticky="nsew",pady=(5,5),padx=(0,5))

        self.console=ctk.CTkTextbox(self,height=300,wrap="word",fg_color="#101010",border_color="#ff0000",border_width=1)
        self.console.grid(row=1,column=0,columnspan=2,sticky="nsew",pady=(0,5),padx=(5,5))
        # self.console.insert(0.0,"Ready...\n")
        self.log_to_console("Ready...")
        self.log_to_console("You can paste several links seperated by [SPACE].")

    def log_to_console(self,message):
        self.console.insert("end",f"{message}\n")
        self.console.see("end")

    def download_audio(self):
        #Check if ~\Downloads\ytDownloads exists, if not, create it.
        if not os.path.exists(str(Path.home() / "Downloads/ytDownloads")):
            self.log_to_console("Folder ytDownloads does not exist.")
            self.log_to_console("Creating the folder user/Downloads/ytDownloads")
            try: 
                os.makedirs(os.path.join(self.downloadsPath, "ytDownloads")) #Permission Required.
            except Exception as e:
                self.log_to_console(f"Exception: {e}\n")
                return
            self.repairsPath=str(Path.home() / "Downloads/ytDownloads")
        else:
            self.repairsPath=str(Path.home() / "Downloads/ytDownloads")

        link=self.linkEntry.get().strip() #Clean leading and trailing whitespaces.
        #Check if there is a link.
        if not link:
            self.log_to_console("ERROR: Please enter a YouTube link.")
            return
        links=link.split(" ") #Seperate several links into list objects.

        self.startTime=0
        x=1 #Iter counter.
        self.startTime=time.time()
        for link in links:
            self.log_to_console(f"Starting download {x} of {len(links)}.")
            # threading.Thread(target=self.start_download, args=(link,)).start() #ARTIFACT
            self.start_download(link)
            x+=1
            time.sleep(1.0)

        #Execution waits for download completion here!!
        elapsedTime=int(time.time()-self.startTime)

        #Formatting the download's time delta:- for logging only.
        timeDay=int(elapsedTime/86400)
        timeHour=int(int(elapsedTime-int(timeDay*86400))/3600)
        timeMin=int(int(elapsedTime-int(timeDay*86400)-int(timeHour*3600))/60)
        timeSec=int(elapsedTime-int(timeDay*86400)-int(timeHour*3600)-int(timeMin*60))

        #Log misc details of the stream.
        if elapsedTime > 86399: #You never know
            self.log_to_console(f"Download Time: {timeDay}Days {timeHour}Hours {timeMin}Minutes {timeSec}Seconds.")
        elif elapsedTime > 3599:
            self.log_to_console(f"Download Time: {timeHour}Hours {timeMin}Minutes {timeSec}Seconds.")
        elif elapsedTime > 59:
            self.log_to_console(f"Download Time: {timeMin}Minutes {timeSec}Seconds.")
        else:
            self.log_to_console(f"Download Time: {timeSec}Seconds.")

    def start_download(self, link):
        try:
            #Test url="https://www.youtube.com/watch?v=y5DAgBaS53Y"

            #Youtube Object.
            thisVideo=YouTube(url=f"{link}")
            
            #Formatting the audio's length:- for logging only.
            timeDay=int(thisVideo.time/86400)
            timeHour=int(int(thisVideo.time-int(timeDay*86400))/3600)
            timeMin=int(int(thisVideo.time-int(timeDay*86400)-int(timeHour*3600))/60)
            timeSec=int(thisVideo.time-int(timeDay*86400)-int(timeHour*3600)-int(timeMin*60)) #Works:|

            #Formatting the stream's time time, fallback to `00`.
            if timeSec <= 9:
                timeSec=f"0{timeSec}"
            elif timeSec > 9:
                timeSec=f"{timeSec}"
            else:
                timeSec=f"00" #Works:|
            
            #Log misc details of the stream.
            if timeDay == 0:
                self.log_to_console(f"\tTitle: {thisVideo.title} \nLength: {timeHour}:{timeMin}:{timeSec}.")
            else:
                self.log_to_console(f"\tTitle: {thisVideo.title} \nLength: {timeDay}Days {timeHour}Hours {timeMin}Minutes {timeSec}Seconds.")

            thisStream=thisVideo.streams.filter(only_audio=True).first()
            thisStream.download(output_path=self.downloadsPath,filename=f"{thisVideo.title}.webm") #`inputPath` depends on this line.

            inputPath=os.path.join(self.downloadsPath,f"{thisVideo.title}.webm") #If the program worked as intended then this path should exist. Possibility of Bug.
            outputPath=os.path.join(self.repairsPath,f"{thisVideo.title}.mp3") #Path to final mp3 audio files.

            #FFMPEG converts our .webm to .mp3 at 320kbps, creating a valid ID3v2.3 tag.
            ffmpeg.input(inputPath).output(outputPath,acodec="libmp3lame",audio_bitrate="320k",write_id3v1="1",id3v2_version="3").run(quiet=True) 

            #Deleting original .webm file.
            if os.path.exists(inputPath): 
                os.remove(inputPath)
                self.log_to_console(f"{inputPath} has been deleted.")
            else:
                self.log_to_console(f"{inputPath} does not exist.")

        except Exception as e:
            self.log_to_console(f"Exception: {e}\n")
            return
            

if __name__=="__main__":
    app=App()
    app.mainloop()
from pytube import YouTube
from tkinter import *
from tkinter.ttk import *

#create window
root = Tk()
root.geometry("500x250")
root.resizable(False,False)
root.title("Youtube To MP4 Downloader")

#window elements
e = Entry(root,background="white")
e.pack()
e.place(relx=.5, rely=.4, anchor="center", width=300, height=20)
e.focus_set()

progress = Progressbar(root, orient = HORIZONTAL, length = 100, mode = 'determinate')
progress.place(relx=.5, rely=.9, anchor="center", width=300, height=20)

def download_video():
    
    link = e.get()

    #weird problem where button function runs on initialsation
    if link.__len__() != 0:
        try:
            yt = YouTube(link)

            video = yt.streams.get_highest_resolution()
            video.download(output_path=r'C:\Users\butuz\Videos\Captures')

            import time 
            progress['value'] = 20
            root.update_idletasks() 
            time.sleep(1) 
        
            progress['value'] = 40
            root.update_idletasks() 
            time.sleep(1) 
        
            progress['value'] = 50
            root.update_idletasks() 
            time.sleep(1) 
        
            progress['value'] = 60
            root.update_idletasks() 
            time.sleep(1) 
        
            progress['value'] = 80
            root.update_idletasks() 
            time.sleep(1) 
            progress['value'] = 100

            label = Label(root, text=("Finished downloading: " + yt.title), foreground="black", wraplength= 300, )
            progress['value'] = 0
            label.pack()
            label.place(relx=.6, rely=.7, anchor="center", width=400, height=50)
            
        except:
            label = Label(root, text="Download Failed", foreground="black")

        


button = Button(root, text="Download Video", command=download_video, cursor="hand2")

button.pack(padx=20, pady=20)
button.place(relx=.5, rely=.5, anchor="center")

root.mainloop()
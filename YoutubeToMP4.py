import customtkinter as ctk
import urllib.request
from PIL import Image, ImageTk
from io import BytesIO
from pytube import YouTube
import threading
import re
import os
from moviepy.editor import VideoFileClip

class YouTubeDownloader:
    def __init__(self):
        # Configure appearance
        ctk.set_appearance_mode("system")  # Can be "system" (default), "light" or "dark"
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("YouTube Downloader")
        self.root.geometry("800x600")
        
        # Create main container
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="YouTube Downloader",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(0, 20))
        
        # URL Entry Frame
        self.url_frame = ctk.CTkFrame(self.main_frame)
        self.url_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.url_entry = ctk.CTkEntry(
            self.url_frame,
            placeholder_text="Enter YouTube URL here...",
            height=40,
            width=500
        )
        self.url_entry.pack(side="left", padx=(0, 10), fill="x", expand=True)
        
        self.fetch_button = ctk.CTkButton(
            self.url_frame,
            text="Fetch Video",
            width=100,
            command=self.update_thumbnail
        )
        self.fetch_button.pack(side="right")
        
        # Thumbnail Frame
        self.thumbnail_frame = ctk.CTkFrame(self.main_frame)
        self.thumbnail_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.thumbnail_label = ctk.CTkLabel(self.thumbnail_frame, text="")
        self.thumbnail_label.pack(pady=10)
        
        # Video Info Frame
        self.info_frame = ctk.CTkFrame(self.main_frame)
        self.info_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.title_info = ctk.CTkLabel(
            self.info_frame,
            text="",
            wraplength=700,
            font=ctk.CTkFont(size=16)
        )
        self.title_info.pack(pady=5)
        
        # Download Options Frame
        self.options_frame = ctk.CTkFrame(self.main_frame)
        self.options_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Quality Selection
        self.quality_var = ctk.StringVar(value="Highest")
        self.quality_label = ctk.CTkLabel(
            self.options_frame,
            text="Quality:",
            font=ctk.CTkFont(size=14)
        )
        self.quality_label.pack(side="left", padx=10)
        
        self.quality_menu = ctk.CTkOptionMenu(
            self.options_frame,
            values=["Highest", "720p", "480p", "360p"],
            variable=self.quality_var
        )
        self.quality_menu.pack(side="left", padx=10)
        
        # Download Buttons
        self.mp4_button = ctk.CTkButton(
            self.options_frame,
            text="Download MP4",
            command=lambda: self.start_download('mp4'),
            width=150,
            height=40
        )
        self.mp4_button.pack(side="right", padx=10)
        
        self.mp3_button = ctk.CTkButton(
            self.options_frame,
            text="Download MP3",
            command=lambda: self.start_download('mp3'),
            width=150,
            height=40
        )
        self.mp3_button.pack(side="right", padx=10)
        
        # Progress Frame
        self.progress_frame = ctk.CTkFrame(self.main_frame)
        self.progress_frame.pack(fill="x", padx=20)
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.pack(fill="x", padx=10, pady=10)
        self.progress_bar.set(0)
        
        self.status_label = ctk.CTkLabel(
            self.progress_frame,
            text="Ready to download",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=5)
        
    def is_valid_youtube_url(self, url):
        youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        return bool(re.match(youtube_regex, url))
        
    def update_thumbnail(self):
        url = self.url_entry.get()
        if not self.is_valid_youtube_url(url):
            self.status_label.configure(text="Please enter a valid YouTube URL")
            return
            
        try:
            yt = YouTube(url)
            thumbnail_url = yt.thumbnail_url
            
            # Download and display thumbnail
            response = urllib.request.urlopen(thumbnail_url)
            img_data = response.read()
            img = Image.open(BytesIO(img_data))
            
            # Resize thumbnail
            img = img.resize((400, 225), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            self.thumbnail_label.configure(image=photo)
            self.thumbnail_label.image = photo
            
            # Update video title
            self.title_info.configure(text=yt.title)
            self.status_label.configure(text="Video fetched successfully!")
            
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}")
            
    def progress_callback(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size)
        self.progress_bar.set(percentage)
        self.root.update_idletasks()
        
    def start_download(self, format_type):
        url = self.url_entry.get()
        if not self.is_valid_youtube_url(url):
            self.status_label.configure(text="Please enter a valid YouTube URL")
            return
            
        # Disable buttons during download
        self.mp4_button.configure(state="disabled")
        self.mp3_button.configure(state="disabled")
        self.status_label.configure(text=f"Starting {format_type.upper()} download...")
        
        # Start download in a separate thread
        thread = threading.Thread(target=lambda: self.download_video(format_type))
        thread.start()
        
    def convert_to_mp3(self, video_path):
        try:
            mp3_path = video_path.rsplit('.', 1)[0] + '.mp3'
            video_clip = VideoFileClip(video_path)
            audio_clip = video_clip.audio
            audio_clip.write_audiofile(mp3_path)
            audio_clip.close()
            video_clip.close()
            
            # Remove the original video file
            os.remove(video_path)
            return mp3_path
        except Exception as e:
            raise Exception(f"Error converting to MP3: {str(e)}")
        
    def download_video(self, format_type):
        try:
            url = self.url_entry.get()
            yt = YouTube(url, on_progress_callback=self.progress_callback)
            
            # Get save location
            initial_filename = f"{yt.title}.{format_type}"
            save_path = ctk.filedialog.asksaveasfilename(
                defaultextension=f".{format_type}",
                initialfile=initial_filename,
                filetypes=[(f"{format_type.upper()} files", f"*.{format_type}")]
            )
            
            if not save_path:
                self.status_label.configure(text="Download cancelled")
                return
                
            # Get stream based on quality selection
            if format_type == 'mp4':
                if self.quality_var.get() == "Highest":
                    video_stream = yt.streams.get_highest_resolution()
                else:
                    resolution = self.quality_var.get().replace('p', '')
                    video_stream = yt.streams.filter(res=self.quality_var.get()).first()
                    if not video_stream:
                        video_stream = yt.streams.get_highest_resolution()
            else:
                video_stream = yt.streams.get_highest_resolution()
                
            # Download
            video_path = video_stream.download(filename=save_path if format_type == 'mp4' else 'temp_video.mp4')
            
            if format_type == 'mp3':
                self.status_label.configure(text="Converting to MP3...")
                mp3_path = self.convert_to_mp3(video_path)
                self.status_label.configure(text=f"MP3 saved successfully!")
            else:
                self.status_label.configure(text=f"MP4 saved successfully!")
                
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}")
        finally:
            # Re-enable buttons
            self.mp4_button.configure(state="normal")
            self.mp3_button.configure(state="normal")
            self.progress_bar.set(0)

if __name__ == "__main__":
    app = YouTubeDownloader()
    app.root.mainloop()
from os import scandir, makedirs
from os.path import splitext, exists, join
from shutil import move
from time import sleep  
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
# === CONFIGURATION ===
source_dir = r"C:\Users\joele\Downloads"
dest_dir_sfx = r"C:\Users\joele\Downloads\downloaded_sfx"
dest_dir_music = r"C:\Users\joele\Downloads\downloaded_music"
dest_dir_video = r"C:\Users\joele\Downloads\downloaded_videos"
dest_dir_image = r"C:\Users\joele\Downloads\downloaded_images"
dest_dir_documents = r"C:\Users\joele\Downloads\downloaded_pdfs"
dest_dir_stls = r"C:\Users\joele\Downloads\downloaded_stl"
dest_dir_solidworks = r"C:\Users\joele\Downloads\downloaded_solidworks"

# Create destination directories if they don't exist
for path in [dest_dir_sfx, dest_dir_music, dest_dir_video, dest_dir_image, dest_dir_documents, dest_dir_stls, dest_dir_solidworks]:
    try:
        makedirs(path, exist_ok=True)
    except Exception as e:
        logging.error(f"Error creating directory {path}: {e}")

# === FILE EXTENSIONS ===
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg", ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
audio_extensions = [".m4a", ".flac", ".mp3", ".wav", ".wma", ".aac"]
document_extensions = [".doc", ".docx", ".odt", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]
stl_extensions = [".stl", ".3mf"]
solidworks_extensions = [".sldprt", ".sldasm", ".slddrw"]

# === FILE MOVING LOGIC ===
def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    while exists(join(dest, name)):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1
    return name

def move_file(dest, entry, name):
    if exists(join(dest, name)):
        name = make_unique(dest, name)
    try:
        move(entry.path, join(dest, name))
        logging.info(f"Moved file: {name} to {dest}")
    except Exception as e:
        logging.error(f"Error moving file {name}: {e}")

# === WATCHDOG EVENT HANDLER ===
class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with scandir(source_dir) as entries:
            for entry in entries:
                if not entry.is_file():
                    continue
                name = entry.name
                self.check_audio_files(entry, name)
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.check_document_files(entry, name)
                self.check_stl_files(entry, name)
                self.check_solidworks_files(entry, name)

    def check_audio_files(self, entry, name):
        for ext in audio_extensions:
            if name.lower().endswith(ext):
                dest = dest_dir_sfx if entry.stat().st_size < 10_000_000 or "SFX" in name.upper() else dest_dir_music
                move_file(dest, entry, name)
                break

    def check_video_files(self, entry, name):
        for ext in video_extensions:
            if name.lower().endswith(ext):
                move_file(dest_dir_video, entry, name)
                break

    def check_image_files(self, entry, name):
        for ext in image_extensions:
            if name.lower().endswith(ext):
                move_file(dest_dir_image, entry, name)
                break

    def check_document_files(self, entry, name):
        for ext in document_extensions:
            if name.lower().endswith(ext):
                move_file(dest_dir_documents, entry, name)
                break

    def check_stl_files(self, entry, name):
        for ext in stl_extensions:
            if name.lower().endswith(ext):
                move_file(dest_dir_stls, entry, name)
                break

    def check_solidworks_files(self, entry, name):
        for ext in solidworks_extensions:
            if name.lower().endswith(ext):
                move_file(dest_dir_solidworks, entry, name)
                break

# === MAIN EXECUTION ===
def run_observer():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, source_dir, recursive=True)
    observer.start()
    logging.info("Observer started, waiting for file changes...")
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# === EXECUTION ===
if __name__ == "__main__":
    run_observer()

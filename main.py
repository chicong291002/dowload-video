import concurrent.futures
import logging
import os
import re
import shutil
import threading
from tkinter import filedialog, messagebox
import customtkinter

from format_conversion import convert_to_format
from format_conversion_gui import ConversionFrame
from video_download import (download_audio, download_description,
                            download_subtitles, download_thumbnail,
                            download_video, get_youtube_streams)
from video_download_gui import DownloadFrame, ProcessingDialog

INVALID_CHARS_REGEX = re.compile(r'[\\\/:\*\?"<>|]')

# Thiết lập cấp độ logging là INFO, nghĩa là chỉ những thông điệp có mức độ lớn hơn hoặc bằng INFO mới được ghi vào file log
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('./vdb_logging.log', encoding='utf-8'), logging.StreamHandler()]
)

class MyTabView(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        self.add("Download")
        self.add("Format conversion")

        self.download_frame = DownloadFrame(master=self.tab(
            'Download'), corner_radius=0, fg_color="transparent")
        self.download_frame.pack(fill='both', expand=True)

        self.conversion_frame = ConversionFrame(master=self.tab(
            'Format conversion'), corner_radius=0, fg_color="transparent")
        self.conversion_frame.pack(fill='both', expand=True)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("700x500") 
        self.title("Video Downloader Basic")
        #self.minsize(400, 200)

        self.update()  # Cập nhật cửa sổ để xác định kích thước

        # Lấy kích thước màn hình
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Tính toán vị trí mới cho cửa sổ
        x = (screen_width - self.winfo_width()) // 2
        y = (screen_height - self.winfo_height()) // 2

        # Đặt vị trí mới cho cửa sổ
        self.geometry(f"+{x}+{y}")
        
        def on_closing():
            self.destroy()
            os._exit(0)
        self.protocol("WM_DELETE_WINDOW", on_closing)

        self.tab_view = MyTabView(master=self)
        self.tab_view.pack(padx=20, pady=(5, 20), fill="both", expand=True)
        self.tab_view.download_frame.download_button.configure(
            command=lambda: self.start_video_download(self.download_video_collection, self.tab_view.download_frame))

        self.tab_view.conversion_frame.download_button.configure(
            command=lambda: self.start_conversion(self.tab_view.conversion_frame))

        self.flag_urls = []

    def start_video_download(self, download_package_func, source):
        links = source.textbox.get('1.0', 'end-1c').split('\n')
        links = list(filter(bool, links))
        unique_links = list(set(links))
        print(unique_links)
        if (len(unique_links) == 0):
            messagebox.showwarning('Warning', 'Please input a url')
            return
        urls = [i for i in unique_links]
        package_name = source.entry.get()
        if not package_name:
            messagebox.showwarning('Warning', 'Please input a package name')
            return
        package_name = re.sub(INVALID_CHARS_REGEX, "'", package_name)
        try:
            # Hiển thị cửa sổ cho người dùng chọn nơi lưu
            dir_path = filedialog.askdirectory()
            if dir_path:
                os.chmod(dir_path, 0o777)
                package_path = os.path.join(dir_path, package_name)
                if not os.path.exists(package_path):
                    os.makedirs(package_path)
                logging.info(f'Package: {package_path}')
                t = threading.Thread(
                    target=download_package_func, args=(package_path, urls,))
                t.start()
        except Exception as e:
            messagebox.showerror(
                'Error', f'Invalid path or inaccessible path\n {str(e)}')

    def download_video_collection(self, package_path, urls):
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                futures = []
                self.dialog_processing = ProcessingDialog(self)

                def exit():
                    try:
                        shutil.rmtree(package_path)
                    except OSError as e:
                        logging.error(f"Error: {e.filename} - {e.strerror}.")
                    self.dialog_processing.destroy()
                # Ngăn người dùng thoát cửa sổ
                self.dialog_processing.protocol("WM_DELETE_WINDOW", exit)
                for index, url in enumerate(urls):
                    self.flag_urls.append(False)
                    found_valid_video, youtube_folder, message_error, youtube = self.check_valid_video(
                        url)
                    if not found_valid_video:
                        self.dialog_processing.error(title=message_error)
                        continue
                    self.dialog_processing.set_progressbar(
                        index=len(futures), title=youtube_folder)
                    self.dialog_processing.start_progressbar(
                        index=len(futures))
                    dir_folder = os.path.join(package_path, youtube_folder)
                    future = executor.submit(
                        self.display_download_progress, index, youtube, youtube_folder, dir_folder)
                    futures.append(future)
                # Kiểm tra các đối tượng Future đã hoàn thành
                for future in concurrent.futures.as_completed(futures):
                    if future.done():
                        result = future.result()
                        logging.info(
                            f"Future {future} completed with result: {result}")
                        self.dialog_processing.stop_progressbar(
                            int(futures.index(future)))

                concurrent.futures.wait(futures)

                self.finish_video_download(urls)
        except Exception as e:
            logging.error(f"Error: {str(e)}")

    def check_valid_video(self, url):
        found_valid_video = False
        attempts = 0
        message_error = ""
        youtube_folder = ""
        while not found_valid_video:
            if attempts == 3:
                break
            youtube = get_youtube_streams(url)
            if isinstance(youtube, str):
                attempts += 1
                message_error = youtube
                continue
            try:
                youtube_folder = re.sub(
                    INVALID_CHARS_REGEX, "'", str(youtube.title))
            except Exception:
                attempts += 1
                message_error = f'Error link "{url}"'
                continue
            found_valid_video = True
        return found_valid_video, youtube_folder, message_error, youtube

    def finish_video_download(self, urls):
        self.dialog_processing.destroy()
        message = ''
        for index, url in enumerate(urls):
            if self.flag_urls[index]:
                message += f'Link {url}: Download successful!\n'
            else:
                message += f'Link {url}: Download fail!\n'

        messagebox.showinfo('Announcement', message)
        self.flag_urls = []

    def display_download_progress(self, index, youtube, youtube_folder, dir_folder):
        if not os.path.exists(dir_folder):
            os.makedirs(dir_folder)

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            futures.append(executor.submit(
                download_video, youtube, dir_folder))
            if self.tab_view.download_frame.additional_options.audio_check.get() == 1:
                futures.append(executor.submit(
                    download_audio, youtube, dir_folder))
            if self.tab_view.download_frame.additional_options.thumbnail_check.get() == 1:
                futures.append(executor.submit(
                    download_thumbnail, youtube, youtube_folder, dir_folder))
            if self.tab_view.download_frame.additional_options.description_check.get() == 1:
                futures.append(executor.submit(
                    download_description, youtube, youtube_folder, dir_folder))
            if self.tab_view.download_frame.additional_options.subtitles_check.get() == 1:
                futures.append(executor.submit(download_subtitles, youtube, dir_folder))

            concurrent.futures.wait(futures)

        for future in futures:
            if future.exception() is not None:
                self.flag_urls[index] = False
                break
        else:
            self.flag_urls[index] = True

    def start_conversion(self, source):
        input_file = source.entry_video_path.get()
        if not input_file:
            messagebox.showwarning('Warning', 'Please input a video path')
            return
        folder_name = source.entry_folder_name.get()
        if not folder_name:
            messagebox.showwarning('Warning', 'Please input a folder name')
            return
        folder_name = re.sub(INVALID_CHARS_REGEX, "'", folder_name)
        format_selection = source.combobox_format.get()
        try:
            # Hiển thị cửa sổ cho người dùng chọn nơi lưu
            dir_path = filedialog.askdirectory()
            if dir_path:
                os.chmod(dir_path, 0o777)
                output_path = os.path.join(dir_path, folder_name)
                if not os.path.exists(output_path):
                    os.makedirs(output_path)
                logging.info(f'Folder: {output_path}')
                t = threading.Thread(target=self.converting, args=(
                    input_file, output_path, format_selection))
                t.start()
        except Exception as e:
            messagebox.showerror(
                'Error', f'Invalid path or inaccessible path\n {str(e)}')

    def converting(self, input_file, output_path, format_selection):        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            processing = ProcessingDialog()
            processing.set_progressbar(
                index=0, title=os.path.basename(input_file))
            processing.start_progressbar(index=0)
            
            futures.append(executor.submit(
                convert_to_format, input_file, output_path, format_selection.lower()))
            concurrent.futures.wait(futures)
            processing.stop_progressbar(0)
            processing.destroy()
            messagebox.showinfo('Announcement', "Successfully")
            logging.info(f'{input_file} successfully')


# Khởi tạo ứng dụng GUI
app = App()
app.mainloop()

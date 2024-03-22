from tkinter import filedialog
import customtkinter

class ConversionFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets on to the frame
        self.title_label = customtkinter.CTkLabel(master=self, text="Convert video formats from mp4 to other formats\n(The conversion process takes quite a long time)")
        self.title_label.pack(padx=10, pady=(5, 5), fill='x', expand=True)

        self.frame_get_video_path = customtkinter.CTkFrame(master=self)
        self.frame_get_video_path.pack(padx=10, pady=(0, 10), fill='x', expand=True)
        self.frame_get_video_path.grid_rowconfigure(0, weight=1)
        self.frame_get_video_path.grid_columnconfigure(0, weight=1)

        self.entry_video_path = customtkinter.CTkEntry(
            master=self.frame_get_video_path, placeholder_text='Enter video path or Select "GET" button to get video path')
        self.entry_video_path.grid(row=0, column=0, sticky='nsew')

        self.button_get_video_path = customtkinter.CTkButton(
            master=self.frame_get_video_path, text="GET", width=100, command=self.get_video_path)
        self.button_get_video_path.grid(
            row=0, column=1, padx=(10, 0), sticky='ew')

        self.label = customtkinter.CTkLabel(
            master=self, text="Enter a saving folder name and choose a conversion format")
        self.label.pack(padx=10, pady=(20, 5), fill='x', expand=True)

        self.frame_select_format = customtkinter.CTkFrame(master=self)
        self.frame_select_format.pack(
            padx=10, pady=(0, 10), fill='x', expand=True)
        self.frame_select_format.grid_rowconfigure(0, weight=1)
        self.frame_select_format.grid_columnconfigure(0, weight=1)

        self.entry_folder_name = customtkinter.CTkEntry(
            master=self.frame_select_format, placeholder_text='Enter folder name (Example: Converted Video)')
        self.entry_folder_name.grid(row=0, column=0, sticky='nsew')

        self.combobox_format = customtkinter.CTkComboBox(
            master=self.frame_select_format, width=100, values=["avi", "mkv", "wmv", "mov", "flv"])
        self.combobox_format.grid(row=0, column=1, padx=(10, 0), sticky='nsew')

        self.download_button = customtkinter.CTkButton(
            master=self, text='Convert')
        self.download_button.pack(
            padx=10, pady=(20, 10), fill='x', expand=True)

    def get_video_path(self):
        file_path = filedialog.askopenfilename(
            initialdir='/', title='Select a file', filetypes=[('WEBM Files', '*.webm')])
        self.entry_video_path.insert(0, file_path)

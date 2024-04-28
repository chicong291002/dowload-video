from tkinter import filedialog
import customtkinter

class ConversionFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.frame_get_video_path = customtkinter.CTkFrame(master=self, fg_color="orange")
        self.frame_get_video_path.pack(padx=10, pady=10, fill='x', expand=True)
        self.frame_get_video_path.grid_rowconfigure(0, weight=1)
        self.frame_get_video_path.grid_columnconfigure(0, weight=1)

        self.entry_video_path = customtkinter.CTkEntry(
            master=self.frame_get_video_path, placeholder_text='Enter video path or Select "GET" button to get video path')
        self.entry_video_path.grid(row=0, column=0, sticky='nsew')

        self.button_get_video_path = customtkinter.CTkButton(
            master=self.frame_get_video_path, text="GET", width=100, command=self.get_video_path)
        self.button_get_video_path.grid(row=0, column=1, padx=(10, 0), sticky='ew')

        self.frame_select_format = customtkinter.CTkFrame(master=self, fg_color="orange")
        self.frame_select_format.pack(padx=10, pady=(10, 10), fill='x', expand=True)

        self.label = customtkinter.CTkLabel(
            master=self.frame_select_format, text="Choose a conversion format:")
        self.label.grid(row=0, column=0, sticky='nsew')

        self.combobox_format = customtkinter.CTkComboBox(
            master=self.frame_select_format, width=100, values=["avi","mp4", "mkv", "wmv", "mov", "flv"])
        self.combobox_format.grid(row=0, column=1, padx=10, sticky='nsew')

        self.download_button = customtkinter.CTkButton(master=self, text='Convert')
        self.download_button.pack(padx=10, pady=(20, 10), fill='x', expand=True)
    
    def get_video_path(self):
        file_path = filedialog.askopenfilename(
            initialdir='/', title='Select a file', filetypes=[('WEBM Files', '*.webm'), ('MP4 Files', '*.mp4')])
        self.entry_video_path.insert(0, file_path)
    def clear_inputs(self):
        # Clear the textbox
         self.entry_video_path.delete(0, customtkinter.END)
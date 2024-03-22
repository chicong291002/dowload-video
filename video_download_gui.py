import customtkinter

class DownloadFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        # add widgets on to the frame
        self.title_label = customtkinter.CTkLabel(
            master=self, text="Enter YouTube links here \n(if you enter multiple links, go down the line)")
        self.title_label.grid(row=0, column=0, columnspan=2,
                              padx=10, pady=(5, 10), sticky="ew")
        self.textbox = customtkinter.CTkTextbox(master=self)
        self.textbox.grid(row=1, column=0, columnspan=2,
                          padx=10, sticky="nsew")
        self.additional_options = AdditionalOptionsFrame(master=self)
        self.additional_options.grid(
            row=2, column=0, rowspan=2, padx=10, pady=10, sticky='ew')
        self.entry = customtkinter.CTkEntry(
            master=self, placeholder_text='Enter package name (Example: Video)')
        self.entry.grid(row=2, column=1, padx=10, pady=10, sticky='sew')
        self.download_button = customtkinter.CTkButton(
            master=self, text='Download')
        self.download_button.grid(
            row=3, column=1, padx=10, pady=(0, 10), sticky='sew')

class AdditionalOptionsFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.audio_check = customtkinter.IntVar()
        self.thumbnail_check = customtkinter.IntVar()
        self.subtitles_check = customtkinter.IntVar()
        self.description_check = customtkinter.IntVar()

        self.header = customtkinter.CTkLabel(self, text='Additional Options')
        self.header.grid(row=0, column=0, pady=10)

        self.audio_checkbox = customtkinter.CTkCheckBox(
            master=self, text='Audio', onvalue=1, offvalue=0, variable=self.audio_check, checkbox_height=20, checkbox_width=20, border_width=2)
        self.audio_checkbox.grid(row=1, column=0, pady=10, sticky='ew')

        self.thumbnail_checkbox = customtkinter.CTkCheckBox(
            master=self, text='Thumbnail', onvalue=1, offvalue=0, variable=self.thumbnail_check, checkbox_height=20, checkbox_width=20, border_width=2)
        self.thumbnail_checkbox.grid(row=1, column=1, pady=10, sticky='ew')

        self.subtitles_checkbox = customtkinter.CTkCheckBox(
            master=self, text='Subtitles', onvalue=1, offvalue=0, variable=self.subtitles_check, checkbox_height=20, checkbox_width=20, border_width=2)
        self.subtitles_checkbox.grid(row=2, column=0, pady=10, sticky='ew')

        self.description_checkbox = customtkinter.CTkCheckBox(
            master=self, text='Description', onvalue=1, offvalue=0, variable=self.description_check, checkbox_height=20, checkbox_width=20, border_width=2)
        self.description_checkbox.grid(row=2, column=1, pady=10, sticky='ew')

class ProcessingDialog(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Processing...')
        self.minsize(800, 200)
        self.resizable(width=False, height=True)
        self.grab_set()

        self.message_label = customtkinter.CTkLabel(
            self, text="Processing, please wait...", font=("Arial", 16))
        self.message_label.pack(padx=20, pady=20, fill='x', expand=True)

        self.scrollable_frame = customtkinter.CTkScrollableFrame(
            master=self, fg_color="transparent")
        self.scrollable_frame.pack(fill='both', expand=True)

        self.progressbar = []

    def set_progressbar(self, index, title):
        progressbar = ProgressBar(title=title, master=self.scrollable_frame)
        self.progressbar.append(progressbar)
        self.progressbar[index].pack(padx=20, pady=10, fill='x', expand=True)

    def start_progressbar(self, index):
        self.progressbar[index].progressbar.start()

    def stop_progressbar(self, index):
        self.progressbar[index].progressbar.stop()
        self.progressbar[index].done()

    def error(self, title):
        ErrorLabel(title=title, master=self.scrollable_frame).pack(
            padx=20, pady=10, fill='x', expand=True)

class ErrorLabel(customtkinter.CTkFrame):
    def __init__(self, title, master, **kwargs):
        super().__init__(master, **kwargs)
        customtkinter.CTkLabel(master=self, text=title).grid(
            row=0, column=0, padx=10, pady=10, sticky='ew')

class ProgressBar(customtkinter.CTkFrame):
    def __init__(self, title, master, **kwargs):
        super().__init__(master, **kwargs)

        self.progressbar = customtkinter.CTkProgressBar(
            master=self, mode='indeterminate')
        self.progressbar.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.title = title[:int(len(title) - len(title)/2)] + '...'

        self.label = customtkinter.CTkLabel(
            self, text=f'{self.title} processing...')
        self.label.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

    def done(self):
        self.label.configure(text=f'{self.title} done!')

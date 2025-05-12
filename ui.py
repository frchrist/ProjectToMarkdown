""" This file is part of ToMdConverter. """
import datetime
import os
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askdirectory
import process
import errors
APP_NAME = "To Md Converter"

class Commands:
    """
    This class is used to process the files and directories.
    It contains methods to select directories, process files, and save the output.
    """
    @staticmethod
    def process(root_dir,**kwargs) -> None:
        """"
        This method is used to process the files and directories. """
        try:
            out_name = process.processing(root_dir,**kwargs)
        except errors.FileProcessingException as e:
            print(f"ERROR [-] {e}")
            return None

        Commands.select_dir_and_save(out_name)

    @staticmethod
    def open_dir(title="choose your project folder") -> str:
        """
        This method is used to open the directory.
        """
        select_dir = askdirectory(title=title)
        if select_dir == "" or select_dir is None:
            return ""
        return select_dir

    @staticmethod
    def select_dir_and_save(filename:str) -> str:
        """"
        This method is used to select the directory and save the file.
        It uses the tkinter library to open a file dialog for the user to select a directory. 
        """
        dir_ = Commands.open_dir(title="Choose your file destination folder")
        path = os.path.join(dir,filename)
        shutil.copy(filename,path)
        os.remove(filename)
        return dir_

class UI(tk.Tk):
    """
    This class represents the main user interface for the application using the tkinter library. 
    It provides methods and layouts for user interaction, including selecting directories, 
    providing project information, and displaying logs.
    """
    def __init__(self) -> None:
        super().__init__()
        self.title(APP_NAME)
        self.geometry("650x400")
        self.resizable(0,0)
        self.entry_font = ("Helvetica", 13)
        self.info_frame = ttk.LabelFrame(self,text="Logs[+]", padding=10,)
        self.logs_var = tk.Text(self.info_frame)
        self.properties()
        self.setup_main_layout()

    def properties(self):
        """
        This method is used to set the properties of the main window.
        """
        self.main_project_dir_var = tk.StringVar()
        self.output_var = tk.StringVar()
        self.folder_and_files_var = tk.StringVar()
        #self.logs_var = tk.StringVar()

    def setup_main_layout(self):
        """
        This method is used to set up the main layout of the application."""
        self.create_main_label()
        self.create_file_info_side()
        self.create_log_side()

    def _process_ignore_content(self):
        self.folder_and_files_var.get()

    def create_main_label(self):
        """
        This method is used to create the main label of the application.
        """
        label = tk.Label(self, text="Convert it Now", font=("Helvetica", 16, "bold"), bg="#CDCDCD")
        label.pack(side=tk.TOP, fill=tk.X)

    def logging(self,func):
        """"
        This method is used to log the output of the application.
        """

    def update_entry_section(self,entry_var,value):
        """
        This method is used to update the entry variable with the selected directory.
        """
        if value in ("", None):
            return
        self.logs_var.config(state="normal")
        self.logs_var.insert(tk.END, f"[{datetime.datetime.now()}] Choosing folder\n")
        entry_var.set(value)
        self.logs_var.insert(tk.END, f"[{datetime.datetime.now()}] Choosing folder {value} Done\n")
        self.logs_var.config(state="disable")
    
    def create_file_info_side(self):
        """
        This method is used to create the file information side of the application. 
        """
        main_frame = tk.Frame(self, padx=10)
        info_frame = ttk.LabelFrame(main_frame,text="Information",padding=10)
        frame = tk.Frame(info_frame)
        tk.Label(frame, text="Select your project" ).grid(column=0, row=0)
        tk.Entry(frame, font=self.entry_font,
         textvariable=self.main_project_dir_var).grid(column=1,row=0)
        ttk.Button(frame,text="Select",
                   command=lambda :self.update_entry_section(self.main_project_dir_var,Commands.open_dir()
                    )).grid(column=3, row=0, ipady=3, padx=2)
        tk.Label(frame, text="Project name" ).grid(column=0, row=1)
        tk.Entry(frame, font=self.entry_font,textvariable=self.output_var).grid(column=1,row=1)
        ttk.Button(frame,text="Destination directory",
        ).grid(column=3, row=1, ipady=3, padx=2)


        ttk.Button(frame,text="Process",
        command=lambda : Commands.process(
            self.main_project_dir_var.get(),
            output=self.output_var.get(),sysout=self.insert_content_to_log )
            ).grid(column=0, row=3, ipady=3, pady=3, columnspan=3)

        frame.pack(padx=2, pady=2)
        info_frame.pack(side=tk.LEFT)

        ignores_frame = ttk.LabelFrame(main_frame, 
                                       text="Ignore file and folders", height=15, padding=10)
        folder_and_files_var = tk.Text(ignores_frame, 
                                       width=40, height=5, font=("Poppins",9,"italic"))
        folder_and_files_var.pack()

        ignores_frame.pack(side=tk.RIGHT)
        main_frame.pack(fill=tk.X)

    def create_log_side(self):
        """
            Create the log Text area.
        """
        self.logs_var.pack()
        self.logs_var.insert(tk.END,"[+]Start\n")
        self.logs_var.insert(tk.END,"[+]Success\n")
        self.logs_var.config(state="disable")
        self.info_frame.pack(fill=tk.X, padx=10)
    def insert_content_to_log(self, content : str):
        """
            Logging the content to the log window.
        """
        self.logs_var.config(state=tk.NORMAL)
        self.logs_var.insert(tk.END, f"[{datetime.datetime.now()}]{content}\n")
        self.logs_var.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = UI()
    root.mainloop()

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
    @staticmethod
    def process(root_dir,**kwargs):
        out_name = process.processing(root_dir,**kwargs)
        if out_name in errors.ERROR_CODE.ALL_E100:
            return
        Commands.selectDirAndSave(out_name)
    @staticmethod
    def openDir(title="choose your project folder") -> str:
        select_dir = askdirectory(title=title)
        if select_dir == "" or select_dir == None:
            return
        return select_dir

    @staticmethod
    def selectDirAndSave(filename:str) -> str:
        dir = Commands.openDir(title="Choose your file destination folder")
        path = os.path.join(dir,filename)
        shutil.copy(filename,path)
        os.remove(filename)
        return dir

class UI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(APP_NAME)
        self.geometry("650x400")
        self.resizable(0,0)
        self.properties()
        self.mainLayout()

    def properties(self):
        self.main_project_dir_var = tk.StringVar()
        self.output_var = tk.StringVar()
        self.folder_and_files_var = tk.StringVar()
        self.logs_var = tk.StringVar()

    def mainLayout(self):
        self.__MainLabel()

    def _process_ignore_content(self):
        self.folder_and_files_var.get()

    def __MainLabel(self):
        label = tk.Label(self, text="Convert it Now", font=("Helvetica", 16, "bold"), bg="#CDCDCD")
        label.pack(side=tk.TOP, fill=tk.X)
        self.__FileInformations()
        self.__LogsSections()

    def logging(self,func):
        pass

    def _updateEntry(self,entryVariable,value):
        if value == "" or value ==None:
            return
        self.logs_var.config(state="normal")
        self.logs_var.insert(tk.END, f"[{datetime.datetime.now()}] Choosing folder\n")
        entryVariable.set(value)
        self.logs_var.insert(tk.END, f"[{datetime.datetime.now()}] Choosing folder {value} Done\n")
        self.logs_var.config(state="disable")
    
    def _sysout(self, content : str):
       
        self.logs_var.config(state=tk.NORMAL)
        self.logs_var.insert(tk.END, f"[{datetime.datetime.now()}]{content}\n")
        self.logs_var.config(state=tk.DISABLED)



    def __FileInformations(self):
        self.Entryfont = ("Helvetica", 13)
        mainFrame = tk.Frame(self, padx=10)
        infoFrame = ttk.LabelFrame(mainFrame,text="Information",padding=10)
        frame = tk.Frame(infoFrame)
        tk.Label(frame, text="Select your project" ).grid(column=0, row=0)
        tk.Entry(frame, font=self.Entryfont,
         textvariable=self.main_project_dir_var).grid(column=1,row=0)

        ttk.Button(frame,text="Select", 
        command=lambda :self._updateEntry(self.main_project_dir_var,Commands.openDir())).grid(column=3, row=0, ipady=3, padx=2)
       
        tk.Label(frame, text="Project name" ).grid(column=0, row=1)


        tk.Entry(frame, font=self.Entryfont,textvariable=self.output_var).grid(column=1,row=1)
        ttk.Button(frame,text="Destination directory", 
        ).grid(column=3, row=1, ipady=3, padx=2)


        ttk.Button(frame,text="Process",
        command=lambda : Commands.process(
            self.main_project_dir_var.get(),
            output=self.output_var.get(),ignore_files_plus=[],ignore_dirs_plus=[],sysout=self._sysout )).grid(column=0, row=3, ipady=3, pady=3, columnspan=3)

        frame.pack(padx=2, pady=2)
        infoFrame.pack(side=tk.LEFT)

        ignoreFrame = ttk.LabelFrame(mainFrame, text="Ignore file and folders", height=15, padding=10)
        self.folder_and_files_var = tk.Text(ignoreFrame, width=40, height=5, font=("Poppins",9,"italic"))
        self.folder_and_files_var.pack()

        ignoreFrame.pack(side=tk.RIGHT)
        mainFrame.pack(fill=tk.X)

    def __LogsSections(self):
        infoFrame = ttk.LabelFrame(self,text="Logs[+]", padding=10,)
        self.logs_var = tk.Text(infoFrame)
        self.logs_var.pack()
        self.logs_var.insert(tk.END,"[+]Start\n")
        self.logs_var.insert(tk.END,"[+]Success\n")
        self.logs_var.config(state="disable")
        infoFrame.pack(fill=tk.X, padx=10)
if __name__ == "__main__":
    root = UI()
    root.mainloop()
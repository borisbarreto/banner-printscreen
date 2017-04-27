import os
import csv
import unittest
import pyautogui
import datetime
import tkinter as tk

from tkinter import ttk
from tkinter import filedialog
from time import sleep
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException

class Application(tk.Frame):
    running = True
    data_path = os.getcwd() +"\\data\\"

    def __init__(self, master = None):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)
        self.build_grid()
        self.build_title()
        self.build_buttons()
        self.build_content()
        self.build_credits()

    def build_grid(self):
        """ Create the grid base """
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)

    def build_title(self):
        """ Grid title """
        self.win_title = tk.Label(self,
            text="BANNER SCANNER",
            font = ('Helvetica', 14, 'bold')
            )
        self.win_title.grid(
            row=0, column=0,
            sticky='ew',
            pady=20
            )

    def build_buttons(self):
        """ Grid buttons start and stop """
        button_frame = tk.Frame(self)
        button_frame.grid(row=2,column=0, sticky='nsew',pady=15)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        self.start = ttk.Button(button_frame, text="Start", command=self.start)
        self.start.grid(row=0, column=0, sticky='e', padx=10)

        self.stop = ttk.Button(button_frame, text="Close", command=self.stop)
        self.stop.grid(row=0, column=1, sticky='w', padx=10)

    def build_content(self):
        """ Grid content - adrress and banner files in a csv files
        used for check the web address and banner names
        """
        self.content_frame = tk.Frame(self)
        self.content_frame.grid(row=1, column=0, sticky='nsew', pady=10)
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.columnconfigure(1, weight=1)
        self.content_frame.columnconfigure(3, weight=1)
        self.content_frame.rowconfigure(0, weight=1)
        self.content_frame.rowconfigure(1, weight=1)
        self.content_frame.rowconfigure(2, weight=1)
        self.content_frame.rowconfigure(3, weight=1)

        self.label1 = ttk.Label(self.content_frame, text="Web Sites")
        self.label1.grid(row=0,column=0, sticky="e", padx=5)

        self.default_text1 = tk.StringVar()
        self.default_text1.set("")
        self.text1 = ttk.Entry(
            self.content_frame,
            textvariable = self.default_text1
            )
        self.text1.grid(row=0, column=1, sticky="we")

        self.browse_button1 = ttk.Button(
            self.content_frame,
            text="Browse",
            command=self.web_file
            )
        self.browse_button1.grid(row=0, column=2, sticky="w")

        self.label2 = ttk.Label(self.content_frame, text="Banners")
        self.label2.grid(row=1,column=0, sticky="e", padx=5)

        self.default_text2 = tk.StringVar()
        self.default_text2.set("")
        self.text2 = ttk.Entry(
            self.content_frame,
            textvariable = self.default_text2
            )
        self.text2.grid(row=1, column=1, sticky="we")

        self.browse_button2 = ttk.Button(
            self.content_frame,
            text="Browse",
            command=self.banner_file
            )
        self.browse_button2.grid(row=1, column=2, sticky="w")

        self.label2 = ttk.Label(self.content_frame, text="Repeat times")
        self.label2.grid(row=2,column=0, sticky="e", padx=5)

        self.default_text3 = tk.StringVar()
        self.default_text3.set("10")
        self.text3 = ttk.Entry(
            self.content_frame,
            textvariable = self.default_text3
            )
        self.text3.grid(row=2, column=1, sticky="we")

        self.running_text1 = tk.StringVar()
        self.running_text1.set("")
        self.scan_message1 = ttk.Label(
            self.content_frame,
            textvariable=self.running_text1
            )
        self.scan_message1.grid(row=3, column=0, columnspan=4, pady=5)

    def build_credits(self):
        """ Author """
        self.win_credits = tk.Label(self,
            text="Created by: Boris Ivan Barreto",
            font = ('Helvetica', 9, 'italic')
            )
        self.win_credits.grid(
            row=3, column=0,
            sticky='e'
            )

    def scanning(self, web_path, banner_path, repeat_time_text):
        """ Open the banner class which will perform the process """
        Banners(
            websites = web_path,
            banners= banner_path,
            repeat_times=repeat_time_text
            ).start_runner()
        self.task_completed()

    def start(self):
        """ Check if cvs files exits before start the scanning """
        self.running = True
        chromedriver = os.getcwd() + "\\chromedriver.exe"
        pict_directory = os.getcwd() + "\\pictures"

        if not os.path.isdir(pict_directory):
            os.makedirs(pict_directory)

        if bool(self.text1.get()) and bool(self.text2.get()):
            web_path = self.text1.get()
            banner_path = self.text2.get()
            repeat_time_text = int(self.text3.get())
            if os.path.isfile(banner_path) and os.path.isfile(web_path):
                if os.path.isfile(chromedriver):
                    self.running_text1.set("*** Scanner started ****")
                    self.after(
                        1000,
                        self.scanning(web_path, banner_path, repeat_time_text)
                        )
                else:
                    self.running_text1.set("chromedriver is missing please " +
                        "download from source")
            else:
                self.running_text1.set("** Some csv file doesn't exist *****")
        else:
            self.running_text1.set("** The testing data is missing ****")

    def stop(self):
        """ Close the application """
        self.running = False
        root.destroy()

    def web_file(self):
        """ Open the explorer dialog to browse and select the
        file in csv file that contains the web addresses"""
        path_web_list = os.path.abspath(filedialog.askopenfilename(
            initialdir = "/",
            title = "Select the web file",
            filetypes = (("csv files","*.csv"),("All Files","*.*")))
            )
        self.default_text1.set(path_web_list)

    def banner_file(self):
        """ Open the explorer dialog to browse and select the
        file in csv file that contains the banners names """
        path_banner_list = os.path.abspath(filedialog.askopenfilename(
            initialdir = "/",
            title = "Select the banner file",
            filetypes = (("csv files","*.csv"),("All Files","*.*")))
            )
        self.default_text2.set(path_banner_list)

    def task_completed(self):
        """ Message which appers after the process is completed """
        self.running_text1.set("** Scanner Completed ****")

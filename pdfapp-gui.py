# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 00:24:07 2017

@author: Piotrek
"""

import threading
from tkinter import Tk, Label, OptionMenu, messagebox, Scrollbar, Listbox, RIGHT, LEFT, END, Text, Button, Y, Entry, \
    X, TOP, BOTTOM, StringVar, W, E, Frame, BOTH, NORMAL, DISABLED, IntVar, Checkbutton, SUNKEN, HORIZONTAL
from tkinter.filedialog import askopenfilename, askopenfilenames, asksaveasfile

from pdfapp import do_work


class PdfGui:
    def __init__(self, master):
        self.master = master
        master.title("PDF-App GUI")
        master.resizable(False, False)

        main_frame = Frame(master)
        top_frame = Frame(main_frame)
        bottom_frame = Frame(main_frame)

        label_input_path = Label(top_frame, text="Input file(s)")
        self.input_path = StringVar()
        input_path_field = Entry(top_frame, textvariable=self.input_path)
        input_browse_button = Button(top_frame, text="Browse", command=lambda: self.browse_multiple(self.input_path))

        self.add_bookmarks = IntVar()
        bookmarks_checkbox = Checkbutton(top_frame, text="Add bookmarks", variable=self.add_bookmarks)

        label_watermark_path = Label(top_frame, text="Watermark")
        self.watermark_path = StringVar()
        watermark_path_field = Entry(top_frame, textvariable=self.watermark_path)
        watermark_browse_button = Button(top_frame, text="Browse",
                                         command=lambda: self.browse_single(self.watermark_path,
                                                                            [("PDF files", "*.pdf")]))

        label_js_path = Label(top_frame, text="Javascript file")
        self.js_path = StringVar()
        js_path_field = Entry(top_frame, textvariable=self.js_path)
        js_browse_button = Button(top_frame, text="Browse", command=lambda: self.browse_single(self.js_path, [
            ("Javascript files", "*.js"), ("Any files", "*.*")]))

        label_js = Label(top_frame, text="Javascript")
        js_frame = Frame(top_frame)
        scrollbar = Scrollbar(js_frame)
        self.js_field = Text(js_frame, height=4, width=30)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.js_field.pack(side=LEFT, fill=Y)
        scrollbar.config(command=self.js_field.yview)
        self.js_field.config(yscrollcommand=scrollbar.set)

        self.encrypt = StringVar()
        label_encrypt = Label(top_frame, text="Encrypt")
        encrypt_field = Entry(top_frame, textvariable=self.encrypt)
        self.encryption = StringVar()
        encryptions = ["128bit", "40bit"]
        self.encryption.set(encryptions[0])
        encryption_dropdown = OptionMenu(top_frame, self.encryption, *encryptions)

        self.decrypt = StringVar()
        label_decrypt = Label(top_frame, text="Decrypt")
        decrypt_field = Entry(top_frame, textvariable=self.decrypt)

        label_rotation = Label(top_frame, text="Rotation")
        self.rotation = StringVar()
        rotations = [0, 90, 180, 270]
        self.rotation.set(rotations[0])
        rotation_dropdown = OptionMenu(top_frame, self.rotation, *rotations)

        self.start_button = Button(top_frame, text="Start", command=self.start)

        # self.progress_listbox = Listbox(bottomFrame)
        progress_listbox_frame = Frame(root, bd=0, relief=SUNKEN)
        xscrollbar = Scrollbar(progress_listbox_frame, orient=HORIZONTAL)
        yscrollbar = Scrollbar(progress_listbox_frame)
        xscrollbar.pack(side=BOTTOM, fill=X)
        yscrollbar.pack(side=RIGHT, fill=Y)
        self.progress_listbox = Listbox(progress_listbox_frame, xscrollcommand=xscrollbar.set,
                                        yscrollcommand=yscrollbar.set)
        self.progress_listbox.pack(fill=X)
        xscrollbar.config(command=self.progress_listbox.xview)
        yscrollbar.config(command=self.progress_listbox.yview)

        main_frame.pack(fill=BOTH, expand=True)
        top_frame.pack(fill=X, side=TOP, expand=False)

        label_input_path.grid(row=0, column=0, sticky=W + E)
        input_path_field.grid(row=0, column=1, sticky=W + E)
        input_browse_button.grid(row=0, column=2, sticky=W + E)

        bookmarks_checkbox.grid(row=1, column=0, columnspan=3, sticky=W + E)

        label_rotation.grid(row=2, column=0, sticky=W + E)
        rotation_dropdown.grid(row=2, column=1, columnspan=2, sticky=W + E)

        label_encrypt.grid(row=3, column=0, sticky=W + E)
        encrypt_field.grid(row=3, column=1, sticky=W + E)
        encryption_dropdown.grid(row=3, column=2, sticky=W + E)

        label_decrypt.grid(row=4, column=0, sticky=W + E)
        decrypt_field.grid(row=4, column=1, columnspan=2, sticky=W + E)

        label_watermark_path.grid(row=5, column=0, sticky=W + E)
        watermark_path_field.grid(row=5, column=1, sticky=W + E)
        watermark_browse_button.grid(row=5, column=2, sticky=W + E)

        label_js_path.grid(row=6, column=0, sticky=W + E)
        js_path_field.grid(row=6, column=1, sticky=W + E)
        js_browse_button.grid(row=6, column=2, sticky=W + E)

        label_js.grid(row=7, column=0, sticky=W + E)
        js_frame.grid(row=7, column=1, columnspan=2, sticky=W + E)

        self.start_button.grid(row=8, column=0, columnspan=3, sticky=W + E)

        bottom_frame.pack(fill=X, side=BOTTOM, expand=False)
        progress_listbox_frame.pack(fill=X)

    def browse_single(self, field, types):
        field.set(askopenfilename(filetypes=types))

    def browse_multiple(self, field):
        fnames = askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        splitted = self.master.tk.splitlist(fnames)
        paths = ""
        for file in splitted:
            paths += "%s;" % file
        field.set(paths[:-1])

    def start(self):
        if not self.input_path.get():
            messagebox.showerror("An error occurred", "No input files")
            return
        fname = asksaveasfile(defaultextension=".pdf",
                              filetypes=[("PDF file", "*.pdf"),
                                         ("All Files", "*.*")])
        inputs = self.input_path.get().split(';')

        rotation = None
        if int(self.rotation.get()) != 0:
            rotation = int(self.rotation.get())

        use_40bit = False
        if self.encryption.get() == "40bit":
            use_40bit = True

        js = self.js_field.get("1.0", END)
        if len(js) <= 1:
            js = None

        self.progress_listbox.delete(0, END)
        self.start_button.configure(state=DISABLED)
        work_thread = threading.Thread(target=do_work,
                                       args=[inputs, fname.name, self.encrypt.get(), use_40bit, self.decrypt.get(),
                                             rotation, self.watermark_path.get(), js, self.js_path.get(),
                                             self.add_bookmarks.get(), self.update_progress])
        work_thread.start()

    def update_progress(self, message, exit_code=None):
        print(message)
        self.progress_listbox.insert(END, message)
        if exit_code is not None:
            if exit_code == 0:
                messagebox.showinfo("Progress update", "Done")
            else:
                messagebox.showerror("Progress update", "Error occurred during processing")
            self.start_button.configure(state=NORMAL)


root = Tk()
my_gui = PdfGui(root)
root.mainloop()

#!/usr/bin/env python3

import os.path
import PyPDF2
import tkinter as tk
from tkinter import PhotoImage, filedialog, messagebox
from tkinter.ttk import *
from PIL import Image, ImageTk
import webbrowser as wb

def getFile():
    global file_input
    file_input = filedialog.askopenfilenames()


def pdf_merger():
    global file_input
    merge_pdfs = PyPDF2.PdfFileMerger()
    for pdf in file_input:
        merge_pdfs.append(open(pdf, 'rb'))
    file_output = filedialog.asksaveasfilename(defaultextension='.pdf')
    merge_pdfs.write(open(file_output, 'wb'))


def pdf_splitter():
    global file_input
    file_input = file_input[0]
    fname = os.path.splitext(os.path.basename(file_input))[0]
    pdf = PyPDF2.PdfFileReader(file_input)
    for page in range(pdf.getNumPages()):
        pdf_writer = PyPDF2.PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))
        output_filename = '{}_page_{}.pdf'.format(
            fname, page+1
        )
        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)


def help():
    wb.open("https://github.com/rusl2019/pdf-tools")

def about():
    about_button = messagebox.showinfo(
        title="about",
        message="Tools PDF Version {}\n\nCreated by ruslan\nMIT License".format(version)
)


if __name__ == "__main__":
    # --- init ---
    root = tk.Tk()
    root.wm_title("PDF Tool")
    version = "1.0.0"
    # --- Window ---
    canvas = tk.Canvas(root, width=400, height=400,
                       relief="raised", background="white")
    canvas.pack()
    p1 = PhotoImage(file="../img/favicon.png")
    root.iconphoto(False,p1)
    # --- logo ---
    logo = Image.open("../img/logo2.png")
    logo = ImageTk.PhotoImage(logo)
    logo_label = tk.Label(image=logo, background="white")
    logo_label.image = logo
    canvas.create_window(200, 75, window=logo_label)
    # --- menu ---
    menubar = tk.Menu(root)
    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="GitHub", command=help)
    helpmenu.add_command(label="About...", command=about)
    menubar.add_cascade(label="Help", menu=helpmenu)
    root.config(menu=menubar)
    # --- tombol select file ---
    browseButton = tk.Button(
        text="Select File", command=getFile, font=('helvetica', 12, 'bold'),
        background="#9D3BE1", foreground="#79FFA0"
    )
    canvas.create_window(200, 150, window=browseButton)
    # --- pdf merger ---
    pdfMerger = tk.Button(
        text='Merger PDF', command=pdf_merger, font=('helvetica', 12, 'bold'),
        background="#9D3BE1", foreground="#79FFA0"
    )
    canvas.create_window(200, 200, window=pdfMerger)
    # --- pdf splitter ---
    pdfSplitter = tk.Button(
        text='Splitter PDF', command=pdf_splitter, font=('helvetica', 12, 'bold'),
        background="#9D3BE1", foreground="#79FFA0"
    )
    canvas.create_window(200, 250, window=pdfSplitter)
    # --- loop app ---
    root.mainloop()

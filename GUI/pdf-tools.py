#!/usr/bin/env python3

import PyPDF2
import tkinter as tk
from tkinter import PhotoImage, filedialog, messagebox
import webbrowser as wb
import sys
import os
from PIL import Image

version = "1.1.0"

def getFile():
    global file_input
    file_input = filedialog.askopenfilenames(
        filetypes=[('file pdf', '*.pdf'), ('file gambar', '*.png *.jpg')],
        title="Pilih file"
    )
    file_input = list(file_input)
    tk.Label(root, text="*========================================*").pack()
    for file in file_input:
        tk.Label(root, text="File = {}".format(file), font=('helvetica', 10)).pack()


def pdf_merger():
    global file_input
    if file_input[0].split('.')[-1].lower() != 'pdf':
        messagebox.showerror(
            title="Error!!!", 
            message="File masukan bukan file PDF"
        )
        sys.exit(1)
    file_output = filedialog.asksaveasfilename(
        defaultextension='.pdf',
        filetypes=[("PDF files", '*.pdf')],
    )
    tk.Label(root, text="Menggabungkan file PDF ...", font=('helvetica', 10)).pack()
    merge_pdfs = PyPDF2.PdfFileMerger()
    for pdf in file_input:
        merge_pdfs.append(open(pdf, 'rb'))
    merge_pdfs.write(open(file_output, 'wb'))
    tk.Label(root, text="File disimpan di {}".format(os.path.dirname(file_output)), font=('helvetica', 10)).pack()
    tk.Label(root, text="*========================================*").pack()


def pdf_splitter():
    global file_input
    if file_input[0].split('.')[-1].lower() != 'pdf':
        messagebox.showerror(
            title="Error!!!", 
            message="File masukan bukan file PDF"
        )
        sys.exit(1)
    file_dir = filedialog.asksaveasfilename()
    tk.Label(root, text="Membagi file PDF ...", font=('helvetica', 10)).pack()
    file_input = file_input[0]
    pdf = PyPDF2.PdfFileReader(file_input)
    for page in range(pdf.getNumPages()):
        pdf_writer = PyPDF2.PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))
        output_filename = '_page_{}.pdf'.format(page+1)
        with open("{}{}".format(file_dir, output_filename), 'wb') as out:
            pdf_writer.write(out)
    tk.Label(root, text="File disimpan di {}".format(os.path.dirname(file_dir)), font=('helvetica', 10)).pack()
    tk.Label(root, text="*========================================*").pack()


def convertToPdf():
    global file_input
    export_file_path = filedialog.asksaveasfilename(defaultextension='.pdf')
    tk.Label(root, text="Mengkonversi file gambar ...", font=('helvetica', 10)).pack()
    tk.Label()
    imagelist = [ ]
    for name in file_input:
        file_name = Image.open(name)
        file = file_name.convert('RGB')
        imagelist.append(file)
    im1 = imagelist[0]
    imagelist.pop(0)
    im1.save(export_file_path, save_all=True, append_images=imagelist)
    tk.Label(root, text="File disimpan di {}".format(os.path.dirname(export_file_path)), font=('helvetica', 10)).pack()
    tk.Label(root, text="*========================================*").pack()


def GitHub():
    wb.open("https://github.com/rusl2019/pdf-tools")


def about():
    about_button = messagebox.showinfo(
        title="Tentang",
        message="Tools PDF Versi {}\n\nDibuat oleh ruslan\nLisensi MIT".format(version)
    )


if __name__ == "__main__":
    # --- init ---
    root = tk.Tk()
    root.wm_title("PDF Tools")
    # --- Window ---
    canvas = tk.Canvas(
        root,
        width=400,
        height=400,
        relief="raised",
        background="white"
    )
    canvas.pack()
    icon = PhotoImage(
        file="../img/favicon.png"
    )
    root.iconphoto(False,icon)
    # --- logo ---
    logo = PhotoImage(
        file="../img/logo2.png"
    )
    logo_label = tk.Label(
        image=logo, 
        background="white"
    )
    logo_label.image = logo
    canvas.create_window(
        200, 
        75, 
        window=logo_label
    )
    # --- menu ---
    menubar = tk.Menu(root)
    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="GitHub", command=GitHub)
    helpmenu.add_command(label="Tentang...", command=about)
    menubar.add_cascade(label="Bantuan", menu=helpmenu)
    root.config(menu=menubar)
    # --- tombol select file ---
    browseButton = tk.Button(
        text="Pilih file", 
        command=getFile, 
        font=('helvetica', 12, 'bold'),
        background="#9D3BE1", 
        foreground="#79FFA0"
    )
    canvas.create_window(200, 150, window=browseButton)
    # --- pdf merger ---
    pdfMerger = tk.Button(
        text='Gabungkan file PDF', 
        command=pdf_merger, 
        font=('helvetica', 12, 'bold'),
        background="#9D3BE1", 
        foreground="#79FFA0"
    )
    canvas.create_window(200, 200, window=pdfMerger)
    # --- pdf splitter ---
    pdfSplitter = tk.Button(
        text='Membagi file PDF', 
        command=pdf_splitter, 
        font=('helvetica', 12, 'bold'),
        background="#9D3BE1", 
        foreground="#79FFA0"
    )
    canvas.create_window(200, 250, window=pdfSplitter)
    # --- Img to PDF ---
    imgToPDF = tk.Button(
        text='Konversi File\nGambar Ke File PDF', 
        command=convertToPdf, 
        font=('helvetica', 12, 'bold'),
        background="#9D3BE1", 
        foreground="#79FFA0"
    )
    canvas.create_window(200, 300, window=imgToPDF)
    # --- loop app ---
    root.mainloop()

#!/usr/bin/env python

# Author: Rusl2019
# Date: 03/02/2021

"""
pdf-tools version 1.0.0

script untuk menggabungkan atau memisahkan file pdf

fitur :
    1. menggabungkan file pdf
    2. memisahkan file pdf
    3. mengkompres file pdf

memerlukan :
    Python 3
    PyPDF2 (Python Module)
    Ghostscript

catatan: untuk kompresi file pdf dapat memilih level

level kompresi:
    0: default
    1: prepress
    2: printer
    3: ebook
    4: screen
"""

import argparse
import subprocess
import os.path
import sys
import PyPDF2


def option():
    parser = argparse.ArgumentParser(
        usage="pdf-tools-cli.py -i input [input ...] [-o output] [-c (default 0)] [-s] [-m] [--open] [-h]",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '-i',
        metavar='input',
        nargs='+',
        help='file masukan dengan format PDF',
        required=True
    )
    parser.add_argument(
        '-o',
        metavar='output',
        help='file keluaran dengan format PDF (default file_output.pdf)',
        default="file_output.pdf"
    )
    parser.add_argument(
        '-m',
        action='store_true',
        default=False,
        help='menggabungkan file PDF'
    )
    parser.add_argument(
        '-s',
        action='store_true',
        default=False,
        help='memisahkan file PDF'
    )
    parser.add_argument(
        '-c',
        metavar='',
        type=int,
        help='level kompresi 0 sampai 4 (default 0)',
        default=0
    )
    parser.add_argument(
        '--open',
        action='store_true',
        default=False,
        help='buka PDF setelah digabung'
    )
    args = parser.parse_args()
    return args


def compress(input_file_path, power):
    """
    Author: Sylvain Carlioz
    Date: 06/03/2017
    GitHub: https://github.com/theeko74/pdfc
    Function to compress PDF via Ghostscript command line interface
    """
    quality = {
        0: '/default',
        1: '/prepress',
        2: '/printer',
        3: '/ebook',
        4: '/screen'
    }
    output_file_path = "compress.pdf"
    # Basic controls
    # Check if valid path
    if not os.path.isfile(input_file_path):
        print("Error: invalid path for input PDF file")
        sys.exit(1)
    # Check if file is a PDF by extension
    if input_file_path.split('.')[-1].lower() != 'pdf':
        print("Error: input file is not a PDF")
        sys.exit(1)
    print("Compress PDF...")
    subprocess.call(['gs', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
                     '-dPDFSETTINGS={}'.format(quality[power]),
                     '-dNOPAUSE', '-dQUIET', '-dBATCH',
                     '-sOutputFile={}'.format(output_file_path),
                     input_file_path]
                    )


def pdf_merger(file_name, file_output):
    print("Merge PDF...")
    merge_pdfs = PyPDF2.PdfFileMerger()
    for pdf in file_name:
        merge_pdfs.append(open(pdf, 'rb'))
    merge_pdfs.write(open(file_output, 'wb'))


def pdf_splitter(path):
    fname = os.path.splitext(os.path.basename(path))[0]
    pdf = PyPDF2.PdfFileReader(path)
    for page in range(pdf.getNumPages()):
        pdf_writer = PyPDF2.PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))
        output_filename = '{}_page_{}.pdf'.format(
            fname, page+1
        )
        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)
        print('Created: {}'.format(output_filename))


if __name__ == '__main__':

    version = "1.0.0"

    args = option()

    if args.m:
        pdf_merger(args.i, args.o)
        if args.c == 0:
            print("Tidak mengkompres PDF")
            size = os.path.getsize(args.o)
            print("Ukuran File: {0:.1f}MB".format(size / 1000000))
            print("Selesai.")
        else:
            file_name = args.o
            compress(file_name, args.c)
            initial_size = os.path.getsize(file_name)
            final_size = os.path.getsize("compress.pdf")
            ratio = 1 - (final_size / initial_size)
            print("Terkompresi {0:.0%}.".format(ratio))
            print("Ukuran File: {0:.1f}MB".format(final_size / 1000000))
            print("Selesai.")
    if args.s:
        pdf_splitter(args.i)
    if not args.m and not args.s:
        print("Pilih salah satu opsi antara merger (-m) atau splitter (-s) PDF!!!")

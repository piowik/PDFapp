# -*- coding: utf-8 -*-
"""
Created on Wed May 23 20:05:27 2018

@author: Piotrek
"""

import argparse
import time

from PyPDF2 import PdfFileWriter, PdfFileReader


def print_progress(message, exit_code=0):
    print(message)


def do_work(input_files, output_filename, encrypt, use_40bit, decrypt, rotate,
            watermark_path, javascript, javascript_file, add_bookmarks, progress_callback):
    start_time = time.time()
    progress_callback("PDF-App")
    output = PdfFileWriter()
    watermark = None  # shitty workaround
    if watermark_path:
        progress_callback("Loading watermark file %s" % watermark_path)
        watermark_pdf = PdfFileReader(watermark_path, "rb")
        watermark = watermark_pdf.getPage(0)
    for input_file in input_files:
        progress_callback("Processing %s" % input_file)
        pdf_file = PdfFileReader(input_file, "rb")
        if pdf_file.isEncrypted:
            if not decrypt:
                progress_callback("%s is encrypted, required password" % input_file, 1)
                return
            else:
                progress_callback("Decrypting %s" % input_file)
                decrypt_result = pdf_file.decrypt(decrypt)
                if decrypt_result == 0:
                    progress_callback("Couldn't decrypt file, wrong password?", 1)
                    return
                progress_callback("File decrypted")
        bookmark_added = False
        for i in range(pdf_file.getNumPages()):
            page = pdf_file.getPage(i)
            if rotate:
                page.rotateClockwise(rotate)
            if watermark_path:
                page.mergePage(watermark)

            output.addPage(page)
            if not bookmark_added and add_bookmarks:
                bookmark_page = output.getNumPages() - 1
                progress_callback("Adding bookmark at page %d" % bookmark_page)
                output.addBookmark(input_file, bookmark_page)
                bookmark_added = True
        progress_callback("File processed")
    if javascript:
        progress_callback("Adding javascript")
        output.addJS(javascript)
    if javascript_file:
        try:
            js_file = open(javascript_file, "rb")
        except IOError:
            progress_callback("Error opening javascript file", 1)
            return
        try:
            js = js_file.read()
        except:
            progress_callback("Error reading javascript file", 1)
            return
        output.addJS(str(js))
        js_file.close()

    if encrypt:
        progress_callback("Encrypting output with %s" % encrypt)
        output.encrypt(encrypt, use_128bit=use_40bit)

    progress_callback("Saving as %s" % output_filename)
    if encrypt:
        progress_callback("Saving encrypted file takes some time")

    with open(output_filename, 'wb') as f:
        try:
            output.write(f)
        except IOError:
            progress_callback("Error saving file", 1)
            return
        file_size = f.tell()
    summary_message = "Done. Pages: %d, File size: %.2f MB" % (output.getNumPages(), (file_size / 1024 / 1024))
    progress_callback(summary_message)
    progress_callback("Process took %s seconds" % (time.time() - start_time), 0)


if __name__ == "__main__":
    out_filename = "out.pdf"

    parser = argparse.ArgumentParser(prog="pdfapp")
    parser.add_argument("input", metavar="PATH", type=str, nargs='+',
                        help='input path(s), multiple files will be merged')
    parser.add_argument("-o", "--output", type=str, help="output path (default out.pdf)")  # OK
    parser.add_argument("-e", "--encrypt", type=str,
                        help="encrypt output file with password")  # OK
    parser.add_argument("--use_40bit", action='store_true', help="use 40 bit encryption instead of 128bit")  # OK
    parser.add_argument("--add_bookmarks", action='store_true',
                        help="add bookmarks pointing beginnings of merged PDFs")  # OK
    parser.add_argument("-d", "--decrypt", type=str, help="decrypt pdf file")  # OK
    parser.add_argument("--rotate", type=int, choices=[90, 180, 270],
                        help="clockwise rotation in degrees")  # OK
    parser.add_argument("--watermark", type=str, help="watermark .pdf path")  # OK
    parser.add_argument("-j", "--javascript", type=str, help="add javascript to pdf")  # OK
    parser.add_argument("-jf", "--javascriptfile", type=str, help="add javascript from file to pdf")  # OK
    args = parser.parse_args()

    if args.output:
        out_filename = args.output

    do_work(args.input, out_filename, args.encrypt, args.use_40bit, args.decrypt,
            args.rotate, args.watermark, args.javascript, args.javascriptfile, args.add_bookmarks, print_progress)

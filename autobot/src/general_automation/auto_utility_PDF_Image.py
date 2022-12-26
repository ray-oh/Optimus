#!/usr/bin/env python
# coding: utf-8

"""
Module:         generalAutomationScript.py
Description:    RPA automation with Excel front end
Created:        30 Jul 2022

Versions:
20210216    Refactor KB Quest code - reusable sub routines - sub_TXT_*
            helper functions - hoverClick, hoverRclick, waitImage, waitImageDisappear, try_catch
            Logging
            Reorganize assets - image, log, output folders

"""
from config import *

from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import os
from PyPDF4.pdf import PdfFileReader, PdfFileWriter

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))

def createPagePdf(numPages, tmp, pageHeight, title):
    # create pdf with title from bottom left X, Y
    c = canvas.Canvas(tmp)
    #c.drawString(10, 150, "Some text encoded in UTF-8")
    #c.drawString(10, 100, "In the Vera TT Font!")
    print(numPages, len(title))

    for i in range(1, numPages + 1):
        #c.drawString((210 // 2) * mm, (4) * mm, str(i))
        #c.setFillColorRGB(1,0,0) # font color RED, (255,255,255) white
        c.setFillColorRGB(255, 255, 0) # Yellow
        c.setFont('VeraBd', 22)
        c.drawString((25) * mm, pageHeight - (9) * mm, title[i-1])
        #c.drawString(10, 40, title[i-1])
        c.showPage()
    c.save()


def addContentPDF(pageTitlesList, sourcePDF, targetPDF):
    """
    Add page titles or numbers to a pdf, save the result as a new pdf
    @param pdf_path: path to pdf
    """
    tmp = "__tmp.pdf"

    output = PdfFileWriter()
    with open(sourcePDF, 'rb') as f:
        pdf = PdfFileReader(f, strict=False)
        n = pdf.getNumPages()
        #reader = PdfFileReader('./Output/my_images.pdf')
        #pageHeight = reader.pages[0].mediaBox.getHeight()
        pageHeight = int(pdf.pages[0].mediaBox.getHeight())
        print('page height', pageHeight)

        # create new PDF with page numbers
        createPagePdf(n, tmp, pageHeight, pageTitlesList)

        with open(tmp, 'rb') as ftmp:
            numberPdf = PdfFileReader(ftmp)
            # iterarte pages
            for p in range(n):
                page = pdf.getPage(p)
                numberLayer = numberPdf.getPage(p)
                # merge number page with actual page
                page.mergePage(numberLayer)
                output.addPage(page)

            # write result
            if output.getNumPages():
                #newpath = pdf_path[:-4] + file_extension
                with open(targetPDF, 'wb') as f:
                    output.write(f)
        os.remove(tmp)


from PIL import Image
def createPDFfromImages(files, path, saveFile):
    files = files
    iterator = map(lambda file: Image.open(path + file).convert('RGB'), files)
    image_list = list(iterator)
    image_list[0].save(saveFile, save_all=True, append_images=image_list[1:])
    return

#createPDFfromImages(['grid_Day_WHB.png', 'grid_MTD_WHB.png', 'grid_WTD_WHB.png'], './Output/20220717/', './Output/my_images.pdf')
#add_page_numbers('./Output/my_images.pdf')

from pathlib import Path, PureWindowsPath
def cropImage(files, savefiles, left, top, right, bottom, boolPercentage):
    # Importing Image class from PIL module
    #from PIL import Image
    i = 0
    #print('Files to crop:',files)
    for file in files:
        # Opens a image in RGB mode
        #im = Image.open(r"C:\Users\Admin\Pictures\geeks.png")
        im = Image.open(file)
        # Size of the image in pixels (size of original image)
        # (This is not mandatory)
        width, height = im.size
        print('      ','File:', Path(file).name, ' Size:', im.size)
        # Setting the points for cropped image
        if boolPercentage == True:
            if left is None: left = 0
            if top is None: top = 0        
            if right is None: right = 1
            if bottom is None: bottom = 1        
            left_ = int(left) * width
            top_ = int(top) * height
            right_ = int(right) * width
            bottom_ = int(bottom) * height
        else:
            if left is None: left = 0
            if top is None: top = 0        
            if right is None: right = width
            if bottom is None: bottom = height        
            left_ = int(left)
            top_ = int(top)
            right_ = int(right)
            bottom_ = int(bottom)
        
        #print(left_, top_, right_, bottom_)
        # Cropped image of above dimension
        # (It will not change original image)
        im1 = im.crop((left_, top_, right_, bottom_))
        
        # Shows the image in image viewer
        #im1.show()    

        im1.save(savefiles[i])
        i = i + 1
    return


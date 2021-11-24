import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from fpdf import FPDF
import os
from tkinter import *
from tkinter import filedialog
import PyPDF2

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

def generate_text(file):
    page = convert_from_path(file, 600)
    text = pytesseract.image_to_string(page[0])
    updated = text.replace('\n', ' ')
    updated = updated.replace(b'\xe2\x80\x94'.decode('utf-8'),'')
    t = updated.split(' ')
    return t

def create_path(name_array, root_dir):
    path_arr = []
    for names in name_array:
        single_path = root_dir + names + '.pdf'
        path_arr.append(single_path)

    print('path_arr')
    print(path_arr)
    return path_arr

def create_hyperlink(link_array):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=12)
    y_in = 20
    for names in link_array:
        text1 = names.split('.')[0]
        annotation = names.split('data/')[1]
        text = text1 + '_updated.pdf'
        print('generated_link')
        print(text)
        width = pdf.get_string_width(text)
        pdf.text(x=200, y=y_in, txt=annotation)
        pdf.link(x=200, y=y_in, w=width, h=5, link=text)
        y_in+=10
    pdf.output("hyperlink.pdf")

def final_pdf(watermark_pdf_path, pdf_path):

    map_pdf = open(pdf_path, 'rb')
    watermark_pdf = open(watermark_pdf_path, 'rb')

    pdfReader = PyPDF2.PdfFileReader(map_pdf, strict=False)
    pdfWatermarkReader = PyPDF2.PdfFileReader(watermark_pdf)
    pdfWriter = PyPDF2.PdfFileWriter()

    map_pdf_first_page = pdfReader.getPage(0)
    map_pdf_first_page.mergePage(pdfWatermarkReader.getPage(0))
    pdfWriter.addPage(map_pdf_first_page)

    intermediate_name = pdf_path.split('.')[0]
    new_path = intermediate_name + '_updated.pdf'
    resultPdfFile = open(new_path, 'wb')

    pdfWriter.write(resultPdfFile)
    map_pdf.close()
    watermark_pdf.close()
    resultPdfFile.close()

def generate_link(folder):
    pdf_files = os.listdir(folder)
    references = []
    complete_path = []
    for names in pdf_files:
        stripped = names.split('.')[0]
        references.append(stripped)
        path = folder + names
        complete_path.append(path)
    for paths in complete_path:
        text = generate_text(paths)
        drawing_list = []
        for i in text:
            for j in references:
                if i == j:
                    drawing_list.append(i)
        path_arr1 = create_path(drawing_list, folder)
        print(path_arr1)
        create_hyperlink(path_arr1)
        final_pdf("hyperlink.pdf", paths)
        print('file updated')


root = Tk()

myLabel2 = Label(root, text = 'Select Root Folder')
myLabel2.pack()
Path1 = ''
def open_infer():
    global Path1
    root.directory = filedialog.askdirectory()
    Path1 = str(root.directory) + r'/'
    myLabel3 = Label(root, text= 'you are annotating' + Path1)
    myLabel3.pack()

my_btn1 = Button(root, text = 'Select your file', command = open_infer).pack()

def myClick():
    generate_link(Path1)
    myLabel3 = Label(root, text= 'Your File is ready, check in folder')
    myLabel3.pack()

myButton = Button(root, text = 'Get linked docs', command = myClick)
myButton.pack()

root.mainloop()
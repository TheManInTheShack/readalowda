# ------------------------------------------------------------------------------
# For text extraction from multi-page pdfs where the text is stored as images
# Requires:
# ImageMagick 7.0 64-bit (with C/C++ bindings, in PATH and MAGICK_PATH)
# GhostScript (in PATH)
# Python 3.7 64-bit
# Python Library 'pip install wand'
# Python Library 'pip install pillow'
# Python Library 'pip install pytesseract'
# Python Library 'pip install numpy'
# Python Library 'pip install pandas'
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from datetime import datetime
import io
from PIL import Image
import pytesseract as pt
from wand.image import Image as wi

# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------

iname = "data\\Drive.pdf"
oname = "data\\drive.txt"

include_page_numbers = True

# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------
def main():
    # --------------------------------------------------------------------------
    # Start
    # --------------------------------------------------------------------------
    print("Starting procedure...")

    # --------------------------------------------------------------------------
    # Open the pdf and convert it to jpgs
    # --------------------------------------------------------------------------
    print("...loading pdf and reading as jpeg format...")
    pdf = wi(filename=iname, resolution=300)
    pdfImg = pdf.convert("jpeg")
    print("...pdf successfully loaded as images...")
    print(str(datetime.utcnow())[:20])
    
    # --------------------------------------------------------------------------
    # We're just holding those jpgs in memory, so we'll want to feed them to the
    # OCR function as bytestrings, or 'blobs'...we will have one for each page
    # --------------------------------------------------------------------------
    print("...converting image sequence to bytestrings...")
    imgBlobs = []
    for i, img in enumerate(pdfImg.sequence):
        page = wi(image=img)
        imgBlobs.append(page.make_blob('jpeg'))
    print("..." + str(i) + " images finished converting...")
    print(str(datetime.utcnow())[:20])
    
    # --------------------------------------------------------------------------
    # Go through the series of images and run the OCR on each one, adding the 
    # text to a running array as it goes
    # --------------------------------------------------------------------------
    print("...extracting text from images using OCR...")

    pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    extracted_text = []
    for i, imgBlob in enumerate(imgBlobs):
        im = Image.open(io.BytesIO(imgBlob))
        text = pt.image_to_string(im, lang='eng')
        extracted_text.append(text)
        if include_page_numbers:
            pageno_slug = "||PAGE:: " + str(i+1) + " ||"
            extracted_text.append(pageno_slug)
    print("...text extracted...")
    print(str(datetime.utcnow())[:20])
    
    # --------------------------------------------------------------------------
    # Dump extracted text to a simple .txt file
    # --------------------------------------------------------------------------
    print("...writing text data to file...")
    ofile = open(oname, "w")
    for line in extracted_text:
        print(line, file=ofile)
    print("...text file written...")
    print(str(datetime.utcnow())[:20])
    
    # --------------------------------------------------------------------------
    # Finish
    # --------------------------------------------------------------------------
    print("...finished!")

# ------------------------------------------------------------------------------
# Run
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    start_time = datetime.utcnow()
    main()
    end_time     = datetime.utcnow()
    elapsed_time = end_time - start_time
    print("Elapsed time: " + str(elapsed_time))



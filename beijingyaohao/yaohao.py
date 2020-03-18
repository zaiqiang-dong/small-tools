from urllib.request import urlopen
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from io import open

def readPDF(pdfFile):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    process_pdf(rsrcmgr, device, pdfFile)
    device.close()

    content = retstr.getvalue()
    retstr.close()
    return content
pdfFile = open("./t-1.pdf","rb")
outputString = readPDF(pdfFile)
sline = outputString.splitlines()
data = {}
for line in sline:
    line = line.strip()
    if len(line.split()) > 2:
        l = line.split()
        data[l[2]] = l[2][6:8]
print(data)
pdfFile.close()

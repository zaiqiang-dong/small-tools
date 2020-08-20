from PIL import Image
import sys

i = 1
j = 1
img = Image.open(sys.argv[1])

needW = 960;

width = img.size[0]
height = img.size[1]

needH = (height / width) * 960;

if(len(sys.argv) > 2 and sys.argv[2] == "c"):
    print("need exchange to gray picture first.")
    for i in range(0, width):
        for j in range(0, height):
            data = (img.getpixel((i, j)))
            if(len(data) >3 and data[3] == 0):
                img.putpixel((i,j),(255,255,255,0))
                continue
            gray = (data[0] * 30 + data[1] * 59 + data[2] * 11) / 100
            gray = int(gray)
            if(gray >= 86 * 2):
                img.putpixel((i,j),(255,255,255,255))
            elif(gray >= 86):
                img.putpixel((i,j),(62,175,124,255))
            else:
                img.putpixel((i,j),(44,62,80,255))
    imggt = img
    imggt = imggt.resize((needW, int(needH)))
    imggt.save("gt-" + sys.argv[1])

for i in range(0, width):
    for j in range(0, height):
        data = (img.getpixel((i, j)))
        if(len(data) >3 and data[3] == 0):
            img.putpixel((i,j),(255,255,255,0))
            continue
        gray = (data[0] * 30 + data[1] * 59 + data[2] * 11) / 100
        if(gray >= 240):
            img.putpixel((i,j),(255,255,255,255))
        else:
            img.putpixel((i,j),(44,62,80,255))

img = img.convert("RGB")
img = img.resize((needW, int(needH)))
img.save("t-" + sys.argv[1])

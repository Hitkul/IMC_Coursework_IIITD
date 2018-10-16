from PIL import Image
import sys
image_name = sys.argv[1]


def load_image(image_name):
    return im = Image.open(image_name)




im = load_image(image_name)

max_value = 255
p=1.2

im = Image.open('foo.jpg') # Can be many different formats.
pix = im.load()

for x in range(0,im.size[0]):
    for y in range(0,im.size[1]):
            # pix[x,y]=(max_value-pix[x,y][0],max_value-pix[x,y][1],max_value-pix[x,y][2])
            pix[x,y]=(int(pix[x,y][0]**p),int(pix[x,y][1]**p),int(pix[x,y][2]**p))


# print(pix[0,0])  # Get the RGBA Value of the a pixel of an image
# for x,y in enumerate(range(0,100)):
#     pix[x,y] = (0,0,0,255)  # Set the RGBA Value of the image (tuple)
im.save('alive_parrot.png')  # Save the modified pixels as .png
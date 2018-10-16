from PIL import Image
import sys
import copy

image_name = sys.argv[1]

max_value=255
def load_image(image_name):
    return Image.open(image_name)

def negate_pixel(pixel_tuple):
    return (max_value-pixel_tuple[0],max_value-pixel_tuple[1],max_value-pixel_tuple[2])

def brighten_or_darken_pixel(pixel_tuple,ration):
    return (int(pixel_tuple[0]**ration),int(pixel_tuple[1]**ration),int(pixel_tuple[2]**ration))

def write_image(image_object,image_name):
    image_object.save(image_name)


im = load_image(image_name)
negate = copy.deepcopy(im)
bright = copy.deepcopy(im)
darken = copy.deepcopy(im)

for x in range(0,im.size[0]):
    for y in range(0,im.size[1]):
        pix_negate = negate.load()
        pix_bright = bright.load()
        pix_darken = darken.load()
        pix_negate[x,y]=negate_pixel(pix_negate[x,y])
        pix_bright[x,y]=brighten_or_darken_pixel(pix_bright[x,y],1.2)
        pix_darken[x,y]=brighten_or_darken_pixel(pix_darken[x,y],0.6) 
        # pix[x,y]=(int(pix[x,y][0]**p),int(pix[x,y][1]**p),int(pix[x,y][2]**p))

write_image(negate,"negate.jpg")
write_image(bright,"bright.jpg")
write_image(darken,"darken.jpg")

# im = Image.open('foo.jpg') # Can be many different formats.
# pix = im.load()



# # print(pix[0,0])  # Get the RGBA Value of the a pixel of an image
# # for x,y in enumerate(range(0,100)):
# #     pix[x,y] = (0,0,0,255)  # Set the RGBA Value of the image (tuple)
# im.save('alive_parrot.png')  # Save the modified pixels as .png
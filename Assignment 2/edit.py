from PIL import Image

im = Image.open('foo.jpg') # Can be many different formats.
pix = im.load()
red_values = [pix[x,y][0] for x in range(0,im.size[0]) for y in range(0,im.size[1])]

print(max(red_values))  # Get the width and hight of the image for iterating over


# print(pix[0,0])  # Get the RGBA Value of the a pixel of an image
# for x,y in enumerate(range(0,100)):
#     pix[x,y] = (0,0,0,255)  # Set the RGBA Value of the image (tuple)
# im.save('alive_parrot.png')  # Save the modified pixels as .png
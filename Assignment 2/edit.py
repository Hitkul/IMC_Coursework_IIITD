from PIL import Image
import sys
import copy
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color

image_name = sys.argv[1]
source_image_name_for_style_transfer = sys.argv[2]

max_value=255
def load_image(image_name):
    return Image.open(image_name)

def negate_pixel(pixel_tuple):
    return (max_value-pixel_tuple[0],max_value-pixel_tuple[1],max_value-pixel_tuple[2])

def brighten_or_darken_pixel(pixel_tuple,ration):
    return (int(pixel_tuple[0]**ration),int(pixel_tuple[1]**ration),int(pixel_tuple[2]**ration))

def write_image(image_object,image_name):
    image_object.save(image_name)

def convert_pixel_rgb_to_lab(rgb_pixel_tuple):
    rgb = sRGBColor(rgb_pixel_tuple[0], rgb_pixel_tuple[1], rgb_pixel_tuple[2])
    lab = convert_color(rgb, LabColor)
    return (lab.lab_l,lab.lab_a,lab.lab_b)

def convert_pixel_lab_to_rgb(lab_pixel_tuple):
    lab = LabColor(lab_pixel_tuple[0],lab_pixel_tuple[1],lab_pixel_tuple[2])
    rgb = convert_color(lab, sRGBColor)
    return (rgb.rgb_r,rgb.rgb_g,rgb.rgb_b)

def style_transfer(source_image,target_image):
    source_pix_data = source_image.load()
    target_pix_data = target_image.load()
    
    rgb = sRGBColor(152, 255, 80)
    print(rgb)
    lab = convert_color(rgb, LabColor)
    print(lab.lab_l)
    rgb = convert_color(lab, sRGBColor)
    print(rgb)




im = load_image(image_name)
source_image = load_image(source_image_name_for_style_transfer)

style_transfer(source_image,im)


# negate = copy.deepcopy(im)
# bright = copy.deepcopy(im)
# darken = copy.deepcopy(im)

# for x in range(0,im.size[0]):
#     for y in range(0,im.size[1]):
#         pix_negate = negate.load()
#         pix_bright = bright.load()
#         pix_darken = darken.load()
#         pix_negate[x,y]=negate_pixel(pix_negate[x,y])
#         pix_bright[x,y]=brighten_or_darken_pixel(pix_bright[x,y],1.2)
#         pix_darken[x,y]=brighten_or_darken_pixel(pix_darken[x,y],0.6) 

# write_image(negate,"negate.jpg")
# write_image(bright,"bright.jpg")
# write_image(darken,"darken.jpg")
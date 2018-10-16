from PIL import Image
import sys
import copy
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color
import statistics

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
    # print("in here")
    lab = LabColor(lab_pixel_tuple[0],lab_pixel_tuple[1],lab_pixel_tuple[2])
    rgb = convert_color(lab, sRGBColor)
    return (int(rgb.rgb_r),int(rgb.rgb_g),int(rgb.rgb_b))

def get_mean_and_sd_for_each_channel(pix_data):
    l_data = [] 
    a_data = []
    b_data = []
    for x in range(0,len(pix_data)):
        for y in range(0,len(pix_data[0])):
            l_data.append(pix_data[x][y][0])
            a_data.append(pix_data[x][y][1])
            b_data.append(pix_data[x][y][2])
    mean_tuple = (statistics.mean(l_data),statistics.mean(a_data),statistics.mean(b_data)) 
    sd_tuple = (statistics.stdev(l_data),statistics.stdev(a_data),statistics.stdev(b_data)) 
    return mean_tuple,sd_tuple
    

def style_transfer(source_image,target_image):
    source_pix_rgb_data = source_image.load()
    target_pix_rgb_data = target_image.load()

    source_pix_lab_data = []
    target_pix_lab_data = []
    print("source color conversion")
    for x in range(0,source_image.size[0]):
        temp = []
        for y in range(0,source_image.size[1]):
            temp.append(convert_pixel_rgb_to_lab(source_pix_rgb_data[x,y]))
        source_pix_lab_data.append(temp)

    print("target color conversion")
    for x in range(0,target_image.size[0]):
        temp = []
        for y in range(0,target_image.size[1]):
            temp.append(convert_pixel_rgb_to_lab(target_pix_rgb_data[x,y]))
        target_pix_lab_data.append(temp)
    
    # print(target_pix_lab_data[0])
    # exit()
    print("source mean and sd")
    mean_source,sd_source = get_mean_and_sd_for_each_channel(source_pix_lab_data)
    print("target mean and sd")
    mean_target,sd_target = get_mean_and_sd_for_each_channel(target_pix_lab_data)

    # print(mean_source,sd_source)
    # print(mean_target,sd_target)
    
    print("doing style transfer")
    for x in range(0,len(target_pix_lab_data)):
        for y in range(0,len(target_pix_lab_data[0])):
            temp = []
            for k in range(0,len(target_pix_lab_data[0][0])):
                temp.append(((sd_source[k]/sd_target[k])*(target_pix_lab_data[x][y][k]-mean_target[k]))+mean_source[k])
            target_pix_lab_data[x][y]= tuple(temp)

    print("converting back to rgb")
    # print(target_image.size)
    # print(len(target_pix_lab_data),len(target_pix_lab_data[0]))
    # exit()
    for x in range(0,target_image.size[0]):
        for y in range(0,target_image.size[1]):
            # print(target_pix_lab_data[x][y])
            # temp = convert_pixel_lab_to_rgb(target_pix_lab_data[x][y])
            # print(temp)
            # print(target_pix_rgb_data[x][y])
            target_pix_rgb_data[x,y] = convert_pixel_lab_to_rgb(target_pix_lab_data[x][y])

    return target_image
    

    
    # rgb = sRGBColor(152, 255, 80)
    # print(rgb)
    # lab = convert_color(rgb, LabColor)
    # print(lab.lab_l)
    # rgb = convert_color(lab, sRGBColor)
    # print(rgb)




im = load_image(image_name)
source_image = load_image(source_image_name_for_style_transfer)

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

write_image(negate,"negate.jpg")
write_image(bright,"bright.jpg")
write_image(darken,"darken.jpg")


target_image = style_transfer(source_image,im)
write_image(target_image,"transfer.jpg")


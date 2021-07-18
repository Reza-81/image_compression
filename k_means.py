import random
import numpy as np
from PIL import Image


def distance(color_of_pixel, color_of_center):
    return abs((color_of_pixel[0]**2 + color_of_pixel[1]**2 + color_of_pixel[2]**2)**(1/2) - (color_of_center[0]**2 + color_of_center[1]**2 + color_of_center[2]**2)**(1/2))


def near_center(color_of_pixel, list_of_centers):
    dis = distance(color_of_pixel, list_of_centers[0])
    color_of_nearest_center = list_of_centers[0]
    for i in list_of_centers[1:]:
        color_of_center = i
        temp = distance(color_of_pixel, color_of_center)
        if temp < dis:
            dis = temp
            color_of_nearest_center = color_of_center
    return color_of_nearest_center


def new_centers(clusters, list_of_centers):
    new_list_of_centers = []
    for k in list_of_centers:
        temp = [0, 0, 0]
        flag = 0
        for i in range(len(clusters)):
            for j in range(len(clusters[0])):
                if k[0] == clusters[i][j][0] and k[1] == clusters[i][j][1] and k[2] == clusters[i][j][2]:
                    temp[0] += image.getpixel((i, j))[0]
                    temp[1] += image.getpixel((i, j))[1]
                    temp[2] += image.getpixel((i, j))[2]
                    flag += 1
        if flag != 0:
            new_list_of_centers += [(temp[0]/flag, temp[1]/flag, temp[2]/flag)]
    return new_list_of_centers


def accuracy(list_of_centers, new_list_of_centers):
    global the_accuracy
    for i in range(len(list_of_centers)):
        delta_r = abs(list_of_centers[i][0] - new_list_of_centers[i][0])
        delta_g = abs(list_of_centers[i][1] - new_list_of_centers[i][1])
        delta_b = abs(list_of_centers[i][2] - new_list_of_centers[i][2])
        temp = (delta_r + delta_g + delta_b)
        if temp < the_accuracy:
            return True
        else:
            return False


number_of_centers = int(input('number of centers: '))
the_accuracy = float(input('the accuracy: '))
image=Image.open('your_directory')
width, height = image.size

list_of_centers = []

h = random.sample(range(height), number_of_centers)
w = random.sample(range(width), number_of_centers)
for i in list(zip(w, h)):
    list_of_centers += [image.getpixel(i)]

clusters = np.zeros((width, height, 3))
for i in range(width):
    for j in range(height):
        clusters[i,j] = near_center(image.getpixel((i,j)), list_of_centers)

new_list_of_centers = new_centers(clusters, list_of_centers)
while(not accuracy(list_of_centers, new_list_of_centers)):
    list_of_centers = new_list_of_centers
    for i in range(width):
        for j in range(height):
            clusters[i,j] = near_center(image.getpixel((i,j)), list_of_centers)
    new_list_of_centers = new_centers(clusters, list_of_centers)

clusters = np.array(clusters, dtype=np.uint8)
img = Image.fromarray(clusters)
img.save('your_directory')
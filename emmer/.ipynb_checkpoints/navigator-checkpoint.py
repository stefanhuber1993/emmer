import os
import numpy as np
import matplotlib.pyplot as plt

def get_acquired_images_from_navigator(navfile, first_item):
    nav_text = open(navfile, "r").read()
    nav_text = [i for i in nav_text.split('\n') if i!='']
    nav_text_numbers = [i for i in nav_text if i[0]=='[']
    nav_text_pos = [i for i in nav_text if i[0:2]=='St']
    numbers = []
    coords = []
    for n,pos in zip(nav_text_numbers[first_item-1:],nav_text_pos[first_item-1:]):
        number = [int(s) for s in n[:-1].split() if s.isdigit()][0]
        numbers.append(number)
        coord = []
        for t in pos.split():
            try:
                coord.append(float(t))
            except ValueError:
                pass
        coords.append(coord)
    numbers = np.array(numbers); coords = np.array(coords)[:,0:2]; coords = np.flip(coords, 1)
    return numbers, coords

def rotate_coordinates(coords, angle, normalize=True):
    """Angle is in degrees, anticlockwise from x-axis"""
    theta = np.radians(angle)
    r = np.array(( (np.cos(theta), -np.sin(theta)),
               (np.sin(theta),  np.cos(theta)) ))
    shape = coords.shape
    coords_rot = r.dot(coords.reshape(-1,2).T).T
    if normalize:
        coords_rot -= coords_rot.mean(0)
    coords_rot = coords_rot.reshape(shape)
    return coords_rot
    
def plot_membrane(image_rot, ex, stretch, x_shift, y_shift, xlim, ylim, dpi=150):
    fig,ax = plt.subplots(figsize=(7.5, 5), dpi=dpi)
    plt.imshow(image_rot, extent=[-ex+x_shift,ex+x_shift,-ex*stretch+y_shift,ex*stretch+y_shift], cmap='gray')
    plt.xlabel('x [um]'); plt.ylabel('y [um]'); 
    plt.gca().set_aspect(1)
    plt.xlim(xlim); plt.ylim(ylim)
    return fig,ax
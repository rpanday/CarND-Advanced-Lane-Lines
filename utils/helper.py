import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import pickle

# Here I put all the functions used in notebook after they are working successfully to reduce size of jupyter notebook and keep things easier to manage and read

def save_image(path, img):
#     plt.imsave(path, img)
    cv2.imwrite(path, img)

def read_image(img_path):
    #read img
    #return mpimg.imread(img_path) #RGB
    return cv2.imread(img_path) #BGR

def show_before_after(before, after):
    # Visualize undistortion
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(20,10))
    ax1.imshow(before)
    ax1.set_title('Original Image', fontsize=30)
    ax2.imshow(after)
    ax2.set_title('Processed Image', fontsize=30)
    
def show_images(img1, img2=None, title1='before', title2='after', fontsize=30):
    """Display 1 or 2 images
    
    Parameters
    ----------
    img1 : numpy.ndarray
        image 1 (BGR format)
    title1 : str
        title 1
    img2 : numpy.ndarray, None
        image 2 (BGR format)
    title2 : str, None
        title 2
    fontsize : int
        the font size for the image titles
    
    """
    # Visualize the images
    if img2 is None:
        f, ax1 = plt.subplots(1, 1, figsize=(20,10))
    else:
        f, (ax1, ax2) = plt.subplots(1, 2, figsize=(20,10))
        
        # show image 2
        if len(img2.shape) == 2:
            ax2.imshow(img2, cmap='gray')
        else:
            ax2.imshow(img2[:,:,::-1])
        ax2.set_title(title2, fontsize=fontsize)
        
    # show image 1
    if len(img1.shape) == 2:
        ax1.imshow(img1, cmap='gray')
    else:
        ax1.imshow(img1[:,:,::-1])
    ax1.set_title(title1, fontsize=30)
    
    plt.show()
    
import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import pickle

from utils.helper import *

def calibrate_camera(calibrate_img_paths, nx, ny, outDir = None):
    '''
    given calibration images as input (calibrate_img_paths) and their number of inside corners in x,y (nx, ny)
    return the camera calibration matrix (mtx) and distortion corefficients (dist) and use these later down the pipeline
    code used from lesson: https://classroom.udacity.com/nanodegrees/nd013/parts/edf28735-efc1-4b99-8fbb-ba9c432239c8/modules/5d1efbaa-27d0-4ad5-a67a-48729ccebd9c/lessons/78afdfc4-f0fa-4505-b890-5d8e6319e15c/concepts/5415176a-d615-49af-8535-53a385768a23
    repo: https://github.com/udacity/CarND-Camera-Calibration
    '''
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((ny*nx,3), np.float32)
    objp[:,:2] = np.mgrid[0:nx, 0:ny].T.reshape(-1,2)
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d points in real world space
    imgpoints = [] # 2d points in image plane.
    img_size = None
    # Step through the list and search for chessboard corners
    for idx, fname in enumerate(calibrate_img_paths):
#         print(idx)
        img = cv2.imread(fname)
        if img_size == None:
            img_size = (img.shape[1], img.shape[0])
        #convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, (nx,ny), None)
        # If found, add object points, image points
        if ret == True:
            objpoints.append(objp)
            imgpoints.append(corners)
            # Draw and display the corners
            cv2.drawChessboardCorners(img, (nx,ny), corners, ret)
            if outDir != None:
                write_name = '{}/calibration_corners{}.jpg'.format(outDir, str(idx+1))
                save_image(write_name, img)
                if(idx < 2):
                    show_images(img, None, write_name) #display some samples
        
    # Do camera calibration given object points and image points
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_size,None,None)
    return mtx, dist    

def undistort(mtx, dist, raw_image_paths, outDir = None):
    all_images = []
    for idx, fname in enumerate(raw_image_paths):
        img = cv2.imread(fname)
        dst = cv2.undistort(img, mtx, dist, None, mtx)
        if outDir != None:
            write_name = '{}/undist_{}'.format(outDir,os.path.basename(fname)) 
            save_image(write_name,dst)
            if(idx < 2):
                show_images(img,dst,fname,write_name) #display some samples


import cv2
import numpy as np

from utils import line
from utils import threshold
from utils import camera
from utils import fit_lane

# Define a class to receive the characteristics of each line detection
class Processor():
    def __init__(self, Mtx, Dist, line):
#         self.M = M
#         self.Minv = Minv
        self.Mtx = Mtx
        self.Dist = Dist
        self.line = line
        
    def fit_lane_on_frame(self, img):
        copy_image = np.copy(img)
        img_size = (img.shape[1], img.shape[0])
        bin_thresholded = threshold.white_yellow_threshold(copy_image)
        binary_warped, M, Minv = camera.perspective_transform(bin_thresholded)
        
        # HYPERPARAMETERS
        window_height = 80 # Break image into 9 vertical layers since image height is 720
        # Choose the number of sliding windows 720 (frame height)/80 (window height) = 9
        nwindows = 9
        # Set the width of the windows +/- margin
        margin = 100
        # Set minimum number of pixels found to recenter window
        minpix = 50
        
        left_fit = None
        right_fit = None
        if self.line.detected:
            left_fit = self.line.left_fit
            right_fit = self.line.right_fit

        if not self.line.detected:
            leftx, lefty, rightx, righty, out_img = fit_lane.find_lane_pixels(binary_warped, nwindows, margin, minpix)
            left_fit, right_fit, left_fitx, right_fitx, ploty = fit_lane.fit_poly(binary_warped.shape, leftx, lefty, rightx, righty)
            self.line.detected = True
            self.line.set_fits(left_fit, right_fit)
        else:
            leftx, lefty, rightx, righty = fit_lane.find_lane_pixels_with_prev_fit(binary_warped, left_fit, right_fit, margin)
            left_fit, right_fit, left_fitx, right_fitx, ploty = fit_lane.fit_poly(binary_warped.shape, leftx, lefty, rightx, righty)
            self.line.update_fits(left_fit, right_fit)
            
        undistorted_image = cv2.undistort(copy_image, self.Mtx, self.Dist)
        result = fit_lane.find_lane_pixels_with_prev_fit2(undistorted_image, binary_warped, self.line.left_fit, self.line.right_fit, Minv)
            
        cv2.putText(result,'Radius of Curvature: %.2fm' % self.line.radius_of_curvature,(20,40), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
        position_from_center = self.line.line_base_pos
        if position_from_center < 0:
            text = 'left'
        else:
            text = 'right'
        cv2.putText(result,'Distance From Center: %.2fm %s' % (np.absolute(position_from_center), text),(20,80), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
        
        return result
            

        
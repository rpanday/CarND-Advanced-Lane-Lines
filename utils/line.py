import cv2
import numpy as np

# Define a class to receive the characteristics of each line detection
class Line():
    def __init__(self):
        # was the line detected in the last iteration?
        self.detected = False  
        # x values of the last n fits of the line
        self.recent_xfitted = [] 
        #average x values of the fitted line over the last n iterations
        self.bestx = None     
        #polynomial coefficients averaged over the last n iterations
        self.best_fit = None  
        #polynomial coefficients for the most recent fit
        self.current_fit = [np.array([False])]  
        #radius of curvature of the line in some units
        self.radius_of_curvature = None 
        #distance in meters of vehicle center from the line
        self.line_base_pos = None 
        #difference in fit coefficients between last and new fits
        self.diffs = np.array([0,0,0], dtype='float') 
        #x values for detected line pixels
        self.allx = None  
        #y values for detected line pixels
        self.ally = None  
        
        self.y_eval = 700
        self.midx = 640
        self.ym_per_pix = 3.0/72.0 # meters per pixel in y dimension
        self.xm_per_pix = 3.7/660.0 # meters per pixel in x dimension
        
        self.left_fit = [np.array([False])]
        self.right_fit = [np.array([False])]
        
    def set_radius_of_curvature(self):
        y1 = (2*self.left_fit[0]*self.y_eval + self.left_fit[1])*self.xm_per_pix/self.ym_per_pix
        y2 = 2*self.left_fit[0]*self.xm_per_pix/(self.ym_per_pix*self.ym_per_pix)
        self.radius_of_curvature = ((1 + y1*y1)**(1.5))/np.absolute(y2)
        
    def set_position_from_center(self):
        x_left_pix = self.left_fit[0]*(self.y_eval**2) + self.left_fit[1]*self.y_eval + self.left_fit[2]
        x_right_pix = self.right_fit[0]*(self.y_eval**2) + self.right_fit[1]*self.y_eval + self.right_fit[2]
        
        self.line_base_pos = ((x_left_pix + x_right_pix)/2.0 - self.midx) * self.xm_per_pix
    
    def set_fits(self, left_fit, right_fit):
        self.left_fit = left_fit
        self.right_fit = right_fit
        self.detected = True
        self.set_radius_of_curvature()
        self.set_position_from_center()
    
    def update_fits(self, left_fit, right_fit):
        tolerance = 0.01
        left_error = ((self.left_fit[0] - left_fit[0]) ** 2).mean(axis=None)      
        right_error = ((self.right_fit[0] - right_fit[0]) ** 2).mean(axis=None)        
        if left_error < tolerance:
            self.left_fit = 0.75 * self.left_fit + 0.25 * left_fit   
        if right_error < tolerance:
            self.right_fit = 0.75 * self.right_fit + 0.25 * right_fit
            
        if self.detected:    
            self.set_radius_of_curvature()
            self.set_position_from_center()
        
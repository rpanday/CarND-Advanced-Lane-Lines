import numpy as np
import cv2

def s_channel_l_channel_sobelx_threshold(undistorted, s_thresh=(90, 255), sx_thresh=(20, 100)):
    undistorted = np.copy(undistorted)
    # Convert to HLS color space and separate the V channel
    hls = cv2.cvtColor(undistorted, cv2.COLOR_BGR2HLS)
    l_channel = hls[:,:,1]
    s_channel = hls[:,:,2]
    # Sobel x
    sobelx = cv2.Sobel(s_channel, cv2.CV_64F, 1, 0, ksize=5) # Take the derivative in x
    abs_sobelx = np.absolute(sobelx) # Absolute x derivative to accentuate lines away from horizontal
    scaled_sobel = np.uint8(255*abs_sobelx/np.max(abs_sobelx))
    
    # Threshold x gradient
    sxbinary = np.zeros_like(scaled_sobel)
    sxbinary[(scaled_sobel >= sx_thresh[0]) & (scaled_sobel <= sx_thresh[1])] = 1
    
    # Threshold color channel
    l_binary = np.zeros_like(l_channel)
    l_binary[(l_channel >= 255)] = 1
    s_binary = np.zeros_like(s_channel)
    s_binary[(s_channel >= s_thresh[0]) & (s_channel <= s_thresh[1])] = 1

    # Stack each channel
#     binary = np.dstack(( sxbinary, sxbinary, s_binary)) * 255 #BGR
#     binary = cv2.addWeighted(sxbinary, 1.0, l_binary, 1.0, 0)
#     binary = cv2.addWeighted(l_binary, 1.0, binary, 1.0, 0)
#     return binary
    # Combine the two binary thresholds
    combined_binary = np.zeros_like(sxbinary)
    combined_binary[(sxbinary == 1) | (l_binary == 1) & (s_binary == 1)] = 1
    return combined_binary



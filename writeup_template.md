**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./output_images/undistortedchess.png "Undistorted"
[image2]: ./output_images/undistortion%20on%20frame.png "Road Transformed"
[image3]: ./output_images/perspective.png "Binary Example"
[image4]: ./output_images/perspective.png "Warp Example"
[image5]: ./output_images/lanedetected.png "Fit Visual"
[image6]: ./output_images/result.png "Output"
[video1]: ./output_video/project_video_output.mp4 "Video"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---

### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  
This readme will cover all the rubric points with details.

### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for camera calibration is in file `camera.py` under `utils/` folder. I collected all the `object points` and `image points` using the `cv2.findChessboardCorners()` function and later used `cv2.calibrateCamera()` function to get camera matrix `mtx` and distortion coefficients `dist`. It can be seen in the second cell of workbook `Workbook-Final`. I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result: 

![alt text][image1]

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

To demonstrate this step, I will describe how I apply the distortion correction to one of the test images like this one. Excuse the wonky colors because my show images was confused between gray and colored but the flattening can be seen in the car to the right.
![alt text][image2]

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

First I tried using the light threashold and sobelx gradient method but the results had a lot of noise. Later I used color masks for while and yellow color which has less noise. The code is in `/utils/threshold.py` file. Here's an example of my output for this step.  

![alt text][image3]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for my perspective transform includes a function called `perspective_transform()` in file `/utils/camera.py`. This is also demonstrated in workbook with images. I have applied the transform on the thresholded image because the next step was to histogram on this image to detect lane lines. I chose the hardcode the source and destination points in the following manner:

```python
src = np.float32([
        [590,446],
        [690,446],
        [1130,670],
        [150, 670],
    ])
    
offsetx = 200
offsety = 0
img_size = (img.shape[1], img.shape[0])
dst = np.float32([[offsetx, offsety], [img_size[0]-offsetx, offsety], 
                                     [img_size[0]-offsetx, img_size[1]-offsety], 
                                     [offsetx, img_size[1]-offsety]])
```

This resulted in the following source and destination points:

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image.

![alt text][image4]

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

First I tried to use windows centroid approach to detect lanes but due to inconsistent nature of lane lines, results were not good. Later I used the sliding window approach in file `/utils/fit_lane.py` (method `find_lane_pixels()`) to get the left/right fit for lane-lines and used `fit_poly()` function in same file to fit a 2nd degree polynomial on the points detected as lane lines. This gave a smooth extended lane line on both side. 
To make the process faster, I reused the fit values from previous approach to fit polynomial on lane lines in next frames. Here is the result: 

![alt text][image5]

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

I used the code from the Lesson 9, section Measure curvature II to calculate radius of curvature and position of vehicle was calculated with respect to the center. I also used the conversions of pixel to meters given in the lesson to calculate the values in meters. The code is in file `/utils/line.py` method `set_radius_of_curvature()` and `set_position_from_center()`. There is also a cell in the workbook which shows this calculation with results on test image.

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

Here is the result on the test image.

![alt text][image6]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./output_video/project_video_output.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

I faced a lot of problems while working out the coordinates for perspective transform. Next I faced issue in thresholding the image because there are so many approaches. Finding the one with optimum output and least noise with good adjustment of parameters was a challenge. Finally I had failures in detecting lane lines and tried multiple approaches related to window centroids, then sliding window but had failures on few frames due to bad fit. I would again wonder whether the fits are bad or there is problem with thresholding. 
This code fails on the challenge video because of failure to fit the lane lines. To make it more robust, I guess a fallback approach for lane line detection is needed. I also think due to dynamic nature of scenes and light conditions that arrive while driving, thresholding criterias will also change dyanmically according to frame.

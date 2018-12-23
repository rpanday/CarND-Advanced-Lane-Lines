
def undistort_bulk(paths, outDir=None):
    #load pickled mtx, dist & run undistort
    # load the object from the file into var b
    pickle_load = pickle.load(open("{}/mtx_dist_pickle.p".format(outDirectory),'rb'))  
    # print(pickle_load)
    camera.undistort(pickle_load['mtx'], pickle_load['dist'], paths, outDir)
    print('undistortion completed')

outDirectory = 'camera_cal_out' 
undistort_bulk(calibrate_img_paths, outDirectory)
###########################################################
def sobel_thresh_bad():
    for p in glob.glob('test_images/*.jpg'):
        undist = plt.imread(p)
        binary = threshold.s_channel_l_channel_sobelx_threshold(undist)
        binary2 = threshold.threshold(undist)
        helper.show_images(binary, binary2) #display some samples
    
# sobel_thresh_bad()

#########################################################
Attempt 1 at fitting Lane using centroids (BAD DETECTION)
Finding fit with windows centroids did not turn out great. The lane with non-continous line almost gets swayed towards the other lane. The results can be seen below.

from utils import fit_lane_window_centroids as centroid

def run_window_centroids_fit_lane():
    # window settings
    window_width = 50 
    window_height = 80 # Break image into 9 vertical layers since image height is 720
    margin = 100 # How much to slide left and right for searching

    for p in glob.glob('output_images/undist_*.jpg')[:2]: #just process 2 frames
        undist = cv2.imread(p)
        warped,_,_ = camera.perspective_transform(threshold.s_channel_l_channel_sobelx_threshold(undist))
        lane = centroid.detect_lane_pixel(warped, window_width, window_height, margin)
        helper.show_images(undist, lane, p) #display some samples
        break #bad result, just exit
        
# run_window_centroids_fit_lane()

###########################################


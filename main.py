#!/usr/bin/env python

# Personal libraries
import dil_ero
from general import *
from ploting import *
from calculation import *


def generate(cap, to_show, to_print, to_video, rotate):
    
    try:
        # if imutils.is_cv2():
        fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
        #elif imutils.is_cv3():
    except:
        fps = cap.get(cv2.CAP_PROP_FPS)
    if ( not fps ):
        fps = 30.0
    print "Frames per second (fps): {0}".format(fps)
    ifps = int(fps)

    # Capture first frame
    ret, frame = cap.read()

    # resize image
    # frame = imutils.resize(frame, width=600)
    height, width, layers =  frame.shape
    print "Dimensions: ", height, width, layers

    if (to_video):
        name_out = out_path + out_video + ((path.split("/")[-1:])[0]).split(".")[0] + ".avi"
        try:
            video = cv2.VideoWriter(name_out,cv2.cv.FOURCC('M','J','P','G'), 15, (width,height))
        except:
            video = cv2.VideoWriter(name_out,cv2.cv.FOURCC('M','J','P','G'), 15, (width,height))
        print name_out

    color = 'yellow'
    color_type = 'BGR'
    lower, upper = set_color(color, color_type)
    y = np.zeros(ifps)
    frame_count = 0
    
    fixed = [ rotate, color_type, lower, upper, fps, ifps, width, height ]
    complement = [0, 0, 0]

    while(frame is not None):

        # Calling calculation function
        compact = [ frame, y, frame_count ]
        
        frame, nope, res, k_mask, start_coord, track_start_second, track_start_frame_count  =  frequency_check( compact, fixed, complement )
        
        complement = [ start_coord, track_start_second, track_start_frame_count ]


        display(k_mask, res, to_show, to_print, to_video)
        if (to_video):
            video.write(res)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Capture frame-by-frame
        ret, frame = cap.read()
        frame_count += 1


    # When everything done, release the capture
    print "TERMINOU"
    if (to_video):
        video.release()
    cap.release()
    cv2.destroyAllWindows()



def ocv():
    print cv2.getBuildInformation()


if __name__ == "__main__":

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="path to the video. Write 'webcam' if you wish on real time entry")
    ap.add_argument("-s", "--show", action='store_true', help="add this if you would like to open images while program is running")
    ap.add_argument("-p", "--print", action='store_true', help="add this if you would like to save the frames on ../outputs_rcp/image_frames/")
    ap.add_argument("-pv", "--printVideo", action='store_true', help="add this if you would like to save video on ../outputs_rcp/videos/")
    ap.add_argument("-pl", "--plot", action='store_true', help="add this if you would like to show the graphic plotted")
    ap.add_argument("-r", "--rotate", required=False, help="optional entry to rotate images")
    ap.add_argument("-v", "--version", action='version', version="Analisador_RCP 1.0 [x86_64-linux]" )
    # ap.add_argument("--info", action='version', version=ocv(), help="show opencv version and details" )
    args = vars(ap.parse_args())

    path = args["input"]
    to_show = args["show"]
    to_print = args["print"]
    to_video = args["printVideo"]
    to_plot = args["plot"]
    rotate = (float(args['rotate']) if (args['rotate']) else 0.0)

    print "To show: ", to_show
    print "To print: ", to_print
    print "To print video: ", to_video
    print "To plot: ", to_plot
    print "To rotate: ", rotate
    print path
    
    if (to_print or to_video):
        setup()


    # to the webcam
    if path == "webcam":
    	cap = cv2.VideoCapture(0)
    # otherwise, grab a reference to the video file
    else:
        cap = cv2.VideoCapture(path)

    # Check if camera opened successfully
    if (cap.isOpened() == False):
        print("Error opening video stream or file")


    if ( to_plot ):
        anim = animation.FuncAnimation(fig, animate, frames=generate_with_plot(cap, to_show, to_print, to_video, rotate),
                                    init_func=init, interval=20, blit=True)
        plt.show()
        plt.close(fig)
    
    else:
        generate(cap, to_show, to_print, to_video, rotate)

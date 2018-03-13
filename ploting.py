#!/usr/bin/env python

# Personal libraries
from general import *
from calculation import *

def init():
    line.set_data([], [])
    return line,

def animate(data):
    new_x, new_y = data
    global min_y
    global max_y

    old_x = line.get_xdata()
    old_y = line.get_ydata()

    # add the new data to the end of the old data
    x = np.r_[old_x, new_x]
    y = np.r_[old_y, new_y]

    # update the data in the line
    ax.set_xlim(new_x[0], new_x[-1])
    nmin_y = np.amin(new_y); nmax_y = np.amax(new_y)
    if ( nmin_y < min_y and nmax_y > max_y ): ax.set_ylim(nmin_y, nmax_y); min_y = nmin_y; max_y = nmax_y;
    elif (nmin_y < min_y): ax.set_ylim(nmin_y, max_y); min_y = nmin_y;
    if (nmax_y > max_y): ax.set_ylim(min_y, nmax_y); max_y = nmax_y;
    ax.figure.canvas.draw()

    line.set_data(new_x, new_y)
    # return the line2D object so the blitting code knows what to redraw
    return line,


def generate_with_plot(cap, to_show, to_print, to_video, rotate):

    try:
        fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
    except:
        fps = cap.get(cv2.CAP_PROP_FPS)
    if ( not fps ):
        fps = 30.0
    print "Frames per second (fps): {0}".format(fps)
    ifps = int(fps)

    # Capture first frame
    ret, frame = cap.read()

    # resize image
    frame = imutils.resize(frame, width=600)
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
        
        compact = [ frame, y, frame_count ]
        
        frame, y, res, k_mask, start_coord, track_start_second, track_start_frame_count  =  frequency_check( compact, fixed, complement )
        
        complement = [ start_coord, track_start_second, track_start_frame_count ]
        

        x = np.arange((frame_count-ifps), (frame_count))
        # yield res, x, y, frame_count

        display(k_mask, res, to_show, to_print, to_video)
        if (to_video):
            video.write(res)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Capture frame-by-frame
        ret, frame = cap.read()
        frame_count += 1

        yield x, y


    # When everything done, release the capture
    print "TERMINOU"
    if (to_video):
        video.release()
    cap.release()
    cv2.destroyAllWindows()



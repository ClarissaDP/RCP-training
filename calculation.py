#!/usr/bin/env python

from general import *


def frequency_check( compact, fixed, complement ): 
        
        global y_diff_min, y_diff_max, x_diff_max, first_event, speed_conv, second_time, buff, end_y, travel_count, previous_travel, travel

        frame, y, frame_count  =  compact
        rotate, color_type, lower, upper, fps, ifps, width, height = fixed
        start_coord, track_start_second, track_start_frame_count = complement

        print "Frame: ", frame_count

        # if the image is turned
        frame = imutils.rotate(frame, rotate)

        # resize image
        # frame = imutils.resize(frame, width=600)

        # Change from BGR image to HSV easily
        if (color_type == 'BGR'):
            to_use_frame = frame
        else:
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            to_use_frame = hsv_frame

        # Threshold the image to get only yellow colors
        mask = cv2.inRange(to_use_frame, lower, upper)
        k_mask = np.array(mask, copy=True)
        res = frame

        # Find the contours in the image
        try:
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        except:
            _, contours, _ = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        coord = {}
        res, coord['x'], coord['y'] = largest_contour(contours, mask, res)

        # set frame_count and buffer for fps not int
        diff =  float( abs( (frame_count - fps*second_time) - fps - buff ) )
        if ( diff < 1 ):
            print "ENTROU DIFF"
            second_time += 1
            buff = diff

        # found the box
        if ( coord['x'] and coord['y'] ):
            if ( first_event ):
                print "ENTROU first_event"
                first_event = False
                start_coord = coord
                # track_start_time = time.time()
                track_start_second = second_time
                track_start_frame_count = frame_count

            else:
                if ( ('start_coord' in locals() ) and abs(start_coord['x'] - coord['x']) > x_diff_max ):
                    cv2.putText(res, "Ventilation?", (30,50), cv2.FONT_HERSHEY_TRIPLEX, 1, 255)
                    print travel
                    first_event = True
                else:
                    diff = (abs(coord['y'] - start_coord['y'])) if ('start_coord' in locals() ) else 0
                    if ( diff and diff > y_diff_min and diff < y_diff_max ):
                        track_dist = abs( end_y - start_coord['y'] )

                        # track_time = abs( time.time() - track_start_time )
                        track_second = second_time - track_start_second
                        track_frame = frame_count - track_start_frame_count
                        # track_time = (track_second * fps) + ((track_frame / fps) * fps)
                        track_time = ((track_frame / fps) * fps)
                        # track_time = (track_second * fps) + ( fps / (fps - frame_count) )
                        if ( track_time ):
                            ave_speed = float( (abs( track_dist / track_time )) * speed_conv )
                            print track_dist, track_time, ave_speed

                        if ( (end_y - coord['y']) > 0 ):
                            travel_direction = "U2D"
                        else:
                            travel_direction = "D2U"

                        if ( previous_travel == travel_direction ):
                            travel_count += 1
                        else:
                            if ( previous_travel == "U2D" and travel_count > 3 ):
                                travel['down'] += 1
                            elif ( previous_travel == "D2U" and travel_count > 3 ):
                                travel['up'] += 1
                            travel_count = 0
                            previous_travel = travel_direction

                        y = np.append(y, coord['y'])
                        y = np.delete(y, [0], None)

                        
                        # frequencia media das ultimas 10 compressoes
                        if ( y[-10] ):
                            print "Pode calcular", y[-10]


                        cv2.putText(res, travel_direction, ((width-200), (height-200)), cv2.FONT_HERSHEY_TRIPLEX, 1, 255)
                        end_y = coord['y']


        return (frame, y, res, k_mask, start_coord, track_start_second, track_start_frame_count)

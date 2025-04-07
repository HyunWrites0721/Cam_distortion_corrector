import numpy as np
import cv2 as cv

def select_img_from_video(video_file, board_pattern, select_rate=24, wait_msec=10, wnd_name='Camera Calibration'):
    # Open a video
    video = cv.VideoCapture(video_file)
    assert video.isOpened()

    # Select images
    img_select = []
    frames_shown = 0
    while True:
        # Grab an images from the video
        valid, img = video.read()
        if not valid:
            break
        
        #select frame from every 24 frames.
        frames_shown += 1
        if frames_shown % select_rate == 0:    
            img_select.append(img)
            
        #display = img.copy()
        #cv.putText(display, f'NSelect: {len(img_select)}', (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))
        #cv.imshow(wnd_name, display)
        
        complete, pts = cv.findChessboardCorners(img, board_pattern)
        #cv.drawChessboardCorners(display, board_pattern, pts, complete)
        #cv.imshow(wnd_name, display)
        
        # Process the key event
        key = cv.waitKey(wait_msec)
        if key == 27:             # Space: Pause and show corners
            break
                
    cv.destroyAllWindows()
    return img_select

def calib_camera_from_chessboard(images, board_pattern, board_cellsize, K=None, dist_coeff=None, calib_flags=None):
    # Find 2D corner points from given images
    img_points = []
    for img in images:
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        complete, pts = cv.findChessboardCorners(gray, board_pattern)
        if complete:
            img_points.append(pts)
    assert len(img_points) > 0

    # Prepare 3D points of the chess board
    obj_pts = [[c, r, 0] for r in range(board_pattern[1]) for c in range(board_pattern[0])]
    obj_points = [np.array(obj_pts, dtype=np.float32) * board_cellsize] * len(img_points) # Must be `np.float32`

    # Calibrate the camera
    return cv.calibrateCamera(obj_points, img_points, gray.shape[::-1], K, dist_coeff, flags=calib_flags)


if __name__ == '__main__':
    video_file = 'Chess.MOV'
    board_pattern = (10, 7)
    board_cellsize = 0.025

    img_select = select_img_from_video(video_file, board_pattern)
    assert len(img_select) > 0, 'There is no selected images!'
    rms, K, dist_coeff, rvecs, tvecs = calib_camera_from_chessboard(img_select, board_pattern, board_cellsize)

    # Print calibration results
    if img_select:
        print('## Camera Calibration Results')
        print(f'* The number of selected images = {len(img_select)}')
        print(f'* RMS error = {rms}')
        print(f'* Camera matrix (K) = \n{K}')
        print(f'* Distortion coefficient (k1, k2, p1, p2, k3, ...) = {dist_coeff.flatten()}')
    
    # Open a video
    video = cv.VideoCapture(video_file)
    assert video.isOpened(), 'Cannot read the given input, ' + video_file

    fourcc = cv.VideoWriter_fourcc(*'avc1')  #codec specifying
    frame_width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = int(video.get(cv.CAP_PROP_FPS))
    output = cv.VideoWriter('Undistorted.mp4', fourcc, fps, (frame_width , frame_height))
    
    # Run distortion correction
    show_rectify = True
    map1, map2 = None, None
    while True:
        # Read an image from the video
        valid, img = video.read()
        if not valid:
            break

        # Rectify geometric distortion
        info = "Original"
        if show_rectify:
            if map1 is None or map2 is None:
                new_K, roi = cv.getOptimalNewCameraMatrix(K, dist_coeff, (img.shape[1], img.shape[0]), alpha=0)  #to eliminate black area.
                map1, map2 = cv.initUndistortRectifyMap(K, dist_coeff, None, new_K, (img.shape[1], img.shape[0]), cv.CV_32FC1)
            img = cv.remap(img, map1, map2, interpolation=cv.INTER_LINEAR)
            info = "Rectified"
        cv.putText(img, info, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))

        # Show the image and process the key event
        cv.imshow("Geometric Distortion Correction", img)
        output.write(img)
        key = cv.waitKey(10)
        if key == ord(' '):     # Space: Pause
            key = cv.waitKey()
        if key == 27:           # ESC: Exit
            break
        elif key == ord('\t'):  # Tab: Toggle the mode
            show_rectify = not show_rectify

    video.release()
    cv.destroyAllWindows()
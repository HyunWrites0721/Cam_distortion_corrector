# Cam_distortion_corrector

This program performs geometric distortion correction on a chessboard video.

Description
- First, the program selects one frame from every 24 frames in the video and uses those frames for calibration.
- Then, it performs geometric distortion correction using the calibration results (Camera Matrix K and Distortion Coefficients).
- Finally, the program saves the corrected video in .mp4 format.

Controls (while recording)
- Space key: Pause the video
- ESC key: Exit the program
- Tab key: Toggle between the original and rectified video


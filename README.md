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

Calibration result(from given chessboard video.)
- RMS error = 1.726774380729615
- fx, fy, cx, cy = 1.73193038e+03, 1.72300973e+03, 6.18500789e+02, 9.96528529e+02
- Distortion coefficient (k1, k2, p1, p2, k3) = [ 0.14031321 -0.05553018  0.01209608  0.0187642  -0.15186641]

Demo(corredted video)

https://github.com/user-attachments/assets/90f15cfc-9e29-4336-b6b7-6af85e0c6873


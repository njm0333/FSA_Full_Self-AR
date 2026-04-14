import numpy as np
import cv2 as cv

video_file = 'chessboard.avi'
K = np.array([[956.49661865, 0.0, 961.37566344],
              [0.0, 962.04059292, 536.96602399],
              [0.0, 0.0, 1.0]])
dist_coeff = np.array([-0.00342753, 0.01778027, -0.00133933, 0.00100904, -0.01872466])

board_pattern = (10, 7)
board_cellsize = 0.025
board_criteria = cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_NORMALIZE_IMAGE + cv.CALIB_CB_FAST_CHECK

video = cv.VideoCapture(video_file)
assert video.isOpened(), 'Cannot read the given input, ' + video_file

pyramid_base = board_cellsize * np.array([[3, 2, 0], [5, 2, 0], [5, 4, 0], [3, 4, 0]])

pyramid_apex = board_cellsize * np.array([[4, 3, -2]])

obj_points = board_cellsize * np.array([[c, r, 0] for r in range(board_pattern[1]) for c in range(board_pattern[0])], dtype=np.float32)

while True:
    valid, img = video.read()
    if not valid:
        break

    success, img_points = cv.findChessboardCorners(img, board_pattern, board_criteria)
    if success:
        ret, rvec, tvec = cv.solvePnP(obj_points, img_points, K, dist_coeff)

        base_points, _ = cv.projectPoints(pyramid_base, rvec, tvec, K, dist_coeff)
        apex_point, _ = cv.projectPoints(pyramid_apex, rvec, tvec, K, dist_coeff)

        base_points = np.int32(base_points).reshape(-1, 2)
        apex_point = np.int32(apex_point).flatten()

        cv.polylines(img, [base_points], True, (255, 0, 0), 2)
        for p in base_points:
            cv.line(img, tuple(p), tuple(apex_point), (0, 255, 0), 2)

        cv.circle(img, tuple(apex_point), 5, (0, 0, 255), -1)

        R, _ = cv.Rodrigues(rvec)
        p = (-R.T @ tvec).flatten()
        info = f'XYZ: [{p[0]:.3f} {p[1]:.3f} {p[2]:.3f}]'
        cv.putText(img, info, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))

    cv.imshow('Pose Estimation (Pyramid AR)', img)

    key = cv.waitKey(10)
    if key == ord(' '):
        key = cv.waitKey()
    if key == 27:
        break

video.release()
cv.destroyAllWindows()
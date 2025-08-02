import cv2
import numpy as np

def compare_socks_from_file(image_path):
    frame = cv2.imread(image_path)
    if frame is None:
        return None, None

    height, width, _ = frame.shape
    mid = width // 2

    left_sock = frame[:, :mid]
    right_sock = frame[:, mid:]

    left_sock = cv2.resize(left_sock, (200, 200))
    right_sock = cv2.resize(right_sock, (200, 200))

    hist_left = cv2.calcHist([left_sock], [0, 1, 2], None, [8, 8, 8], [0,256]*3)
    hist_right = cv2.calcHist([right_sock], [0, 1, 2], None, [8, 8, 8], [0,256]*3)

    cv2.normalize(hist_left, hist_left)
    cv2.normalize(hist_right, hist_right)

    similarity = cv2.compareHist(hist_left, hist_right, cv2.HISTCMP_CORREL)

    mean_left = cv2.mean(left_sock)[:3]
    mean_right = cv2.mean(right_sock)[:3]
    color_diff = np.linalg.norm(np.array(mean_left) - np.array(mean_right))

    return similarity, color_diff

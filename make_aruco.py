import cv2
import cv2.aruco as aruco
import numpy as np

# Aruco 사전 설정 (DICT_6X6_250: 6x6 그리드, 250개의 ID)
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

# ID 1의 마커 생성 (200x200 크기)
marker_image = np.zeros((200, 200), dtype=np.uint8)
marker_image = aruco.drawMarker(aruco_dict, 1, 200)

# 이미지 저장
cv2.imwrite("aruco_marker_id1.png", marker_image)

# 마커 출력
cv2.imshow('Aruco Marker', marker_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
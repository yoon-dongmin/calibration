import cv2
import cv2.aruco as aruco

# 카메라에서 프레임을 캡처
cap = cv2.VideoCapture(0)

# Aruco 사전 불러오기
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters_create()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Aruco 마커 감지
    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)
    
    # 마커를 프레임에 그리기
    frame = aruco.drawDetectedMarkers(frame, corners, ids)

    # 결과 출력
    cv2.imshow('Aruco Markers', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
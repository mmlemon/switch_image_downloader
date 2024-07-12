import cv2
from inc.qr_processor import QRProcessor

camera_id = 2
delay = 1
window_name = 'Get media from Nintendo Switch( Press "Q" to quit program)'

qcd = cv2.QRCodeDetector()
cap = cv2.VideoCapture(camera_id)
mes = ""
qrproc = QRProcessor()
loopflg = True
while loopflg:
    ret, frame = cap.read()
    if ret:
        ret_qr, decoded_info, points, _ = qcd.detectAndDecodeMulti(frame)
        if ret_qr:
            for s, p in zip(decoded_info, points):
                if s:
                    print(s)
                    parseResult = qrproc.parse(s)
                    color = (0, 255, 0)
                    if parseResult:
                        loopflg = False
                    break
                else:
                    color = (0, 0, 255)
                frame = cv2.polylines(frame, [p.astype(int)], True, color, 8)
        cv2.imshow(window_name, frame)

    if cv2.waitKey(delay) & 0xFF == ord('q'):
        break

cv2.destroyWindow(window_name)
import cv2
import dlib
from scipy.spatial import distance
import time
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
import sys


class DrowsinessDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        # 카메라 설정
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 640)
        self.cap.set(4, 480)
        self.close_eyes_count = 0
        self.lastsave = 0
        self.frame = None

        # dlib을 사용한 얼굴 검출 모델과 랜드마크 모델 초기화
        self.hog_face_detector = dlib.get_frontal_face_detector()
        self.dlib_facelandmark = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

        # QTimer를 사용하여 화면 업데이트 간격 설정
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # 30ms마다 업데이트

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.label = QLabel(self)
        self.layout.addWidget(self.label)
        self.central_widget.setLayout(self.layout)

    def calculate_EAR(self, eye):
        A = distance.euclidean(eye[1], eye[5])
        B = distance.euclidean(eye[2], eye[4])
        C = distance.euclidean(eye[0], eye[3])
        ear_aspect_ratio = (A + B) / (2.0 * C)
        return ear_aspect_ratio

    def close_eyes(self):
        if not hasattr(self, 'close_eyes_count'):
            self.close_eyes_count = 0
        self.close_eyes_count += 1
        cv2.putText(self.frame, "DROWSY", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 4)

        # 지연 및 카운트 관리 코드 추가
        if time.time() - self.lastsave > 5:
            self.lastsave = time.time()
            self.close_eyes_count = 0

    def update_frame(self):
        _, self.frame = self.cap.read()
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

        # 얼굴 검출
        faces = self.hog_face_detector(gray)
        for face in faces:
            face_landmarks = self.dlib_facelandmark(gray, face)
            leftEye = []
            rightEye = []

            # 눈 주위의 랜드마크를 검출하여 눈의 모양을 추정
            for n in range(36, 42):  # 오른쪽 눈
                x = face_landmarks.part(n).x
                y = face_landmarks.part(n).y
                leftEye.append((x, y))
                next_point = n + 1
                if n == 41:
                    next_point = 36
                x2 = face_landmarks.part(next_point).x
                y2 = face_landmarks.part(next_point).y
                cv2.line(self.frame, (x, y), (x2, y2), (0, 255, 0), 1)

            for n in range(42, 48):  # 왼쪽 눈
                x = face_landmarks.part(n).x
                y = face_landmarks.part(n).y
                rightEye.append((x, y))
                next_point = n + 1
                if n == 47:
                    next_point = 42
                x2 = face_landmarks.part(next_point).x
                y2 = face_landmarks.part(next_point).y
                cv2.line(self.frame, (x, y), (x2, y2), (0, 255, 0), 1)

            # EAR(눈 종횡비) 계산 및 눈 깜빡임 감지
            left_ear = self.calculate_EAR(leftEye)
            right_ear = self.calculate_EAR(rightEye)
            EAR = (left_ear + right_ear) / 2
            EAR = round(EAR, 2)

            if EAR < 0.19:
                self.close_eyes()
                print(f'close count : {self.close_eyes_count}')  # 수정된 부분
                if self.close_eyes_count == 15:
                    print("Driver is sleeping")

        # OpenCV 프레임을 PyQt 이미지로 변환하여 표시
        h, w, ch = self.frame.shape
        bytesPerLine = ch * w
        convertToQtFormat = QImage(self.frame.data, w, h, bytesPerLine, QImage.Format_RGB888)
        p = convertToQtFormat.scaled(640, 480, aspectRatioMode=True)
        self.label.setPixmap(QPixmap.fromImage(p))

    def keyPressEvent(self, event):
        if event.key() == 27:  # ESC 키를 누르면 창 닫기
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DrowsinessDetectionApp()
    window.setWindowTitle("Drowsiness Detection")
    window.setGeometry(100, 100, 640, 480)
    window.show()
    sys.exit(app.exec_())

import cv2
import dlib
from PyQt5.QtGui import QPixmap, QIcon, QImage
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QApplication, QWidget, QLabel
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QUrl, QTimer
import time

from scipy.spatial import distance

from Source.cam.webcam import WebCam


class Main(QDialog):
    def __init__(self, object_1, object_2):
        super().__init__()
        loadUi('../../UI/MainPage.ui', self)
        self.webcam_timer = QTimer(self)
        self.btn_event()
        self.window_option()
        self.object_1 = object_1
        self.object_2 = object_2
        self.sleep_count = 0
        self.close_eyes_count = 0
        self.face_code = 0
        # 강의 정지시간
        self.current_position = 0
        self.empty_media_content = QMediaContent()  # 빈 QMediaContent 객체 생성

    def window_option(self):
        """프로그램 초기 설정 이벤트 함수"""
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget_2.setCurrentIndex(0)

        # 동영상 재생 위젯
        self.layout = QVBoxLayout()
        self.movie_widget.setLayout(self.layout)
        self.movie_ = QVideoWidget(self)
        self.layout.addWidget(self.movie_)

        # 미디어 플레이어 초기화
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.movie_)
        self.media_player.stop()

        # 동영상 파일 경로
        self.video_url_list = ["../../Movie/Korean.wmv", "../../Movie/Math.wmv", "../../Movie/English.wmv"]

    def btn_event(self):
        """버튼 클릭 이벤트 함수"""
        self.exit_btn.clicked.connect(self.close_event)
        self.exit_btn2.clicked.connect(self.close_event)
        self.join_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.back_btn.clicked.connect(self.join_page_back_situation)
        self.hide_btn.clicked.connect(self.hide_btn_clicked_situation)
        self.login_btn.clicked.connect(self.go_main_page)
        self.lecture_btn_1.clicked.connect(self.go_lecture_page)
        self.home_btn.clicked.connect(self.home_btn_clicked_situation)
        self.webcam_timer.timeout.connect(self.update_frame)
        # 강의 버튼 리스트
        self.lec_btn_list = [self.lec_btn_1, self.lec_btn_2, self.lec_btn_3]
        for idx, btn in enumerate(self.lec_btn_list):
            btn.clicked.connect(lambda x=None, y=idx: self.lecture_page_show(y))
        self.logout_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.mypage_btn.clicked.connect(self.go_my_page)

    def page_ch(self):
        try:
            self.media_player.setMedia(self.empty_media_content)  # media_player의 미디어 콘텐츠를 비우기
            # 타이머 정지
            self.webcam_timer.stop()
            # 웹캠 종료
            self.cap.release()
        except:
            pass
    # ========================================== 타이틀 클릭 이벤트 ======================================== #
    def close_event(self):
        """홈페이지 닫기 버튼 클릭 했을 때 이벤트 함수"""
        self.media_player.stop()
        self.object_1.hide()
        self.object_2.hide()
        self.close()

    def hide_btn_clicked_situation(self):
        """윈도우 타이틀 창 숨기기 버튼 클릭시 발생 이벤트 함수"""
        self.hide()

    def home_btn_clicked_situation(self):
        """윈도우 타이틀 뒤로가기 버튼 클릭 시 이벤트 함수"""
        self.media_player.stop()
        self.stackedWidget_2.setCurrentIndex(0)

    # ========================================== 로그인 / 회원가입 ========================================= #
    def join_page_back_situation(self):
        """회원가입 페이지에서 뒤로가기 버튼 클릭 시 이벤트 함수"""
        self.join_id.clear()
        self.join_pw.clear()
        self.check_pw.clear()
        self.join_name.clear()
        self.stackedWidget.setCurrentIndex(0)

    def go_main_page(self):
        """로그인 버튼 클릭 시 메인 페이지로 이동하는 함수"""
        self.stackedWidget.setCurrentIndex(2)

    # ============================================ 강의 페이지 ============================================= #
    def go_lecture_page(self):
        """강의실 버튼 클릭 시 강의 페이지로 이동하는 함수"""
        self.page_ch()
        self.stackedWidget_2.setCurrentIndex(1)

    def lecture_page_show(self, idx):
        """강의실 페이지에서 강의실 입장 버튼 클릭 시 이동하는 함수"""
        self.media_player.setPosition(self.current_position)
        self.stackedWidget_2.setCurrentIndex(2)
        # 웹캠 띄우기
        self.webcam_start()

        video_url = QUrl.fromLocalFile(self.video_url_list[idx])
        media_content = QMediaContent(video_url)
        self.media_player.setMedia(media_content)
        self.media_player.play()

    # ============================================ 웹캠 ==============================================
    def webcam_start(self):
        # 카메라 설정
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 640)
        self.cap.set(4, 480)

        self.lastsave = 0
        self.frame = None

        # dlib을 사용한 얼굴 검출 모델과 랜드마크 모델 초기화
        self.hog_face_detector = dlib.get_frontal_face_detector()
        self.dlib_facelandmark = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

        self.webcam_timer.start(30)  # 30ms마다 업데이트

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

        # 추가: 얼굴이 검출되지 않은 경우
        if len(faces) == 0:
            if self.face_code != 1:
                self.handle_no_face()
                self.face_code = 1
        elif len(faces) > 0 and self.face_code != 0:
            self.face_code = 0

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

            position = self.media_player.position()
            duration = self.media_player.duration()

            if position >= duration:    # 강의 모두 들었을때
                # todo: 강의 종료 이밴트들
                # 미디어가 끝에 도달했을 때 실행할 코드를 여기에 추가
                print("강의를 모두 수강하셨습니다")

            if self.sleep_count == 3:
                self.page_ch()
                # todo: 강의 종료 메인화면으로
                self.sleep_count = 0  # 강의내 세번째 경고를 세번 받으면 강의 종료
            if EAR < 0.19:
                self.close_eyes()
                print(f'close count : {self.close_eyes_count}')  # 수정된 부분
                if self.close_eyes_count == 40:  # 첫번째 알람
                    self.current_position = self.media_player.position()
                    self.media_player.pause()
                    print("3번 알람 강의 멈춤 -> 서버에 회원,졸음,시간 보내서 db에저장")
                    self.sleep_count += 1
            elif position != duration:
                # 미디어를 재생
                # print(f"강의 다시 재생 시간 {self.current_position}")
                # self.media_player.setPosition(self.current_position)
                self.media_player.play()

        # BGR에서 RGB로 색상 순서 변경
        rgb_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

        # OpenCV 프레임을 PyQt 이미지로 변환하여 표시
        h, w, ch = rgb_frame.shape
        bytesPerLine = ch * w
        convertToQtFormat = QImage(rgb_frame.data, w, h, bytesPerLine, QImage.Format_RGB888)
        p = convertToQtFormat.scaled(640, 480, aspectRatioMode=True)
        self.webcam_lbl.setPixmap(QPixmap.fromImage(p))

    # 얼굴을 검출하지 못한 경우 호출될 메서드
    def handle_no_face(self):
        self.media_player.pause()
        print("강의 멈춤 -> 서버에 회원,자리비움,시간 보내서 db에저장 ")

    # ============================================ 마이 페이지 ============================================== #
    def go_my_page(self):
        """마이 페이지 클릭 시 이동하는 함수"""
        self.media_player.stop()
        self.stackedWidget_2.setCurrentIndex(3)

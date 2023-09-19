import cv2
import dlib
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLayout
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QUrl, QTimer, pyqtSignal
import time

from Source.View.Lecture import Lectures
from Source.View.Message import Messages
from scipy.spatial import distance

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
import matplotlib.font_manager as fm

from Source.cam.webcam import WebCam


class Main(QDialog):
    login_check_signal = pyqtSignal(bool)
    member_join_signal = pyqtSignal(bool)

    def __init__(self, object_1, object_2, clientapp):
        super().__init__()
        loadUi('../../UI/MainPage.ui', self)
        self.webcam_timer = QTimer(self)
        self.btn_event()
        self.signal_event()
        self.window_option()
        self.client = clientapp
        self.client.set_widget(self)
        self.object_1 = object_1
        self.object_2 = object_2


    def window_option(self):
        """프로그램 초기 설정 이벤트 함수"""
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget_2.setCurrentIndex(0)

        # 메시지 박스 다이얼로그
        self.messages = Messages()

        # 강의 위젯
        self.lecture = Lectures()

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

        # 기본 한글 폰트 설정
        font_path = "../../Font/GmarketSansTTFMedium.ttf"
        font_name = fm.FontProperties(fname=font_path).get_name()
        plt.rc('font', family=font_name)
        self.pushButton_10.setChecked(True)
        self.show_day_attitude()

        self.sleep_count = 0
        self.close_eyes_count = 0
        self.face_code = 0

        # 강의 정지시간
        self.current_position = 0
        self.empty_media_content = QMediaContent()  # 빈 QMediaContent 객체 생성

    def btn_event(self):
        """버튼 클릭 이벤트 함수"""
        self.exit_btn.clicked.connect(self.close_event)
        self.exit_btn2.clicked.connect(self.close_event)
        self.join_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.join_request_btn.clicked.connect(self.member_join_request)
        self.back_btn.clicked.connect(self.join_page_back_situation)
        self.hide_btn.clicked.connect(self.hide_btn_clicked_situation)
        self.login_btn.clicked.connect(self.login_check)
        self.lecture_btn_1.clicked.connect(self.go_lecture_page)
        self.home_btn.clicked.connect(self.home_btn_clicked_situation)
        # self.webcam_timer.timeout.connect(self.update_frame)

        # 수업 태도 출력
        self.pushButton_10.clicked.connect(self.show_day_attitude)
        self.pushButton_11.clicked.connect(self.show_week_attitude)
        self.pushButton_12.clicked.connect(self.show_month_attitude)


        # 강의 버튼 리스트
        self.lec_btn_list = [self.lec_btn_1, self.lec_btn_2, self.lec_btn_3]
        for idx, btn in enumerate(self.lec_btn_list):
            btn.clicked.connect(lambda x=None, y=idx: self.lecture_page_show(y))
        self.logout_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.mypage_btn.clicked.connect(self.go_my_page)

    def signal_event(self):
        """시그널 이벤트 함수"""
        self.login_check_signal.connect(self.login_clear)
        self.member_join_signal.connect(self.member_join_clear)

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

    def login_check(self):
        """로그인 성공 여부 체크하는 함수"""
        user_id = self.id_line.text()
        user_pwd = self.pw_line.text()

        if len(user_id) == 0 or len(user_pwd) == 0:
            self.messages.error_text(0)
            self.messages.exec_()
        else:
            self.client.send_login_check_access(user_id, user_pwd)

    def login_clear(self, login_):
        """로그인 결과값 받아오는 함수"""
        if login_:
            self.messages.error_text(6)
            self.messages.exec_()
            self.go_main_page()
        else:
            self.messages.error_text(7)
            self.messages.exec_()

    def member_join_request(self):
        """서버에 회원가입 요청 보내는 함수"""
        join_id = self.join_id.text()
        join_pwd = self.join_pw.text()
        check_pwd = self.check_pw.text()
        user_name = self.join_name.text()

        if len(join_id) == 0:
            self.messages.error_text(1)
            self.messages.exec_()

        if len(join_pwd) < 8 or len(join_pwd) > 16:
            self.join_pw.clear()
            self.check_pw.clear()
            self.messages.error_text(2)
            self.messages.exec_()
            return

        if join_pwd != check_pwd:
            self.messages.error_text(3)
            self.messages.exec_()
            return

        # 비밀번호에 영문자, 숫자, 특수기호 각각 1개 이상 사용하는지 확인
        pw_valid_result = self.is_valid_password(join_pwd)

        if pw_valid_result == -1:
            self.messages.error_text(4)
            self.messages.exec_()
            return

        if len(user_name) > 10 or len(user_name) < 1:
            self.messages.error_text(5)
            self.messages.exec_()
            return

        self.client.send_member_join_access(join_id, join_pwd, user_name)

    def member_join_clear(self, join_):
        """회원가입 결과 받아오는 함수"""
        if join_:
            self.messages.error_text(8)
            self.messages.exec_()
            self.join_page_back_situation()

    def is_valid_password(self, password):
        """비밀번호 영문자, 숫자, 특수기호 각각 1개 이상 사용하는지 확인하는 함수"""
        has_lowercase = any(c.islower() for c in password)
        has_uppercase = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c for c in password if c in "!@#$%^&*()_+[]{}|;:,.<>?")

        # 모든 조건을 만족하는지 검사
        if (has_lowercase or has_uppercase) and has_digit and has_special:
            return 1
        else:
            return -1

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
        if idx == 0:
            self.clear_layout(self.verticalLayout_2)
            self.verticalLayout_2.addWidget(self.lecture)
            self.scrollAreaWidgetContents.setMaximumHeight(len(1) * 35)

        # 웹캠 띄우기
        # self.webcam_start()
        video_url = QUrl.fromLocalFile(self.video_url_list[idx])
        media_content = QMediaContent(video_url)
        self.media_player.setMedia(media_content)
        self.media_player.play()

    # ============================================ 웹캠 ==============================================
    # def webcam_start(self):
    #     # 카메라 설정
    #     self.cap = cv2.VideoCapture(0)
    #     self.cap.set(3, 640)
    #     self.cap.set(4, 480)
    #
    #     self.lastsave = 0
    #     self.frame = None
    #
    #     # dlib을 사용한 얼굴 검출 모델과 랜드마크 모델 초기화
    #     self.hog_face_detector = dlib.get_frontal_face_detector()
    #     self.dlib_facelandmark = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    #
    #     self.webcam_timer.start(30)  # 30ms마다 업데이트
    #
    # def calculate_EAR(self, eye):
    #     A = distance.euclidean(eye[1], eye[5])
    #     B = distance.euclidean(eye[2], eye[4])
    #     C = distance.euclidean(eye[0], eye[3])
    #     ear_aspect_ratio = (A + B) / (2.0 * C)
    #     return ear_aspect_ratio
    #
    # def close_eyes(self):
    #     if not hasattr(self, 'close_eyes_count'):
    #         self.close_eyes_count = 0
    #     self.close_eyes_count += 1
    #     cv2.putText(self.frame, "DROWSY", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 4)
    #
    #     # 지연 및 카운트 관리 코드 추가
    #     if time.time() - self.lastsave > 5:
    #         self.lastsave = time.time()
    #         self.close_eyes_count = 0
    #
    # def update_frame(self):
    #     _, self.frame = self.cap.read()
    #     gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
    #
    #     # 얼굴 검출
    #     faces = self.hog_face_detector(gray)
    #
    #     # 추가: 얼굴이 검출되지 않은 경우
    #     if len(faces) == 0:
    #         if self.face_code != 1:
    #             self.handle_no_face()
    #             self.face_code = 1
    #     elif len(faces) > 0 and self.face_code != 0:
    #         self.face_code = 0
    #
    #     for face in faces:
    #         face_landmarks = self.dlib_facelandmark(gray, face)
    #         leftEye = []
    #         rightEye = []
    #
    #         # 눈 주위의 랜드마크를 검출하여 눈의 모양을 추정
    #         for n in range(36, 42):  # 오른쪽 눈
    #             x = face_landmarks.part(n).x
    #             y = face_landmarks.part(n).y
    #             leftEye.append((x, y))
    #             next_point = n + 1
    #             if n == 41:
    #                 next_point = 36
    #             x2 = face_landmarks.part(next_point).x
    #             y2 = face_landmarks.part(next_point).y
    #             cv2.line(self.frame, (x, y), (x2, y2), (0, 255, 0), 1)
    #
    #         for n in range(42, 48):  # 왼쪽 눈
    #             x = face_landmarks.part(n).x
    #             y = face_landmarks.part(n).y
    #             rightEye.append((x, y))
    #             next_point = n + 1
    #             if n == 47:
    #                 next_point = 42
    #             x2 = face_landmarks.part(next_point).x
    #             y2 = face_landmarks.part(next_point).y
    #             cv2.line(self.frame, (x, y), (x2, y2), (0, 255, 0), 1)
    #
    #         # EAR(눈 종횡비) 계산 및 눈 깜빡임 감지
    #         left_ear = self.calculate_EAR(leftEye)
    #         right_ear = self.calculate_EAR(rightEye)
    #         EAR = (left_ear + right_ear) / 2
    #         EAR = round(EAR, 2)
    #
    #         position = self.media_player.position()
    #         duration = self.media_player.duration()
    #
    #         if position >= duration:    # 강의 모두 들었을때
    #             # todo: 강의 종료 이밴트들
    #             # 미디어가 끝에 도달했을 때 실행할 코드를 여기에 추가
    #             print("강의를 모두 수강하셨습니다")
    #
    #         if self.sleep_count == 3:
    #             self.page_ch()
    #             # todo: 강의 종료 메인화면으로
    #             self.sleep_count = 0  # 강의내 세번째 경고를 세번 받으면 강의 종료
    #
    #         if EAR < 0.19:
    #             self.close_eyes()
    #             print(f'close count : {self.close_eyes_count}')  # 수정된 부분
    #             if self.close_eyes_count == 40:  # 첫번째 알람
    #                 self.current_position = self.media_player.position()
    #                 self.media_player.pause()
    #                 print("3번 알람 강의 멈춤 -> 서버에 회원,졸음,시간 보내서 db에저장")
    #                 self.sleep_count += 1
    #         elif position != duration:
    #             # 미디어를 재생
    #             # print(f"강의 다시 재생 시간 {self.current_position}")
    #             # self.media_player.setPosition(self.current_position)
    #             self.media_player.play()
    #
    #     # BGR에서 RGB로 색상 순서 변경
    #     rgb_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
    #
    #     # OpenCV 프레임을 PyQt 이미지로 변환하여 표시
    #     h, w, ch = rgb_frame.shape
    #     bytesPerLine = ch * w
    #     convertToQtFormat = QImage(rgb_frame.data, w, h, bytesPerLine, QImage.Format_RGB888)
    #     p = convertToQtFormat.scaled(640, 480, aspectRatioMode=True)
    #     self.webcam_lbl.setPixmap(QPixmap.fromImage(p))
    #
    # # 얼굴을 검출하지 못한 경우 호출될 메서드
    # def handle_no_face(self):
    #     self.media_player.pause()
    #     print("강의 멈춤 -> 서버에 회원,자리비움,시간 보내서 db에저장 ")

    # ============================================ 마이 페이지 ============================================== #
    def go_my_page(self):
        """마이 페이지 클릭 시 이동하는 함수"""
        self.media_player.stop()
        self.stackedWidget_2.setCurrentIndex(3)

    # ============================================== 데이터 시각화 =========================================== #
    def clear_layout(self, layout: QLayout):
        """레이아웃 안의 모든 객체를 지웁니다."""
        if layout is None or not layout.count():
            return
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.setParent(None)
            # 아이템이 레이아웃일 경우 재귀 호출로 레이아웃 내의 위젯 삭제
            else:
                self.clear_layout(item.layout())

    def show_day_attitude(self):
        """일간 수업 태도 출력 함수"""
        self.clear_layout(self.verticalLayout_3)
        canvas = FigureCanvas(plt.figure())
        self.verticalLayout_3.addWidget(canvas)
        self.create_day_attitude_plot()

    def create_day_attitude_plot(self):
        """일간 수업 태도 꺾은선 그래프 출력 함수"""
        df1 = pd.DataFrame({'x': ['월', '화', '수', '목', '금', '토', '일'], 'y': [3, 4, 3, 2, 5, 1, 7]})
        plt.plot(df1['x'], df1['y'], color='red', alpha=0.3, linestyle='-', marker='*')
        plt.xlabel('일간')
        plt.ylabel('졸음 횟수')
        plt.title("9월 3주차 수업 태도")

    def show_week_attitude(self):
        """주간 수업 태도 출력 함수"""
        self.clear_layout(self.verticalLayout_3)
        canvas = FigureCanvas(plt.figure())
        self.verticalLayout_3.addWidget(canvas)
        self.create_week_attitude_plot()

    def create_week_attitude_plot(self):
        """주간 수업 태도 꺾은선 그래프 출력 함수"""
        df1 = pd.DataFrame({'x': ['8월 1주', '8월 2주', '8월 3주', '8월 4주', '8월 5주'], 'y': [5, 3, 2, 3, 2]})
        plt.plot(df1['x'], df1['y'], color='red', alpha=0.3, linestyle='-', marker='*')
        plt.xlabel('주간')
        plt.ylabel('평균 졸음 횟수')
        plt.title("8월 수업 태도")

    def show_month_attitude(self):
        """주간 수업 태도 출력 함수"""
        self.clear_layout(self.verticalLayout_3)
        canvas = FigureCanvas(plt.figure())
        self.verticalLayout_3.addWidget(canvas)
        self.create_month_attitude_plot()

    def create_month_attitude_plot(self):
        """주간 수업 태도 꺾은선 그래프 출력 함수"""
        df1 = pd.DataFrame({'x': ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월'],
                            'y': [6, 4, 3, 5, 4, 3, 3, 2]})
        plt.plot(df1['x'], df1['y'], color='red', alpha=0.3, linestyle='-', marker='*')
        plt.xlabel('월간')
        plt.ylabel('평균 졸음 횟수')
        plt.title("23년 수업 태도")

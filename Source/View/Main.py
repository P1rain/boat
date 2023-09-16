from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QUrl


class Main(QDialog):
    def __init__(self, object_1, object_2):
        super().__init__()
        loadUi('../../UI/MainPage.ui', self)
        self.btn_event()
        self.window_option()
        self.object_1 = object_1
        self.object_2 = object_2

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

        # 강의 버튼 리스트
        self.lec_btn_list = [self.lec_btn_1, self.lec_btn_2, self.lec_btn_3]
        for idx, btn in enumerate(self.lec_btn_list):
            btn.clicked.connect(lambda x=None, y=idx: self.lecture_page_show(y))

        self.logout_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.mypage_btn.clicked.connect(self.go_my_page)

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
        self.media_player.stop()
        self.stackedWidget_2.setCurrentIndex(1)

    def lecture_page_show(self, idx):
        """강의실 페이지에서 강의실 입장 버튼 클릭 시 이동하는 함수"""
        self.media_player.setPosition(0)
        self.stackedWidget_2.setCurrentIndex(2)

        video_url = QUrl.fromLocalFile(self.video_url_list[idx])
        media_content = QMediaContent(video_url)
        self.media_player.setMedia(media_content)
        self.media_player.play()

    # ============================================ 마이 페이지 ============================================== #
    def go_my_page(self):
        """마이 페이지 클릭 시 이동하는 함수"""
        self.media_player.stop()
        self.stackedWidget_2.setCurrentIndex(3)



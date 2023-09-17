from PyQt5.QtWidgets import QDialog

from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class Messages(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('../../UI/MessageBox.ui', self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.btn_lbl_event()
        self.move(770, 370)

    def error_text(self, num, t_txt: str = None):
        """에러 메시지 텍스트 출력"""
        if num == 0:
            self.label_2.setPixmap(QPixmap("../../Images/경고.png"))
            self.label_3.setText("아이디 또는 비밀번호를 입력해주세요.")

        if num == 1:
            self.label_2.setPixmap(QPixmap("../../Images/경고.png"))
            self.label_3.setText("아이디를 입력해주세요.")

        if num == 2:
            self.label_2.setPixmap(QPixmap("../../Images/경고.png"))
            self.label_3.setText("비밀번호는 8~16자로 입력해주세요.")

        if num == 3:
            self.label_2.setPixmap(QPixmap("../../Images/경고.png"))
            self.label_3.setText("비밀번호가 일치하지 않습니다.")

        if num == 4:
            self.label_2.setPixmap(QPixmap("../../Images/경고.png"))
            self.label_3.setText("비밀번호에 영문자,숫자,특수기호를 각 1개 이상 입력해주세요.")

        if num == 5:
            self.label_2.setPixmap(QPixmap("../../Images/경고.png"))
            self.label_3.setText("실명을 정확히 입력해주세요.")

        if num == 6:
            self.label_2.setPixmap(QPixmap("../../Images/clear.png"))
            self.label_3.setText("로그인 성공했습니다.")

        if num == 7:
            self.label_2.setPixmap(QPixmap("../../Images/경고.png"))
            self.label_3.setText("아이디 또는 비밀번호가 일치하지 않습니다.")

    def btn_lbl_event(self):
        """버튼, 라벨 클릭 이벤트 함수"""
        self.pushButton.clicked.connect(self.close_event)

    def close_event(self, e):
        """에러 다이얼로그 종료 함수"""
        self.close()
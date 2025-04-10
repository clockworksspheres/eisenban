# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)
import eisenban_rc

class Ui_About(object):
    def setupUi(self, About):
        if not About.objectName():
            About.setObjectName(u"About")
        About.resize(628, 398)
        About.setStyleSheet(u"background-color: #393f4b;")
        self.centralwidget = QWidget(About)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(25, 25, 25, 25)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_logo_top = QLabel(self.centralwidget)
        self.label_logo_top.setObjectName(u"label_logo_top")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_logo_top.sizePolicy().hasHeightForWidth())
        self.label_logo_top.setSizePolicy(sizePolicy)
        self.label_logo_top.setMaximumSize(QSize(55, 55))
        self.label_logo_top.setPixmap(QPixmap(u":/eisenban/resources/img/icon.png"))
        self.label_logo_top.setScaledContents(True)

        self.horizontalLayout.addWidget(self.label_logo_top)

        self.horizontalSpacer = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_title = QLabel(self.centralwidget)
        self.label_title.setObjectName(u"label_title")
        font = QFont()
        font.setFamilies([u"Arimo"])
        font.setPointSize(24)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet(u"color: #ffffff")

        self.verticalLayout.addWidget(self.label_title)

        self.label_sub_title = QLabel(self.centralwidget)
        self.label_sub_title.setObjectName(u"label_sub_title")
        font1 = QFont()
        font1.setFamilies([u"Arimo"])
        font1.setPointSize(13)
        self.label_sub_title.setFont(font1)
        self.label_sub_title.setStyleSheet(u"color: #ffffff")

        self.verticalLayout.addWidget(self.label_sub_title)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.label_description = QLabel(self.centralwidget)
        self.label_description.setObjectName(u"label_description")
        font2 = QFont()
        font2.setFamilies([u"Arimo"])
        font2.setPointSize(12)
        self.label_description.setFont(font2)
        self.label_description.setStyleSheet(u"color: #ffffff")
        self.label_description.setWordWrap(True)
        self.label_description.setOpenExternalLinks(True)
        self.label_description.setTextInteractionFlags(Qt.LinksAccessibleByMouse)

        self.verticalLayout_2.addWidget(self.label_description)

        self.verticalSpacer_3 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)

        self.label_description_2 = QLabel(self.centralwidget)
        self.label_description_2.setObjectName(u"label_description_2")
        self.label_description_2.setMaximumSize(QSize(370, 16777215))
        self.label_description_2.setFont(font2)
        self.label_description_2.setStyleSheet(u"color: #ffffff")
        self.label_description_2.setWordWrap(True)
        self.label_description_2.setOpenExternalLinks(True)

        self.verticalLayout_2.addWidget(self.label_description_2)

        self.label_logo_bottom = QLabel(self.centralwidget)
        self.label_logo_bottom.setObjectName(u"label_logo_bottom")
        sizePolicy.setHeightForWidth(self.label_logo_bottom.sizePolicy().hasHeightForWidth())
        self.label_logo_bottom.setSizePolicy(sizePolicy)
        self.label_logo_bottom.setMaximumSize(QSize(210, 40))
        self.label_logo_bottom.setPixmap(QPixmap(u":/eisenban/resources/img/kanbaru.png"))
        self.label_logo_bottom.setScaledContents(True)

        self.verticalLayout_2.addWidget(self.label_logo_bottom)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalSpacer_4 = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_4)

        self.label_license = QLabel(self.centralwidget)
        self.label_license.setObjectName(u"label_license")
        self.label_license.setFont(font2)
        self.label_license.setStyleSheet(u"color: #ffffff")
        self.label_license.setWordWrap(True)
        self.label_license.setOpenExternalLinks(True)

        self.verticalLayout_3.addWidget(self.label_license)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        About.setCentralWidget(self.centralwidget)

        self.retranslateUi(About)

        QMetaObject.connectSlotsByName(About)
    # setupUi

    def retranslateUi(self, About):
        About.setWindowTitle(QCoreApplication.translate("About", u"About", None))
        self.label_logo_top.setText("")
        self.label_title.setText(QCoreApplication.translate("About", u"Eisenban", None))
        self.label_sub_title.setText(QCoreApplication.translate("About", u"Eisenban Project Manager", None))
        self.label_description.setText(QCoreApplication.translate("About", u"<html><head/><body><p>eisenban is a rebranding of the Kanbaru project on <a href=\"https://github.com/dulapahv/Kanbaru\"><span style=\" text-decoration: underline; color:#007af4;\">Github</span></a>.</p><p>Beware of the easter-egg and font license problems with the Kanbaru project.</p><p><span style=\" font-weight:700;\">Respun by:</span></p></body></html>", None))
        self.label_description_2.setText(QCoreApplication.translate("About", u"<html><head/><body><p>1. Roy Nielsen (<a href=\"https://github.com/roynielsen17\"><span style=\" font-weight:700; text-decoration: underline; color:#fb568a;\">github/roynielsen17</span></a>)</p><p><span style=\" font-weight:700;\">View eisenban on </span><a href=\"https://github.com/roynielsen17/eisenban\"><span style=\" font-weight:700; text-decoration: underline; color:#fb568a;\">Github</span></a></p>\n"
"Previously Kanbaru:</body></html>", None))
        self.label_logo_bottom.setText("")
        self.label_license.setText(QCoreApplication.translate("About", u"<html><head/><body><p>Eisenban is released under the MIT license. See <a href=\"https://github.com/dulapahv/eisenban/blob/main/LICENSE\"><span style=\" font-weight:700; text-decoration: underline; color:#fb568a;\">LICENSE</span></a> for more information.</p></body></html>", None))
    # retranslateUi


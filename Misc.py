# Copyright Killian Steunou

import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
from PyQt5.QtCore import Qt


class AutoscaledGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setRenderHint(QtGui.QPainter.Antialiasing, True)
        self.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.fitInView(self.scene().sceneRect(), Qt.KeepAspectRatio)


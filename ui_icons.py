"""Minimal vector glyphs for the KF2 Randomizer desktop GUI.

Icons are drawn directly by Qt; no emoji fonts, external assets or icon kits.
"""
from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPainterPath, QPen, QPixmap


def icon(name: str, color: str = "#AAB3C0", size: int = 20) -> QIcon:
    scale = 2
    pix = QPixmap(size * scale, size * scale)
    pix.setDevicePixelRatio(scale)
    pix.fill(Qt.GlobalColor.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.scale(size / 24, size / 24)
    pen = QPen(QColor(color), 1.75, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
    p.setPen(pen)
    p.setBrush(Qt.BrushStyle.NoBrush)

    def lines(*pairs: tuple[tuple[float, float], tuple[float, float]]) -> None:
        for (ax, ay), (bx, by) in pairs:
            p.drawLine(QPointF(ax, ay), QPointF(bx, by))

    def poly(*points: tuple[float, float]) -> None:
        path = QPainterPath(QPointF(*points[0]))
        for pt in points[1:]:
            path.lineTo(QPointF(*pt))
        p.drawPath(path)

    if name in {"random", "dice"}:
        p.drawRoundedRect(QRectF(4, 4, 16, 16), 3, 3)
        p.setBrush(QColor(color))
        for x, y in ((8, 8), (16, 8), (12, 12), (8, 16), (16, 16)):
            p.drawEllipse(QRectF(x - .8, y - .8, 1.6, 1.6))
    elif name in {"reroll", "update"}:
        path = QPainterPath(QPointF(19, 10))
        path.arcTo(QRectF(4, 4, 16, 16), 22, 300)
        p.drawPath(path)
        poly((17, 5), (20, 10), (15, 10))
    elif name == "copy":
        p.drawRoundedRect(QRectF(8, 7, 11, 13), 1.3, 1.3)
        poly((5, 17), (5, 4), (16, 4))
    elif name == "check":
        poly((5, 12), (10, 17), (19, 7))
    elif name == "map":
        poly((3, 6), (9, 3), (15, 6), (21, 3), (21, 18), (15, 21), (9, 18), (3, 21), (3, 6))
        lines(((9, 3), (9, 18)), ((15, 6), (15, 21)))
    elif name == "clock":
        p.drawEllipse(QRectF(3, 3, 18, 18))
        lines(((12, 7), (12, 12)), ((12, 12), (16, 14)))
    elif name == "settings":
        lines(((4, 7), (20, 7)), ((4, 12), (20, 12)), ((4, 17), (20, 17)))
        for x,y in ((9,7), (16,12), (7,17)):
            p.setBrush(QColor("#20252D"))
            p.drawEllipse(QRectF(x-2, y-2, 4, 4))
    elif name in {"class", "shield"}:
        poly((12, 3), (20, 6), (20, 12), (17, 17), (12, 21), (7, 17), (4, 12), (4, 6), (12, 3))
        poly((9, 12), (11, 14), (15, 10))
    elif name == "weapon":
        p.drawEllipse(QRectF(4, 4, 16, 16))
        lines(((12, 2), (12, 7)), ((12, 17), (12, 22)), ((2, 12), (7, 12)), ((17, 12), (22, 12)))
        p.drawEllipse(QRectF(10, 10, 4, 4))
    elif name == "history":
        path = QPainterPath(QPointF(6, 7))
        path.arcTo(QRectF(4, 4, 16, 16), 135, -300)
        p.drawPath(path)
        poly((6, 3), (6, 8), (11, 8))
        lines(((12, 8), (12, 12)), ((12, 12), (15, 14)))
    elif name == "trash":
        p.drawRoundedRect(QRectF(7, 8, 10, 12), 1, 1)
        lines(((5, 6), (19, 6)), ((10, 4), (14, 4)), ((10, 11), (10, 17)), ((14, 11), (14, 17)))
    elif name in {"medic", "medical"}:
        poly((10, 3), (14, 3), (14, 10), (21, 10), (21, 14), (14, 14), (14, 21), (10, 21), (10, 14), (3, 14), (3, 10), (10, 10), (10, 3))
    elif name in {"flame", "fire"}:
        path = QPainterPath(QPointF(12, 21))
        path.cubicTo(3, 21, 4, 14, 8, 10)
        path.cubicTo(9, 15, 11, 8, 13, 3)
        path.cubicTo(13, 9, 20, 11, 19, 16)
        path.cubicTo(19, 19, 16, 21, 12, 21)
        p.drawPath(path)
    elif name in {"explosive", "burst"}:
        poly((12, 2), (14, 9), (21, 6), (17, 12), (22, 17), (15, 16), (12, 22), (9, 16), (2, 18), (7, 12), (3, 6), (10, 9), (12, 2))
    elif name == "melee":
        lines(((5, 4), (19, 20)), ((19, 4), (5, 20)))
        poly((3, 4), (7, 4), (5, 8), (3, 4))
        poly((21, 4), (17, 4), (19, 8), (21, 4))
    elif name in {"handgun", "smg", "assault", "shotgun"}:
        # Abstract stacked instrument bars, not realistic firearm silhouettes.
        p.drawRoundedRect(QRectF(4, 5, 16, 4), 1.5, 1.5)
        p.drawRoundedRect(QRectF(4, 11, 12, 4), 1.5, 1.5)
        lines(((8, 15), (8, 20)))
    elif name == "precision":
        p.drawEllipse(QRectF(5, 5, 14, 14))
        p.drawEllipse(QRectF(9, 9, 6, 6))
        lines(((12, 2), (12, 6)), ((12, 18), (12, 22)), ((2, 12), (6, 12)), ((18, 12), (22, 12)))
    elif name == "special":
        poly((12, 3), (14.8, 9.5), (21, 12), (14.8, 14.5), (12, 21), (9.2, 14.5), (3, 12), (9.2, 9.5), (12, 3))
    elif name == "external":
        p.drawRoundedRect(QRectF(4, 7, 13, 13), 2, 2)
        poly((11, 4), (20, 4), (20, 13))
        lines(((20, 4), (11, 13)))
    else:
        p.drawEllipse(QRectF(9.5, 9.5, 5, 5))

    p.end()
    return QIcon(pix)
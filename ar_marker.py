# -*- coding: utf-8 -*-

import cv2
import sys

# arucoライブラリ
aruco = cv2.aruco
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)


def arGenerator():
    for i in range(50):
        generator = aruco.drawMarker(dictionary, i, 100)
        cv2.imwrite(str(i) + '.png', generator)


def arReader():
    cap = cv2.VideoCapture(0)

    while True:

        # ビデオキャプチャから画像を取得
        ret, frame = cap.read()

        # sizeを取得
        Height, Width = frame.shape[:2]

        # sizeを半分に縮小
        #halfHeight = Height / 2
        #halfWidth = Width / 2
        #imghalf = cv2.resize(frame, (halfWidth, halfHeight))

        # マーカを検出
        corners, ids, rejectedImgPoints = aruco.detectMarkers(
            frame, dictionary)
        # 検出したマーカに描画する
        aruco.drawDetectedMarkers(
            frame, corners, ids, (0, 255, 0))
        # print(rejectedImgPoints)
        # print(corners)

        # マーカが描画された画像を表示
        cv2.imshow('drawDetectedMarkers', frame)

        # Escキーで終了
        key = cv2.waitKey(33)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    args = sys.argv
    ar = args[1]
    if ar == "Generator":
        arGenerator()
    elif ar == "Reader":
        arReader()
    else:
        print("Please enter valid argument")

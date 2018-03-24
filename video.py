# -*- Coding: utf-8 -*-

import numpy as np
import cv2


def video_recording():
    # カメラの設定
    cap = cv2.VideoCapture(0)

    # オブジェクトの作成
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')

    # 動画保存の設定
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            #frame = cv2.flip(frame,0)

            # write the flipped frame
            out.write(frame)

            cv2.imshow('frame', frame)
            # qのキーを押すと動画停止
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # リリースする
    cap.release()
    out.release()
    cv2.destroyAllWindows()

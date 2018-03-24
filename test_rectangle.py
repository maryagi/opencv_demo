import cv2
from datetime import datetime


def cv_fourcc(c1, c2, c3, c4):
    return (ord(c1) & 255) + ((ord(c2) & 255) << 8) + \
        ((ord(c3) & 255) << 16) + ((ord(c4) & 255) << 24)


if __name__ == '__main__':
    # 定数定義
    ESC_KEY = 27     # Escキー
    INTERVAL = 33     # 待ち時間
    FRAME_RATE = 30  # fps

    ORG_WINDOW_NAME = "org"
    GAUSSIAN_WINDOW_NAME = "gaussian"

    output_video = "output_{}.MOV".format(
        datetime.now().strftime("%Y%m%d_%H%M"))
    OUTPUT_FILE_NAME = output_video

    DEVICE_ID = 1

    # カメラ映像取得
    cap = cv2.VideoCapture(DEVICE_ID)

    # 保存ビデオファイルの準備
    end_flag, c_frame = cap.read()
    height, width, channels = c_frame.shape
    rec = cv2.VideoWriter(OUTPUT_FILE_NAME,
                          cv_fourcc('X', 'V', 'I', 'D'),
                          FRAME_RATE,
                          (width, height),
                          True)

    # ウィンドウの準備
    cv2.namedWindow(ORG_WINDOW_NAME)
    cv2.namedWindow(GAUSSIAN_WINDOW_NAME)

    # 変換処理ループ
    while end_flag == True:

        rectangle_frame = c_frame.copy()

        # グレースケール変換と画面の平滑化を行う
        im_gray = cv2.cvtColor(rectangle_frame, cv2.COLOR_BGR2GRAY)
        im_blur = cv2.GaussianBlur(im_gray, (11, 11), 0)

        # 部分に応じて適応的にしきい値を設定する adaptiveThreshold 関数を使用する
        thresh = cv2.adaptiveThreshold(
            im_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 3)

        # OpenCVで画像の輪郭抽出を行う場合には、findContoursという関数を使用する
        # 第一引数に入力画像、第二引数に抽出モード、第三引数に近似手法を取る
        imgEdge, contours, hierarchy = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # filtered with area over (all area / 100 )
        th_area = rectangle_frame.shape[0] * rectangle_frame.shape[1] / 500
        contours_large = list(
            filter(lambda c: cv2.contourArea(c) > th_area, contours))

        crops = []
        # draw contour
        for c in contours_large:
            if cv2.contourArea(c) < 4:
                continue

            # rectangle area
            x, y, w, h = cv2.boundingRect(c)

            # cv2.drawContoursで簡単に画像上に描画する
            # 点で囲む
            # cv2.drawContours(im, c, -1, (0, 0, 255), 3)
            # 線で囲む
            cv2.rectangle(rectangle_frame, (x, y),
                          (x + w, y + h), (100, 255, 100), 3)

        # フレーム表示
        cv2.imshow(ORG_WINDOW_NAME, c_frame)
        cv2.imshow(GAUSSIAN_WINDOW_NAME, rectangle_frame)

        # フレーム書き込み
        rec.write(rectangle_frame)

        # Escキーで終了
        key = cv2.waitKey(INTERVAL)
        if key == ESC_KEY:
            break

        # 次のフレーム読み込み
        end_flag, c_frame = cap.read()

    # 終了処理
    cv2.destroyAllWindows()
    cap.release()
    rec.release()

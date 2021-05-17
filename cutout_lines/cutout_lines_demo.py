import cv2
import numpy as np


def get_y_axis(image):
    y_axises = []  # 出力用の切り出し座標がを保存するリスト
    all_white_axises = []  # 対象の行となり得る座標を一時保存するリスト
    image_top = 0
    image_bottom = image.shape[0]
    image_left = 0
    image_right = image.shape[1]
    for y in range(image_top, image_bottom):
        # 二次元配列の配列要素ごと行内の黒の有無を調べる
        includeBlackFlag = np.count_nonzero(
            image[y][image_left:image_right] == 0)
        # 全て白の場合は切り出し行候補として一時保存
        if includeBlackFlag == 0:
            all_white_axises.append(y)

        # 黒が含まれる行が出てきた場合は次の行に到達したと判断
        elif len(all_white_axises) > 0:
            centerIndex = int(len(all_white_axises) / 2)
            y_axises.append(all_white_axises[centerIndex])
            all_white_axises.clear()
    y_axises.append(image_bottom)
    return y_axises


def search_and_add_x_axis(image_rotate_90, image_height, image_left,
                          image_right, all_white_axises, x_axises, index):

    # 二次元配列の配列要素ごと行内の黒の有無を調べる
    includeBlackFlag = np.count_nonzero(
        image_rotate_90[image_height][image_left:image_right] == 0)
    # 全て白の場合は切り出し行候補として一時保存
    if includeBlackFlag == 0:
        all_white_axises.append(image_height)
        return 0

    # 黒が含まれる行が出てきた場合は次の行に到達したと判断
    elif len(all_white_axises) > 0:
        x_axises.append(all_white_axises[index])
        all_white_axises.clear()
        return 1


def get_x_axis(image, top, bottom):
    x_axises = []  # 出力用の切り出し座標がを保存するリスト
    all_white_axises = []  # 対象の行となり得る座標を一時保存するリスト

    # 画像を90度回転
    image_rotate_90 = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    image_top = 0
    image_bottom = image_rotate_90.shape[0]
    image_left = top
    image_right = bottom

    for image_height in range(image_top, image_bottom):
        flag = search_and_add_x_axis(image_rotate_90,
                                     image_height,
                                     image_left,
                                     image_right,
                                     all_white_axises,
                                     x_axises,
                                     -5)
        if flag == 1:
            break

    for image_height in reversed(range(image_top, image_bottom)):
        flag = search_and_add_x_axis(image_rotate_90,
                                     image_height,
                                     image_left,
                                     image_right,
                                     all_white_axises,
                                     x_axises,
                                     -5)
        if flag == 1:
            break
    return x_axises

if __name__ == "__main__":
    img = cv2.imread("sample.jpg")

    y_axis_list = get_y_axis(img)
    for index in range(0, len(y_axis_list) - 1):
        top = y_axis_list[index]
        bottom = y_axis_list[index + 1]
        x_axises = get_x_axis(img, top, bottom)

        left = x_axises[0]
        right = x_axises[1]
        cv2.imwrite(str(index) + ".jpg", img[top: bottom, left: right])

import cv2

img_object = cv2.imread("object.jpg")
img_background = cv2.imread("background.jpg")

img_bgt = cv2.split(img_object)

height = img_object.shape[0]
width = img_object.shape[1]
img_background = cv2.resize(img_background, (int(width), int(height)))

# 画素値ごとに二値化
img_bgtR = cv2.threshold(img_bgt[0], 230, 255, cv2.THRESH_BINARY_INV)[1]
img_bgtG = cv2.threshold(img_bgt[1], 170, 255, cv2.THRESH_BINARY_INV)[1]
img_bgtB = cv2.threshold(img_bgt[2], 175, 255, cv2.THRESH_BINARY_INV)[1]

# 背景が黒になってしまうため逆値をとる(閾値を下げて調節すれば必要ない)
img_bgtR = cv2.bitwise_not(img_bgtR)
img_bgtG = cv2.bitwise_not(img_bgtG)
img_bgtB = cv2.bitwise_not(img_bgtB)

# R,G,B要素ごと画像生成
img_mskR = cv2.merge((img_bgtR, img_bgtR, img_bgtR))
img_mskG = cv2.merge((img_bgtG, img_bgtG, img_bgtG))
img_mskB = cv2.merge((img_bgtB, img_bgtB, img_bgtB))

# 物体を切り抜いていく
img_msk = cv2.bitwise_and(img_object, img_mskB)
img_msk = cv2.bitwise_and(img_msk, img_mskG)
img_msk = cv2.bitwise_and(img_msk, img_mskR)

# シルエット作成
img_msk = cv2.cvtColor(img_msk, cv2.COLOR_BGR2GRAY)
img_msk = cv2.threshold(img_msk, 10, 255, cv2.THRESH_BINARY_INV)[1]

# マスク画像にする(チャネル数を揃える)
img_msk = cv2.merge((img_msk, img_msk, img_msk))

# 合成対象物の背景を消す
img_s1m = cv2.bitwise_and(img_object, img_msk)

# 背景用のマスキング画像作成
img_mskn = cv2.bitwise_not(img_msk)

# 背景から対象物のシルエットを抜き出す
img_s2m = cv2.bitwise_and(img_background, img_mskn)

# 合成
img_synthetic = cv2.bitwise_or(img_s1m, img_s2m)
cv2.imwrite("Synthetic_image.jpg", img_synthetic)

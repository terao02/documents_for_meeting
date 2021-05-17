"""
論文内の「鞍点で学習速度の低下するが学習速度を上げることで鞍点を早く抜け出すことができる」
とあったが、オプティマイザ(SGD以降)のアルゴリズムは学習率も変更されるはずであり、
その条件下でも学習速度が低下するのか、また学習率を上げた時の挙動はどうなるのか疑問に
思ったため検証するために作成したプログラム。
(プレゼン資料5、6ページ図作成用プログラム)
"""
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

 
# グラフプロット用基準関数
def f(x, y):
    z = x ** 2  - y ** 2
    return z

# 基準関数の微分
def df(x, y):
    dzdx = 2 * x
    dzdy = - y ** 2
    dz = np.array([dzdx, dzdy])
    return dz

 
# 共通のパラメータ
max_iteration = 20 # 最大反復回数


# RMSpropのパラメータ
eta_rms = 0.31
ro = 0.9
x0_rms = -2
y0_rms = -1
x_rms = [x0_rms]
y_rms = [y0_rms]
h0_rms = np.array([1, 0])
rms_lr_rate = []

# adamのパラメータ
eta_adam = 0.0001
bata_1 = 0.9
bata_2 = 0.999
x0_adam = 0
y0_adam = 0
x_adams = [x0_adam]
y_adams = [y0_adam]
v = np.array([0, 0])
s = np.array([0, 0])
x_adam_eta = []
y_adam_eta = []
iteras = []

# adaDelta
ro_adaD = 0.95
x0_adaD = -10
y0_adaD = 2
x_adaD = [x0_adaD]
y_adaD = [y0_adaD]
u_t = np.array([0, 0])
v_t = np.array([0, 0])

# 最大反復回数まで計算する
for i in range(max_iteration):
    
    # RMSPropの更新
    h0_rms = ro * h0_rms + (1.0 - ro) * df(x0_rms, y0_rms) ** 2.0
    lr = eta_rms
    x0_rms, y0_rms = np.array([x0_rms, y0_rms]) - lr * (1.0 / np.sqrt(h0_rms + 1e-7)) * df(x0_rms, y0_rms)
    x_rms.append(x0_rms)
    y_rms.append(y0_rms)
    
    # adamの更新
    v = bata_1 * v + (1 - bata_1) * df(x0_adam, y0_adam)
    s = bata_2 * s + (1 - bata_2) * df(x0_adam, y0_adam) ** 2
    x0_adam, y0_adam = np.array([x0_adam, y0_adam]) - eta_adam * (v/(np.sqrt(s)+1e-7))
    x_adams.append(x0_adam)
    y_adams.append(y0_adam)

    # adamDeltaの更新
    g_t = np.array([x0_adaD, y0_adaD])
    v_t = ro_adaD * v_t + (1 - ro_adaD)*(g_t**2)
    u_t = ro_adaD * u_t + (1 - ro_adaD)*((-np.sqrt(u_t + 1e-7)/np.sqrt(v_t + 1e-7) * df(x0_adaD, y0_adaD))** 2)
    x0_adaD, y0_adaD = np.array([x0_adaD, y0_adaD]) - np.sqrt(u_t + 1e-7)/np.sqrt(v_t + 1e-7) * df(x0_adaD, y0_adaD)
    x_adaD.append(x0_adaD)
    y_adaD.append(y0_adaD)

x_rms = np.array(x_rms)
y_rms = np.array(y_rms)
z_rms = f(x_rms, y_rms)

x_adams = np.array(x_adams)
y_adams = np.array(y_adams)
z_adams = f(x_adams, y_adams)

x_adaD = np.array(x_adaD)
y_adaD = np.array(y_adaD)
z_adaD = f(x_adaD, y_adaD)


# フォントの種類とサイズを設定する。
plt.rcParams['font.size'] = 14
plt.rcParams['font.family'] = 'Times New Roman'
 
#  グラフの入れ物を用意する。
#fig = plt.figure()
#ax1 = Axes3D(fig)
fig = plt.figure(figsize=(8, 8))
ax1 = fig.add_subplot(111, projection='3d') 
# 軸のラベルを設定する。
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_zlabel('z')

# 基準関数の表示用
x = np.linspace(-2.5, 2.5, 100)
y = np.linspace(-2.5, 2.5, 100)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)
ax1.view_init(elev=60, azim=-30)

# データプロットする。
ax1.plot_wireframe(X, Y, Z, color="gray", linewidth=0.5)
ax1.scatter3D(x_rms, y_rms, z_rms, label="PMSProp(lr=" + str(eta_rms) +")", color='b', s=10)
ax1.scatter3D(x_rms[0], y_rms[0], z_rms[0], label="start(" + str(x_rms[0]) + ", " + str(y_rms[0]) + ", " +  str(z_rms[0]) + ")", c='r', s=50)
ax1.scatter3D(x0_rms, y0_rms, f(x0_rms, y0_rms), label="end", c='g', s=50)

# グラフを表示する。
plt.legend()
plt.show()
plt.close()

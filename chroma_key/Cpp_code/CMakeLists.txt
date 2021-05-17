# CMakeのバージョン
cmake_minimum_required(VERSION 3.1)

# プロジェクト名
project (test)

# OpenCVのパッケージを探す
find_package(OpenCV REQUIRED)

# ヘッダファイルのパスを指定
include_directories( ${OpenCV_INCLUDE_DIRS} )

# 実行ファイル名とソースファイル指定
add_executable(new_croma_key new_croma_key.cpp)

# リンク先のライブラリを指定
target_link_libraries(new_croma_key ${OpenCV_LIBS})

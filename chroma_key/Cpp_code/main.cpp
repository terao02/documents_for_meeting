# define _USE_MATH_DEFINES
# include <iostream>
# include <opencv2/opencv.hpp>
# include <cmath>
int main() {
    // 対象画像の読み込み(img_src1: 物体画像, img_src2: 背景画像)
    cv::Mat img_src1 = cv::imread("../sample/object.jpg", 1);
    cv::Mat img_src2 = cv::imread("../sample/backGround.jpg", 1);
    //cv::Mat img_src2;
    cv::Mat img_g1;
    cv::Mat img_mskg;
    cv::Mat img_msk;
    cv::Mat img_s1m;
    cv::Mat img_mskn;
    cv::Mat img_s2m;
    cv::Mat img_dst;

    float width = img_src1.rows;
    float height = img_src1.cols;
    
    resize(img_src2, img_src2, cv::Size(), height/img_src2.cols , width/img_src2.rows);
    cv::cvtColor(img_src1, img_g1, cv::COLOR_BGR2GRAY);
    cv::threshold(img_g1, img_mskg, 170, 255, cv::THRESH_BINARY_INV);

    std::vector<cv::Mat> channels;
    channels.push_back(img_mskg);
    channels.push_back(img_mskg);
    channels.push_back(img_mskg);

    cv::merge(channels, img_msk);

    cv::bitwise_and(img_src1, img_msk, img_s1m);

    cv::bitwise_not(img_msk, img_mskn);

    cv::bitwise_and(img_src2, img_mskn, img_s2m);

    cv::bitwise_or(img_s1m, img_s2m, img_dst);
    
    cv::imwrite("../sample/synthetic_image_old.jpg", img_dst);
    return 0;
}

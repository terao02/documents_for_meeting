# include <iostream>
# include <opencv2/opencv.hpp>
# include <vector>

using namespace std;

cv::Mat make_nega_Binarization_img(int, cv::Mat*);

cv::Mat make_mask_image(cv::Mat*);

int main(){
    cv::Mat img_src1 = cv::imread("../sample/object.jpg", 1);
    cv::Mat img_src2 = cv::imread("../sample/backGround.jpg", 1);

    float width = img_src1.rows;
    float height = img_src1.cols;
    resize(img_src2, img_src2, cv::Size(), height/img_src2.cols , width/img_src2.rows);

    // RGB要素ごとに画像を分解
    cv::Mat split_channels[3], red, blue, green;
    cv::split(img_src1, split_channels);
    green = split_channels[0];
    blue = split_channels[1];
    red = split_channels[2];

    // 各要素ごとに二値化を行い二値化画像を逆値に変換
    cv::Mat mskg_green = make_nega_Binarization_img(230, &green);
    cv::Mat mskg_blue = make_nega_Binarization_img(170, &blue);
    cv::Mat mskg_red = make_nega_Binarization_img(175, &red);

    // 緑要素のマスク画像を作成
    cv::Mat img_msk_green = make_mask_image(&mskg_green);

    // 青要素のマスク画像を作成
    cv::Mat img_msk_blue = make_mask_image(&mskg_blue);

    // 赤要素のマスク画像を作成
    cv::Mat img_msk_red = make_mask_image(&mskg_red);

    // 各画素値のマスク画像を使用し対象物が写っている画像の背景を白に変換
    cv::Mat img_mskg;
    cv::bitwise_and(img_src1, img_msk_green, img_mskg);
    cv::bitwise_and(img_mskg, img_msk_blue, img_mskg);
    cv::bitwise_and(img_mskg, img_msk_red, img_mskg);
    cv::cvtColor(img_mskg, img_mskg, cv::COLOR_BGR2GRAY);
    cv::threshold(img_mskg, img_mskg, 10, 255, cv::THRESH_BINARY_INV);

    // RGBマスク画像生成
    cv::Mat img_msk = make_mask_image(&img_mskg);

    cv::Mat img_s1m;
    cv::Mat img_mskn;
    cv::Mat img_s2m;
    cv::Mat img_dst;

    // メイン画像から対象物を切り抜き
    cv::bitwise_and(img_src1, img_msk, img_s1m);
    // 1,0逆転
    cv::bitwise_not(img_msk, img_mskn);
    // 背景から対象物領域を切り抜き
    cv::bitwise_and(img_src2, img_mskn, img_s2m);
    // 合成
    cv::bitwise_or(img_s1m, img_s2m, img_dst);
    cv::imshow("synthetic image", img_dst);
    cv::waitKey(0);
    cv::imwrite("../sample/synthetic_cpp.jpg", img_dst);
    return 0;
}

cv::Mat make_nega_Binarization_img(int treshold, cv::Mat* target_image){
    /*
    二値化処理と1,0逆転処理を行う関数
    param: treshold        二値化処理時の閾値
    param: target_image    二値化処理対象の画像
    param: binarized_image 二値化処理後の画像
    */
    cv::Mat binarized_image;
    cv::threshold(*target_image, binarized_image, treshold, 255, cv::THRESH_BINARY_INV);
    cv::bitwise_not(binarized_image, binarized_image);
    return binarized_image;
}

cv::Mat make_mask_image(cv::Mat* mskg_img){
    /*
    マスク画像の生成を行う関数
    param mskg_img マスク画像の元(二値化画像)
    param msk_img  ]マスク画像
    */
    cv::Mat msk_img;
    vector<cv::Mat> channels;
    channels.push_back(*mskg_img);
    channels.push_back(*mskg_img);
    channels.push_back(*mskg_img);
    cv::merge(channels, msk_img);
    return msk_img;
}

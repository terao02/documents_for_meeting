from functools import lru_cache

# 流動資産 辞書(代表科目名参照)
CURRENT_ASSETS = ["現金", "小口現金", "普通預金", "当座預金", "定期預金",
                  "定期積金", "通知預金", "別段預金", "受取手形", "売掛金",
                  "△貸倒引当金", "有価証券", "商品", "製品", "半製品",
                  "仕掛品", "原材料", "貯蔵品", "短期貸付金", "△貸倒引当金",
                  "前渡金", "立替金", "仮払金", "仮払消費税等", "未収入金",
                  "未収消費税等", "前払費用", "未収収益", "繰延税金資産",
                  # "現金及び預金","繰延税金資産", "貸倒引当金" # +科目名
                  ]

# 固定資産 辞書(代表科目名参照)
FIXED_ASSETS = ["建物", "建物付属設備", "構築物", "機械及び装置",
                "車両運搬具", "器具及び備品", "△減価償却累計額", "土地",
                "建設仮勘定", "電話加入権", "特許権", "借地権", "のれん",
                "営業権", "水道施設利用権", "ソフトウェア", "投資有価証券",
                "関連会社株式", "出資金", "長期貸付金", "△貸倒引当金",
                "ゴルフ会員権", "敷金", "保証金", "保険積立金",
                "長期前払費用", "破産更生債権", "繰延税金資産",
                # "繰延税金資産", "貸倒引当金" # +科目
                ]

# 繰越資産 辞書(代表科目名参照)
DEFERRED_ASSETS = ["創立費", "開業費", "株式交付費", "社債発行費", "開発費"]

# 流動負債 辞書(代表科目名参照)
CURRENT_LIABILITIES = ["支払手形", "買掛金", "短期借入金", "未払金",
                       "未払配当金", "未払法人税等", "未払消費税等",
                       "未払費用",
                       # "前受金","賞与引当金" # +科目
                       ]

# 固定負債 辞書(代表科目名参照)
FIXED_LIABILITIES = ["社債", "長期借入金", "退職給与引当金", "負ののれん",
                     "繰延税金負債"]

# 株主資本 辞書(代表科目名参照)
CAPITAL_STOCK = ["資本金", "新株式申込証拠金", "資本準備金",
                 "その他の資本剰余金", "利益準備金", "繰越利益剰余金",
                 "自己株式",
                 ]

# 評価・換算差額(代表科目名参照)
TRANSLATION_DIFFERENCES = ["その他有価証券評価差額金", "繰越ヘッジ損失",
                           "土地再評価差額金",
                           # "為替換算調整勘定" # +科目
                           ]

# 新株予約権(代表科目名参照)
CALL_OPTION = ["新株予約権"]

ALL_DICTIONARY = [CURRENT_ASSETS, FIXED_ASSETS,
                  DEFERRED_ASSETS, CURRENT_LIABILITIES,
                  FIXED_LIABILITIES, CAPITAL_STOCK, TRANSLATION_DIFFERENCES,
                  CALL_OPTION]

COURSE_TITLE = ["流動資産", "固定資産", "繰越資産", "流動負債",
                "固定負債", "株主資本", "評価・換算差額", "新株予約権"]


@lru_cache(maxsize=4096)
def get_distance(s, t):
    if not s:
        return len(t)
    if not t:
        return len(s)
    if s[0] == t[0]:
        return get_distance(s[1:], t[1:])

    l1 = get_distance(s, t[1:])
    l2 = get_distance(s[1:], t)
    l3 = get_distance(s[1:], t[1:])
    return 1 + min(l1, l2, l3)


def categorize_course_title(value, all_dictionary):
    # 辞書全ての最小レーベンシュタイン距離を保存するリスト
    leven_distance_all_dict = []
    for dictionary in all_dictionary:
        # 辞書内の全文字とのレーベンシュタイン距離を補完するリスト
        leven_distance_in_dict = []
        for object in dictionary:

            normalization = (max(len(value), len(object)) * 1.00)
            leven_shtein_distance = get_distance(value, object)
            leven_shtein_distance = leven_shtein_distance / normalization

            leven_distance_in_dict.append(leven_shtein_distance)
        leven_distance_all_dict.append(min(leven_distance_in_dict))

    min_index = [index for index, v in enumerate(leven_distance_all_dict)
                 if v == min(leven_distance_all_dict)]
    return min_index


# 株式会社ラクス2016年貸借対照表科目名(分類対象の決算書名)
sample_data = ["現金及び預金", "売掛金", "商品", "繰延税金資産", "貸倒引当金",
               "建物及び構築物（純額）", "工具、器具及び備品（純額）",
               "ソフトウエア", "差入保証金", "繰延税金資産", "貸倒引当金", "買掛金",
               "未払金", "未払費用", "未払法人税等", "未払消費税等", "前受金",
               "賞与引当金", "資本金", "資本剰余金", "利益剰余金", "繰延ヘッジ損益",
               "為替換算調整勘定"]
# 分類対象の正解科目名
answer_label = ["流動資産", "流動資産", "流動資産", "流動資産", "流動資産", "固定資産",
               "固定資産", "固定資産", "固定資産", "固定資産", "固定資産", "流動負債",
               "流動負債", "流動負債", "流動負債", "流動負債", "流動負債", "流動負債",
               "株主資本", "株主資本", "株主資本", "評価・換算差額", "評価・換算差額"]

ok_sum = 0
all_subject = 0

for i in range(len(sample_data)):
    # 科目名の分類先検索
    course_title_index = categorize_course_title(sample_data[i], ALL_DICTIONARY)

    number_of_out_put_index = len(course_title_index)
    predict_name = COURSE_TITLE[course_title_index[0]]

    if predict_name == answer_label[i] and number_of_out_put_index == 1:
        answer = " "
        ok_sum += 1

    elif number_of_out_put_index != 1:
        answer = "△"
    else:
        answer = "X"

    print(answer, " ", "予測 : ", predict_name,
          "  " * (15 - len("予測 : " + predict_name)),
          "正解 : ", answer_label[i])

but_sum = len(sample_data) - ok_sum

print("正: ", ok_sum, "不: ", but_sum, "正答率 ", ok_sum / len(sample_data))

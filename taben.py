import glob
import datetime
import requests
import json
import csv
from dataclasses import replace
import requests
from bs4 import BeautifulSoup
import re
import numpy as np
from pathlib import Path
import os

# 今日の日にち
dt = datetime.datetime.today()
d = dt.date()
print("\n")
print("今日は" + str(d) + "です。")
print("どのようなご用件ですか？")
line = int(input("1:予定登録, 2:予定確認, 3:天気, 4:ニュース, 5:出欠登録, 0:予定削除:"))

# 予定の登録
if line == 1:
    print("\n")
    print("予定は？")
    j = input()
    print("何年、何月、何日ですか？ (例:2000,01,23)")
    i = input()
    a = i.split(",")
    b = [int(i) for i in a]

    dt1 = datetime.datetime.today()
    dt2 = datetime.datetime(b[0], b[1], b[2])
    dt3 = dt2 - dt1

    print(str(j) + "までは、後" + str(dt3.days) + "日後です。")
    x = int(input("何番に保存しますか？:"))

    # セーブデータ

    f = open(f'yotei/yotei{x}.csv', 'w')
    data = [str(j), str(i)]
    writer = csv.writer(f)
    writer.writerows(data)
    f.close()
    os.system('git add .')
    os.system('git commit -m "test"')
    os.system('git push heroku master')

elif line == 2:
    print("\n")
    print("今後の予定は、")

    files = os.listdir("./yotei")
    for filename in files:
        a = np.genfromtxt("yotei/" + filename, encoding='utf8', dtype=None)
        aa = (f"{filename}:"+str(a).replace('"', ""))
        print(str(aa).replace(",", ""))

    # 今日の天気

elif line == 3:
    print("\n")

    # エリアコード
    area_dic = {'兵庫県': '280000', }

    # CSV出力先
    output_file = "tenki.csv"

    # CSVヘッダー
    header = ["都道府県", "データ配信元",
              "地方名", "予報日時", "天気", ]

    def main():
        make_csv()

    def make_csv():
        with open(output_file, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, lineterminator="\n")
            writer.writerow(header)

            # JSONから情報を取得
            write_lists = get_info()

            # CSV書き込み
            writer.writerows(write_lists)

    def get_info():
        write_lists = []
        base_url = "https://www.jma.go.jp/bosai/forecast/data/forecast/"
        for k, v in area_dic.items():

            if k.find("/"):
                prefecture = k[0:k.find("/")]
            else:
                prefecture = k

            url = base_url + v + ".json"

            res = requests.get(url).json()

            for re in res:
                publishingOffice = re["publishingOffice"]
                reportDatetime = re["reportDatetime"]

                timeSeries = re["timeSeries"]

                for time in timeSeries:
                    # 降水確率など今回のターゲット以外は除外する
                    if 'pops' in time["areas"][0]:
                        pass
                    elif 'temps' in time["areas"][0]:
                        pass
                    elif 'tempsMax' in time["areas"][0]:
                        pass
                    else:
                        for i in range(len(time["areas"])):

                            local_name = time["areas"][i]["area"]["name"]

                            for j in range(len(timeSeries[0]["timeDefines"])):

                                if 'weathers' not in time["areas"][i]:
                                    weather = ""
                                else:
                                    weather = time["areas"][i]["weathers"][j]

                                if 'winds' not in time["areas"][i]:
                                    wind = ""
                                else:
                                    wind = time["areas"][i]["winds"][j]

                                if 'waves' not in time["areas"][i]:
                                    wave = ""
                                else:
                                    wave = time["areas"][i]["waves"][j]

                                timeDefine = time["timeDefines"][j]

                                # 各情報をリストに格納
                                write_list = []
                                write_list.append(prefecture)
                                write_list.append(publishingOffice)
                                write_list.append(local_name)
                                write_list.append(timeDefine)
                                write_list.append(weather)
                                write_lists.append(write_list)
        return write_lists

    if __name__ == '__main__':
        main()

    filename = 'tenki.csv'
    with open(filename, encoding='utf8', newline='') as f:
        csvreader = csv.reader(f)
        os.system('git add .')
        os.system('git commit -m "test"')
        os.system('git push heroku master')
        for i in csvreader:
            j = [item.replace("\u3000", "") for item in i]
            print(str(j).replace(",", ""))

    # ニュース
elif line == 4:
    print("\n")
    # ヤフーニュースのトップページ情報を取得する
    URL = "https://www.yahoo.co.jp/"
    rest = requests.get(URL)

    # BeautifulSoupにヤフーニュースのページ内容を読み込ませる
    soup = BeautifulSoup(rest.text, "html.parser")

    # ヤフーニュースの見出しとURLの情報を取得して出力する
    data_list = soup.find_all(href=re.compile("news.yahoo.co.jp/pickup"))
    for data in data_list:
        print(data.span.string)
        print(data.attrs["href"])

elif line == 5:
    print("\n")
    print("出席:" + "\n"+"[ " + "https://forms.gle/uXYUTBYEti5ofuRm6" + " ]")
    print("欠席:" + "\n"+"[ " + "https://forms.gle/ZgbsebUJgVLx8i3s7" + " ]")
    print("AI開発情報サイト:" + "\n" + "[ " + "https://sites.google.com/st.kobedenshi.ac.jp/it-info/%E3%82%AA%E3%83%B3%E3%83%A9%E3%82%A4%E3%83%B3%E6%8E%88%E6%A5%AD%E3%83%9D%E3%83%BC%E3%82%BF%E3%83%AB2022/ai%E3%83%86%E3%82%AF%E3%83%8E%E3%83%AD%E3%82%B8%E3%83%BC%E3%82%B3%E3%83%BC%E3%82%B9?authuser=0" + " ]")

elif line == 0:
    print("\n")
    yesno = input("本当に削除しますか？( y / n ):")

    if yesno == "y":
        x = int(input("どの予定を消しますか？:"))
        files = os.remove(f"yotei/yotei{x}.csv")
        print(str(x)+"の予定を消去しました。")

    elif yesno == "n":
        print("わかりました。")

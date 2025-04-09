import streamlit as st
import matplotlib.pyplot as plt
from math import pi
import matplotlib.font_manager as fm
from PIL import Image

from trend_analysis.process_trend import analysis_trend

# 日本語フォントのパスを指定
jp_font_path = jp_font_path = 'trend_analysis/fonts/NotoSansJP-VariableFont_wght.ttf'   # フォントのパス


def save_radar_chart(categories, values, save_file_path):
    """
    レーダーチャートを描画し、必要に応じてPNGファイルとして保存する。

    Parameters:
    categories (list): チャートに表示するカテゴリ名のリスト
    values (list): 各カテゴリに対応する値のリスト
    filename (str, optional): PNGとして保存するファイルのパス。Noneの場合は保存しない
    """

    # 各カテゴリの角度を計算
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]  # 最後の角度を最初と同じにして閉じる
    values += values[:1]  # データを閉じるために再度最初の値を追加

    # レーダーチャートをプロット
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # ラベルをセット
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    # 各カテゴリに対応する軸を設定
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontproperties=fm.FontProperties(fname=jp_font_path))

    # グラフを描画
    ax.plot(angles, values, linewidth=2, linestyle='solid')
    ax.fill(angles, values, 'b', alpha=0.3)

    # タイトルを設定
    plt.title('', fontproperties=fm.FontProperties(fname=jp_font_path))

    # PNGファイルとして保存する場合
    if save_file_path:
        fig.savefig(save_file_path, format='png')


# メインのStreamlitアプリケーション
def create_chart():
    # CSVファイルが既に存在する場合
    file_path_1 = 'database/word_db.csv'
    file_path_2 = 'database/paper_db.csv'

    # レーダーチャート画像の保存パス
    chart_path_1 = 'images/trend_word.png'
    chart_path_2 = 'images/trend_paper.png'

    # ボタンが押された場合のみレーダーチャートを再生成
    if st.button("レーダーチャートを再生成"):
        categories_1, values_1 = analysis_trend(file_path_1)
        save_radar_chart(categories_1, values_1, chart_path_1)

        categories_2, values_2 = analysis_trend(file_path_2)
        save_radar_chart(categories_2, values_2, chart_path_2)


def main():
    
    st.title("単語傾向の可視化")
    create_chart()

    # 画像を読み込む
    image_word = Image.open('images/trend_word.png')
    st.header("単語検索")
    st.image(image_word, use_column_width=True)

    # 画像を読み込む
    image_paper = Image.open('images/trend_paper.png')
    st.header("論文")
    st.image(image_paper, use_column_width=True)

    
main()

if __name__ == "__main__":
    main()
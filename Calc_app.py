import streamlit as st
import pandas as pd
from PIL import Image # 画像を扱うためのライブラリを追加

# ページの設定
st.set_page_config(page_title="Fenice 金額検索", layout="centered")

# --- タイトル部分を画像に差し替え ---
try:
    image = Image.open('Feniceロゴ.jpg')
    width, height = image.size
    new_height = height // 6
    new_width = int(width * (new_height / height))
    
    # ロゴを表示
    st.image(image, width=new_width)

    # CSSで余白を強制的に詰め、自作の線を入れる
    st.markdown("""
        <style>
            /* ロゴ画像の直後の余白を消す */
            .stImage {
                margin-bottom: -20px;
            }
            /* 独自の区切り線スタイル */
            .custom-line {
                border-bottom: 1px solid #ddd;
                margin-top: 0px;
                margin-bottom: 20px;
            }
        </style>
        <div class="custom-line"></div>
    """, unsafe_allow_html=True)
    
except FileNotFoundError:    # 万が一画像がない場合はテキストを表示
    st.title("💰 Fenice 商品金額検索")
st.divider() # 区切り線を入れる
# -------------------------------------

# 加算する金額の定義
ADD_VALUES = {
    'SVP': 19500, 'SP': 15000, 'J': 10500, 'P': 9000, 'V': 6000
}

@st.cache_data
def load_data():
    # items.xlsx を読み込み
    df = pd.read_excel('items.xlsx', header=2)
    df['品番'] = df['品番'].astype(str).str.strip()
    return df

try:
    df = load_data()
    search_query = st.text_input("品番を入力してください（例: RAT）").strip()

    if search_query:
        # 部分一致で検索
        result = df[df['品番'].str.contains(search_query, case=False, na=False)]

        if not result.empty:
            for _, row in result.iterrows():
                st.subheader(f"品番: {row['品番']}")
                st.caption(f"ブランド: {row['ブランド']}")

                # 表示用のデータリストを作成
                display_data = []
                for label, add_price in ADD_VALUES.items():
                    base_val = row[label]
                    if pd.notnull(base_val) and isinstance(base_val, (int, float)):
                        calc_tax_ex = base_val + add_price
                        calc_tax_in = calc_tax_ex * 1.1
                        
                        display_data.append({
                            "項目": label,
                            "税抜(加算後)": f"{calc_tax_ex:,.0f}円",
                            "税込(10%)": f"{calc_tax_in:,.0f}円"
                        })
                
                # 前回の表（テーブル）形式で表示
                st.table(pd.DataFrame(display_data))
                st.divider()
        else:
            st.warning("該当する品番が見つかりませんでした。")

except Exception as e:
    st.error("エラーが発生しました。ファイル名や形式を確認してください。")
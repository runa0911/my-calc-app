import streamlit as st
import pandas as pd

# ページの設定（スマホで見やすく）
st.set_page_config(page_title="26SS原価表検索", layout="centered")

st.title("🔍 商品情報検索")

@st.cache_data
def load_data():
    # 最初の2行（タイトル行など）を飛ばして3行目をヘッダーとして読み込む
    df = pd.read_excel('items.xlsx', header=2)
    # 余分な空白を削除
    df['品番'] = df['品番'].astype(str).str.strip()
    return df

try:
    df = load_data()

    # 品番検索（大文字で入力しても探せるようにします）
    search_query = st.text_input("品番を入力してください").strip()

    if search_query:
        # 大文字小文字を区別せずに検索
        result = df[df['品番'].str.contains(search_query, case=False, na=False)]

        if not result.empty:
            for _, row in result.iterrows():
                st.success(f"品番: {row['品番']}")
                
                # 縦に情報を並べる
                # ラベルと値を整理して表示
                data_list = [
                    ("ブランド", row['ブランド']),
                    ("SP", row['SP']),
                    ("SVP", row['SVP']),
                    ("J", row['J']),
                    ("P", row['P']),
                    ("V", row['V']),
                ]

                for label, value in data_list:
                    # 数値の場合はカンマ区切り、それ以外はそのまま表示
                    display_value = f"{value:,.0f}" if isinstance(value, (int, float)) else value
                    st.write(f"**{label}**")
                    st.info(display_value)
                
                st.divider() # 複数ヒットした場合の区切り線
        else:
            st.warning("該当する品番が見つかりませんでした。")

except Exception as e:
    st.error(f"エラーが発生しました: {e}")
    st.info("GitHubに 'items.xlsx' という名前でファイルをアップロードしているか確認してください。")
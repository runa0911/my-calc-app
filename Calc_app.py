import streamlit as st
import pandas as pd

# ページの設定
st.set_page_config(page_title="26SS 原価・税込計算", layout="centered")

st.title("💰 商品金額計算検索")

# 加算する金額の定義
ADD_VALUES = {
    'SVP': 19500,
    'SP': 15000,
    'J': 10500,
    'P': 9000,
    'V': 6000
}

@st.cache_data
def load_data():
    # 3行目をヘッダーとして読み込み
    df = pd.read_excel('items.xlsx', header=2)
    df['品番'] = df['品番'].astype(str).str.strip()
    return df

try:
    df = load_data()

    # 品番検索
    search_query = st.text_input("品番を入力してください").strip()

    if search_query:
        # 部分一致で検索
        result = df[df['品番'].str.contains(search_query, case=False, na=False)]

        if not result.empty:
            for _, row in result.iterrows():
                st.success(f"品番: {row['品番']} (ブランド: {row['ブランド']})")
                
                # ヘッダー表示
                col_h1, col_h2, col_h3 = st.columns([1, 2, 2])
                col_h1.write("**項目**")
                col_h2.write("**計算後(税抜)**")
                col_h3.write("**税込(10%)**")
                st.divider()

                # 各項目の計算と表示
                for label, add_price in ADD_VALUES.items():
                    base_val = row[label]
                    
                    if pd.notnull(base_val) and isinstance(base_val, (int, float)):
                        # ① 指定金額を足す
                        calc_tax_ex = base_val + add_price
                        # ② 税込(10%)を計算
                        calc_tax_in = calc_tax_ex * 1.1
                        
                        # 画面表示
                        c1, c2, c3 = st.columns([1, 2, 2])
                        c1.write(f"**{label}**")
                        c2.write(f"{calc_tax_ex:,.0f} 円")
                        c3.write(f"**{calc_tax_in:,.0f} 円**")
                
                st.divider()
        else:
            st.warning("該当する品番が見つかりませんでした。")

except Exception as e:
    st.error(f"エラーが発生しました: {e}")
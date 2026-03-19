import streamlit as st
import pandas as pd

# ページの設定
st.set_page_config(page_title="26SS 金額計算", layout="centered")

# スマホで横並びを維持するためのカスタムCSS
st.markdown("""
    <style>
    .reportview-container .main .block-container { max-width: 1000px; }
    .price-table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
    .price-table th, .price-table td { 
        border-bottom: 1px solid #ddd; 
        padding: 12px 8px; 
        text-align: left; 
        font-size: 14px;
    }
    .price-table th { background-color: #f8f9fa; }
    .tax-in { color: #d32f2f; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("💰 商品金額検索")

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
    search_query = st.text_input("品番を入力してください（部分一致OK）").strip()

    if search_query:
        result = df[df['品番'].str.contains(search_query, case=False, na=False)]

        if not result.empty:
            for _, row in result.iterrows():
                st.subheader(f"品番: {row['品番']}")
                st.caption(f"ブランド: {row['ブランド']}")
                
                # HTMLテーブルで強制的に横並びにする
                html_table = f"""
                <table class="price-table">
                    <tr>
                        <th>項目</th>
                        <th>税抜(加算後)</th>
                        <th>税込(10%)</th>
                    </tr>
                """
                
                for label, add_price in ADD_VALUES.items():
                    base_val = row[label]
                    if pd.notnull(base_val) and isinstance(base_val, (int, float)):
                        calc_tax_ex = base_val + add_price
                        calc_tax_in = calc_tax_ex * 1.1
                        
                        html_table += f"""
                        <tr>
                            <td><b>{label}</b></td>
                            <td>{calc_tax_ex:,.0f}円</td>
                            <td class="tax-in">{calc_tax_in:,.0f}円</td>
                        </tr>
                        """
                
                html_table += "</table>"
                st.markdown(html_table, unsafe_allow_html=True)
                st.divider()
        else:
            st.warning("該当する品番が見つかりませんでした。")

except Exception as e:
    st.error(f"エラーが発生しました。ファイル名や形式を確認してください。")
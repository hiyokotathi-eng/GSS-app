import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt

# タイトル設定
st.set_page_config(page_title="GSS Calculator", page_icon="🏆")
st.title("🏆 GSS計算システム (Ver.3.1)")
st.write("学連（Gakuren）公式スコアリングシステム")

# 入力欄
rank = st.number_input("自分の順位を入力してください", min_value=1, value=1, step=1)
total_people = st.number_input("学年人数を入力してください", min_value=2, value=360, step=1)

def calculate_gss(r, A):
    # 正規化 (1位でx=0)
    x = (r - 1) / (A - 1) if A > 1 else 0
    
    # 円のパーツ（下位層をなだらかに）
    c_part = 1 - math.sqrt(max(0, 1 - (x - 0.8)**2))
    
    # ガウス分布（山の頂点を0.2にずらして、1位が最高点になるよう調整）
    gaussian_part = (1.5 / math.sqrt(2 * math.pi)) * math.exp(-3 * (x - 0.2)**2)
    
    # 係数を調整（1位でちょうど10000点になるように計算）
    base = 1000 * (c_part + gaussian_part) + 500 * x + 70.3
    
    return math.floor(10 * base)

# 計算実行
my_score = calculate_gss(rank, total_people)

# スコア表示
st.markdown(f"""
<div style="background-color: #fff; padding: 30px; border-radius: 15px; border: 4px solid #ff4b4b; text-align: center;">
    <h2 style="margin:0; font-size:20px; color:#333;">今回のキミの GSS は...</h2>
    <p style="font-size: 70px; font-weight: bold; color: #ff4b4b; margin: 10px 0;">{my_score:,} <span style="font-size: 24px;">点</span></p>
    <p style="color: #666; font-size:18px;">学年 {total_people} 人中 {rank} 位</p>
</div>
""", unsafe_allow_html=True)

# グラフ描画
rs = np.arange(1, total_people + 1)
ss = [calculate_gss(r, total_people) for r in rs]
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(rs, ss, color='#0056b3', linewidth=2)
ax.scatter(rank, my_score, color='red', s=100, zorder=5)
ax.set_title(f"GSS Map (A={total_people})")
ax.set_xlabel("Rank (r)")
ax.set_ylabel("GSS Score")
ax.grid(True, linestyle=':', alpha=0.6)
ax.set_ylim(min(ss)-500, 10500)
st.pyplot(fig)

st.caption("Developed by 学連 理数科チーム")

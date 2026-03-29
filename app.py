import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt

# タイトル
st.set_page_config(page_title="GSS Calculator", page_icon="🏆")
st.title("🏆 GSS計算システム (Ver.3.1 最終確定版)")
st.write("学連公式：ノートの定義・形状を完全再現")

# 入力欄
rank = st.number_input("自分の順位を入力してください", min_value=1, value=1, step=1)
total_people = st.number_input("学年人数を入力してください", min_value=2, value=360, step=1)

def calculate_gss(r, A):
    # 1. 順位の正規化 (ノート通り)
    x = (r - 1) / (A - 1) if A > 1 else 0
    
    # 2. 各パーツの計算 (ノートの数式を一字一句正確に再現)
    # 円の項
    circle_part = 1 - math.sqrt(max(0, 1 - (x - 0.8)**2))
    
    # ガウス分布の項
    gauss_const = 2 / math.sqrt(2 * math.pi)
    gaussian_part = gauss_const * math.exp(-2 * (x - 0.3)**2)
    
    # 3. カッコの中身の計算
    # 1位が10000点になるための精密な定数 -66.44919 を使用
    inner_val = 1000 * (circle_part + gaussian_part) + 300 * x - 66.44919
    
    # 4. 全体を10倍してガウス記号（切り捨て）を適用
    return math.floor(10 * inner_val)

# 計算実行
my_score = calculate_gss(rank, total_people)

# スコア表示
st.markdown(f"""
<div style="background-color: #fff; padding: 30px; border-radius: 15px; border: 4px solid #ff4b4b; text-align: center;">
    <h2 style="margin:0; font-size:20px; color:#333;">今回のキミの GSS は...</h2>
    <p style="font-size: 80px; font-weight: bold; color: #ff4b4b; margin: 10px 0;">{my_score:,} <span style="font-size: 30px;">点</span></p>
    <p style="color: #666; font-size:18px;">学年 {total_people} 人中 {rank} 位</p>
</div>
""", unsafe_allow_html=True)

# グラフ描画
rs = np.arange(1, total_people + 1)
ss = [calculate_gss(r, total_people) for r in rs]
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(rs, ss, color='#0056b3', linewidth=3)
ax.scatter(rank, my_score, color='red', s=150, zorder=5, edgecolors='white')
ax.set_title("GSS Master Curve (Perfect Shape)")
ax.set_xlabel("Rank (r)")
ax.set_ylabel("GSS Score")
ax.grid(True, linestyle=':', alpha=0.6)
st.pyplot(fig)

st.caption("Developed by 学連 理数科チーム")

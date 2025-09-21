import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
st.write("✅ App loaded successfully")

# ==============================
# 定义模型函数
# ==============================
def bid_rent_model(P_com, C_com, P_res, C_res, P_ind, C_ind, P_agr, C_agr):
    d = np.linspace(0, 20, 200)

    # 参数字典
    params = {
        "Commercial": (P_com, C_com),
        "Residential": (P_res, C_res),
        "Industrial": (P_ind, C_ind),
        "Agricultural": (P_agr, C_agr)
    }

    # 计算地租曲线
    rents = {land_use: P - C * d for land_use, (P, C) in params.items()}

    # 每个距离下的主导用途
    land_use_at_d = np.array([max(params.keys(), key=lambda u: rents[u][i]) for i in range(len(d))])

    # 计算分界点
    critical_points = []
    keys = list(params.keys())
    for i in range(len(keys)):
        for j in range(i+1, len(keys)):
            P1, C1 = params[keys[i]]
            P2, C2 = params[keys[j]]
            if C1 != C2:
                d_star = (P1 - P2) / (C1 - C2)
                if 0 < d_star < 20:
                    critical_points.append((d_star, keys[i], keys[j]))
    critical_points = sorted(critical_points, key=lambda x: x[0])

    # ==============================
    # 绘制地租曲线
    # ==============================
    fig1, ax1 = plt.subplots(figsize=(10,6))
    for land_use, rent in rents.items():
        ax1.plot(d, rent, label=land_use)

    max_rent = np.maximum.reduce(list(rents.values()))
    ax1.plot(d, max_rent, 'k--', label="Dominant Land Use")

    for d_star, u1, u2 in critical_points:
        r_val = params[u1][0] - params[u1][1]*d_star
        ax1.scatter(d_star, r_val, color="black", zorder=5)
        ax1.text(d_star, r_val+2, f"{u1}/{u2}\n({d_star:.1f} km)",
                 ha="center", fontsize=8, bbox=dict(facecolor='white', alpha=0.6, edgecolor='none'))

    ax1.set_title("Bid-Rent Model")
    ax1.set_xlabel("Distance from city center d (km)")
    ax1.set_ylabel("Willingness to Pay Rent R")
    ax1.legend()
    ax1.grid(True)

    # ==============================
    # 绘制土地利用格局
    # ==============================
    fig2, ax2 = plt.subplots(figsize=(10,2))
    color_list = plt.cm.tab10.colors
    colors = {u: color_list[i % len(color_list)] for i, u in enumerate(params.keys())}
    for i in range(len(d)-1):
        ax2.fill_between([d[i], d[i+1]], 0, 1, color=colors[land_use_at_d[i]])

    ax2.set_title("Land Use Spatial Pattern")
    ax2.set_xlabel("Distance from city center d (km)")
    ax2.set_yticks([])

    for d_star, _, _ in critical_points:
        ax2.axvline(d_star, color="black", linestyle="--")
        ax2.text(d_star, 1.05, f"{d_star:.1f} km", ha="center", fontsize=8)

    return fig1, fig2, land_use_at_d, d


# ==============================
# Streamlit 界面
# ==============================
st.title("Bid-Rent Model (Web App)")

st.sidebar.header("Model Parameters")

P_com = st.sidebar.slider("Commercial P", 50, 150, 100, 5)
C_com = st.sidebar.slider("Commercial C", 0.5, 10.0, 5.0, 0.5)
P_res = st.sidebar.slider("Residential P", 30, 120, 70, 5)
C_res = st.sidebar.slider("Residential C", 0.5, 5.0, 2.0, 0.5)
P_ind = st.sidebar.slider("Industrial P", 20, 100, 50, 5)
C_ind = st.sidebar.slider("Industrial C", 0.1, 3.0, 1.0, 0.1)
P_agr = st.sidebar.slider("Agricultural P", 10, 60, 30, 5)
C_agr = st.sidebar.slider("Agricultural C", 0.1, 2.0, 0.5, 0.1)

fig1, fig2, land_use_at_d, d = bid_rent_model(P_com, C_com, P_res, C_res, P_ind, C_ind, P_agr, C_agr)

st.pyplot(fig1)
st.pyplot(fig2)

# ==============================
# 输出主导区间
# ==============================
st.subheader("Dominant Intervals")
current_use = land_use_at_d[0]
start_d = 0
for i in range(1, len(d)):
    if land_use_at_d[i] != current_use:
        end_d = d[i]
        st.write(f"**{current_use}**: {start_d:.1f} km – {end_d:.1f} km")
        current_use = land_use_at_d[i]
        start_d = d[i]
st.write(f"**{current_use}**: {start_d:.1f} km – {d[-1]:.1f} km")

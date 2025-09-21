import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

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
st.title("Bid-Rent Model")
st.sidebar.header("Model Parameters")

# ==============================
# 场景选择
# ==============================
scenario = st.sidebar.selectbox(
    "Choose a scenario",
    [
        "Custom",
        "Scenario 1: Classic Concentric",
        "Scenario 2: CBD Dominance",
        "Scenario 3: Industrial-Oriented",
        "Scenario 4: Low Transport Costs",
        "Scenario 5: High Residential Demand"
    ]
)

# 默认参数（Custom 模式的起始值）
default_params = {
    "Commercial": (100, 5),
    "Residential": (70, 2),
    "Industrial": (50, 1),
    "Agricultural": (30, 0.5),
    "desc": "Custom scenario — adjust parameters manually."
}

# 不同场景的预设
scenarios = {
    "Scenario 1: Classic Concentric": {
        "Commercial": (100, 5),
        "Residential": (70, 2),
        "Industrial": (50, 1),
        "Agricultural": (30, 0.5),
        "desc": "Commercial dominates the core, then Residential, Industrial, and Agricultural."
    },
    "Scenario 2: CBD Dominance": {
        "Commercial": (150, 6),
        "Residential": (80, 2),
        "Industrial": (60, 1),
        "Agricultural": (30, 0.5),
        "desc": "CBD expands strongly, squeezing housing and pushing industry/agriculture outward."
    },
    "Scenario 3: Industrial-Oriented": {
        "Commercial": (80, 4),
        "Residential": (60, 2),
        "Industrial": (90, 1),
        "Agricultural": (30, 0.5),
        "desc": "Industry extends outward from center, compressing residential; an industrial-centered pattern."
    },
    "Scenario 4: Low Transport Costs": {
        "Commercial": (100, 2),
        "Residential": (80, 1.5),
        "Industrial": (70, 1),
        "Agricultural": (40, 0.3),
        "desc": "Flatter rent gradients, blurred land-use boundaries — reflects impact of modern transport."
    },
    "Scenario 5: High Residential Demand": {
        "Commercial": (90, 5),
        "Residential": (120, 2.5),
        "Industrial": (70, 1),
        "Agricultural": (30, 0.5),
        "desc": "Residential dominates widely; commercial limited to core, industry/agriculture squeezed outward."
    }
}

# 选择参数集
params = scenarios.get(scenario, default_params)
desc = params["desc"]

# 用滑块显示，初始值取场景数值
P_com = st.sidebar.slider("Commercial P", 50, 150, params["Commercial"][0], 5)
C_com = st.sidebar.slider("Commercial C", 0.5, 10.0, float(params["Commercial"][1]), 0.5)

P_res = st.sidebar.slider("Residential P", 30, 120, params["Residential"][0], 5)
C_res = st.sidebar.slider("Residential C", 0.5, 5.0, float(params["Residential"][1]), 0.5)

P_ind = st.sidebar.slider("Industrial P", 20, 100, params["Industrial"][0], 5)
C_ind = st.sidebar.slider("Industrial C", 0.1, 3.0, float(params["Industrial"][1]), 0.1)

P_agr = st.sidebar.slider("Agricultural P", 10, 60, params["Agricultural"][0], 5)
C_agr = st.sidebar.slider("Agricultural C", 0.1, 2.0, float(params["Agricultural"][1]), 0.1)

# ==============================
# 在主界面显示场景标题和描述
# ==============================
if scenario != "Custom":
    st.subheader(scenario)
st.write(desc)

# ==============================
# 调用模型并展示结果
# ==============================
fig1, fig2, land_use_at_d, d = bid_rent_model(
    P_com, C_com,
    P_res, C_res,
    P_ind, C_ind,
    P_agr, C_agr
)

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

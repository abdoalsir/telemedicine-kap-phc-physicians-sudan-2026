"""
Project  : Knowledge, Attitudes, and Practices Toward Telemedicine Among
           Primary Healthcare Physicians in Sudan – 2026
Script   : Figure Generation (all figures)
Author   : Abdulrahman Sirelkhatim
Date     : May 2026
Input    : 1_data/cleaned/cleaned_data.xlsx
Output   : 5_figures/ directory (PNG, 300 DPI)

Figures produced:
    fig01_age_distribution.png
    fig02_gender_work_setting.png
    fig03_qualification_distribution.png
    fig04_knowledge_category_distribution.png
    fig05_knowledge_item_accuracy.png
    fig06_attitude_item_means.png
    fig07_attitude_category_distribution.png
    fig08_practice_indicators.png
    fig09_practice_category_distribution.png
    fig10_platforms_used.png
    fig11_barriers_to_telemedicine.png
    fig12_knowledge_attitude_stacked.png
"""

import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

warnings.filterwarnings("ignore")

DATA_PATH = "1_data/cleaned/cleaned_data.xlsx"
FIGURES_DIR = "5_figures/"

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 11
plt.rcParams["figure.dpi"] = 200

BLUE = sns.color_palette("Blues_r", 6)
PALETTE = sns.color_palette("Set2")
CONTRAST = [BLUE[1], BLUE[3], BLUE[5]]

K_COLS = [
    "K1_InformedConsent",
    "K2_WrittenConsent",
    "K3_ReduceTravel",
    "K4_VideoMandatory",
    "K5_ControlledMeds",
    "K6_DataPrivacy",
    "K7_Emergencies",
    "K8_Documentation",
]

K_CORRECT = {
    "K1_InformedConsent": 1,
    "K2_WrittenConsent": 1,
    "K3_ReduceTravel": 1,
    "K4_VideoMandatory": 0,
    "K5_ControlledMeds": 1,
    "K6_DataPrivacy": 1,
    "K7_Emergencies": 0,
    "K8_Documentation": 1,
}

K_LABELS = [
    "K1: Informed consent required",
    "K2: Written consent mandatory",
    "K3: Reduces patient travel",
    "K4: Video mandatory for TM (False)",
    "K5: Controlled meds restricted",
    "K6: Data privacy laws apply",
    "K7: Suitable for emergencies (False)",
    "K8: Documentation required",
]

A_COLS = [
    "A1_Privacy_Risk",
    "A2_Rural_Access",
    "A3_DocPt_Relation",
    "A4_Confidence",
    "A5_MedError_Risk",
    "A6_CME_Tool",
    "A7_CulturalFit",
    "A8_Integration",
    "A9_Recommend",
    "A10_LoadReduce",
]

A_LABELS = [
    "A1: Threatens privacy*",
    "A2: Improves rural access",
    "A3: Weakens doctor–patient relation*",
    "A4: Confident using TM",
    "A5: Risk of medical errors*",
    "A6: Useful CME tool",
    "A7: Culturally inappropriate*",
    "A8: Should be integrated in PHC",
    "A9: Would recommend to colleagues",
    "A10: Reduces patient load",
]

NEGATIVE_A = {
    "A1_Privacy_Risk",
    "A3_DocPt_Relation",
    "A5_MedError_Risk",
    "A7_CulturalFit",
}


def save_fig(fig, filename):
    fig.savefig(FIGURES_DIR + filename, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {filename}")


def remove_spines(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


df = pd.read_excel(DATA_PATH)
n = len(df)

age_order = ["20–29", "30–39", "40–49", "50+"]
age_labels = {1: "20–29", 2: "30–39", 3: "40–49", 4: "50+"}
age_counts = df["B1_Age"].map(age_labels).value_counts().reindex(age_order)

fig, ax = plt.subplots(figsize=(6, 4))
pcts = age_counts / n * 100
bars = ax.bar(age_order, pcts, color=BLUE[:4])
for bar, v in zip(bars, pcts):
    ax.text(
        bar.get_x() + bar.get_width() / 2, v + 0.5, f"{v:.1f}%", ha="center", fontsize=9
    )
ax.set_ylabel("Percentage (%)")
ax.set_xlabel("Age Group")
ax.set_title(f"Age Group Distribution (N={n})")
ax.set_ylim(0, 60)
remove_spines(ax)
plt.tight_layout()
save_fig(fig, "fig01_age_distribution.png")


fig, axes = plt.subplots(1, 2, figsize=(10, 4))
gender_counts = df["B2_Gender"].map({1: "Male", 2: "Female"}).value_counts()
axes[0].pie(
    gender_counts,
    labels=gender_counts.index,
    autopct="%1.1f%%",
    colors=[BLUE[1], PALETTE[1]],
    wedgeprops={"width": 0.4, "edgecolor": "white"},
    pctdistance=0.75,
)
axes[0].set_title("Gender Distribution")

ws_labels = {1: "Urban", 2: "Peri-urban", 3: "Rural"}
ws_counts = df["B4_WorkSetting"].map(ws_labels).value_counts()
axes[1].pie(
    ws_counts,
    labels=ws_counts.index,
    autopct="%1.1f%%",
    colors=CONTRAST,
    wedgeprops={"width": 0.4, "edgecolor": "white"},
    pctdistance=0.75,
)
axes[1].set_title("Work Setting")
plt.suptitle(f"Gender and Work Setting (N={n})", y=1.02)
plt.tight_layout()
save_fig(fig, "fig02_gender_work_setting.png")


qual_labels = {
    1: "MBBS",
    2: "General\nPractitioner",
    3: "FM Specialist",
    4: "MD/MS",
    5: "Other",
}
qual_counts = df["B6_Qualification"].map(qual_labels).value_counts()
qual_order = ["MBBS", "General\nPractitioner", "FM Specialist", "MD/MS", "Other"]
qual_counts = qual_counts.reindex(qual_order).dropna()

fig, ax = plt.subplots(figsize=(7, 4))
pcts = qual_counts / n * 100
bars = ax.bar(qual_counts.index, pcts, color=BLUE[: len(qual_counts)])
for bar, v in zip(bars, pcts):
    ax.text(
        bar.get_x() + bar.get_width() / 2, v + 0.5, f"{v:.1f}%", ha="center", fontsize=9
    )
ax.set_ylabel("Percentage (%)")
ax.set_xlabel("Highest Qualification")
ax.set_title(f"Qualification Distribution (N={n})")
ax.set_ylim(0, 55)
remove_spines(ax)
plt.tight_layout()
save_fig(fig, "fig03_qualification_distribution.png")


k_cat_labels = {1: "Poor (0–4)", 2: "Moderate (5–6)", 3: "Good (7–8)"}
k_cat_order = ["Poor (0–4)", "Moderate (5–6)", "Good (7–8)"]
k_cat_counts = df["KnowledgeCat"].map(k_cat_labels).value_counts().reindex(k_cat_order)

fig, ax = plt.subplots(figsize=(5, 5))
ax.pie(
    k_cat_counts,
    labels=k_cat_counts.index,
    autopct="%1.1f%%",
    colors=CONTRAST,
    wedgeprops={"width": 0.4, "edgecolor": "white"},
    pctdistance=0.75,
)
mean_k = df["KnowledgeScore"].mean()
sd_k = df["KnowledgeScore"].std()
ax.set_title(
    f"Knowledge Category Distribution (N={n})\nMean score = {mean_k:.2f} ± {sd_k:.2f}",
    pad=12,
)
save_fig(fig, "fig04_knowledge_category_distribution.png")


k_pcts = []
for col, label in zip(K_COLS, K_LABELS):
    correct_val = K_CORRECT[col]
    pct = (df[col] == correct_val).mean() * 100
    k_pcts.append((label, pct))
k_pcts_sorted = sorted(k_pcts, key=lambda x: x[1])
labels_s, vals_s = zip(*k_pcts_sorted)
colors = [BLUE[4] if v < 80 else BLUE[1] for v in vals_s]

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(range(len(labels_s)), vals_s, color=colors)
for bar, v in zip(bars, vals_s):
    ax.text(
        v + 0.3,
        bar.get_y() + bar.get_height() / 2,
        f"{v:.1f}%",
        va="center",
        fontsize=9,
    )
ax.set_yticks(range(len(labels_s)))
ax.set_yticklabels(labels_s, fontsize=9)
ax.set_xlabel("Percentage Correct (%)")
ax.set_title(f"Knowledge Item Accuracy (N={n})\nDarker bars = items below 80% correct")
ax.set_xlim(0, 115)
ax.axvline(80, color="gray", linestyle="--", linewidth=0.8, alpha=0.7)
remove_spines(ax)
plt.tight_layout()
save_fig(fig, "fig05_knowledge_item_accuracy.png")


a_means = [(label, df[col].mean()) for col, label in zip(A_COLS, A_LABELS)]
a_sorted = sorted(a_means, key=lambda x: x[1])
a_labels_s, a_vals_s = zip(*a_sorted)
colors_a = [
    BLUE[4] if col in NEGATIVE_A else BLUE[1]
    for col, _ in sorted(zip(A_COLS, A_LABELS), key=lambda x: df[x[0]].mean())
]

fig, ax = plt.subplots(figsize=(9, 5.5))
bars = ax.barh(range(len(a_labels_s)), a_vals_s, color=colors_a)
for bar, v in zip(bars, a_vals_s):
    ax.text(
        v + 0.04,
        bar.get_y() + bar.get_height() / 2,
        f"{v:.2f}",
        va="center",
        fontsize=9,
    )
ax.set_yticks(range(len(a_labels_s)))
ax.set_yticklabels(a_labels_s, fontsize=9)
ax.axvline(3.0, color="gray", linestyle="--", linewidth=0.8, alpha=0.7)
ax.set_xlabel("Mean Score (1–5 Likert scale)")
ax.set_title(
    f"Mean Scores for Attitude Items (N={n})\n* Negative-worded items (darker bars)\nCronbach's α = 0.729"
)
ax.set_xlim(0, 5.8)
remove_spines(ax)
plt.tight_layout()
save_fig(fig, "fig06_attitude_item_means.png")


a_cat_labels = {1: "Negative (<30)", 2: "Neutral (30–39)", 3: "Positive (40–50)"}
a_cat_order = ["Negative (<30)", "Neutral (30–39)", "Positive (40–50)"]
a_cat_counts = df["AttitudeCat"].map(a_cat_labels).value_counts().reindex(a_cat_order)

fig, ax = plt.subplots(figsize=(5, 5))
ax.pie(
    a_cat_counts,
    labels=a_cat_counts.index,
    autopct="%1.1f%%",
    colors=CONTRAST,
    wedgeprops={"width": 0.4, "edgecolor": "white"},
    pctdistance=0.75,
)
mean_a = df["AttitudeScore"].mean()
sd_a = df["AttitudeScore"].std()
ax.set_title(
    f"Attitude Category Distribution (N={n})\nMean score = {mean_a:.2f} ± {sd_a:.2f}",
    pad=12,
)
save_fig(fig, "fig07_attitude_category_distribution.png")


indicators = ["Used TM (past 6 mo)", "Want further training", "Documents always"]
vals_p = [
    (df["P1_Used6Mo"] == 1).mean() * 100,
    (df["P7_WantTraining"] == 1).mean() * 100,
    (df["P4_Documentation_Ord"] == 4).mean() * 100,
]

fig, ax = plt.subplots(figsize=(6, 4))
bars = ax.barh(indicators, vals_p, color=BLUE[1], height=0.5)
for bar, v in zip(bars, vals_p):
    ax.text(
        v + 0.5,
        bar.get_y() + bar.get_height() / 2,
        f"{v:.1f}%",
        va="center",
        fontsize=10,
    )
ax.set_xlabel("Percentage (%)")
ax.set_title(f"Key Practice Indicators (N={n})")
ax.set_xlim(0, 110)
remove_spines(ax)
plt.tight_layout()
save_fig(fig, "fig08_practice_indicators.png")


p_cat_labels = {1: "Low (0)", 2: "Moderate (1)", 3: "High (2–3)"}
p_cat_order = ["Low (0)", "Moderate (1)", "High (2–3)"]
p_cat_counts = df["PracticeCat"].map(p_cat_labels).value_counts().reindex(p_cat_order)

fig, ax = plt.subplots(figsize=(6, 4))
pcts = p_cat_counts / n * 100
bars = ax.bar(p_cat_order, pcts, color=CONTRAST)
for bar, v in zip(bars, pcts):
    ax.text(
        bar.get_x() + bar.get_width() / 2, v + 0.5, f"{v:.1f}%", ha="center", fontsize=9
    )
ax.set_ylabel("Percentage (%)")
ax.set_xlabel("Practice Category")
ax.set_title(f"Practice Category Distribution (N={n})")
ax.set_ylim(0, 90)
remove_spines(ax)
plt.tight_layout()
save_fig(fig, "fig09_practice_category_distribution.png")


platform_cols = ["P3_Phone", "P3_WhatsApp", "P3_Zoom", "P3_SudanHP"]
platform_labels = ["Phone call", "WhatsApp", "Zoom", "Sudan HP Platform"]
platform_pcts = [df[col].mean() * 100 for col in platform_cols]
order = sorted(zip(platform_pcts, platform_labels, platform_cols), reverse=True)
platform_pcts_s, platform_labels_s, _ = zip(*order)

fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.barh(platform_labels_s, platform_pcts_s, color=BLUE[1], height=0.5)
for bar, v in zip(bars, platform_pcts_s):
    ax.text(
        v + 0.5,
        bar.get_y() + bar.get_height() / 2,
        f"{v:.1f}%",
        va="center",
        fontsize=9,
    )
ax.set_xlabel("Percentage of Participants (%)")
ax.set_title(f"Telemedicine Platforms Used (N={n})\n(Multiple responses allowed)")
ax.set_xlim(0, 110)
remove_spines(ax)
plt.tight_layout()
save_fig(fig, "fig10_platforms_used.png")


barrier_cols = [
    "P5_Internet",
    "P5_NoTraining",
    "P5_NoEquip",
    "P5_PtResist",
    "P5_Legal",
    "P5_NoBarrier",
]
barrier_labels = [
    "Poor internet",
    "Lack of training",
    "Lack of equipment",
    "Patient resistance",
    "Legal/regulatory",
    "No barriers",
]
barrier_pcts = [df[col].mean() * 100 for col in barrier_cols]
order_b = sorted(zip(barrier_pcts, barrier_labels), reverse=True)
barrier_pcts_s, barrier_labels_s = zip(*order_b)
colors_b = [
    BLUE[5] if v >= 80 else BLUE[3] if v >= 50 else BLUE[1] for v in barrier_pcts_s
]

fig, ax = plt.subplots(figsize=(7, 4.5))
bars = ax.barh(barrier_labels_s, barrier_pcts_s, color=colors_b, height=0.5)
for bar, v in zip(bars, barrier_pcts_s):
    ax.text(
        v + 0.5,
        bar.get_y() + bar.get_height() / 2,
        f"{v:.1f}%",
        va="center",
        fontsize=9,
    )
ax.set_xlabel("Percentage of Participants (%)")
ax.set_title(f"Reported Barriers to Telemedicine (N={n})\n(Multiple responses allowed)")
ax.set_xlim(0, 115)
remove_spines(ax)
plt.tight_layout()
save_fig(fig, "fig11_barriers_to_telemedicine.png")


k_cat_map = {1: "Poor\n(n=39)", 2: "Moderate\n(n=131)", 3: "Good\n(n=81)"}
a_cat_pct = (
    df.groupby("KnowledgeCat")["AttitudeCat"]
    .value_counts(normalize=True)
    .mul(100)
    .rename("pct")
    .reset_index()
)

fig, ax = plt.subplots(figsize=(7, 4.5))
x = np.arange(3)
w = 0.5
k_groups = [1, 2, 3]
neg_vals = [
    a_cat_pct[(a_cat_pct["KnowledgeCat"] == k) & (a_cat_pct["AttitudeCat"] == 1)][
        "pct"
    ].values
    for k in k_groups
]
neu_vals = [
    a_cat_pct[(a_cat_pct["KnowledgeCat"] == k) & (a_cat_pct["AttitudeCat"] == 2)][
        "pct"
    ].values
    for k in k_groups
]
pos_vals = [
    a_cat_pct[(a_cat_pct["KnowledgeCat"] == k) & (a_cat_pct["AttitudeCat"] == 3)][
        "pct"
    ].values
    for k in k_groups
]

neg_v = [v[0] if len(v) else 0 for v in neg_vals]
neu_v = [v[0] if len(v) else 0 for v in neu_vals]
pos_v = [v[0] if len(v) else 0 for v in pos_vals]

ax.bar(x, neg_v, w, label="Negative", color=CONTRAST[0])
ax.bar(x, neu_v, w, bottom=neg_v, label="Neutral", color=CONTRAST[1])
ax.bar(
    x,
    pos_v,
    w,
    bottom=[a + b for a, b in zip(neg_v, neu_v)],
    label="Positive",
    color=CONTRAST[2],
)
ax.set_xticks(x)
ax.set_xticklabels([k_cat_map[k] for k in k_groups])
ax.set_ylabel("Percentage (%)")
ax.set_ylim(0, 115)
ax.set_title(
    f"Attitude Category by Knowledge Category (N={n})\nχ²(4) = 32.42, p < 0.001"
)
ax.legend(
    title="Attitude",
    loc="upper center",
    bbox_to_anchor=(0.5, 1.06),
    ncol=3,
    frameon=False,
    fontsize=9,
)
remove_spines(ax)
plt.tight_layout()
save_fig(fig, "fig12_knowledge_attitude_stacked.png")

print(f"\nAll figures saved to: {FIGURES_DIR}")

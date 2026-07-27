"""
Project  : Knowledge, Attitudes, and Practices Toward Telemedicine Among
           Primary Healthcare Physicians in Sudan – 2026
Script   : Data Cleaning & Recoding
Author   : Abdulrahman Sirelkhatim
Date     : May 2026
Input    : 1_data/raw/raw_data.xlsx  (Google Form export)
Output   : 1_data/cleaned/cleaned_data.xlsx
"""

import numpy as np
import pandas as pd

RAW_PATH = "1_data/raw/raw_data.xlsx"
OUTPUT_PATH = "1_data/cleaned/cleaned_data.xlsx"

COL_MAP = {
    0: "Timestamp",
    1: "Consent",
    2: "PHC_Physician",
    3: "B1_Age",
    4: "B2_Gender",
    5: "B3_State",
    6: "B4_WorkSetting",
    7: "B5_YearsExp",
    8: "B6_Qualification",
    9: "B7_Training",
    10: "K1_InformedConsent",
    11: "K2_WrittenConsent",
    12: "K3_ReduceTravel",
    13: "K4_VideoMandatory",
    14: "K5_ControlledMeds",
    15: "K6_DataPrivacy",
    16: "K7_Emergencies",
    17: "K8_Documentation",
    18: "C9_Services_Raw",
    19: "A1_Privacy_Risk",
    20: "A2_Rural_Access",
    21: "A3_DocPt_Relation",
    22: "A4_Confidence",
    23: "A5_MedError_Risk",
    24: "A6_CME_Tool",
    25: "A7_CulturalFit",
    26: "A8_Integration",
    27: "A9_Recommend",
    28: "A10_LoadReduce",
    29: "P1_Used6Mo",
    30: "P2_ConsultMonth",
    31: "P3_Platforms_Raw",
    32: "P4_Documentation",
    33: "P5_Barriers_Raw",
    34: "P6_Support_Raw",
    35: "P7_WantTraining",
}

CORRECT_ANSWERS = {
    "K1_InformedConsent": "yes",
    "K2_WrittenConsent": "yes",
    "K3_ReduceTravel": "yes",
    "K4_VideoMandatory": "no",
    "K5_ControlledMeds": "yes",
    "K6_DataPrivacy": "yes",
    "K7_Emergencies": "no",
    "K8_Documentation": "yes",
}

K_COLS = list(CORRECT_ANSWERS.keys())

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

NEGATIVE_A_ITEMS = [
    "A1_Privacy_Risk",
    "A3_DocPt_Relation",
    "A5_MedError_Risk",
    "A7_CulturalFit",
]

C9_OPTIONS = {
    "C9_MedConsult": "Medical consultation",
    "C9_Prescription": "Prescription",
    "C9_MentalHealth": "Mental health",
    "C9_Emergency": "Emergency",
    "C9_ChronicFU": "Follow-up of chronic",
}

P3_OPTIONS = {
    "P3_WhatsApp": "WhatsApp",
    "P3_Zoom": "Zoom",
    "P3_SudanHP": "Official Sudan Health Platform",
    "P3_Phone": "Regular phone call",
}

P5_OPTIONS = {
    "P5_Internet": "Poor internet",
    "P5_NoTraining": "Lack of training",
    "P5_NoEquip": "Lack of equipment",
    "P5_PtResist": "Patient resistance",
    "P5_Legal": "Legal",
    "P5_NoBarrier": "No major barriers",
}

P6_OPTIONS = {
    "P6_TechTrain": "Technical training",
    "P6_Internet": "Improved internet",
    "P6_Guidelines": "Clear national guidelines",
    "P6_Equipment": "Provision of equipment",
    "P6_Financial": "Financial incentives",
}


def clean_qualification(val) -> str:
    if pd.isna(val):
        return np.nan
    v = str(val).strip().lower()
    if v in ("gp", " gp", "gp "):
        return "General Practitioner"
    if "family medicine" in v:
        return "Family Medicine Specialist"
    if "mbbs" in v and ("master" in v or "ms" in v):
        return "MD/MS"
    if v == "mbbs":
        return "MBBS"
    if "md" in v or "ms" in v:
        return "MD/MS"
    if "obs" in v or "specialist" in v:
        return "Other Specialist"
    return str(val).strip()


def recode_age(val) -> int:
    if pd.isna(val):
        return np.nan
    v = str(val).strip()
    if v == "20_29":
        return 1
    if v == "29_39":
        return 2
    if v == "39_49":
        return 3
    if v == ">50":
        return 4
    return np.nan


def recode_knowledge(val) -> int:
    if pd.isna(val):
        return np.nan
    v = str(val).strip().lower().replace("'", "")
    if v == "yes":
        return 1
    if v == "no":
        return 0
    if "don" in v:
        return 9
    return np.nan


def knowledge_score(row) -> int:
    score = 0
    for col, correct in CORRECT_ANSWERS.items():
        val = row[col]
        if pd.isna(val):
            continue
        coded_correct = 1 if correct == "yes" else 0
        if val == coded_correct:
            score += 1
    return score


def k_category(s) -> int:
    if pd.isna(s):
        return np.nan
    if s <= 4:
        return 1
    if s <= 6:
        return 2
    return 3


def a_category(s) -> int:
    if pd.isna(s):
        return np.nan
    if s <= 29:
        return 1
    if s <= 39:
        return 2
    return 3


def practice_score(row) -> int:
    score = 0
    if row.get("P1_Used6Mo") == 1:
        score += 1
    if pd.notna(row.get("P2_ConsultMonth_Ord")) and row["P2_ConsultMonth_Ord"] >= 2:
        score += 1
    if pd.notna(row.get("P4_Documentation_Ord")) and row["P4_Documentation_Ord"] >= 3:
        score += 1
    return score


def p_category(s) -> int:
    if s == 0:
        return 1
    if s <= 1:
        return 2
    return 3


def multi_binary(series, options: dict) -> pd.DataFrame:
    out = {}
    for col_name, keyword in options.items():
        out[col_name] = series.apply(
            lambda x: 1 if pd.notna(x) and keyword.lower() in str(x).lower() else 0
        )
    return pd.DataFrame(out)


raw = pd.read_excel(RAW_PATH)

rename_map = {raw.columns[i]: name for i, name in COL_MAP.items()}
raw.rename(columns=rename_map, inplace=True)

df = (
    raw[raw["PHC_Physician"].str.strip().str.lower() == "yes"]
    .copy()
    .reset_index(drop=True)
)

df["B1_Age"] = df["B1_Age"].apply(recode_age).astype("Int64")
df["B2_Gender"] = df["B2_Gender"].str.strip().map({"Male": 1, "Female": 2})
df["B4_WorkSetting"] = (
    df["B4_WorkSetting"].str.strip().map({"Urban": 1, "Peri-urban": 2, "Rural": 3})
)
df["B5_YearsExp"] = (
    df["B5_YearsExp"]
    .str.strip()
    .map({"<1 year": 1, "1–5 years": 2, "6–10 years": 3, ">10 years": 4})
)
df["B6_Qualification"] = (
    df["B6_Qualification"]
    .apply(clean_qualification)
    .map(
        {
            "MBBS": 1,
            "General Practitioner": 2,
            "Family Medicine Specialist": 3,
            "MD/MS": 4,
            "Other Specialist": 5,
        }
    )
)
df["B7_Training"] = df["B7_Training"].str.strip().map({"Yes": 1, "No": 0})

for col in K_COLS:
    df[col] = df[col].apply(recode_knowledge).astype("Int64")

df["KnowledgeScore"] = df.apply(knowledge_score, axis=1)
df["KnowledgeCat"] = df["KnowledgeScore"].apply(k_category)

for col in A_COLS:
    df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

for col in NEGATIVE_A_ITEMS:
    df[col + "_R"] = (6 - df[col]).astype("Int64")

pos_items = [c for c in A_COLS if c not in NEGATIVE_A_ITEMS]
rev_items = [c + "_R" for c in NEGATIVE_A_ITEMS]
df["AttitudeScore"] = df[pos_items + rev_items].sum(axis=1)
df["AttitudeCat"] = df["AttitudeScore"].apply(a_category)

df["P1_Used6Mo"] = df["P1_Used6Mo"].str.strip().map({"Yes": 1, "No": 0})
df["P2_ConsultMonth_Ord"] = (
    df["P2_ConsultMonth"]
    .str.strip()
    .map({"0-2": 1, "3-5": 2, "6-10": 3, "More than 10": 4})
    .astype("Int64")
)
df["P4_Documentation_Ord"] = (
    df["P4_Documentation"]
    .str.strip()
    .map({"Never": 1, "Rarely": 2, "Sometimes": 3, "Always": 4})
    .astype("Int64")
)
df["P7_WantTraining"] = df["P7_WantTraining"].str.strip().map({"Yes": 1, "No": 0})

df["PracticeScore"] = df.apply(practice_score, axis=1)
df["PracticeCat"] = df["PracticeScore"].apply(p_category)

c9_df = multi_binary(df["C9_Services_Raw"], C9_OPTIONS)
p3_df = multi_binary(df["P3_Platforms_Raw"], P3_OPTIONS)
p5_df = multi_binary(df["P5_Barriers_Raw"], P5_OPTIONS)
p6_df = multi_binary(df["P6_Support_Raw"], P6_OPTIONS)

keep = (
    [
        "B1_Age",
        "B2_Gender",
        "B3_State",
        "B4_WorkSetting",
        "B5_YearsExp",
        "B6_Qualification",
        "B7_Training",
    ]
    + K_COLS
    + ["KnowledgeScore", "KnowledgeCat"]
    + A_COLS
    + [c + "_R" for c in NEGATIVE_A_ITEMS]
    + ["AttitudeScore", "AttitudeCat"]
    + [
        "P1_Used6Mo",
        "P2_ConsultMonth_Ord",
        "P4_Documentation_Ord",
        "P7_WantTraining",
        "PracticeScore",
        "PracticeCat",
    ]
)

final = pd.concat(
    [df[keep].reset_index(drop=True), c9_df, p3_df, p5_df, p6_df],
    axis=1,
)

final.to_excel(OUTPUT_PATH, index=False)
print(f"Saved: {OUTPUT_PATH}")
print(f"Shape: {final.shape[0]} rows × {final.shape[1]} columns")
print(f"Knowledge Good (%):    {(final['KnowledgeCat'] == 3).mean() * 100:.1f}%")
print(f"Attitude Positive (%): {(final['AttitudeCat'] == 3).mean() * 100:.1f}%")
print(f"Practice High (%):     {(final['PracticeCat'] == 3).mean() * 100:.1f}%")

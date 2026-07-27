* Encoding: UTF-8.
* Knowledge, Attitudes, and Practices Toward Telemedicine Among
* Primary Healthcare Physicians in Sudan, 2026.
* Data analyst: Abdulrahman Sirelkhatim.
* Input: cleaned_data.xlsx (output of cleaning.py).

* NOTE: Update the FILE path below before running.
GET DATA
  /TYPE=XLSX
  /FILE="1_data/cleaned/cleaned_data.xlsx"
  /SHEET=name "Sheet1"
  /CELLRANGE=full
  /READNAMES=on.
EXECUTE.

* Variable and value labels.
VARIABLE LABELS
  B1_Age          "Age group"
  B2_Gender       "Gender"
  B3_State        "State of practice"
  B4_WorkSetting  "Work setting"
  B5_YearsExp     "Years of experience in PHC"
  B6_Qualification "Highest qualification"
  B7_Training     "Received formal telemedicine training"
  K1_InformedConsent "K1: Telemedicine requires informed consent"
  K2_WrittenConsent  "K2: Written consent is mandatory (Sudan)"
  K3_ReduceTravel    "K3: Telemedicine reduces travel costs"
  K4_VideoMandatory  "K4: Video mandatory for all TM (False)"
  K5_ControlledMeds  "K5: Controlled medications restricted"
  K6_DataPrivacy     "K6: Data privacy laws apply"
  K7_Emergencies     "K7: Suitable for all emergencies (False)"
  K8_Documentation   "K8: Documentation required"
  KnowledgeScore  "Knowledge score (0–8)"
  KnowledgeCat    "Knowledge category (1=Poor, 2=Moderate, 3=Good)"
  A1_Privacy_Risk "A1: Threatens privacy (negative)"
  A2_Rural_Access "A2: Improves rural access"
  A3_DocPt_Relation "A3: Weakens doctor–patient relation (negative)"
  A4_Confidence   "A4: Confident using telemedicine"
  A5_MedError_Risk "A5: Risk of medical errors (negative)"
  A6_CME_Tool     "A6: Useful CME tool"
  A7_CulturalFit  "A7: Culturally inappropriate (negative)"
  A8_Integration  "A8: Should be integrated into PHC"
  A9_Recommend    "A9: Would recommend to colleagues"
  A10_LoadReduce  "A10: Reduces patient load"
  AttitudeScore   "Attitude score (10–50, reversed items included)"
  AttitudeCat     "Attitude category (1=Negative, 2=Neutral, 3=Positive)"
  P1_Used6Mo      "Used telemedicine in past 6 months"
  P2_ConsultMonth_Ord "Consultation volume per month (ordinal)"
  P4_Documentation_Ord "Documentation frequency (ordinal)"
  P7_WantTraining "Interested in formal TM training"
  PracticeScore   "Practice score (0–3)"
  PracticeCat     "Practice category (1=Low, 2=Moderate, 3=High)".
EXECUTE.

VALUE LABELS B1_Age 1 "20–29" 2 "30–39" 3 "40–49" 4 "50+".
VALUE LABELS B2_Gender 1 "Male" 2 "Female".
VALUE LABELS B4_WorkSetting 1 "Urban" 2 "Peri-urban" 3 "Rural".
VALUE LABELS B5_YearsExp 1 "<1 year" 2 "1–5 years" 3 "6–10 years" 4 ">10 years".
VALUE LABELS B6_Qualification
  1 "MBBS" 2 "General Practitioner" 3 "Family Medicine Specialist" 4 "MD/MS" 5 "Other Specialist".
VALUE LABELS B7_Training P1_Used6Mo P7_WantTraining 0 "No" 1 "Yes".
VALUE LABELS KnowledgeCat 1 "Poor (0–4)" 2 "Moderate (5–6)" 3 "Good (7–8)".
VALUE LABELS AttitudeCat 1 "Negative (<30)" 2 "Neutral (30–39)" 3 "Positive (40–50)".
VALUE LABELS PracticeCat 1 "Low" 2 "Moderate" 3 "High".
VALUE LABELS P2_ConsultMonth_Ord 1 "0–2" 2 "3–5" 3 "6–10" 4 "More than 10".
VALUE LABELS P4_Documentation_Ord 1 "Never" 2 "Rarely" 3 "Sometimes" 4 "Always".
VALUE LABELS
  K1_InformedConsent K2_WrittenConsent K3_ReduceTravel K4_VideoMandatory
  K5_ControlledMeds K6_DataPrivacy K7_Emergencies K8_Documentation
  0 "No / Incorrect" 1 "Yes / Correct" 9 "Don't know".
VALUE LABELS
  A1_Privacy_Risk A2_Rural_Access A3_DocPt_Relation A4_Confidence A5_MedError_Risk
  A6_CME_Tool A7_CulturalFit A8_Integration A9_Recommend A10_LoadReduce
  1 "Strongly Disagree" 2 "Disagree" 3 "Neutral" 4 "Agree" 5 "Strongly Agree".
EXECUTE.

VARIABLE LEVEL
  B1_Age B2_Gender B4_WorkSetting B5_YearsExp B6_Qualification B7_Training
  P1_Used6Mo P7_WantTraining KnowledgeCat AttitudeCat PracticeCat (NOMINAL)
  KnowledgeScore AttitudeScore PracticeScore P2_ConsultMonth_Ord P4_Documentation_Ord (ORDINAL)
  A1_Privacy_Risk A2_Rural_Access A3_DocPt_Relation A4_Confidence A5_MedError_Risk
  A6_CME_Tool A7_CulturalFit A8_Integration A9_Recommend A10_LoadReduce (ORDINAL).
EXECUTE.

* 1. Reliability.
RELIABILITY
  /VARIABLES = A1_Privacy_Risk A2_Rural_Access A3_DocPt_Relation A4_Confidence
    A5_MedError_Risk A6_CME_Tool A7_CulturalFit A8_Integration A9_Recommend A10_LoadReduce
  /SCALE("Attitude_Scale") ALL
  /MODEL=ALPHA.
EXECUTE.

* 2. Descriptive statistics.
FREQUENCIES VARIABLES = B1_Age B2_Gender B4_WorkSetting B5_YearsExp B6_Qualification B7_Training
  /FORMAT=DFREQ
  /STATISTICS=MODE.

DESCRIPTIVES VARIABLES = KnowledgeScore AttitudeScore PracticeScore
  /STATISTICS=MEAN STDDEV MIN MAX.

FREQUENCIES VARIABLES = KnowledgeCat AttitudeCat PracticeCat P1_Used6Mo P7_WantTraining
  /FORMAT=DFREQ.

FREQUENCIES VARIABLES = P2_ConsultMonth_Ord P4_Documentation_Ord
  /FORMAT=DFREQ.

* Item-level frequencies.
FREQUENCIES VARIABLES =
  K1_InformedConsent K2_WrittenConsent K3_ReduceTravel K4_VideoMandatory
  K5_ControlledMeds K6_DataPrivacy K7_Emergencies K8_Documentation
  /FORMAT=DFREQ.

FREQUENCIES VARIABLES =
  A1_Privacy_Risk A2_Rural_Access A3_DocPt_Relation A4_Confidence A5_MedError_Risk
  A6_CME_Tool A7_CulturalFit A8_Integration A9_Recommend A10_LoadReduce
  /STATISTICS=MEAN STDDEV
  /FORMAT=DFREQ.

* Multi-select binary columns.
FREQUENCIES VARIABLES =
  C9_MedConsult C9_Prescription C9_MentalHealth C9_Emergency C9_ChronicFU
  P3_WhatsApp P3_Zoom P3_SudanHP P3_Phone
  P5_Internet P5_NoTraining P5_NoEquip P5_PtResist P5_Legal P5_NoBarrier
  P6_TechTrain P6_Internet P6_Guidelines P6_Equipment P6_Financial
  /FORMAT=DFREQ.
EXECUTE.

* 3. Bivariate analysis: factors associated with Knowledge Category.
CROSSTABS /TABLES = B1_Age BY KnowledgeCat /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
CROSSTABS /TABLES = B2_Gender BY KnowledgeCat /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
CROSSTABS /TABLES = B4_WorkSetting BY KnowledgeCat /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
CROSSTABS /TABLES = B5_YearsExp BY KnowledgeCat /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
CROSSTABS /TABLES = B6_Qualification BY KnowledgeCat /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
CROSSTABS /TABLES = B7_Training BY KnowledgeCat /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
EXECUTE.

* 4. Bivariate analysis: factors associated with Attitude Category.
CROSSTABS /TABLES = B1_Age BY AttitudeCat /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
CROSSTABS /TABLES = B2_Gender BY AttitudeCat /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
CROSSTABS /TABLES = B4_WorkSetting BY AttitudeCat /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
CROSSTABS /TABLES = B5_YearsExp BY AttitudeCat /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
CROSSTABS /TABLES = B6_Qualification BY AttitudeCat /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
CROSSTABS /TABLES = B7_Training BY AttitudeCat /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
CROSSTABS /TABLES = KnowledgeCat BY AttitudeCat /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
EXECUTE.

* 5. Bivariate analysis: factors associated with telemedicine use (P1_Used6Mo).
CROSSTABS /TABLES = B1_Age BY P1_Used6Mo /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
CROSSTABS /TABLES = B2_Gender BY P1_Used6Mo /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
CROSSTABS /TABLES = B4_WorkSetting BY P1_Used6Mo /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
CROSSTABS /TABLES = B5_YearsExp BY P1_Used6Mo /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
CROSSTABS /TABLES = B6_Qualification BY P1_Used6Mo /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
CROSSTABS /TABLES = B7_Training BY P1_Used6Mo /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
CROSSTABS /TABLES = KnowledgeCat BY P1_Used6Mo /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
CROSSTABS /TABLES = AttitudeCat BY P1_Used6Mo /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
EXECUTE.

* 6. Bivariate analysis: factors associated with Practice Category.
CROSSTABS /TABLES = B1_Age BY PracticeCat /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
CROSSTABS /TABLES = B2_Gender BY PracticeCat /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
CROSSTABS /TABLES = B4_WorkSetting BY PracticeCat /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
CROSSTABS /TABLES = B5_YearsExp BY PracticeCat /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
CROSSTABS /TABLES = B6_Qualification BY PracticeCat /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
CROSSTABS /TABLES = B7_Training BY PracticeCat /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
CROSSTABS /TABLES = KnowledgeCat BY PracticeCat /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
CROSSTABS /TABLES = AttitudeCat BY PracticeCat /STATISTICS=CHISQ /CELLS=COUNT ROW COLUMN.
EXECUTE.

* 7. Binary logistic regression: predictors of telemedicine use in past 6 months.
* Reference categories: B1_Age=1 (20–29), B2_Gender=1 (Male), B4_WorkSetting=1 (Urban),
*   B5_YearsExp=1 (<1 year), B6_Qualification=1 (MBBS), KnowledgeCat=1 (Poor), AttitudeCat=1 (Negative).
LOGISTIC REGRESSION VARIABLES P1_Used6Mo
  /METHOD=ENTER B1_Age B2_Gender B4_WorkSetting B5_YearsExp B6_Qualification
    B7_Training KnowledgeCat AttitudeCat
  /CONTRAST (B1_Age)=Indicator(1)
  /CONTRAST (B4_WorkSetting)=Indicator(1)
  /CONTRAST (B5_YearsExp)=Indicator(1)
  /CONTRAST (B6_Qualification)=Indicator(1)
  /CONTRAST (KnowledgeCat)=Indicator(1)
  /CONTRAST (AttitudeCat)=Indicator(1)
  /PRINT=GOODFIT CI(95)
  /CRITERIA=PIN(.05) POUT(.10) ITERATE(20) CUT(.5).
EXECUTE.

* NOTE: Update the OUTFILE path below before running.
SAVE OUTFILE="1_data/cleaned/kap_telemedicine_recoded.sav"
  /COMPRESSED.
EXECUTE.

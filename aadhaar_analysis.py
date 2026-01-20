import pandas as pd
import matplotlib.pyplot as plt
files=["C:\Users\Asus\Downloads\api_data_aadhar_enrolment\api_data_aadhar_enrolment\adhaar analysis\api_data_aadhar_enrolment_0_500000.csv",
     "C:\Users\Asus\Downloads\api_data_aadhar_enrolment\api_data_aadhar_enrolment\adhaar analysis\api_data_aadhar_enrolment_500000_1000000.csv", 
      "C:\Users\Asus\Downloads\api_data_aadhar_enrolment\api_data_aadhar_enrolment\adhaar analysis\api_data_aadhar_enrolment_1000000_1006029.csv" ]

df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)

print("Total Records:", len(df))
df["state_clean"] = df["state"].str.lower().str.strip()

fix_map = {
    "orissa": "odisha",
    "pondicherry": "puducherry",
    "west bangal": "west bengal",
    "westbengal": "west bengal",
    "west  bengal": "west bengal",
    "jammu & kashmir": "jammu and kashmir",
    "andaman & nicobar islands": "andaman and nicobar islands",
    "dadra & nagar haveli": "dadra and nagar haveli and daman and diu",
    "daman and diu": "dadra and nagar haveli and daman and diu",
    "daman & diu": "dadra and nagar haveli and daman and diu",
    "dadra and nagar haveli": "dadra and nagar haveli and daman and diu",
    "the dadra and nagar haveli and daman and diu": "dadra and nagar haveli and daman and diu",
    "100000": None
}
df["state_clean"] = df["state_clean"].replace(fix_map)
df = df[df["state_clean"].notna()]
df["total_enrolments"] = (
    df["age_0_5"] +
    df["age_5_17"] +
    df["age_18_greater"]
)
state_summary = (
    df.groupby("state_clean")["total_enrolments"]
      .sum()
      .reset_index()
      .sort_values(by="total_enrolments", ascending=False)
)
state_summary["Overall_Rank"] = range(1, len(state_summary) + 1)

top10 = state_summary.head(10).copy()
bottom10 = state_summary.tail(10).copy()
colors = ["#38bdf8", "#000407", "#2e5f2a"]

# --------------------------------
# STEP 6 — Top 10 Bar Chart

plt.figure(figsize=(10,5))
plt.bar(top10["state_clean"], top10["total_enrolments"], color=colors * 4)
plt.xticks(rotation=45, ha="right")
plt.title("Top 10 States by Aadhaar Enrolment")
plt.ylabel("Total Aadhaar Enrolments")
plt.tight_layout()

plt.figure(figsize=(10,5))
plt.bar(bottom10["state_clean"], bottom10["total_enrolments"], color=colors * 4)
plt.xticks(rotation=45, ha="right")
plt.title("Bottom 10 States by Aadhaar Enrolment")
plt.ylabel("Total Aadhaar Enrolments")
plt.tight_layout()
df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)
df = df[df["date"].notna()]

daily_pulse = (
    df.groupby("date")["total_enrolments"]
      .sum()
      .reset_index()
)

plt.figure(figsize=(12,5))
plt.plot(
    daily_pulse["date"],
    daily_pulse["total_enrolments"],
    color=colors[1],
    marker="o",
    linewidth=2
)
plt.title("Aadhaar Enrolment Pulse Over Time")
plt.xlabel("Date")
plt.ylabel("Total Aadhaar Enrolments")
plt.grid(True)
plt.tight_layout()


top5 = state_summary.head(5)
others_sum = state_summary.iloc[5:]["total_enrolments"].sum()

pie_data = pd.concat([
    top5[["state_clean", "total_enrolments"]],
    pd.DataFrame([["Others", others_sum]], columns=["state_clean", "total_enrolments"])
])

plt.figure(figsize=(7,7))
plt.pie(
    pie_data["total_enrolments"],
    labels=pie_data["state_clean"],
    autopct="%1.1f%%",
    startangle=140
)
plt.title("State-wise Contribution to Aadhaar Enrolments")
plt.tight_layout()

age_totals = {
    "0–5 Years": df["age_0_5"].sum(),
    "5–17 Years": df["age_5_17"].sum(),
    "18+ Years": df["age_18_greater"].sum()
}

plt.figure(figsize=(6,5))
plt.bar(age_totals.keys(), age_totals.values())
plt.title("Age-wise Aadhaar Enrolment Distribution")
plt.ylabel("Total Enrolments")
plt.tight_layout()


plt.figure(figsize=(6,6))
plt.pie(
    age_totals.values(),
    labels=age_totals.keys(),
    autopct="%1.1f%%",
    startangle=90
)
plt.title("Percentage Share by Age Group")
plt.tight_layout()

df["month"] = df["date"].dt.to_period("M")

monthly_pulse = (
    df.groupby("month")["total_enrolments"]
      .sum()
      .reset_index()
)

monthly_pulse["month"] = monthly_pulse["month"].astype(str)

plt.figure(figsize=(10,5))
plt.plot(
    monthly_pulse["month"],
    monthly_pulse["total_enrolments"],
    marker="o"
)
plt.xticks(rotation=45)
plt.title("Monthly Aadhaar Enrolment Trend")
plt.ylabel("Total Enrolments")
plt.tight_layout()



df["month"] = df["date"].dt.to_period("M")

monthly_pulse = (
    df.groupby("month")["total_enrolments"]
      .sum()
      .reset_index()
)

monthly_pulse["month"] = monthly_pulse["month"].astype(str)

plt.figure(figsize=(10,5))
plt.plot(
    monthly_pulse["month"],
    monthly_pulse["total_enrolments"],
    marker="o"
)
plt.xticks(rotation=45)
plt.title("Monthly Aadhaar Enrolment Trend")
plt.ylabel("Total Enrolments")
plt.tight_layout()

compare = pd.concat([
    state_summary.head(3),
    state_summary.tail(3)
])

plt.figure(figsize=(8,5))
plt.bar(compare["state_clean"], compare["total_enrolments"])
plt.title("Top 3 vs Bottom 3 States Comparison")
plt.ylabel("Total Enrolments")
plt.tight_layout()
state_daily_avg = (
    df.groupby("state_clean")["total_enrolments"]
      .mean()
      .reset_index()
      .sort_values(by="total_enrolments", ascending=False)
      .head(10)
)

plt.figure(figsize=(10,5))
plt.bar(
    state_daily_avg["state_clean"],
    state_daily_avg["total_enrolments"]
)

plt.xticks(rotation=45, ha="right")
plt.title("Top 10 States by Average Daily Aadhaar Enrolment")
plt.ylabel("Average Daily Enrolments")
plt.tight_layout()
plt.show()

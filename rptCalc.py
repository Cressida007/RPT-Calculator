import tkinter as tk
import calendar
from tkinter import ttk, messagebox
from datetime import date
import pandas as pd
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
 
 
# ================= CONSTANTS =================
DISCOUNT_RATE = 0.10
BASIC_RATE = 0.01
SEF_RATE = 0.01
MONTHLY_PENALTY_RATE = 0.02
MAX_PENALTY_MONTHS = 36
 
# ================= LGU COLORS =================
LGU_BLUE = "#1f3c88"
LGU_GOLD = "#f2b705"
LGU_BG = "#f4f6f8"
 
# ================= CALCULATION =================
def calculate_rpt(assessed_value, start_year, end_year, payment_mode, manual_date=None):
    rows = []
 
    annual_basic = round(assessed_value * BASIC_RATE, 2)
    annual_sef = round(assessed_value * SEF_RATE, 2)
 
    for year in range(start_year, end_year + 1):
        if payment_mode == "per_year":
            payment_date = date(year, 1, 10)
            discount_rate = DISCOUNT_RATE
        elif payment_mode == "bulk":
            payment_date = date.today()
            discount_rate = 0
        else:
            payment_date = manual_date
            discount_rate = 0.20 if payment_date.month == 12 else 0.10
 
        def penalty(amount):
            due = date(year, 4, 1)
            if payment_date <= due:
                return 0
            months = (payment_date.year - due.year) * 12 + payment_date.month - due.month
            if payment_date.day > 1:
                months += 1
            months = min(months, MAX_PENALTY_MONTHS)
            return round(amount * MONTHLY_PENALTY_RATE * months, 2)
 
        if payment_mode == "manual":
            discount_bsc = round(annual_basic * discount_rate, 2)
            discount_sef = round(annual_sef * discount_rate, 2)
        else:
            discount_bsc = annual_basic * discount_rate if payment_date <= date(year, 1, 31) else 0
            discount_sef = annual_sef * discount_rate if payment_date <= date(year, 1, 31) else 0
 
        rows.append({
            "Year": year,
            "Tax": "BSC",
            "Regular": annual_basic,
            "Discount": discount_bsc,
            "Penalty": penalty(annual_basic),
            "Total": round(annual_basic - discount_bsc + penalty(annual_basic), 2)
        })
        rows.append({
            "Year": year,
            "Tax": "SEF",
            "Regular": annual_sef,
            "Discount": discount_sef,
            "Penalty": penalty(annual_sef),
            "Total": round(annual_sef - discount_sef + penalty(annual_sef), 2)
        })
 
    return pd.DataFrame(rows)
 
# ================= ROOT =================
root = tk.Tk()
root.title("LGU Real Property Tax System")
root.configure(bg=LGU_BG)
root.attributes("-fullscreen", True)
 
# ================= STYLE =================
style = ttk.Style()
style.theme_use("clam")
 
style.configure(".", font=("Segoe UI", 13), background=LGU_BG)
style.configure("TLabelframe.Label", font=("Segoe UI", 18, "bold"), foreground=LGU_BLUE)
style.configure("TButton", font=("Segoe UI", 15, "bold"), padding=14)
style.map("TButton", background=[("active", LGU_GOLD)], foreground=[("active", "black")])
style.configure("Treeview", font=("Segoe UI", 12), rowheight=32)
style.configure("Treeview.Heading", font=("Segoe UI", 14, "bold"),
                background=LGU_BLUE, foreground="white")
 
style.configure(
    "Total.TLabel",
    font=("Segoe UI", 20, "bold"),
    foreground="darkred",
    background=LGU_BG
)
 
# ================= MAIN LAYOUT =================
main_frame = ttk.Frame(root)
main_frame.pack(fill="both", expand=True)
 
top_frame = ttk.Frame(main_frame)
top_frame.pack(fill="x", padx=20, pady=10)
 
# ================= PROPERTY INFO =================
prop = ttk.LabelFrame(top_frame, text="PROPERTY INFORMATION", padding=20)
prop.pack(fill="x", pady=5)
 
big_entry_font = ("Segoe UI", 15)
 
ttk.Label(prop, text="Owner Name").grid(row=0, column=0, sticky="w")
e_owner = ttk.Entry(prop, width=25, font=big_entry_font)
e_owner.grid(row=0, column=1, padx=(0, 20))
 
ttk.Label(prop, text="T.D. No.").grid(row=0, column=2)
e_td = ttk.Entry(prop, width=25, font=big_entry_font)
e_td.grid(row=0, column=3)
 
ttk.Label(prop, text="PIN").grid(row=1, column=0, sticky="w")
e_pin = ttk.Entry(prop, width=25, font=big_entry_font)
e_pin.grid(row=1, column=1, padx=(0, 20))
 
ttk.Label(prop, text="Location").grid(row=1, column=2)
e_location = ttk.Entry(prop, width=35, font=big_entry_font)
e_location.grid(row=1, column=3)
 
ttk.Label(prop, text="Assessed Value (PHP)").grid(row=2, column=0, pady=10)
e_assessed = ttk.Entry(prop, width=25, font=big_entry_font)
e_assessed.grid(row=2, column=1)
 
# ================= YEAR RANGE =================
year_frame = ttk.LabelFrame(top_frame, text="UNPAID REAL PROPERTY TAX YEARS", padding=20)
year_frame.pack(fill="x", pady=5)
 
start_year = tk.IntVar(value=2000)
end_year = tk.IntVar(value=date.today().year)
 
ttk.Label(year_frame, text="FROM").pack(side="left")
ttk.Spinbox(year_frame, from_=2000, to=2100,
            textvariable=start_year, width=8).pack(side="left", padx=15)
ttk.Label(year_frame, text="TO").pack(side="left")
ttk.Spinbox(year_frame, from_=2000, to=2100,
            textvariable=end_year, width=8).pack(side="left", padx=15)
 
# ================= PAYMENT MODE =================
mode_frame = ttk.LabelFrame(top_frame, text="PAYMENT MODE", padding=20)
mode_frame.pack(fill="x", pady=5)
 
payment_mode = tk.StringVar(value="per_year")
for text, val in [("Per Year (LGU)", "per_year"),
                  ("Bulk Arrears (Today)", "bulk"),
                  ("Manual Payment Date", "manual")]:
    ttk.Radiobutton(mode_frame, text=text,
                    variable=payment_mode, value=val).pack(side="left", padx=20)
 
# ================= MANUAL DATE =================
date_frame = ttk.LabelFrame(top_frame, text="MANUAL PAYMENT DATE", padding=20)
date_frame.pack(fill="x", pady=5)
 
m = tk.IntVar(value=12)
d = tk.IntVar(value=23)
y = tk.IntVar(value=date.today().year)
 
for lbl, var in [("Month", m), ("Day", d), ("Year", y)]:
    ttk.Label(date_frame, text=lbl).pack(side="left")
    ttk.Entry(date_frame, width=6, textvariable=var).pack(side="left", padx=10)
 
def toggle_manual(*args):
    state = "normal" if payment_mode.get() == "manual" else "disabled"
    for w in date_frame.winfo_children():
        if isinstance(w, ttk.Entry):
            w.config(state=state)
 
payment_mode.trace_add("write", toggle_manual)
toggle_manual()
 
# ================= COMPUTE + TOTAL =================
df_result = None
 
def compute():
    global df_result
    try:
        assessed = float(e_assessed.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid numeric Assessed Value.")
        return
 
    md = None
    if payment_mode.get() == "manual":
        try:
            md = date(y.get(), m.get(), d.get())
        except ValueError:
            messagebox.showerror("Date Error", "Invalid manual payment date.")
            return
 
    df_result = calculate_rpt(
        assessed,
        start_year.get(),
        end_year.get(),
        payment_mode.get(),
        md
    )
 
    tree.delete(*tree.get_children())
    for _, r in df_result.iterrows():
        tree.insert("", "end", values=(
            r["Year"], r["Tax"],
            f"{r['Regular']:,.2f}",
            f"{r['Discount']:,.2f}" if r["Discount"] else "",
            f"{r['Penalty']:,.2f}" if r["Penalty"] else "",
            f"{r['Total']:,.2f}"
        ))
 
    lbl_total.config(
        text=f"TOTAL AMOUNT DUE: PHP {df_result['Total'].sum():,.2f}"
    )
 
compute_frame = ttk.Frame(top_frame)
compute_frame.pack(fill="x", pady=15)
 
btn_compute = ttk.Button(
    compute_frame,
    text="COMPUTE REAL PROPERTY TAX",
    command=compute
)
btn_compute.place(relx=0.5, rely=0.5, anchor="center")
 
lbl_total = ttk.Label(
    compute_frame,
    text="TOTAL AMOUNT DUE: PHP 0.00",
    style="Total.TLabel"
)
lbl_total.pack(side="right", padx=40)
 
# ================= TABLE =================
tree_container = ttk.Frame(main_frame)
tree_container.pack(fill="both", expand=True, padx=20, pady=5)
 
columns = ("Year", "Tax", "Regular", "Discount", "Penalty", "Total")
tree = ttk.Treeview(tree_container, columns=columns, show="headings")
tree.pack(fill="both", expand=True)
 
for c in columns:
    tree.heading(c, text=c)
    tree.column(c, width=150, anchor="center")
 
root.mainloop()
 
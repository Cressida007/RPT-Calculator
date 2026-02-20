import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from decimal import Decimal
import pandas as pd
import logging
import sys

# ================= LOGGING =================
logging.basicConfig(
    filename="rpt_system.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ================= GLOBAL EXCEPTION HANDLER =================
def global_exception_handler(exc_type, exc_value, exc_traceback):
    logging.error(f"Unhandled Exception: {exc_value}")
    messagebox.showerror(
        "Critical System Error",
        "An unexpected system error occurred.\nPlease restart the application."
    )

sys.excepthook = global_exception_handler

# ================= CONSTANTS =================
DISCOUNT_RATE = Decimal("0.10")
BASIC_RATE = Decimal("0.01")
SEF_RATE = Decimal("0.01")
MONTHLY_PENALTY_RATE = Decimal("0.02")
MAX_PENALTY_MONTHS = 36

MAX_NAME_LEN = 60
MAX_LOCATION_LEN = 80
MAX_TD_LEN = 20
MAX_PIN_LEN = 30
MAX_ASSESSED_LEN = 12  # max length for numbers

LGU_BLUE = "#1f3c88"
LGU_GOLD = "#f2b705"
LGU_BG = "#f0f4f8"
LGU_ENTRY_BG = "#ffffff"
LGU_SPINBOX_FONT = ("Segoe UI", 16, "bold")  # bigger font

df_result = None

# ================= ROOT WINDOW =================
root = tk.Tk()
root.title("LGU Real Property Tax System")
root.geometry("1200x940")
root.minsize(700, 940)
root.configure(bg=LGU_BG)

def on_close():
    root.destroy()
root.protocol("WM_DELETE_WINDOW", on_close)

# ================= CENTER FRAME =================
main_frame = ttk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# ================= STYLE =================
style = ttk.Style()
style.theme_use("clam")
style.configure(".", font=("Segoe UI", 14), background=LGU_BG)
style.configure("TLabelframe.Label", font=("Segoe UI", 18, "bold"), foreground=LGU_BLUE)
style.configure("Treeview", font=("Segoe UI", 12), rowheight=30, background="#e6f0fa", fieldbackground="#e6f0fa")
style.configure("Treeview.Heading", font=("Segoe UI", 14, "bold"), background=LGU_BLUE, foreground="white")
style.configure("Total.TLabel", font=("Segoe UI", 20, "bold"), foreground="darkred")
style.map("TButton", background=[("active", LGU_GOLD)], foreground=[("active", "black")])

# ================= PROPERTY INFORMATION =================
prop = ttk.LabelFrame(main_frame, text="PROPERTY INFORMATION", padding=15)
prop.pack(fill="x", pady=10)
for i in range(4):
    prop.columnconfigure(i, weight=1)

big_font = ("Segoe UI", 14)

def limit_length(entry, max_len):
    val = entry.get()
    if len(val) > max_len:
        entry.delete(max_len, tk.END)

def numbers_only(action, value):
    if action != "1":
        return True
    return value.isdigit()

def decimal_only(action, value):
    if action != "1":  # deletion or other
        return True
    # allow only digits or one dot
    if value.count('.') > 1:
        return False
    allowed_chars = "0123456789."
    return all(c in allowed_chars for c in value)

num_validate = root.register(numbers_only)
decimal_validate = root.register(decimal_only)

e_owner = ttk.Entry(prop, width=30, font=big_font)
e_td = ttk.Entry(prop, width=25, font=big_font, validate="key", validatecommand=(num_validate, "%d", "%P"))
e_pin = ttk.Entry(prop, width=25, font=big_font, validate="key", validatecommand=(num_validate, "%d", "%P"))
e_location = ttk.Entry(prop, width=40, font=big_font)
e_assessed = ttk.Entry(prop, width=25, font=big_font, validate="key", validatecommand=(decimal_validate, "%d", "%P"))

e_owner.grid(row=0, column=1, sticky="ew", padx=5, pady=3)
e_td.grid(row=0, column=3, sticky="ew", padx=5, pady=3)
e_pin.grid(row=1, column=1, sticky="ew", padx=5, pady=3)
e_location.grid(row=1, column=3, sticky="ew", padx=5, pady=3)
e_assessed.grid(row=2, column=1, sticky="ew", padx=5, pady=3)

ttk.Label(prop, text="Owner Name").grid(row=0, column=0, sticky="w", padx=5)
ttk.Label(prop, text="T.D. No.").grid(row=0, column=2, sticky="w", padx=5)
ttk.Label(prop, text="PIN").grid(row=1, column=0, sticky="w", padx=5)
ttk.Label(prop, text="Location").grid(row=1, column=2, sticky="w", padx=5)
ttk.Label(prop, text="Assessed Value (PHP)").grid(row=2, column=0, sticky="w", padx=5)

e_owner.bind("<KeyRelease>", lambda e: limit_length(e_owner, MAX_NAME_LEN))
e_location.bind("<KeyRelease>", lambda e: limit_length(e_location, MAX_LOCATION_LEN))
e_td.bind("<KeyRelease>", lambda e: limit_length(e_td, MAX_TD_LEN))
e_pin.bind("<KeyRelease>", lambda e: limit_length(e_pin, MAX_PIN_LEN))
e_assessed.bind("<KeyRelease>", lambda e: limit_length(e_assessed, MAX_ASSESSED_LEN))

# ================= YEAR RANGE =================
year_frame = ttk.LabelFrame(main_frame, text="UNPAID REAL PROPERTY TAX YEARS", padding=10)
year_frame.pack(fill="x", pady=10)

start_year = tk.IntVar(value=2000)
end_year = tk.IntVar(value=date.today().year)

ttk.Label(year_frame, text="FROM").pack(side="left", padx=5)
ttk.Spinbox(year_frame, from_=1900, to=date.today().year, textvariable=start_year, width=8, font=LGU_SPINBOX_FONT).pack(side="left", padx=10)
ttk.Label(year_frame, text="TO").pack(side="left", padx=5)
ttk.Spinbox(year_frame, from_=1900, to=date.today().year, textvariable=end_year, width=8, font=LGU_SPINBOX_FONT).pack(side="left", padx=10)

# ================= TREEVIEW =================
tree_frame = ttk.Frame(main_frame)
tree_frame.pack(fill="both", expand=True, pady=10)

columns = ("Year", "Tax", "Regular", "Discount", "Penalty", "Total")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor="center", stretch=True)  # <-- stretch True

# Fixed table: disable moving columns
tree["displaycolumns"] = columns
tree.bind("<Button-1>", lambda e: "break")  # prevent resizing/moving by left-click

vsb_tree = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=vsb_tree.set)

tree.grid(row=0, column=0, sticky="nsew")
vsb_tree.grid(row=0, column=1, sticky="ns")
tree_frame.columnconfigure(0, weight=1)
tree_frame.rowconfigure(0, weight=1)

# ===== DYNAMIC COLUMN RESIZING =====
def resize_tree_columns(event):
    tree_width = tree_frame.winfo_width()
    num_cols = len(columns)
    for col in columns:
        tree.column(col, width=int(tree_width / num_cols))

tree_frame.bind("<Configure>", resize_tree_columns)

# ================= TOTAL LABEL =================
lbl_total = ttk.Label(main_frame, text="TOTAL AMOUNT DUE: PHP 0.00", style="Total.TLabel")
lbl_total.pack(pady=10)

# ================= VALIDATION =================
def validate_inputs():
    errors = []
    if not e_owner.get().strip():
        errors.append("Owner Name is required.")
    if not e_td.get().strip():
        errors.append("T.D. No. is required.")
    if not e_pin.get().strip():
        errors.append("PIN is required.")
    if not e_location.get().strip():
        errors.append("Location is required.")
    if not e_assessed.get().strip():
        errors.append("Assessed Value is required.")
    try:
        assessed = Decimal(e_assessed.get())
        if assessed <= 0:
            errors.append("Assessed Value must be greater than zero.")
    except:
        errors.append("Invalid Assessed Value.")
    if start_year.get() > end_year.get():
        errors.append("Start Year cannot be greater than End Year.")
    return errors

# ================= CALCULATION =================
def calculate_rpt(assessed_value, sy, ey):
    rows = []
    annual_basic = (assessed_value * BASIC_RATE).quantize(Decimal("0.01"))
    annual_sef = (assessed_value * SEF_RATE).quantize(Decimal("0.01"))
    for year in range(sy, ey+1):
        rows.append({
            "Year": year, "Tax": "BSC",
            "Regular": annual_basic, "Discount": Decimal("0.00"),
            "Penalty": Decimal("0.00"), "Total": annual_basic
        })
        rows.append({
            "Year": year, "Tax": "SEF",
            "Regular": annual_sef, "Discount": Decimal("0.00"),
            "Penalty": Decimal("0.00"), "Total": annual_sef
        })
    return pd.DataFrame(rows)

# ================= COMPUTE =================
def compute():
    global df_result
    errors = validate_inputs()
    if errors:
        messagebox.showerror("Input Error", "\n".join(errors))
        return

    assessed = Decimal(e_assessed.get())
    sy, ey = start_year.get(), end_year.get()
    df_result = calculate_rpt(assessed, sy, ey)

    tree.delete(*tree.get_children())
    total = Decimal("0.00")
    for _, r in df_result.iterrows():
        total += r["Total"]
        tree.insert("", "end", values=(
            r["Year"], r["Tax"], f"{r['Regular']:,.2f}",
            f"{r['Discount']:,.2f}", f"{r['Penalty']:,.2f}", f"{r['Total']:,.2f}"
        ))
    lbl_total.config(text=f"TOTAL AMOUNT DUE: PHP {total:,.2f}")
    logging.info(f"Computation successful for {e_owner.get()}")

# ================= BUTTONS =================
btn_compute = ttk.Button(main_frame, text="COMPUTE REAL PROPERTY TAX", command=compute)
btn_compute.pack(pady=5)
ttk.Button(main_frame, text="EXIT APPLICATION", command=root.destroy).pack(pady=5)

root.mainloop()
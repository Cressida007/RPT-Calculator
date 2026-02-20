---

## RPT Calculator – Real Property Tax System for LGUs

An interactive Python Tkinter application designed to calculate **Real Property Tax (RPT)** for Local Government Units (LGUs).
This project demonstrates **workflow automation, backend logic, GUI development, and desktop deployment**, showcasing a practical approach to solving real-world problems.

---

## 🧠 Purpose & Thought Process

Local governments often need to calculate real property taxes for multiple properties over many years. Manual computation is **time-consuming, error-prone, and inefficient**.

This project aims to:

* ✅ **Automate tax calculations including Basic (BSC) and Special Education Fund (SEF) taxes**
* ✅ **Handle discounts, penalties, and multiple payment modes (per year, bulk, manual date)**
* ✅ **Validate user inputs to prevent errors and guide the user with clear messages**
* ✅ **Present results in an interactive, scrollable table**
* ✅ **Provide a foundation for future report generation (PDFs) for administrative purposes**

This reflects my process of analyzing the problem, breaking it into **logical steps**, and building a tool that is **usable, maintainable, and user-proof**.

---

## 🚀 How the Application Works

### 1️⃣ Enter Property Information

* Owner Name, T.D. No., PIN, Location, Assessed Value (supports decimals like **10.60**)
* Input validation prevents unreasonable values and limits text lengths

### 2️⃣ Select Unpaid Tax Years

* Specify a **start and end year** for unpaid taxes

### 3️⃣ Choose Payment Mode

* **Per Year:** standard yearly payment
* **Bulk:** pay all arrears today
* **Manual Date:** apply a specific payment date for discounts and penalties

### 4️⃣ Manual Payment Date (if selected)

* Enter **month, day, and year** to simulate a specific payment date

### 5️⃣ Compute Taxes

* Press **Compute Real Property Tax**
* Calculates:

  * **Annual Basic and SEF taxes**
  * **Discounts based on payment mode**
  * **Penalties for late payments**
  * **Total per year per tax type**
* Displays **total amount due** in a bold, prominent label

---

## 🛠 Tech Stack

* **Python 3.13+** – core programming language
* **Tkinter** – interactive GUI
* **Pandas** – structured data handling
* **Logging** – logs computation events and errors
* **PyInstaller** – native Windows executable with **custom icon**
* **Git & GitHub** – version control and portfolio showcase

---

## 📂 How to Run Locally

### Clone the repository

```bash
git clone https://github.com/Cressida007/RPT-Calculator.git
cd RPT-Calculator
```

### Create a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the application

```bash
python rptCalc.py
```

---

## 🖥 Optional: Run as Native Executable

* A compiled **.exe** version is included for Windows, complete with a **custom icon**
* Simply double-click `rptCalc.exe` to launch—**no Python installation required**

---

## ⚡ Highlights in v2

* ✅ **Input validation for all fields**, including decimals and max text length
* ✅ **Windowed interface** with proper minimize, maximize, and close controls
* ✅ **Logging** for computation tracking and error handling
* ✅ **Scrollable and resizable Treeview** with dynamic column widths
* ✅ **Decimal-based calculations** for accuracy
* ✅ **Native Windows .exe with custom icon** for a professional desktop feel

---

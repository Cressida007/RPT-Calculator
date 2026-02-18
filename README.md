# RPT Calculator – Real Property Tax System for LGUs

An **interactive Python Tkinter application** designed to calculate **Real Property Tax (RPT)** for Local Government Units (LGUs).  
This project showcases **workflow automation, backend logic, and GUI development**, providing a clear view of how I approach solving real-world problems.

---

## 🧠 Purpose & Thought Process

Local governments often need to calculate real property taxes for many properties across multiple years. Manual computation is **time-consuming, error-prone, and inefficient**.  

The purpose of this project is to:

1. Automate tax calculations including **Basic (BSC) and Special Education Fund (SEF) taxes**.  
2. Handle **discounts, penalties, and different payment modes** (per year, bulk, manual date).  
3. Present results in an **interactive and easy-to-read table**.  
4. Provide a foundation for **report generation** (PDFs) for administrative purposes.

This shows my thought process: **analyzing the problem, breaking it into clear logical steps, and building a tool that is usable and maintainable**.

---

## 🚀 How the Application Works

1. **Enter Property Information**  
   - Owner Name, T.D. No., PIN, Location, Assessed Value

2. **Select Unpaid Tax Years**  
   - Specify a year range for which the property has unpaid taxes

3. **Choose Payment Mode**  
   - **Per Year**: standard yearly payment  
   - **Bulk**: pay all arrears today  
   - **Manual Date**: apply a specific payment date to calculate discounts and penalties

4. **Manual Payment Date (if selected)**  
   - Enter month, day, and year to simulate payment date  

5. **Compute Taxes**  
   - Press the **"Compute Real Property Tax"** button  
   - The program calculates:
     - Annual Basic and SEF taxes  
     - Discounts based on payment mode  
     - Penalties for late payments  
     - Total per year per tax type  

6. **View Results**  
   - Results are displayed in a **sortable, scrollable table**  
   - **Total amount due** is highlighted

---

## 🛠 Tech Stack

- **Python 3** – core programming language  
- **Tkinter** – interactive GUI  
- **Pandas** – structured data handling  
- **ReportLab** – future PDF report generation  
- **Git & GitHub** – version control and portfolio showcase  

---

## 📂 How to Run Locally

1. Clone the repository:

```bash
git clone https://github.com/Cressida007/RPT-Calculator.git
cd RPT-Calculator

2. Create a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

3. install dependencies
pip install -r requirements.txt

4. Run the application
python rptCalc.py

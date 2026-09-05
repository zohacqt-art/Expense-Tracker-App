import customtkinter as ctk
from collections import defaultdict
from datetime import datetime
import os

# ---------- File & Theme section----------
FILE_NAME = "expenses.txt"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

YELLOW = "#FFD700"
BLACK = "#1C1C1C"

# ---------- Main_app's look----------
app = ctk.CTk()
app.title("💸 Expense Tracker App")
app.geometry("400x700")
app.configure(fg_color=BLACK)

# ---------- Functions's Section  ----------

#----------Func(1): ADD the expense--------------------
def add_expense():
    amount = entry_amount.get()
    category = entry_category.get()
    date = entry_date.get()

    if not (amount and category and date):
        output_label.configure(text="⚠️ Please fill all fields!", text_color="red")
        return

    with open(FILE_NAME, "a") as f:
        f.write(f"{amount},{category},{date}\n")

#-------how to reset type fields-------------------
    output_label.configure(text="✅ Expense added successfully!", text_color=YELLOW)
    entry_amount.delete(0, 'end')
    entry_category.delete(0, 'end')
    entry_date.delete(0, 'end')
    
           #__________func(1) END____________
           
#----------Func(2): View the expenses--------------------
def view_expenses():
    text_output.delete("1.0", "end")
    if not os.path.exists(FILE_NAME):
        text_output.insert("end", "No expenses recorded yet.\n")
        return

    with open(FILE_NAME, "r") as f:
        lines = f.readlines()
        if not lines:
            text_output.insert("end", "No expenses found.\n")
            return 
        for line in lines:
            amount, category, date = line.strip().split(",")
            text_output.insert("end", f"💰 {amount} PKR | {category} | {date}\n")

                 #__________func(2) END____________
                 
#----------Func(3): Search the expenses by their Dates--------------------                 
def search_by_date():
    text_output.delete("1.0", "end")
    search_date = entry_date.get()
    found = False

    if not os.path.exists(FILE_NAME):
        text_output.insert("end", "No data file found.\n")
        return

    with open(FILE_NAME, "r") as f:
        for line in f:
            amount, category, date = line.strip().split(",")
            if date == search_date:
                text_output.insert("end", f"{amount} PKR | {category}\n")
                found = True
    if not found:
        text_output.insert("end", "No expenses found for this date.\n")
        
           #__________func(3) END____________
        
               
#----------Func(4): Monthly Summary of the Expenses-------------------- 

def monthly_summary():
    text_output.delete("1.0", "end")
    data = defaultdict(int)
    count = 0
    total = 0

    if not os.path.exists(FILE_NAME):
        text_output.insert("end", "No data available.\n")
        return

    with open(FILE_NAME, "r") as f:
        for line in f:
            amount, category, date = line.strip().split(",")
            amount = int(amount)
            total += amount
            count += 1
            data[category] += amount

    if count == 0:
        text_output.insert("end", "No data available.\n")
        return

    average = total / count
    top_category = max(data, key=data.get)

    text_output.insert("end", f"📊 Monthly Summary\n")
    text_output.insert("end", f"Total Expenses: {total} PKR\n")
    text_output.insert("end", f"Entries: {count}\n")
    text_output.insert("end", f"Average per Day: {average:.2f} PKR\n")
    text_output.insert("end", f"Top Category: {top_category}\n")
                #__________func(4) END____________
                
#_______________GUI SECTION______________________                              
# ---------- Title ----------
title = ctk.CTkLabel(app, text="💸 Expense Tracker", font=("Arial Black", 22), text_color=YELLOW)
title.pack(pady=10)

# ---------- Input Frame ----------
frame = ctk.CTkFrame(app, fg_color=BLACK)
frame.pack(pady=5)

entry_amount = ctk.CTkEntry(frame, placeholder_text="Enter Amount (PKR)", width=250)
entry_amount.pack(pady=5)

entry_category = ctk.CTkEntry(frame, placeholder_text="Enter Category (e.g., Food, Travel)", width=250)
entry_category.pack(pady=5)

entry_date = ctk.CTkEntry(frame, placeholder_text="Enter Date (YYYY-MM-DD)", width=250)
entry_date.pack(pady=5)

# ---------- Buttons ----------
btn_add = ctk.CTkButton(app, text="➕ Add Expense", fg_color=YELLOW, text_color=BLACK, hover_color="#FFD966", width=250, command=add_expense)
btn_add.pack(pady=8)

btn_view = ctk.CTkButton(app, text="📋 View Expenses", fg_color=YELLOW, text_color=BLACK, hover_color="#FFD966", width=250, command=view_expenses)
btn_view.pack(pady=8)

btn_search = ctk.CTkButton(app, text="🔍 Search by Date", fg_color=YELLOW, text_color=BLACK, hover_color="#FFD966", width=250, command=search_by_date)
btn_search.pack(pady=8)

btn_summary = ctk.CTkButton(app, text="📊 Monthly Summary", fg_color=YELLOW, text_color=BLACK, hover_color="#FFD966", width=250, command=monthly_summary)
btn_summary.pack(pady=8)

# ---------- Output Box ----------
text_output = ctk.CTkTextbox(app, width=350, height=250, fg_color="#222222", text_color=YELLOW)
text_output.pack(pady=10)

# ---------- Status Label ----------
output_label = ctk.CTkLabel(app, text="", font=("Arial", 13))
output_label.pack(pady=5)

# ---------- Run App ----------
app.mainloop()

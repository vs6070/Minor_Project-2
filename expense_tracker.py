import tkinter as tk
from tkinter import messagebox
import csv
import os

FILE_NAME = "expenses.csv"

# Initialize file
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Type", "Amount", "Category"])

# Load data
def load_data():
    transactions.delete(0, tk.END)
    balance = 0

    with open(FILE_NAME, "r") as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            t_type, amount, category = row
            transactions.insert(tk.END, f"{t_type}: ₹{amount} ({category})")

            if t_type == "Income":
                balance += float(amount)
            else:
                balance -= float(amount)

    balance_label.config(text=f"Balance: ₹{balance:.2f}")

# Add transaction
def add_transaction():
    t_type = type_var.get()
    amount = amount_entry.get()
    category = category_entry.get()

    if not amount.isdigit():
        messagebox.showerror("Error", "Enter valid amount")
        return

    if category == "":
        messagebox.showerror("Error", "Enter category")
        return

    with open(FILE_NAME, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([t_type, amount, category])

    amount_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)

    load_data()

# Clear all data
def clear_data():
    if messagebox.askyesno("Confirm", "Delete all records?"):
        with open(FILE_NAME, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Type", "Amount", "Category"])
        load_data()

# UI
root = tk.Tk()
root.title("💰 Expense Tracker")
root.geometry("400x500")

tk.Label(root, text="Expense Tracker", font=("Arial", 16, "bold")).pack(pady=10)

# Type
type_var = tk.StringVar(value="Expense")
tk.OptionMenu(root, type_var, "Expense", "Income").pack(pady=5)

# Amount
amount_entry = tk.Entry(root)
amount_entry.pack(pady=5)
amount_entry.insert(0, "Amount")

# Category
category_entry = tk.Entry(root)
category_entry.pack(pady=5)
category_entry.insert(0, "Category")

# Add button
tk.Button(root, text="Add Transaction", command=add_transaction).pack(pady=10)

# List
transactions = tk.Listbox(root, width=45)
transactions.pack(pady=10)

# Balance
balance_label = tk.Label(root, text="Balance: ₹0.00", font=("Arial", 12, "bold"))
balance_label.pack(pady=5)

# Clear
tk.Button(root, text="Clear All", command=clear_data).pack(pady=10)

load_data()

root.mainloop()
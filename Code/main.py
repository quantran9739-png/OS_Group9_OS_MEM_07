import tkinter as tk
from tkinter import ttk, messagebox

processes = [
    {"name": "P1", "size": 100},
    {"name": "P2", "size": 200},
    {"name": "P3", "size": 50}
]

blocks = [
    {"name": "B1", "size": 300, "remaining": 300},
    {"name": "B2", "size": 150, "remaining": 150},
    {"name": "B3", "size": 500, "remaining": 500}
]

def run_algorithm():
    # reset lại bộ nhớ
    for b in blocks:
        b["remaining"] = b["size"]

    for row in tree.get_children():
        tree.delete(row)

    for p in processes:
        allocated = False

        for b in blocks:
            if b["remaining"] >= p["size"]:
                b["remaining"] -= p["size"]

                tree.insert("", "end", values=(
                    p["name"],
                    b["name"],
                    b["remaining"],
                    "Allocated"
                ))

                allocated = True
                break

        if not allocated:
            tree.insert("", "end", values=(
                p["name"],
                "Not Allocated",
                0,
                "Fail"
            ))

# GUI
root = tk.Tk()
root.title("Memory Allocation GUI (Week 2)")

# tiêu đề
tk.Label(root, text="Memory Allocation Simulator", font=("Arial", 16)).pack(pady=10)

# run
tk.Button(root, text="Run First-Fit", command=run_algorithm).pack(pady=10)

# kết quả
columns = ("Process", "Block", "Remaining", "Status")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)

tree.pack(pady=10)

root.mainloop()
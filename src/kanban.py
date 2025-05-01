import tkinter as tk
from tkinter import simpledialog, messagebox
import matplotlib.pyplot as plt
import os

# Set up folder for snapshots
KANBAN_FOLDER = "kanban"
os.makedirs(KANBAN_FOLDER, exist_ok=True)

kanban_board = {
    "To Do": [],
    "In Progress": [],
    "Done": []
}

def draw_board(filename="kanban_board.png"):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')

    columns = list(kanban_board.keys())
    num_columns = len(columns)
    width = 1 / num_columns

    for i, column in enumerate(columns):
        x = i * width
        ax.add_patch(plt.Rectangle((x, 0), width, 1, fill=True, color='#f0f0f0', ec='black'))
        ax.text(x + width / 2, 0.95, column, ha='center', va='top', fontsize=14, fontweight='bold')

        tasks = kanban_board[column]
        for j, task in enumerate(tasks):
            y = 0.9 - j * 0.1
            ax.text(x + width / 2, y, f"- {task}", ha='center', va='top', fontsize=10)

    path = os.path.join(KANBAN_FOLDER, filename)
    plt.tight_layout()
    plt.savefig(path, bbox_inches='tight')
    plt.close()

def update_board():
    draw_board()
    refresh_listboxes()

def refresh_listboxes():
    for col, lb in listboxes.items():
        lb.delete(0, tk.END)
        for task in kanban_board[col]:
            lb.insert(tk.END, task)

def add_task():
    task = simpledialog.askstring("New Task", "Enter task name:")
    if task:
        kanban_board["To Do"].append(task)
        update_board()

def move_task():
    selected = None
    from_col = None
    for col, lb in listboxes.items():
        sel = lb.curselection()
        if sel:
            selected = lb.get(sel[0])
            from_col = col
            break
    if not selected:
        messagebox.showwarning("No selection", "Please select a task to move.")
        return

    to_col = simpledialog.askstring("Move Task", "Move to (To Do, In Progress, Done):")
    if to_col not in kanban_board:
        messagebox.showerror("Invalid", f"'{to_col}' is not a valid column.")
        return

    kanban_board[from_col].remove(selected)
    kanban_board[to_col].append(selected)
    update_board()

# GUI Setup
root = tk.Tk()
root.title("Kanban Board")

frame = tk.Frame(root)
frame.pack(pady=10)

listboxes = {}

for col in kanban_board:
    col_frame = tk.Frame(frame)
    col_frame.pack(side=tk.LEFT, padx=10)

    tk.Label(col_frame, text=col, font=("Helvetica", 14, "bold")).pack()
    lb = tk.Listbox(col_frame, width=20, height=10)
    lb.pack()
    listboxes[col] = lb

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add Task", command=add_task).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Move Task", command=move_task).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Update Snapshot", command=update_board).pack(side=tk.LEFT, padx=5)

# Initial draw
update_board()
root.mainloop()
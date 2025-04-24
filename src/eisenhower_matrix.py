import matplotlib.pyplot as plt

# Sample tasks for each quadrant
tasks = {
    "Urgent & Important": ["Finish report", "Doctor appointment"],
    "Not Urgent & Important": ["Workout", "Learn Python"],
    "Urgent & Not Important": ["Answer emails", "Call back supplier"],
    "Not Urgent & Not Important": ["Check Instagram", "Watch YouTube"]
}

fig, ax = plt.subplots(figsize=(10, 10))

# Draw quadrants
ax.axhline(0.5, color='black', linewidth=2)
ax.axvline(0.5, color='black', linewidth=2)

# Hide axes
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# Titles for quadrants
ax.text(0.25, 0.95, "Urgent & Important\n(DO NOW)", ha='center', fontsize=12, fontweight='bold')
ax.text(0.75, 0.95, "Not Urgent & Important\n(SCHEDULE)", ha='center', fontsize=12, fontweight='bold')
ax.text(0.25, 0.45, "Urgent & Not Important\n(DELEGATE)", ha='center', fontsize=12, fontweight='bold')
ax.text(0.75, 0.45, "Not Urgent & Not Important\n(ELIMINATE)", ha='center', fontsize=12, fontweight='bold')

# Place tasks
positions = {
    "Urgent & Important": (0.05, 0.6),
    "Not Urgent & Important": (0.55, 0.6),
    "Urgent & Not Important": (0.05, 0.1),
    "Not Urgent & Not Important": (0.55, 0.1)
}

for quadrant, (x, y_start) in positions.items():
    for i, task in enumerate(tasks[quadrant]):
        ax.text(x, y_start - i * 0.05, f"- {task}", fontsize=10)

plt.title("Eisenhower Matrix", fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt

# Example data: (Market Share, Market Growth)
products = {
    "Product A": (0.8, 0.7),  # Star
    "Product B": (0.3, 0.6),  # Question Mark
    "Product C": (0.9, 0.2),  # Cash Cow
    "Product D": (0.2, 0.1),  # Dog
}

fig, ax = plt.subplots(figsize=(10, 10))

# Draw quadrants
ax.axhline(0.5, color='black', linewidth=2)
ax.axvline(0.5, color='black', linewidth=2)

# Axis labels
ax.set_xlabel("Market Share", fontsize=12)
ax.set_ylabel("Market Growth", fontsize=12)

# Titles for quadrants
ax.text(0.25, 0.95, "Question Marks", ha='center', fontsize=12, fontweight='bold')
ax.text(0.75, 0.95, "Stars", ha='center', fontsize=12, fontweight='bold')
ax.text(0.25, 0.05, "Dogs", ha='center', fontsize=12, fontweight='bold')
ax.text(0.75, 0.05, "Cash Cows", ha='center', fontsize=12, fontweight='bold')

# Set limits
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# Plot products
for name, (share, growth) in products.items():
    ax.plot(share, growth, 'o', markersize=12)
    ax.text(share + 0.02, growth, name, fontsize=10)

plt.title("BCG Matrix", fontsize=16, fontweight='bold')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

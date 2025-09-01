import matplotlib.pyplot as plt
import numpy as np

# Approximate data extracted from the images
x1 = list(range(1, 21))
y1 = [15, 28, 55, 68, 82, 68, 78, 77, 94, 93, 92, 93, 91, 55, 92, 100, 100, 100, 100, 100]

x2 = list(range(1, 21))
y2 = [55, 58, 81, 95, 78, 95, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]

x3 = list(range(1, 11))
y3 = [50, 50, 60, 78, 85, 98, 100, 100, 100, 100]

x4 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y4 = [60, 100, 100, 100, 100, 100, 100, 100, 100, 100]

x5 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y5 = [70, 83, 83, 85, 87, 94, 96, 96, 95, 94]

# Create the plot
plt.figure(figsize=(10, 6))

# Set font sizes
plt.rcParams.update({'font.size': 14})  # Adjust the global font size

# Plot each dataset with different colors
plt.plot(x1[:10], y1[:10], 'b-o', label='sig:sig:sig-lr0008', markersize=4, linewidth=1)
plt.plot(x2[:10], y2[:10], 'r-o', label='lReLU:sig:sig-lr0008', markersize=4, linewidth=1)
plt.plot(x3, y3, 'g-o', label='lReLU:lReLU:sig-lr0008', markersize=4, linewidth=1)
plt.plot(x4, y4, 'm-o', markersize=4, linewidth=1, label='lReLU:lReLU:lReLU-lr001')
plt.plot(x5, y5, 'c-o', markersize=4, linewidth=1, label='lReLU:lReLU:lReLU-lr0008')

# Set plot labels and title
plt.xlabel('Batch Number', fontsize=14)
plt.ylabel('Percentage Match', fontsize=14)
plt.title('Percentage of Matches per 1000 Entries', fontsize=14)

# Set y-axis limits
plt.ylim(0, 105)

# Set x-axis limits
plt.xlim(0.5, 10.5)

# Add grid for readability
plt.grid(True, alpha=0.3)

# Add legend with bigger text
plt.legend(loc='lower right', fontsize=14)

# Show the plot
plt.tight_layout()

# Save the plot before showing it
plt.savefig("combined_lrelu_sig.png", dpi=300, bbox_inches="tight")  # Save as PNG with high resolution
plt.show()

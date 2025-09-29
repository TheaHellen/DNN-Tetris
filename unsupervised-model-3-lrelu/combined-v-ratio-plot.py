import matplotlib.pyplot as plt
import numpy as np

# Extract data from each graph
# lrelulrelusig-lr0005 (Image 1)
data1_rows = [100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000]
data1_scores = [0.52717, 0.5263, 0.52632, 0.52629, 0.52634, 0.52629, 0.52632, 0.52634, 0.52630]

# lrelusigsig-lr0001 (Image 2)
data2_rows = [100000, 200000, 300000, 400000, 500000, 600000, 700000, 725000]
data2_scores = [0.52958, 0.52633, 0.52648, 0.52656, 0.52639, 0.52631, 0.52623, 0.52630]

# lrelusigsig-lr0008 (Image 3)
data3_rows = [100000, 200000, 300000, 400000, 500000, 600000, 625000]
data3_scores = [0.52787, 0.52638, 0.52631, 0.52632, 0.52631, 0.52633, 0.52633]

# lrelusigsig-lr0005 (Image 4)
data4_rows = [100000, 200000, 300000, 400000, 500000, 600000, 650000]
data4_scores = [0.52548, 0.52636, 0.52634, 0.52633, 0.52633, 0.52635, 0.52632]

# lrelusigsig-lr0005 (Image 5)
data5_rows = [100000, 200000, 300000, 400000, 500000, 600000, 650000, 700000]
data5_scores = [0.52401, 0.52643, 0.52637, 0.52635, 0.52634, 0.52631, 0.52635, 0.52624]

# Create figure and axis
plt.figure(figsize=(9, 6))

# Plot each dataset
plt.plot(data1_rows, data1_scores, 'o-', color='#8884d8', linewidth=2, markersize=8, label='lrelulrelusig-lr0005')
plt.plot(data2_rows, data2_scores, 'o-', color='#82ca9d', linewidth=2, markersize=8, label='lrelusigsig-lr0001')
plt.plot(data3_rows, data3_scores, 'o-', color='#ff7300', linewidth=2, markersize=8, label='lrelusigsig-lr0008')
plt.plot(data4_rows, data4_scores, 'o-', color='#0088fe', linewidth=2, markersize=8, label='lrelusigsig-lr0005')
plt.plot(data5_rows, data5_scores, 'o-', color='#ff0000', linewidth=2, markersize=8, label='lrelusigsig-lr0005 (2)')

# Add legend
plt.legend(loc='best', fontsize=16)

# Add labels and title
plt.xlabel('Iteration', fontsize=16)
plt.ylabel('Ratio of v moves', fontsize=16)

# Customize x-axis ticks to show in thousands (k)
plt.xticks(np.arange(100000, 1000000, 100000), 
           [f'{int(x/1000)}k' for x in np.arange(100000, 1000000, 100000)])

# Adjust y-axis to match previous plot
# plt.ylim(2.21, 2.36)

# Add grid
plt.grid(True, linestyle='--', alpha=0.7)

# Add annotations for peak values
max_indices = [
    (np.argmax(data1_scores), data1_rows[np.argmax(data1_scores)], data1_scores[np.argmax(data1_scores)]),
    (np.argmax(data2_scores), data2_rows[np.argmax(data2_scores)], data2_scores[np.argmax(data2_scores)]),
    (np.argmax(data3_scores), data3_rows[np.argmax(data3_scores)], data3_scores[np.argmax(data3_scores)]),
    (np.argmax(data4_scores), data4_rows[np.argmax(data4_scores)], data4_scores[np.argmax(data4_scores)]),
    (np.argmax(data5_scores), data5_rows[np.argmax(data5_scores)], data5_scores[np.argmax(data5_scores)])
]

for _, row, score in max_indices:
    plt.annotate(f'{score:.4f}', 
                xy=(row, score),
                xytext=(0, 10),
                textcoords='offset points',
                ha='center',
                fontsize=14,
                bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.7))

# Improve layout
plt.tight_layout()

# Save the figure
plt.savefig('combined_v_ratio_plot.png', dpi=300, bbox_inches='tight')

# Show the plot
plt.show()
import matplotlib.pyplot as plt
import numpy as np

# Extract data from each graph
# lrelulrelusig-lr0005 (Image 1)
data1_rows = [100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000]
data1_scores = [0.36659, 0.47972, 0.4418, 0.42939, 0.45361, 0.46372, 0.44236, 0.44886, 0.449073]

# lrelusigsig-lr0001 (Image 2)
data2_rows = [100000, 200000, 300000, 400000, 500000, 600000, 700000, 725000]
data2_scores = [0.25535, 0.26486, 0.27911, 0.29728, 0.29555, 0.3075, 0.31297, 0.32146]

# lrelusigsig-lr0008 (Image 3)
data3_rows = [100000, 200000, 300000, 400000, 500000, 600000, 625000]
data3_scores = [0.31438, 0.42222, 0.44499, 0.46793, 0.46188, 0.45018, 0.450746]

# lrelusigsig-lr0005 (Image 4)
data4_rows = [100000, 200000, 300000, 400000, 500000, 600000, 650000]
data4_scores = [0.27542, 0.36673, 0.42486, 0.42949, 0.47212, 0.45726, 0.437515]

# lrelusigsig-lr0005 (Image 5)
data5_rows = [100000, 200000, 300000, 400000, 500000, 600000, 650000, 700000]
data5_scores = [0.29954, 0.36269, 0.42184, 0.41724, 0.44005, 0.40544, 0.40879, 0.38634]

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
plt.ylabel('Mean Gap Left', fontsize=16)

# Customize x-axis ticks to show in thousands (k)
plt.xticks(np.arange(100000, 1000000, 100000), 
           [f'{int(x/1000)}k' for x in np.arange(100000, 1000000, 100000)])

# Adjust y-axis to match previous plot
plt.ylim(0.2, 0.6)

# Add grid
plt.grid(True, linestyle='--', alpha=0.7)

# Add annotations for peak values
max_indices = [
    (np.argmin(data1_scores), data1_rows[np.argmin(data1_scores)], data1_scores[np.argmin(data1_scores)]),
    (np.argmin(data2_scores), data2_rows[np.argmin(data2_scores)], data2_scores[np.argmin(data2_scores)]),
    (np.argmin(data3_scores), data3_rows[np.argmin(data3_scores)], data3_scores[np.argmin(data3_scores)]),
    (np.argmin(data4_scores), data4_rows[np.argmin(data4_scores)], data4_scores[np.argmin(data4_scores)]),
    (np.argmin(data5_scores), data5_rows[np.argmin(data5_scores)], data5_scores[np.argmin(data5_scores)])
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
plt.savefig('combined_mean_gap_left_plot.png', dpi=300, bbox_inches='tight')

# Show the plot
plt.show()
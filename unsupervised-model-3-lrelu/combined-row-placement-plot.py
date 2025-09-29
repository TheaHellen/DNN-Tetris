import matplotlib.pyplot as plt
import numpy as np

# Extract data from each graph
# lrelulrelusig-lr0005 (Image 1)
data1_rows = [100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000]
data1_scores = [2.31459, 2.27885, 2.23093, 2.23837, 2.23796, 2.2468, 2.24409, 2.25842, 2.25675]

# lrelusigsig-lr0001 (Image 2)
data2_rows = [100000, 200000, 300000, 400000, 500000, 600000, 700000, 725000]
data2_scores = [2.31695, 2.30203, 2.30124, 2.31218, 2.28792, 2.27506, 2.26588, 2.26006]

# lrelusigsig-lr0008 (Image 3)
data3_rows = [100000, 200000, 300000, 400000, 500000, 600000, 625000]
data3_scores = [2.27197, 2.24189, 2.25291, 2.25147, 2.26679, 2.23292, 2.254609]

# lrelusigsig-lr0005 (Image 4)
data4_rows = [100000, 200000, 300000, 400000, 500000, 600000, 650000]
data4_scores = [2.34351, 2.26557, 2.24766, 2.24381, 2.27024, 2.26083, 2.26062]

# lrelusigsig-lr0005 (Image 5)
data5_rows = [100000, 200000, 300000, 400000, 500000, 600000, 650000, 700000]
data5_scores = [2.32254, 2.26724, 2.25009, 2.24491, 2.24575, 2.22095, 2.22581, 2.22064]


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
plt.ylabel('Mean Row Placement', fontsize=16)

# Customize x-axis ticks to show in thousands (k)
plt.xticks(np.arange(100000, 1000000, 100000), 
           [f'{int(x/1000)}k' for x in np.arange(100000, 1000000, 100000)])

# Adjust y-axis to match previous plot
plt.ylim(2.21, 2.36)

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
plt.savefig('combined_mean_row_placement_plot.png', dpi=300, bbox_inches='tight')

# Show the plot
plt.show()
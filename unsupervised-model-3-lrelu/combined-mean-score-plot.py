import matplotlib.pyplot as plt
import numpy as np

# Extract data from each graph
# lrelulrelusig-lr0005 (Image 1)
data1_rows = [100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000]
data1_scores = [0.5810, 0.9520, 1.6840, 1.4160, 1.3450, 1.7700, 1.1520, 1.4570, 0.8399]

# lrelusigsig-lr0001 (Image 2)
data2_rows = [100000, 200000, 300000, 400000, 500000, 600000, 700000, 725000]
data2_scores = [1.2630, 0.3170, 0.6490, 0.5890, 0.7450, 0.6730, 0.8310, 0.5709]

# lrelusigsig-lr0008 (Image 3)
data3_rows = [100000, 200000, 300000, 400000, 500000, 600000, 625000]
data3_scores = [0.7680, 1.3970, 1.3080, 1.1450, 1.2330, 1.4820, 1.0097]

# lrelusigsig-lr0005 (Image 4)
data4_rows = [100000, 200000, 300000, 400000, 500000, 600000, 650000]
data4_scores = [0.6800, 1.1560, 1.4430, 1.6440, 1.4120, 1.4680, 2.0957]

# lrelusigsig-lr0005 (Image 5)
data5_rows = [100000, 200000, 300000, 400000, 500000, 600000, 650000, 700000]
data5_scores = [0.5840, 1.0680, 1.0680, 1.2290, 1.3900, 2.2780, 1.9610, 1.5302]

# Create figure and axis
plt.figure(figsize=(12, 8))

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
plt.ylabel('Mean Score', fontsize=16)

# Customize x-axis ticks to show in thousands (k)
plt.xticks(np.arange(100000, 1000000, 100000), 
           [f'{int(x/1000)}k' for x in np.arange(100000, 1000000, 100000)])

# Adjust y-axis to match previous plot
plt.ylim(0, 2.4)

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
plt.savefig('combined_mean_score_plot.png', dpi=300, bbox_inches='tight')

# Show the plot
plt.show()
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import pandas as pd

# Parse the data
column_values = [0.0001, 0.0005, 0.0008, 0.0009, 0.001, 0.005, 0.008, 0.01]
row_values = [10, 20, 30, 40, 50]

# Create the grid data (replace 'n/c' with np.nan for visualization)
grid_data = [
    [140, 40, 23, 17, 17, 7, np.nan, np.nan],
    [105, 19, 10, 14, 11, 9, 15, 8],
    [63, 14, 11, 11, 8, 5, np.nan, np.nan],
    [44, 11, 9, 7, 9, 7, np.nan, np.nan],
    [40, 13, 9, 11, 9, 6, np.nan, np.nan]
]

# Convert to a pandas DataFrame for easier handling
df = pd.DataFrame(grid_data, index=row_values, columns=column_values)

# Create the figure with a grid layout
fig = plt.figure(figsize=(6, 5))
gs = GridSpec(2, 2, width_ratios=[1, 4], height_ratios=[1, 4], 
              left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.05, hspace=0.05)

# Define the axes
ax_top = fig.add_subplot(gs[0, 1])  # Top chart
ax_left = fig.add_subplot(gs[1, 0])  # Left chart
ax_table = fig.add_subplot(gs[1, 1])  # Table
ax_empty = fig.add_subplot(gs[0, 0])  # Empty corner

# Hide the empty corner axes
ax_empty.axis('off')

# Plot top chart (column values)
for idx, row in enumerate(row_values):
    valid_data = df.loc[row].dropna()
    ax_top.plot(valid_data.index, valid_data.values, marker='o', label=f'Row {row}')
ax_top.set_xticklabels([])
ax_top.set_ylabel('Loss Value')
ax_top.set_title("Grid Search Results", pad=20)
ax_top.legend(loc='upper right', bbox_to_anchor=(1.1, 1))

# Plot left chart (row values)
for idx, col in enumerate(column_values):
    valid_data = df[col].dropna()
    ax_left.plot(valid_data.values, valid_data.index, marker='o', label=f'Col {col}')
ax_left.set_yticklabels([])
ax_left.set_xlabel('Loss Value')
ax_left.invert_xaxis()  # Flip x-axis to match table orientation

# Create table visualization
ax_table.axis('tight')
ax_table.axis('off')

# Create cell colors based on values
cell_colors = np.zeros((len(row_values), len(column_values), 3))
for i in range(len(row_values)):
    for j in range(len(column_values)):
        value = grid_data[i][j]
        if not np.isnan(value):
            # Green (low values) to red (high values)
            normalized = min(value / 50, 1)  # Normalize to 0-1 range, capping at 1
            cell_colors[i, j, 0] = normalized  # Red
            cell_colors[i, j, 1] = 1 - normalized  # Green
            cell_colors[i, j, 2] = 0.2  # Blue

# Create table with formatted cell text
cell_text = [[str(val) if not np.isnan(val) else 'n/c' for val in row] for row in grid_data]
table = ax_table.table(cellText=cell_text, rowLabels=row_values, colLabels=column_values, 
                      cellColours=cell_colors, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.5)

# Set axis labels
fig.text(0.5, 0.02, 'Parameter 1', ha='center', fontsize=12)
fig.text(0.02, 0.5, 'Parameter 2', va='center', rotation='vertical', fontsize=12)

plt.show()

# If you want to save the figure
# plt.savefig('grid_search_results.png', dpi=300, bbox_inches='tight')

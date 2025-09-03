import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from collections import defaultdict
import matplotlib.cm as cm

# File path
file_path = 'log.csv'

# Calculate file size in GB
file_size_gb = os.path.getsize(file_path) / (1024**3)
print(f"Processing file: {file_path} ({file_size_gb:.2f} GB)")

# Define all possible move types
move_types = ["v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v0", 
              "h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9"]

# Initialize data structures
chunk_size = 100000  # Process in smaller chunks to manage memory
cumulative_losses = {move: [] for move in move_types}
move_occurrences = {move: 0 for move in move_types}
total_rows_processed = 0

# Create output directory for plots
output_dir = 'move_loss_analysis'
os.makedirs(output_dir, exist_ok=True)

# Process the file in chunks
print("Starting data processing...")
for chunk in pd.read_csv(file_path, chunksize=chunk_size):
    if 'move' not in chunk.columns or 'loss' not in chunk.columns:
        print("Error: Required columns 'move' or 'loss' not found in CSV file.")
        exit(1)
    
    # Group by move type and calculate sum of losses
    move_losses = chunk.groupby('move')['loss'].sum()
    move_counts = chunk.groupby('move').size()
    
    # Update cumulative losses for each move type
    for move in move_types:
        if move in move_losses:
            move_occurrences[move] += move_counts[move]
            
            # If this is the first occurrence of this move, initialize the list
            if not cumulative_losses[move] and move_occurrences[move] > 0:
                cumulative_losses[move].append(move_losses[move])
            # Otherwise, add to the cumulative sum
            elif move_occurrences[move] > 0:
                prev_loss = cumulative_losses[move][-1]
                cumulative_losses[move].append(prev_loss + move_losses[move])
    
    total_rows_processed += len(chunk)
    if total_rows_processed % 1000000 == 0:
        print(f"Processed {total_rows_processed:,} rows...")

print(f"Data processing complete. Processed {total_rows_processed:,} total rows.")

# Generate occurrence points for x-axis (to maintain proper scaling)
occurrence_points = {move: list(range(1, len(cumulative_losses[move]) + 1)) for move in move_types}

# Create individual plots for each move type
print("Generating individual plots...")
for move in move_types:
    if cumulative_losses[move]:  # Only create plots for moves that occur in the data
        plt.figure(figsize=(12, 8))
        
        # Determine color based on move type (v or h)
        color = 'blue' if move.startswith('v') else 'orange'
        
        plt.plot(occurrence_points[move], cumulative_losses[move], 
                 marker='.', linestyle='-', color=color, linewidth=2,
                 label=f'Cumulative Loss for {move}')
        
        plt.title(f'Cumulative Loss Progression for Move Type: {move}', fontsize=16)
        plt.xlabel('Number of Occurrences', fontsize=14)
        plt.ylabel('Cumulative Loss', fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.legend(fontsize=12)
        
        # Add annotations for start and end points
        if len(cumulative_losses[move]) > 0:
            start_val = cumulative_losses[move][0]
            end_val = cumulative_losses[move][-1]
            plt.annotate(f"Start: {start_val:.2f}", 
                         (1, start_val), 
                         textcoords="offset points", 
                         xytext=(5, 5), 
                         fontsize=12)
            plt.annotate(f"End: {end_val:.2f}", 
                         (len(cumulative_losses[move]), end_val), 
                         textcoords="offset points", 
                         xytext=(-40, 5), 
                         fontsize=12)
        
        plt.tight_layout()
        move_plot_path = os.path.join(output_dir, f'cumulative_loss_{move}.png')
        plt.savefig(move_plot_path, dpi=300)
        plt.close()

# Create a combined color-coded plot for all move types
print("Generating combined plot...")
plt.figure(figsize=(16, 10))

# Create color map: blues for v-moves, oranges for h-moves
v_moves = [move for move in move_types if move.startswith('v')]
h_moves = [move for move in move_types if move.startswith('h')]

# Get color maps
n_v_moves = len(v_moves)
n_h_moves = len(h_moves)
blues = cm.Blues(np.linspace(0.4, 1, n_v_moves))
oranges = cm.Oranges(np.linspace(0.4, 1, n_h_moves))

# Plot v-moves in blues
for i, move in enumerate(v_moves):
    if cumulative_losses[move]:
        plt.plot(occurrence_points[move], cumulative_losses[move], 
                 marker='.', linestyle='-', color=blues[i], linewidth=2,
                 label=f'{move} ({move_occurrences[move]:,} occurrences)')

# Plot h-moves in oranges
for i, move in enumerate(h_moves):
    if cumulative_losses[move]:
        plt.plot(occurrence_points[move], cumulative_losses[move], 
                 marker='.', linestyle='-', color=oranges[i], linewidth=2,
                 label=f'{move} ({move_occurrences[move]:,} occurrences)')

plt.title('Cumulative Loss Progression by Move Type', fontsize=18)
plt.xlabel('Number of Occurrences', fontsize=16)
plt.ylabel('Cumulative Loss', fontsize=16)
plt.grid(True, alpha=0.3)

# Create legend with two columns for better organization
plt.legend(fontsize=12, loc='upper left', ncol=2)

plt.tight_layout()
combined_plot_path = os.path.join(output_dir, 'combined_cumulative_loss.png')
plt.savefig(combined_plot_path, dpi=300)
plt.close()

# Create a normalized version where all curves start from 0
plt.figure(figsize=(16, 10))

# Plot normalized v-moves in blues
for i, move in enumerate(v_moves):
    if cumulative_losses[move]:
        # Normalize by subtracting the first value
        normalized_losses = [x - cumulative_losses[move][0] for x in cumulative_losses[move]]
        plt.plot(occurrence_points[move], normalized_losses, 
                 marker='.', linestyle='-', color=blues[i], linewidth=2,
                 label=f'{move} ({move_occurrences[move]:,} occurrences)')

# Plot normalized h-moves in oranges
for i, move in enumerate(h_moves):
    if cumulative_losses[move]:
        # Normalize by subtracting the first value
        normalized_losses = [x - cumulative_losses[move][0] for x in cumulative_losses[move]]
        plt.plot(occurrence_points[move], normalized_losses, 
                 marker='.', linestyle='-', color=oranges[i], linewidth=2,
                 label=f'{move} ({move_occurrences[move]:,} occurrences)')

plt.title('Normalized Cumulative Loss Progression by Move Type', fontsize=18)
plt.xlabel('Number of Occurrences', fontsize=16)
plt.ylabel('Normalized Cumulative Loss (starting at 0)', fontsize=16)
plt.grid(True, alpha=0.3)

# Create legend with two columns for better organization
plt.legend(fontsize=12, loc='upper left', ncol=2)

plt.tight_layout()
normalized_plot_path = os.path.join(output_dir, 'normalized_cumulative_loss.png')
plt.savefig(normalized_plot_path, dpi=300)
plt.close()

# Save summary statistics to CSV
print("Generating summary statistics...")
summary_data = []
for move in move_types:
    if cumulative_losses[move]:
        summary_data.append({
            'move': move,
            'occurrences': move_occurrences[move],
            'total_loss': cumulative_losses[move][-1],
            'avg_loss_per_move': cumulative_losses[move][-1] / move_occurrences[move],
            'first_recorded_loss': cumulative_losses[move][0],
            'last_recorded_loss': cumulative_losses[move][-1] - cumulative_losses[move][-2] if len(cumulative_losses[move]) > 1 else cumulative_losses[move][0]
        })

summary_df = pd.DataFrame(summary_data)
summary_df = summary_df.sort_values('avg_loss_per_move', ascending=False)
summary_csv_path = os.path.join(output_dir, 'move_loss_summary.csv')
summary_df.to_csv(summary_csv_path, index=False)

print(f"\nAnalysis complete! All results saved in '{output_dir}' directory.")
print(f"Generated {len([m for m in move_types if cumulative_losses[m]])} individual plots and 2 combined plots.")
print(f"Summary statistics saved to '{summary_csv_path}'")
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# File path
file_path = 'log-lrelulrelusig-lr0005.csv'

# Calculate file size in GB
file_size_gb = os.path.getsize(file_path) / (1024**3)
print(f"Processing file: {file_path} ({file_size_gb:.2f} GB)")

# Initialize variables
chunk_size = 100000  # Process in smaller chunks to manage memory
scores_mean = []
row_placement_mean = []
gap_left_mean = []
v_move_counts = []
row_markers = []
highest_scores = []

current_score_sum = 0
current_row_placement_sum = 0
current_gap_left_sum = 0
current_v_move_count = 0
current_count = 0
total_rows_processed = 0
current_highest_score = float('-inf')  # Initialize to negative infinity

# For tracking repeated moves
last_move = None
current_repeat_count = 0
repeat_counts = []
repeat_positions = []

# Create output directory for plots
output_dir = 'analysis_plots_lrelulrelusig-lr0005'
os.makedirs(output_dir, exist_ok=True)

# Process the file in chunks
for chunk in pd.read_csv(file_path, chunksize=chunk_size):
    required_columns = ['score', 'row placement', 'gap left', 'move']
    missing_columns = [col for col in required_columns if col not in chunk.columns]
    
    if missing_columns:
        print(f"Error: Missing columns in CSV file: {missing_columns}")
        exit(1)
    
    # Process each row for move repetition analysis
    for idx, row in chunk.iterrows():
        move = row['move']
        
        # Check for v moves
        if move.startswith('v'):
            current_v_move_count += 1
            
        # Track repeated moves
        if move == last_move:
            current_repeat_count += 1
        elif last_move is not None:
            if current_repeat_count > 0:
                repeat_counts.append(current_repeat_count)
                repeat_positions.append(total_rows_processed + idx)
            current_repeat_count = 0
        
        last_move = move
    
    # Add to running calculations
    current_score_sum += chunk['score'].sum()
    current_row_placement_sum += chunk['row placement'].sum()
    current_gap_left_sum += chunk['gap left'].sum()
    current_count += len(chunk)
    total_rows_processed += len(chunk)
    current_highest_score = max(current_highest_score, chunk['score'].max())
    
    # Calculate and store means every 5,000 rows
    if current_count >= 5000:
        # Calculate means
        mean_score = current_score_sum / current_count
        mean_row_placement = current_row_placement_sum / current_count
        mean_gap_left = current_gap_left_sum / current_count
        v_move_ratio = current_v_move_count / current_count
        
        # Store values
        scores_mean.append(mean_score)
        row_placement_mean.append(mean_row_placement)
        gap_left_mean.append(mean_gap_left)
        v_move_counts.append(v_move_ratio)
        row_markers.append(total_rows_processed)
        highest_scores.append(current_highest_score)
        
        print(f"Processed {total_rows_processed:,} rows:")
        print(f"  Mean score: {mean_score:.4f}")
        print(f"  Mean row placement: {mean_row_placement:.4f}")
        print(f"  Mean gap left: {mean_gap_left:.4f}")
        print(f"  V-move ratio: {v_move_ratio:.4f}")
        
        # Reset for next batch
        current_score_sum = 0
        current_row_placement_sum = 0
        current_gap_left_sum = 0
        current_v_move_count = 0
        current_count = 0
        current_highest_score = float('-inf')

# Check if there's a final repeat sequence at the end of the file
if current_repeat_count > 0:
    repeat_counts.append(current_repeat_count)
    repeat_positions.append(total_rows_processed)

# First create the combined dashboard view
plt.figure(figsize=(20, 15))

# Plot mean scores in combined view
plt.subplot(3, 2, 1)
plt.plot(row_markers, scores_mean, marker='o', linestyle='-')
plt.title('Mean Score Every 5,000 Rows')
plt.xlabel('Row Number')
plt.ylabel('Mean Score')
plt.grid(True)

# Plot mean row placements in combined view
plt.subplot(3, 2, 2)
plt.plot(row_markers, row_placement_mean, marker='o', linestyle='-', color='green')
plt.title('Mean Row Placement Every 5,000 Rows')
plt.xlabel('Row Number')
plt.ylabel('Mean Row Placement')
plt.grid(True)

# Plot mean gap left in combined view
plt.subplot(3, 2, 3)
plt.plot(row_markers, gap_left_mean, marker='o', linestyle='-', color='purple')
plt.title('Mean Gap Left Every 5,000 Rows')
plt.xlabel('Row Number')
plt.ylabel('Mean Gap Left')
plt.grid(True)

# Plot V-move ratio in combined view
plt.subplot(3, 2, 4)
plt.plot(row_markers, v_move_counts, marker='o', linestyle='-', color='orange')
plt.title('Ratio of V-Moves Every 5,000 Rows')
plt.xlabel('Row Number')
plt.ylabel('V-Move Ratio')
plt.grid(True)

# Plot repeated move counts in combined view
plt.subplot(3, 2, 5)
if repeat_counts:
    plt.scatter(repeat_positions, repeat_counts, color='red', alpha=0.7)
    plt.title('Repeated Move Counts')
    plt.xlabel('Row Position')
    plt.ylabel('Number of Repeats')
    plt.grid(True)
else:
    plt.text(0.5, 0.5, 'No repeated moves found', 
             horizontalalignment='center', verticalalignment='center')
    plt.title('Repeated Move Counts')

# Add a combined plot showing all means normalized
plt.subplot(3, 2, 6)
# Normalize the data for comparison
normalized_scores = [x/max(scores_mean) for x in scores_mean]
normalized_row_placement = [x/max(row_placement_mean) for x in row_placement_mean]
normalized_gap_left = [x/max(gap_left_mean) for x in gap_left_mean]
normalized_v_move = [x/max(v_move_counts) for x in v_move_counts]

plt.plot(row_markers, normalized_scores, marker='o', linestyle='-', label='Score')
plt.plot(row_markers, normalized_row_placement, marker='s', linestyle='-', label='Row Placement')
plt.plot(row_markers, normalized_gap_left, marker='^', linestyle='-', label='Gap Left')
plt.plot(row_markers, normalized_v_move, marker='d', linestyle='-', label='V-Move Ratio')
plt.title('Normalized Metrics Comparison')
plt.xlabel('Row Number')
plt.ylabel('Normalized Value')
plt.legend()
plt.grid(True)

plt.tight_layout()

# Save the combined dashboard plot
combined_plot_path = os.path.join(output_dir, 'combined_metrics_dashboard.png')
plt.savefig(combined_plot_path, dpi=300)
print(f"Combined dashboard saved as '{combined_plot_path}'")
plt.close()

# Now create individual, larger plots for each metric

# 1. Mean Score Plot
plt.figure(figsize=(12, 8))
plt.plot(row_markers, scores_mean, marker='o', linestyle='-', color='blue', linewidth=2)
plt.title('Mean Score Every 5,000 Rows', fontsize=16)
plt.xlabel('Row Number', fontsize=14)
plt.ylabel('Mean Score', fontsize=14)
plt.grid(True)
# Add data point annotations
for i, (x, y) in enumerate(zip(row_markers, scores_mean)):
    plt.annotate(f"{y:.4f}", (x, y), textcoords="offset points", 
                 xytext=(0,10), ha='center', fontsize=12)
plt.tight_layout()
score_plot_path = os.path.join(output_dir, 'mean_score_plot.png')
plt.savefig(score_plot_path, dpi=300)
print(f"Mean score plot saved as '{score_plot_path}'")
plt.close()

# 2. Mean Row Placement Plot
plt.figure(figsize=(12, 8))
plt.plot(row_markers, row_placement_mean, marker='o', linestyle='-', color='green', linewidth=2)
plt.title('Mean Row Placement Every 5,000 Rows', fontsize=16)
plt.xlabel('Row Number', fontsize=14)
plt.ylabel('Mean Row Placement', fontsize=14)
plt.grid(True)
# Add data point annotations
for i, (x, y) in enumerate(zip(row_markers, row_placement_mean)):
    plt.annotate(f"{y:.4f}", (x, y), textcoords="offset points", 
                 xytext=(0,10), ha='center', fontsize=12)
plt.tight_layout()
row_plot_path = os.path.join(output_dir, 'mean_row_placement_plot.png')
plt.savefig(row_plot_path, dpi=300)
print(f"Mean row placement plot saved as '{row_plot_path}'")
plt.close()

# 3. Mean Gap Left Plot
plt.figure(figsize=(12, 8))
plt.plot(row_markers, gap_left_mean, marker='o', linestyle='-', color='purple', linewidth=2)
plt.title('Mean Gap Left Every 5,000 Rows', fontsize=16)
plt.xlabel('Row Number', fontsize=14)
plt.ylabel('Mean Gap Left', fontsize=14)
plt.grid(True)
# Add data point annotations
for i, (x, y) in enumerate(zip(row_markers, gap_left_mean)):
    plt.annotate(f"{y:.4f}", (x, y), textcoords="offset points", 
                 xytext=(0,10), ha='center', fontsize=12)
plt.tight_layout()
gap_plot_path = os.path.join(output_dir, 'mean_gap_left_plot.png')
plt.savefig(gap_plot_path, dpi=300)
print(f"Mean gap left plot saved as '{gap_plot_path}'")
plt.close()

# 4. V-Move Ratio Plot
plt.figure(figsize=(12, 8))
plt.plot(row_markers, v_move_counts, marker='o', linestyle='-', color='orange', linewidth=2)
plt.title('Ratio of V-Moves Every 5,000 Rows', fontsize=16)
plt.xlabel('Row Number', fontsize=14)
plt.ylabel('V-Move Ratio', fontsize=14)
plt.grid(True)
# Add data point annotations
for i, (x, y) in enumerate(zip(row_markers, v_move_counts)):
    plt.annotate(f"{y:.4f}", (x, y), textcoords="offset points", 
                 xytext=(0,10), ha='center', fontsize=12)
plt.tight_layout()
vmove_plot_path = os.path.join(output_dir, 'v_move_ratio_plot.png')
plt.savefig(vmove_plot_path, dpi=300)
print(f"V-move ratio plot saved as '{vmove_plot_path}'")
plt.close()

# 5. Repeated Moves Plot
plt.figure(figsize=(12, 8))
if repeat_counts:
    plt.scatter(repeat_positions, repeat_counts, color='red', alpha=0.7, s=50)
    plt.title('Repeated Move Counts', fontsize=16)
    plt.xlabel('Row Position', fontsize=14)
    plt.ylabel('Number of Repeats', fontsize=14)
    # Add a trend line if there are enough points
    if len(repeat_counts) > 2:
        z = np.polyfit(repeat_positions, repeat_counts, 1)
        p = np.poly1d(z)
        plt.plot(repeat_positions, p(repeat_positions), "r--", alpha=0.5, 
                 label=f"Trend: y={z[0]:.6f}x+{z[1]:.2f}")
        plt.legend()
    plt.grid(True)
else:
    plt.text(0.5, 0.5, 'No repeated moves found', 
             horizontalalignment='center', verticalalignment='center', fontsize=16)
    plt.title('Repeated Move Counts', fontsize=16)
plt.tight_layout()
repeat_plot_path = os.path.join(output_dir, 'repeated_moves_plot.png')
plt.savefig(repeat_plot_path, dpi=300)
print(f"Repeated moves plot saved as '{repeat_plot_path}'")
plt.close()

# 6. Normalized Comparison Plot
plt.figure(figsize=(14, 10))
plt.plot(row_markers, normalized_scores, marker='o', markersize=8, linestyle='-', linewidth=2.5, label='Score')
plt.plot(row_markers, normalized_row_placement, marker='s', markersize=8, linestyle='-', linewidth=2.5, label='Row Placement')
plt.plot(row_markers, normalized_gap_left, marker='^', markersize=8, linestyle='-', linewidth=2.5, label='Gap Left')
plt.plot(row_markers, normalized_v_move, marker='d', markersize=8, linestyle='-', linewidth=2.5, label='V-Move Ratio')
plt.title('Normalized Metrics Comparison', fontsize=18)
plt.xlabel('Row Number', fontsize=16)
plt.ylabel('Normalized Value', fontsize=16)
plt.legend(fontsize=14)
plt.grid(True)
plt.tight_layout()
norm_plot_path = os.path.join(output_dir, 'normalized_comparison_plot.png')
plt.savefig(norm_plot_path, dpi=300)
print(f"Normalized comparison plot saved as '{norm_plot_path}'")
plt.close()

# Plot highest scores
plt.figure(figsize=(12, 8))
plt.plot(row_markers, highest_scores, marker='o', linestyle='-', color='red', linewidth=2)
plt.title('Highest Score Every 5,000 Rows', fontsize=16)
plt.xlabel('Row Number', fontsize=14)
plt.ylabel('Highest Score', fontsize=14)
plt.grid(True)
# Add data point annotations
for i, (x, y) in enumerate(zip(row_markers, highest_scores)):
    plt.annotate(f"{y:.4f}", (x, y), textcoords="offset points", 
                 xytext=(0,10), ha='center', fontsize=12)
plt.tight_layout()
highest_score_plot_path = os.path.join(output_dir, 'highest_score_plot.png')
plt.savefig(highest_score_plot_path, dpi=300)
print(f"Highest score plot saved as '{highest_score_plot_path}'")
plt.close()

# Save results to CSV
results_df = pd.DataFrame({
    'row_position': row_markers,
    'mean_score': scores_mean,
    'mean_row_placement': row_placement_mean,
    'mean_gap_left': gap_left_mean,
    'v_move_ratio': v_move_counts
})
results_csv_path = os.path.join(output_dir, 'metric_summaries.csv')
results_df.to_csv(results_csv_path, index=False)
print(f"Summary data saved to '{results_csv_path}'")

# Save repeated move data
if repeat_counts:
    repeats_df = pd.DataFrame({
        'position': repeat_positions,
        'repeat_count': repeat_counts
    })
    repeats_csv_path = os.path.join(output_dir, 'repeated_moves.csv')
    repeats_df.to_csv(repeats_csv_path, index=False)
    print(f"Repeated move data saved to '{repeats_csv_path}'")

print(f"\nAll analysis complete. Results saved in '{output_dir}' directory.")
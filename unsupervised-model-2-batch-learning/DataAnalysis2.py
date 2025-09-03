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
chunk_size = 1  # Process in smaller chunks to manage memory
total_rows_processed = int(0)
# Create a matrix of size 1x19 which can be extended for each row to store the cumulative loss
cumulative_loss = np.zeros((1, 19))

# Create output directory for plots
output_dir = 'move_loss_analysis'
os.makedirs(output_dir, exist_ok=True)

# Process the file in chunks
print("Starting data processing...")
for chunk in pd.read_csv(file_path, chunksize=chunk_size):
    if 'move' not in chunk.columns or 'loss' not in chunk.columns:
        print("Error: Required columns 'move' or 'loss' not found in CSV file.")
        exit(1)

    if total_rows_processed == 0:
        print(chunk['move'].values[0])
        index = move_types.index(chunk['move'].values[0])
        loss = float(chunk['loss'].iloc[0])
        cumulative_loss[int(total_rows_processed), int(index)] = loss
        total_rows_processed += 1

    else:
        index = move_types.index(chunk['move'].values[0])
        loss = float(chunk['loss'].iloc[0])
        cumulative_loss = np.vstack([cumulative_loss, cumulative_loss[int(total_rows_processed) - 1, :]])
        cumulative_loss[int(total_rows_processed), int(index)] = cumulative_loss[int(total_rows_processed) , int(index)] + loss
        total_rows_processed += 1

    if total_rows_processed % 10000 == 0:
        print(f"Processed {total_rows_processed:,} rows...")

# Plot the cumulative loss for each move type
print("Plotting cumulative loss for each move type...")
plt.figure(figsize=(12, 8))
for i in range(19):
    plt.plot(cumulative_loss[:, i], label=move_types[i])
plt.xlabel('Time')
plt.ylabel('Cumulative Loss')
plt.title('Cumulative Loss for each Move Type')
plt.legend()
plt.grid()
plt.savefig(f'{output_dir}/cumulative_loss.png')
plt.show()



    

    
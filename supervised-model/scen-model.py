import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import LeakyReLU
import numpy as np
import csv

# Create the model
model = keras.models.Sequential()
model.add(keras.Input(shape=(2, 10)))
model.add(keras.layers.Flatten())
model.add(keras.layers.Dense(30, kernel_initializer='he_normal', 
                                    activation=keras.layers.LeakyReLU(negative_slope=0.01), use_bias=False))
model.add(keras.layers.Dense(30, kernel_initializer='he_normal', 
                                    activation=keras.layers.LeakyReLU(negative_slope=0.01), use_bias=False))
model.add(keras.layers.Dense(30, kernel_initializer='he_normal', 
                                    activation=keras.layers.LeakyReLU(negative_slope=0.01), use_bias=False))
model.add(keras.layers.Dense(19, activation="softmax", 
                                    use_bias=False))
optimizer = keras.optimizers.Adam(learning_rate=0.0008)

# Allocate the moves
moves = ["v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v0", 
         "h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9"]

# Create the scenarios
def scenario(num): # num can take values 1 to 19
    # Create the grid
    grid = np.zeros((2, 10))

    if num <= 10:
        for i in range(10):
            grid[1, i] = 1
            grid[0, i] = 1
        grid[1, num-1] = 0
        grid[0, num-1] = 0
    else:
        for i in range(10):
            grid[1, i] = 1
        grid[1, num-11] = 0
        grid[1, num-10] = 0
    return grid

# Start the count
move_no = 0

# Play the game
while True:
    # Update the count
    move_no += 1
    print(move_no)

    # Pick a random scenario
    scenario_no = np.random.randint(1, 20)
    grid = scenario(scenario_no)

    # Convert input to tensor
    grid = tf.convert_to_tensor(grid, dtype=tf.float32)
    grid = tf.expand_dims(grid, axis=0)

    with tf.GradientTape() as tape:
        # Make a move
        probabilities = model(grid, training=True)

        move_index = tf.argmax(probabilities, axis=1)
        move_probability = tf.reduce_max(probabilities, axis=1)

        # Convert scenario_no-1 to tensor and expand dimensions
        scenario_no_tensor = tf.convert_to_tensor([scenario_no-1], dtype=tf.int64)

        # Get the loss
        loss = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=scenario_no_tensor, logits=probabilities)


    # Calculate the gradients
    grads = tape.gradient(loss, model.trainable_weights)

    # Update the model
    optimizer.apply_gradients(zip(grads, model.trainable_weights))

    # Save the model
    model.save("model-lrelux3-30n-lr0008.keras")

    # Save to csv
    filename = "log-lrelux3-30n-lr0008.csv"
    file_exists = False
    try:
        with open(filename, 'r'):
            file_exists = True
    except FileNotFoundError:
        pass
    
    if not file_exists:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['probability', 'move', 'scenario_no', 'loss', 'move_no'])
    
    row = [move_probability.numpy(), moves[int(move_index)], scenario_no, loss.numpy(), move_no]
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)





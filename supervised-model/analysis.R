library(randomcoloR)
library(ggplot2)
library(dplyr)

data = read.csv("log-lrelux3-30n-lr001.csv") # Load your dataset
n = length(data$probability)

# Mutate the data in the "move" column
data <- data %>%
  mutate(transformed_move = case_when(
    grepl("^h", move) ~ as.numeric(substring(move, 2)) + 10,
    grepl("^v0", move) ~ 10,
    grepl("^v", move) ~ as.numeric(substring(move, 2)),
    TRUE ~ as.numeric(move)  # Handle any other cases
  ))

# Find rows where the AI plays the wrong move using the transformed move
mismatch_rows <- which(data$transformed_move == data$scenario_no)
print(tail(mismatch_rows))

# Define batch size
batch_size <- 1000  # Define batch size
num_batches <- nrow(data) %/% batch_size  # Number of full batches

# Compute percentages for each batch
percentages <- data %>%
  mutate(batch = rep(1:num_batches, each = batch_size, length.out = nrow(data))) %>%
  group_by(batch) %>%
  summarise(match_percent = mean(transformed_move == scenario_no) * 100)

# Plot the percentages
ggplot(percentages, aes(x = batch, y = match_percent)) +
  geom_line() +
  geom_point() +
  ylim(0, 100) +
  labs(x = "Batch Number",
       y = "Percentage Match") +
  theme_bw()

ggsave(filename = "scen1-lrelulrelulrelu-001.png", plot = last_plot(), width = 6, height = 4.5, dpi = 300)

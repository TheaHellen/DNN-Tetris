library(randomcoloR)
library(ggplot2)
library(dplyr)

lr = c(0.001, 0.0005, 0.0008, 0.0009)
lr_orig = lr  # Save original values for labeling
lr = log(lr, base = 10)
conv = c(83, 51, 31, 29)
conv = log(conv, base = 10)
col = c("red", "black", "black", "red")
stability = c("Unstable", "Stable", "Stable", "Unstable")  # For legend

# Create a data frame for the plot
data <- data.frame(
  lr = lr,
  lr_orig = lr_orig,
  conv = conv,
  col = col,
  stability = stability
)

# Another alternative - using as.character directly
data$label[1] <- paste0("eta==0.001")
data$label[2] <- paste0("eta==0.0005")
data$label[3] <- paste0("eta==0.0008")
data$label[4] <- paste0("eta==0.0009")

# Create a subset for the first three points for curve fitting
first_three <- data[2:4, ]

# Fit a curve to the first three points
curve_model <- lm(conv ~ poly(lr, 2), data = first_three)

# Create a sequence of points for curve prediction
curve_data <- data.frame(
  lr = seq(min(first_three$lr), max(first_three$lr), length.out = 100)
)
curve_data$conv <- predict(curve_model, newdata = curve_data)

# Create the plot
options(scipen = 999)
ggplot(data, aes(x = lr, y = conv)) +
  # Add the fitted curve for the first three points
  geom_line(data = curve_data, aes(x = lr, y = conv), 
            color = "blue", linetype = "dashed", size = 0.5) +
  # Add points with color based on stability
  geom_point(aes(color = stability), size = 2) +
  # Add learning rate labels
  geom_text(aes(label = label), 
            vjust = 0.3, hjust = -0.2, size = 3.5, parse = TRUE) +
  # Set colors manually
  scale_color_manual(values = c("black", "red"), 
                     name = "Stability") +
  # Set x and y axis limits
  xlim(-3.31, -2.93) +
  ylim(1.45, 1.95) +
  # Add labels
  labs(x = "Log(Learning Rate)",
       y = "Log(Convergence)") +
  theme_bw() +
  theme(legend.position = "right")

# Save the plot
ggsave(filename = "lr-convergence.png", plot = last_plot(), width = 6, height = 4, dpi = 300)
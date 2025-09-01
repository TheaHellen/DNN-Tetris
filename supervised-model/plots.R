library(randomcoloR)
library(ggplot2)
data = read.csv("log1.csv")
data$loss <- gsub("\\[|\\]", "", data$loss)
data$loss = as.numeric(data$loss)
data$probability <- gsub("\\[|\\]", "", data$probability)
data$probability = as.numeric(data$probability)

n = length(data$probability)

moves = unique(data$move)
colors <- distinctColorPalette(length(moves))
names(colors) <- moves

ggplot(data, aes(x=move_no, y=loss, color=move))+
  geom_point(size=1)+
  theme_minimal()+
  labs(x="Move Number", y="Loss")+
  theme(
    text = element_text(size = 16),  # Increase all text size
    axis.title = element_text(size = 18),  # Increase axis titles
    axis.text = element_text(size = 14),  # Increase axis labels
    legend.title = element_text(size = 16),  # Increase legend title size
    legend.text = element_text(size = 14)  # Increase legend text size
  )

ggsave(filename = "lr01-noconvergence-loss.png", plot = last_plot(), width = 6, height = 4.5, dpi = 300)

ggplot(data, aes(x=move_no, y=probability, color=move))+
  geom_point(size=1)+
  theme_minimal()+
  labs(x="Move Number", y="Probability")+
  theme(
    text = element_text(size = 16),  # Increase all text size
    axis.title = element_text(size = 18),  # Increase axis titles
    axis.text = element_text(size = 14),  # Increase axis labels
    legend.title = element_text(size = 16),  # Increase legend title size
    legend.text = element_text(size = 14)  # Increase legend text size
  )

ggsave(filename = "lr01-noconvergence-prob.png", plot = last_plot(), width = 6, height = 4.5, dpi = 300)



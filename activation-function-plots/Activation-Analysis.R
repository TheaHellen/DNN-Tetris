library(ggplot2)
library(dplyr)

ss = read.csv("log-ss.csv")
st = read.csv("log-st.csv")
tt = read.csv("log-tt.csv")

# Truncate to same number of observations
no.obs = nrow(ss)
st = st[1:no.obs, ]
tt = tt[1:no.obs, ]

# Game Duration
count.game.duration = function(data){
  data %>%
    group_by(game.no.) %>%
    summarise(moves = n()) %>%
    mutate(game = row_number())
}

ss.moves = count.game.duration(ss)
st.moves = count.game.duration(st)
tt.moves = count.game.duration(tt)

# Plot game durations
ggplot(ss.moves, aes(x = game, y = moves)) +
  geom_line() +
  labs(x = "Game Number", y = "Number of Moves") +
  ylim(2, 12) + xlim(0, 5000) +
  theme_minimal() +
  theme(text = element_text(size = 16))

ggplot(st.moves, aes(x = game, y = moves)) +
  geom_line() +
  labs(x = "Game Number", y = "Number of Moves") +
  ylim(2, 12) + xlim(0, 5000) +
  theme_minimal() +
  theme(text = element_text(size = 16))

ggplot(tt.moves, aes(x = game, y = moves)) +
  geom_line() +
  labs(x = "Game Number", y = "Number of Moves") +
  ylim(2, 12) + xlim(0, 5000) +
  theme_minimal() +
  theme(text = element_text(size = 16))

# Ratio vertical:horizontal
count.ratio = function(data){
  data %>%
    mutate(type = substr(move, 1, 1)) %>%
    group_by(game.no.) %>%
    summarise(
      v = sum(type == "v"),
      total = n()
    ) %>%
    mutate(ratio = v / total, game = row_number())
}

ss.ratio = count.ratio(ss)
st.ratio = count.ratio(st)
tt.ratio = count.ratio(tt)

cor.ss = cor.test(ss.ratio$game.no., ss.ratio$ratio, alternative = 'greater', 
                  method = 'pearson')
cor.st = cor.test(st.ratio$game.no., st.ratio$ratio, alternative = 'greater', 
                  method = 'pearson')
cor.tt = cor.test(tt.ratio$game.no., tt.ratio$ratio, alternative = 'greater', 
                  method = 'pearson')

cor.ss2 = cor.test(ss.ratio$game.no., ss.ratio$ratio, alternative = 'greater', 
                  method = 'spearman')
cor.st2 = cor.test(st.ratio$game.no., st.ratio$ratio, alternative = 'greater', 
                  method = 'spearman')
cor.tt2 = cor.test(tt.ratio$game.no., tt.ratio$ratio, alternative = 'greater', 
                  method = 'spearman')

# Plot ratios
ggplot(ss.ratio, aes(x = game, y = ratio)) +
  geom_line() +
  labs(x = "Game Number", y = "Ratio v/total") +
  ylim(0, 1) + xlim(0, 5000) +
  theme_minimal() +
  theme(text = element_text(size = 16))

ggplot(st.ratio, aes(x = game, y = ratio)) +
  geom_line() +
  labs(x = "Game Number", y = "Ratio v/total") +
  ylim(0, 1) + xlim(0, 5000) +
  theme_minimal() +
  theme(text = element_text(size = 16))

ggplot(tt.ratio, aes(x = game, y = ratio)) +
  geom_line() +
  labs(x = "Game Number", y = "Ratio v/total") +
  ylim(0, 1) + xlim(0, 5000) +
  theme_minimal() +
  theme(text = element_text(size = 16))



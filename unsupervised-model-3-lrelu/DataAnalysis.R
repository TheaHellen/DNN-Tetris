data = read.csv("log.csv")

#Calculate the average score over every (39,500-40,000) moves
obs = length(data[,1])
ind = 40000
iter = floor(obs/ind)
av.score = 0
var.score = 0
for (i in 1:iter){
  av.score[i] = mean(data$score[(i*ind-500):(i*ind)]) #mean
  var.score[i] = var(data$score[(i*ind-500):(i*ind)]) #variance
}

#Calculate the v-h ratio and no. gaps over every (39,500-40,000) moves
av.ratio = 0
gaps = 0
for (i in 1:iter){
  v = 0
  g = 0
  for (j in (i*ind-500):(i*ind)){
    if (substr(data$move[j], 1, 1) == "v"){
      v = v+1
    }
    g = g + data$gap.left[j]
  }
  av.ratio[i] = v/500
  gaps[i] = g
}

plot(seq(1,iter,1), av.score, xlab="40,000 interval no.", 
     ylab="average score", main="average score over 500 moves every 40,000 moves")

plot(seq(1,iter,1), av.ratio, xlab="40,000 interval no.", 
     ylab="v/total ratio", main="ratio of v moves over 500 moves every 40,000 moves")

plot(seq(1,iter,1), gaps, xlab="40,000 interval no.", 
     ylab="total number of gaps left", 
     main="number of gaps left over 500 moves every 40,000 moves")
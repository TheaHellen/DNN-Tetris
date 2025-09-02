data = read.csv("log.csv")

convert_string_to_matrix <- function(input_string, nrow, ncol) {
  clean_string <- gsub("\n", " ", input_string)
  clean_string <- gsub("\\(", " ", clean_string)
  clean_string <- gsub("\\)", " ", clean_string)
  clean_string <- gsub("\\[", " ", clean_string)
  clean_string <- gsub("\\]", " ", clean_string)
  clean_string <- gsub("array", " ", clean_string)
  clean_string <- gsub("dtype=float32", " ", clean_string)
  clean_string <- gsub("\\,", " ", clean_string)
  clean_string <- gsub("\\s+", " ", clean_string)
  clean_string <- sub("^\\s+", "", clean_string)
  print(clean_string)
  number_vector <- as.numeric(strsplit(clean_string, " ")[[1]])
  matrix_result <- matrix(number_vector, nrow = nrow, ncol = ncol, byrow = TRUE)
  
  return(matrix_result)
}

convert_gridstring_to_vector = function(str){
  clean_str <- gsub("\\[|\\]", "", str)
  clean_str <- gsub("\\.", "", clean_str)
  number_vector <- as.numeric(strsplit(clean_str, " ")[[1]])
  
  return(number_vector)
}

softmax = function(z){
  n = length(z)
  v = matrix(NA, 1, n)
  for (i in 1:n){
    v[i] = exp(z[i])/sum(exp(z))
  }
  return(v)
}

#Check the forward pass is correct
weights.01 = convert_string_to_matrix(data$weights.layer.1[2], 20, 2)
weights.02 = convert_string_to_matrix(data$weights.layer.2[2], 2, 2)
weights.03 = convert_string_to_matrix(data$weights.layer.3[2], 2, 19)

grid = convert_gridstring_to_vector(data$grid[2])
layer1 = grid%*%weights.01
layer1 = pmax(0, layer1)
layer2 = layer1%*%weights.02
layer2 = 1/(1+exp(-layer2))
layer3 = layer2%*%weights.03
output.probs = softmax(layer3)
action.index = which.max(output.probs)
actions = c("h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9", 
            "v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v0")
action = actions[action.index]

#Then we know the loss
loss = data$loss[2]

weights3.01 = convert_string_to_matrix(data$weights.layer.1[3], 20, 2)
weights3.02 = convert_string_to_matrix(data$weights.layer.2[3], 2, 2)
weights3.03 = convert_string_to_matrix(data$weights.layer.3[3], 2, 19)

which(weights3.01 != weights.01)
which(weights3.02 != weights.02)
which(weights3.03 != weights.03)



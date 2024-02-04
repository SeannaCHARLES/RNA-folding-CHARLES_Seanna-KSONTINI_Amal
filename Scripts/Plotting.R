library(ggplot2)
library(dplyr)

plot_interaction_profiles <- function(csv_path, output_folder) {
  df <- read.csv(csv_path, header = TRUE, stringsAsFactors = FALSE)
  
  colnames(df) <- make.names(colnames(df))
  
  if (!dir.exists(output_folder)) {
    dir.create(output_folder)
  }
  
  p_all_pairs <- ggplot()
  
  for (pair in unique(df$Nucleotide.pairs)) {
    scores <- suppressWarnings(as.numeric(df[df$Nucleotide.pairs == pair, -1]))
    scores <- na.omit(scores)
    distances <- seq_along(scores)
    data_to_plot <- data.frame(distances = distances, scores = scores, pair = rep(pair, length(scores)))
    p_pair <- ggplot(data_to_plot, aes(x = distances, y = scores, color = pair)) +
      geom_line() +
      labs(x = "Distance", y = "Score", title = paste("Interaction Profile for", pair)) +
      theme_minimal() +
      theme(legend.position = "top")

    output_path <- file.path(output_folder, paste("interaction_profile_", gsub("/", "_", pair), ".png", sep = ""))
    ggsave(filename = output_path, plot = p_pair, width = 8, height = 4)
    
    p_all_pairs <- p_all_pairs + geom_line(data = data_to_plot, aes(x = distances, y = scores, color = pair))
    
    print(p_pair)
  }
  
  p_all_pairs <- p_all_pairs +
    labs(x = "Distance", y = "Score", title = "Interaction Profiles for All Pairs") +
    theme_minimal() +
    theme(legend.position = "top")
  
  output_path_all_pairs <- file.path(output_folder, "interaction_profiles_all_pairs.png")
  ggsave(filename = output_path_all_pairs, plot = p_all_pairs, width = 8, height = 4)
  
  print(p_all_pairs)
}

csv_path <- "Results/Final_res_train.csv"
output_folder <- "Results"
plot_interaction_profiles(csv_path, output_folder)

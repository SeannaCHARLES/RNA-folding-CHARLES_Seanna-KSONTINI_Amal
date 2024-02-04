library(ggplot2)
library(dplyr)

plot_interaction_profiles <- function(csv_path, output_folder) {
  # Read CSV file into a data frame
  df <- read.csv(csv_path, header = TRUE, stringsAsFactors = FALSE)
  
  # Remove spaces from column names for easier handling
  colnames(df) <- make.names(colnames(df))
  
  # Create output folder if it doesn't exist
  if (!dir.exists(output_folder)) {
    dir.create(output_folder)
  }
  
  # Create an empty ggplot object for all pairs
  p_all_pairs <- ggplot()
  
  # Add lines for each base pair
  for (pair in unique(df$Nucleotide.pairs)) {
    scores <- suppressWarnings(as.numeric(df[df$Nucleotide.pairs == pair, -1]))
    
    # Handle missing values
    scores <- na.omit(scores)
    
    # Ensure distances and scores have the same length
    distances <- seq_along(scores)
    
    # Create a data frame for ggplot
    data_to_plot <- data.frame(distances = distances, scores = scores, pair = rep(pair, length(scores)))
    
    # Create a ggplot object for each pair
    p_pair <- ggplot(data_to_plot, aes(x = distances, y = scores, color = pair)) +
      geom_line() +
      labs(x = "Distance", y = "Score", title = paste("Interaction Profile for", pair)) +
      theme_minimal() +
      theme(legend.position = "top")
    
    # Save the individual plot as a PNG file
    output_path <- file.path(output_folder, paste("interaction_profile_", gsub("/", "_", pair), ".png", sep = ""))
    ggsave(filename = output_path, plot = p_pair, width = 8, height = 4)
    
    # Add lines for the current pair to the plot aggregating all pairs
    p_all_pairs <- p_all_pairs + geom_line(data = data_to_plot, aes(x = distances, y = scores, color = pair))
    
    # Display the individual plot
    print(p_pair)
  }
  
  # Customize the plot for all pairs
  p_all_pairs <- p_all_pairs +
    labs(x = "Distance", y = "Score", title = "Interaction Profiles for All Pairs") +
    theme_minimal() +
    theme(legend.position = "top")
  
  # Save the plot for all pairs as a PNG file
  output_path_all_pairs <- file.path(output_folder, "interaction_profiles_all_pairs.png")
  ggsave(filename = output_path_all_pairs, plot = p_all_pairs, width = 8, height = 4)
  
  # Display the plot for all pairs
  print(p_all_pairs)
}

# Example usage
csv_path <- "Results/Final_res_train.csv"
output_folder <- "Results"
plot_interaction_profiles(csv_path, output_folder)

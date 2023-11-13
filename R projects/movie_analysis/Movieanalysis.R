rm(list=ls())
library(tidyverse)
library(lubridate)
library(dplyr)
library(ggplot2)  # For plotting
library(stringr) 
# Load the CSV file
movie_data <- read.csv("D:\\R prg\\movie_databas.csv")
# Function to display the main menu
show_menu <- function() {
  cat("Movie Database Analysis Menu:\n")
  cat("1.  Add Movie Data\n")
  cat("2.  Search Movies\n")
  cat("3.  Sort Movies\n")
  cat("4.  Highest Rated Movies\n")
  cat("5.  Genre Trend Analysis\n")
  cat("6.  Year-wise Genre Analysis\n")
  cat("7.  Language Analysis\n")
  cat("8.  Country Analysis\n")
  cat("9.  Delete Movie\n")
  cat("10. Exit\n")
}
# Function to add movie data
add_movie_data <- function(data) {
  cat("Enter movie details:\n")
  
  # Prompt the user for movie details
  cat("Enter movie name: ")
  movie_name <- readline()
  
  # Duplicate check
  if (movie_name %in% data$movienames) {
    cat("Movie name already exists in the database. Skipping data entry.\n")
    return(data)
  }
  
  cat("Enter release date (dd-mm-yyyy): ")
  release_date <- readline()
  
  cat("Enter movie score: ")
  movie_score <- as.numeric(readline())
  
  cat("Enter movie genre: ")
  movie_genre <- readline()
  
  cat("Enter original language: ")
  orig_language <- readline()
  
  cat("Enter budget (in Rupees): ")
  movie_budget <- as.numeric(readline())
  
  cat("Enter the number of days the movie is running: ")
  num_days_running <- as.numeric(readline())
  
  cat("Enter the average collection per day (in Rupees): ")
  avg_collection_per_day <- as.numeric(readline())
  
  cat("Enter the number of theaters the movie is released in: ")
  num_theaters <- as.numeric(readline())
  
  # Calculate revenue
  movie_revenue <- num_days_running * avg_collection_per_day * num_theaters
  cat("Enter country: ")
  movie_country <- readline()
  
  # Create a new data frame with the entered data
  new_movie <- data.frame(
    movienames = movie_name,
    date_x = release_date,
    score = movie_score,
    genre = movie_genre,
    orig_lang = orig_language,
    budget_x = movie_budget,
    revenue = movie_revenue,
    country = movie_country
  )
  
  # Add the new movie data to the existing data
  updated_data <- bind_rows(data, new_movie)
  
  # Save the updated data to the CSV file
  write.csv(updated_data, "D:\\R prg\\movie_databas.csv", row.names = FALSE)
  
  cat("Movie data added and CSV file updated successfully.\n")
  
  return(updated_data)  # Return the updated data
}
search_movies <- function(data) {
  cat("Enter search criteria:\n")
  cat("1. Movie Name\n")
  cat("2. Genre\n")
  cat("3. Original Language\n")
  cat("4. Country\n")
  search_option <- as.integer(readline("Enter your search option: "))
  
  # Initialize a variable to store the filtered data
  filtered_data <- NULL
  
  # Perform the search based on user's choice
  switch(
    search_option,
    {
      # Search by movie name
      cat("Enter movie name to search: ")
      search_term <- readline()
      indices <- str_which(data$movienames, regex(search_term, ignore_case = TRUE))
      filtered_data <- data[indices, ]
    },
    {
      # Search by genre
      cat("Enter genre to search: ")
      search_term <- readline()
      indices <- str_which(data$genre, regex(search_term, ignore_case = TRUE))
      filtered_data <- data[indices, ]
    },
    {
      # Search by original language
      cat("Enter original language to search: ")
      search_term <- readline()
      indices <- str_which(data$orig_lang, regex(search_term, ignore_case = TRUE))
      filtered_data <- data[indices, ]
    },
    {
      # Search by country
      cat("Enter country to search: ")
      search_term <- readline()
      indices <- str_which(data$country, regex(search_term, ignore_case = TRUE))
      filtered_data <- data[indices, ]
    }
  )
  
  if (nrow(filtered_data) == 0) {
    cat("No movies found matching the search criteria.\n")
  } else {
    cat("Search results:\n")
    print(filtered_data)
    
    # Ask the user if they want to save the search results
    save_option <- as.integer(readline("Do you want to save the search results to a CSV file? (1: Yes, 0: No): "))
    if (save_option == 1) {
      cat("Enter the full file path for the CSV file (e.g., C:\\path\\to\\sorted_results.csv): ")
      save_filepath <- readline()
      
      # Add the ".csv" extension to the file name if not provided by the user
      if (!grepl(".csv$", save_filepath)) {
        save_filepath <- paste0(save_filepath, ".csv")
      }
      
      # Save the sorted results to the specified CSV file
      write.csv(filtered_data, save_filepath, row.names = FALSE)
      cat("Sorted results saved to", save_filepath, "successfully.\n")
    }
  }
  
  return(filtered_data)
}

#Function to sort movies
sort_movies <- function(data) {
  cat("Select sorting option:\n")
  cat("1. A-Z\n")
  cat("2. Z-A\n")
  cat("3. Lowest to Highest Rating\n")
  cat("4. Highest to Lowest Rating\n")
  cat("5. Year-wise\n")
  option <- as.integer(readline())
  
  sorted_data <- switch(
    option,
    data %>% arrange(movienames),
    data %>% arrange(desc(movienames)),
    data %>% arrange(score),
    data %>% arrange(desc(score)),
    data %>%
      mutate(year_x = lubridate::year(dmy(date_x))) %>%  # Extract and convert to year (yyyy)
      arrange(desc(year_x)) %>%
      select(-year_x)
  )
  cat("Do you want to save the sorted results to a CSV file? (1: Yes, 0: No): ")
  save_option <- as.integer(readline())
  
  if (save_option == 1) {
    cat("Enter the full file path for the CSV file (e.g., C:\\path\\to\\sorted_results.csv): ")
    save_filepath <- readline()
    
    # Add the ".csv" extension to the file name if not provided by the user
    if (!grepl(".csv$", save_filepath)) {
      save_filepath <- paste0(save_filepath, ".csv")
    }
    
    # Save the sorted results to the specified CSV file
    write.csv(sorted_data, save_filepath, row.names = FALSE)
    cat("Sorted results saved to", save_filepath, "successfully.\n")
  }
  
  return(sorted_data)
}

# Function for highest rated movies
highest_rated_movies <- function(data, num = 10) {
  top_movies <- data %>%
    arrange(desc(score)) %>%
    head(num)
  save_option <- as.integer(readline("Do you want to save the search results to a CSV file? (1: Yes, 0: No): "))
  if (save_option == 1) {
    cat("Enter the full file path for the CSV file (e.g., C:\\path\\to\\sorted_results.csv): ")
    save_filepath <- readline()
    
    # Add the ".csv" extension to the file name if not provided by the user
    if (!grepl(".csv$", save_filepath)) {
      save_filepath <- paste0(save_filepath, ".csv")
    }
    
    # Save the sorted results to the specified CSV file
    write.csv(top_movies, save_filepath, row.names = FALSE)
    cat("Sorted results saved to", save_filepath, "successfully.\n")
  }
  return(top_movies)
}

# Function for genre trend analysis
genre_trend_analysis <- function(data) {
  genre_counts <- data %>%
    group_by(genre) %>%
    summarise(movie_count = n(), avg_rating = mean(score))
  
  genre_plot <- genre_counts %>%
    ggplot(aes(x = reorder(genre, -movie_count), y = movie_count)) +
    geom_bar(stat = "identity", fill = "skyblue") +
    labs(x = "Genre", y = "Number of Movies", title = "Genre Trend Analysis") +
    geom_text(aes(label = movie_count), vjust = -0.5, size = 3)  # Add text labels
  
  return(genre_plot)
}

year_genre_analysis <- function(data) {
  # Ask the user for the year
  cat("Enter the year you want to analyze (e.g., 2020): ")
  input_year <- as.integer(readline())
  
  # Convert the date_x column to a proper Date type
  data$date_x <- dmy(data$date_x)  # Assuming date_x contains dates in dd-mm-yyyy format
  
  # Filter movies for the specified year
  year_data <- data %>%
    filter(year(date_x) == input_year)
  
  if (nrow(year_data) == 0) {
    cat("No movies found for the specified year.\n")
  } else {
    # Perform genre analysis on the filtered data
    genre_counts <- year_data %>%
      group_by(genre) %>%
      summarise(movie_count = n())
    
    # Display movie movienames per genre per year in console
    cat("Movies for each genre in", input_year, ":\n")
    genre_movies <- year_data %>%
      select(genre, movienames) %>%
      group_by(genre) %>%
      summarise(movie_movienames = paste(movienames, collapse = ", "))
    print(genre_movies)
    view(genre_movies)
    
    # Create a bar chart to visualize genre distribution
    genre_plot <- ggplot(genre_counts, aes(x = reorder(genre, -movie_count), y = movie_count)) +
      geom_bar(stat = "identity", fill = "skyblue") +
      labs(x = "Genre", y = "Number of Movies", title = paste("Genre Analysis for", input_year)) +
      theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
      geom_text(aes(label = movie_count), vjust = -0.5, size = 3, color = "black")  # Add text labels
    
    print(genre_plot)
  }
}
# Function to analyze language distribution and create a pie chart with percentages in legends
language_analysis <- function(data) {
  # Convert the language column to lowercase for case-insensitive grouping
  data$orig_lang <- tolower(data$orig_lang)
  
  language_counts <- data %>%
    group_by(orig_lang) %>%
    summarise(movie_count = n())
  
  # Calculate percentages
  language_counts <- language_counts %>%
    mutate(percentage = (movie_count / sum(movie_count)) * 100)
  
  # Create a pie chart to visualize language distribution
  pie_chart <- ggplot(language_counts, aes(x = 1, y = movie_count, fill = orig_lang)) +
    geom_bar(stat = "identity", width = 1) +
    coord_polar(theta = "y") +
    labs(x = NULL, y = NULL, fill = "Language", title = "Language Distribution") +
    theme_void()
  
  # Modify legend labels to include percentages
  pie_chart +
    scale_fill_discrete(labels = paste(language_counts$orig_lang, " (", round(language_counts$percentage, 1), "%)", sep = "")) +
    theme(legend.position = "bottom", legend.box = "horizontal")
}

# Function to analyze country distribution and create a visualization
country_analysis <- function(data) {
  country_counts <- data %>%
    group_by(country) %>%
    summarise(movie_count = n())
  
  # Create a bar chart to visualize country distribution
  country_chart <- ggplot(country_counts, aes(x = reorder(country, -movie_count), y = movie_count)) +
    geom_bar(stat = "identity", fill = "skyblue") +
    geom_text(aes(label = movie_count), vjust = -0.5, size = 3) +  # Add text labels
    labs(x = "Country", y = "Number of Movies", title = "Country Distribution") +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  return(country_chart)
}
# Function to delete a movie from the dataset
delete_movie <- function(data) {
  cat("Enter the name of the movie you want to delete: ")
  movie_name <- readline()
  
  # Check if the movie exists in the dataset
  if (movie_name %in% data$movienames) {
    # Confirm deletion with the user
    cat("Are you sure you want to delete '", movie_name, "' from the dataset? (1: Yes, 0: No): ")
    confirmation <- as.integer(readline())
    
    if (confirmation == 1) {
      # Delete the movie from the dataset
      updated_data <- data %>%
        filter(movienames != movie_name)
      
      # Save the updated data to the CSV file
      write.csv(updated_data, "D:\\R prg\\movie_databas.csv", row.names = FALSE)
      
      cat("'", movie_name, "' has been deleted from the dataset.\n")
      
      return(updated_data)
    } else {
      cat("'", movie_name, "' was not deleted.\n")
      return(data)
    }
  } else {
    cat("'", movie_name, "' does not exist in the dataset. No action taken.\n")
    return(data)
  }
}


# Main loop
while (TRUE) {
  show_menu()
  choice <- as.integer(readline("Enter your choice: "))
  
  switch(
    choice,
    {
      cat("Add Movie Data:\n")
      movie_data <- add_movie_data(movie_data)  # Assign the updated data
    },
    {
      cat("Search Movies:\n")
      search_result <- search_movies(movie_data)
      if (!is.null(search_result) && nrow(search_result) > 0) {
        cat("Search results:\n")
        print(search_result)
        view(search_result)
      }
    },
    {
      cat("Sort Movies:\n")
      sorted_result <- sort_movies(movie_data)
      view(sorted_result)
    },
    {
      cat("Highest Rated Movies:\n")
      top_rated <- highest_rated_movies(movie_data)
      view(top_rated)
    },
    {
      cat("Genre Trend Analysis:\n")
      genre_plot <- genre_trend_analysis(movie_data)
      print(genre_plot)
    },
    {
      cat("Year-wise Genre Analysis:\n")
      year_genre_analysis(movie_data)
    },
    {
      cat("Language Analysis:\n")
      lang_dist <- language_analysis(movie_data)
      print(lang_dist)
    },
    {
      cat("Country Analysis:\n")
      country_dist <- country_analysis(movie_data)
      print(country_dist)
    },
    {
      cat("Delete Movie:\n")
      movie_data <- delete_movie(movie_data)
    },
    {
      cat("Exiting program.\n")
      break
    }
  )
  cat("\n")
}

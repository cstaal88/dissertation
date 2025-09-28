library(ggplot2)
library(dplyr)
library(readr)

# Import data from CSV file
data <- read_csv("anes/polarization-anes.csv")

# Filter for "All" demographic group and select relevant columns
data_filtered <- data %>%
  filter(Demographics == "All", Subgroup == "All") %>%
  select(Year, `Own-party feeling`, `Rival-party feeling`)

# Create the plot
p <- ggplot(data_filtered, aes(x = Year)) +
  geom_line(aes(y = `Own-party feeling`), color = "#D2691E", size = 1.2) +
  geom_point(aes(y = `Own-party feeling`), color = "#D2691E", size = 2.5) +
  geom_line(aes(y = `Rival-party feeling`), color = "#8B4513", size = 1.2) +
  geom_point(aes(y = `Rival-party feeling`), color = "#8B4513", size = 2.5) +
  
  # Add labels directly on the plot near the lines
  annotate("text", x = 2016, y = 78, label = "Own-party feeling", 
           color = "#D2691E", size = 4, hjust = 0, fontface = "bold") +
  annotate("text", x = 2016, y = 15, label = "Rival-party feeling", 
           color = "#8B4513", size = 4, hjust = 0, fontface = "bold") +
  
  scale_x_continuous(breaks = seq(1980, 2020, 10),
                     limits = c(1976, 2026)) +
  scale_y_continuous(breaks = seq(0, 100, 20),
                     limits = c(0, 100)) +
  
  labs(
    title = "Affective Polarization in the United States (1978-2024)",
    caption = "Source: American National Election Studies (ANES)"
  ) +
  
  theme_minimal() +
  theme(
    plot.title = element_text(size = 14, hjust = 0.5, face = "bold", margin = margin(b = 20)),
    axis.title = element_blank(),  # Remove both axis labels
    axis.text = element_text(size = 10),
    legend.position = "none",  # Remove legend since we have direct labels
    plot.caption = element_text(size = 9, hjust = 1, color = "gray50", margin = margin(t = 15)),
    panel.grid.minor = element_blank(),
    panel.grid.major = element_line(color = "gray90", size = 0.5),
    plot.margin = margin(20, 20, 20, 20)
  )

# Display the plot
print(p)

# Print summary statistics using the actual data range
data_summary <- data_filtered %>%
  summarise(
    own_start = first(`Own-party feeling`),
    own_end = last(`Own-party feeling`),
    rival_start = first(`Rival-party feeling`),
    rival_end = last(`Rival-party feeling`)
  )

cat("\nKey observations:\n")
cat(sprintf("Own-party feeling: %.1f → %.1f (change: %+.1f)\n", 
            data_summary$own_start, data_summary$own_end, 
            data_summary$own_end - data_summary$own_start))
cat(sprintf("Rival-party feeling: %.1f → %.1f (change: %+.1f)\n", 
            data_summary$rival_start, data_summary$rival_end, 
            data_summary$rival_end - data_summary$rival_start))
cat(sprintf("Polarization gap at start: %.1f points\n", 
            data_summary$own_start - data_summary$rival_start))
cat(sprintf("Polarization gap at end: %.1f points\n", 
            data_summary$own_end - data_summary$rival_end))

# Optional: Save the plot
# ggsave("party_feelings_anes.png", plot = p, width = 10, height = 6, dpi = 300, bg = "white")
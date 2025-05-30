## Instantiate
library(corrplot)
library(FactoMineR)
library(factoextra)
library(lmtest)
library(sandwich)

## Beta regression
breg <- function(propdata) {
  # Fit fractional logit (quasibinomial model)
  model <- glm(
    Proportion ~ Temperature,
    data = propdata,
    family = quasibinomial(link = "logit")
  )
  
  stats <- coeftest(model, vcov = sandwich)
  print(stats)
  
  temp_range <- seq(min(propdata$Temperature), max(propdata$Temperature), length.out = 100)
  predicted_probs <- plogis(coef(model)[1] + coef(model)[2] * temp_range)
  plot_data <- data.frame(Temperature = temp_range, Predicted = predicted_probs)
  
  # Plot data with curve for validation
  plot(propdata$Temperature, propdata$Proportion, 
       xlab = "Temperature", ylab = "Proportion", 
       pch = 19, col = "blue", ylim = c(0, 1))
  lines(plot_data$Temperature, plot_data$Predicted, col = "red", lwd = 2)

  # Convert to linear equation for use in Prism
  predicted_probs <- plogis(coef(model)[1] + coef(model)[2] * propdata$Temperature)
  linear_approx <- lm(predicted_probs ~ propdata$Temperature)
  linear_coefficients <- coef(linear_approx)
}

correlation_matrix <- function(data) {
  ndata <- data[, sapply(data, is.numeric)]
  cor <- cor(ndata)
  print(cor)
  corrplot(cor)
}

famdit <- function(famddata) {
  # Perform FAMD
  res.famd <- FAMD(famddata, graph = FALSE)
  
  # Eigenvalues / Variances
  eig.val <- get_eigenvalue(res.famd)
  print(head(eig.val))
  print(fviz_screeplot(res.famd))
  
  # All variables
  var <- get_famd_var(res.famd)
  fviz_famd_var(res.famd, repel = TRUE) 
  print(fviz_contrib(res.famd, "var", axes = 1))
  print(fviz_contrib(res.famd, "var", axes = 2))
  
  # Quantitative vars
  quanti.var <- get_famd_var(res.famd, "quanti.var")
  print(fviz_famd_var(res.famd, "quanti.var", col.var = "contrib", 
                gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07"),
                repel = TRUE))
  
  # Qualitative vars
  quali.var <- get_famd_var(res.famd, "quali.var")
  print(fviz_famd_var(res.famd, "quali.var", col.var = "contrib", 
                gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07")))
  
  # Individuals
  ind <- get_famd_ind(res.famd)
  print(fviz_mfa_ind(res.famd, 
               habillage = "Size",
               palette = c("#00AFBB", "#E7B800", "#FC4E07"),
               repel = TRUE))
}


## Script
propdata <- read.csv('/path/to/propdata.csv') # X-Y Temperature | Playtio 
corrdata <- read.csv('/path/to/corrdata.csv') # Numeric data
famddata <- read.csv('/path/to/famddata.csv') # Whatever you wanna FAMD

breg(propdata)
correlation_matrix(corrdata)
famdit(famddata)

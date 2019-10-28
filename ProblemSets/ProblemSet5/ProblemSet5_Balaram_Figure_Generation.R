## Install/load packages
# if all packages are correctly loaded, the last message should be all true
pkg <- c("magrittr","dplyr","tidyr","stringr",
         "lubridate","zoo",
         "rvest","knitr","ggplot2", "VGAM",
         "xtable", "AER", "texreg")
new.pkg <- pkg[!(pkg %in% installed.packages()[, "Package"])]
if (length(new.pkg)) install.packages(new.pkg, dependencies = TRUE)
sapply(pkg, require, character.only = TRUE)
rm(new.pkg,pkg)


# Read data
load("bb_data.rda")

# Will be using the d.ord dataset for this homework assignment

# Check the distribution of the proportion of returned products.
# Including baskets with no returned products produces a histogram
# that doesn't say much since a large fraction of baskets have 
# no returns

d.ord.return.dist <- d.ord %>% mutate(return_check = !is.na(rma_date)) %>% 
  group_by(order_id) %>% 
  summarize(basket_size = n(), return_check = sum(return_check)) %>% 
  mutate(return_frac = return_check/basket_size) %>%
  filter(return_frac > 0)

ggplot(d.ord.return.dist, aes(return_frac)) + geom_histogram(binwidth = 0.025) +
  labs(x = "Fraction of products returned", y = "Frequency")


# Begin by calculating the mean proportion of returned products
# for each basket size. This provides evidence that the larger
# the basket size, the more likely consumers will return

d.ord.bsize <- d.ord %>% mutate(return_check = !is.na(rma_date)) %>% 
  group_by(order_id) %>% 
  summarize(total_price = sum(price_paid), basket_size = n(), return_check = sum(return_check)) %>% 
  mutate(return_check=return_check/basket_size) %>% 
  filter(basket_size<=20) %>% 
  group_by(basket_size) %>% 
  summarize(num_of_baskets = n(),
            return_prob_mean = mean(return_check))

ggplot(d.ord.bsize, aes(x = basket_size, y = return_prob_mean)) + geom_point() + 
  labs(x = "Basket size", y = "Mean of return proportion")

# This plot suggests that consumers who order larger baskets are more likely to return products

# Compute the average value of each basket and the fraction of products returned
# from a basket. This provides evidence that consumers who order more
# expensive products are more likely to return products

d.ord.price <- d.ord %>% mutate(return_check = !is.na(rma_date)) %>% 
  group_by(order_id) %>% 
  summarize(total_price = sum(price_paid), basket_size = n(), return_check = sum(return_check)) %>% 
  mutate(return_frac=return_check/basket_size, avg_price = total_price/basket_size) %>% 
  filter(basket_size<=20)

ggplot(d.ord.price, aes(x = total_price, y = return_frac)) + geom_point() +
  labs(x = "Average basket value", y = "Return proportion")

# This plot provides very weak evidence that the more valuable a basket, the more number of products
# that will be returned


















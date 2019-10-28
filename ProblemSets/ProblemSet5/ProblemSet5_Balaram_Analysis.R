# Regression analysis to study how basket characteristics affect the fraction of returned products
# Include basket size, total basket value, shipping amount paid, store credit used

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

# Start by converting data from individual item level to basket level

d.analysis <- d.ord %>% mutate(return_check = !is.na(rma_date)) %>% 
  group_by(order_id) %>% 
  summarize(shipping_price = mean(shipping_amount_paid),total_price = sum(price_paid),
            basket_size = n(), return_check = sum(return_check), 
            store_cred_amt = mean(store_credit_amount_paid)) %>% 
  mutate(return_frac = return_check/basket_size)

# First model is a simple OLS model where the return fraction is the dependent variable
# and the independent variables are basket size, total basket value, total shipping amount
# paid, and amount of store credit used

# Use the log of the three price variables so that they are of comparable scales to the 
# basket size. I add 1 to these variables so that I don't encounter errors when
# computing log(0).

ols_mod <- lm(return_frac ~ log(total_price + 1) + basket_size + log(store_cred_amt + 1)
              + log(shipping_price + 1), data = d.analysis)
summary(ols_mod)

# Generate table for Latex


# Given that the dependent variable is a proportion, I now use a logistic regression model
# with the same set of regressors

logit_mod <- glm(return_frac ~ log(total_price + 1) + basket_size + log(store_cred_amt + 1)
                 + log(shipping_price + 1), data = d.analysis, family = "binomial")

# The downside with using a logit model is that the number of "trials" isn't
# consistent across each basket. This leads to inconsistent estimates.

# The dependent variable is censored to the left at zero and to the right at one, since it
# is a proportion. I use a Tobit model to attempt to overcome this issue

tobit_mod <- vglm(return_frac ~ log(total_price + 1) + basket_size + log(store_cred_amt + 1)
                  + log(shipping_price + 1), tobit(Upper = 1, Lower = 0), data = d.analysis)

summary(tobit_mod)

# I used texreg to obtain a table with the results of the OLS and logit models,
# but obtained an error when trying to include the Tobit model as well.
# I modified the table manually to include these results as well and this can
# be seen from the generated PDF file that I have submitted. I know this isn't
# particularly efficient but it turned out to be easier to just add these
# values manually.
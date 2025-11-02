conditions <- 3
(sampl <- pwr::pwr.anova.test(k = conditions, f = 0.15, sig.level = 0.05, power = 0.90) ) # verified manually with G*Power 3.1.
per_condition <- ceiling(sampl$n)
cat("Per condition:", per_condition)
cat("Required sample size:", per_condition * 3)
cat("Final sample size to allow for 10% attrition:", ceiling(per_condition * 3 * 1.1) )

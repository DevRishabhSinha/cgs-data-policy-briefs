import numpy as np
from scipy.stats import norm

# Data provided
sample_size = 200  # number of surveyed individuals
number_of_successes = 85  # individuals who recalled seeing the advertisements
sample_proportion = number_of_successes / sample_size
null_proportion = 0.36  # The company's threshold for success
alpha = 0.01  # significance level

# Calculate the z-statistic for a one-proportion z-test
z_statistic = (sample_proportion - null_proportion) / np.sqrt(null_proportion * (1 - null_proportion) / sample_size)

# Calculate the critical z-value for a one-tailed test at the 1% significance level
critical_z_value = norm.ppf(1 - alpha)

# Calculate the p-value for the one-tailed test
p_value = 1 - norm.cdf(z_statistic)

# Print the results
print(f"Sample Proportion: {sample_proportion}")
print(f"Z-Statistic: {z_statistic}")
print(f"Critical Z-Value (one-tailed test): {critical_z_value}")
print(f"P-Value (one-tailed test): {p_value}")

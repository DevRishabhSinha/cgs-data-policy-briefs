import numpy as np
from scipy import stats

# Data provided
data = [
    1.998, 2.104, 1.976, 2.075, 2.065, 2.057, 2.052, 2.044, 2.036, 2.038,
    2.031, 2.029, 2.025, 2.029, 2.023, 2.020, 2.015, 2.014, 2.013, 2.014,
    2.012, 2.012, 2.012, 2.010, 2.005, 2.003, 1.999, 1.996, 1.997, 1.992,
    1.994, 1.986, 1.984, 1.981, 1.973, 1.975, 1.971, 1.969, 1.966, 1.967,
    1.963, 1.957, 1.951, 1.951, 1.947, 1.941, 1.941, 1.938, 1.908, 1.894
]

# Calculate the sample mean and sample standard deviation
sample_mean = np.mean(data)
sample_std = np.std(data, ddof=1)
n = len(data)
pop_mean = 2.0  # The hypothesized population mean

# Calculate the t-statistic
t_statistic = (sample_mean - pop_mean) / (sample_std / np.sqrt(n))

# Degrees of freedom
df = n - 1

# Calculate the critical t-value for a two-tailed test at the 0.05 significance level
alpha = 0.05
critical_t_value = stats.t.ppf(1 - alpha/2, df)

# Calculate the p-value for the two-tailed test
p_value = (1 - stats.t.cdf(np.abs(t_statistic), df)) * 2

# Printing the results
print(f"Sample Mean: {sample_mean}")
print(f"Sample Standard Deviation: {sample_std}")
print(f"T-Statistic: {t_statistic}")
print(f"Critical T-Value: ±{critical_t_value}")
print(f"P-Value: {p_value}")

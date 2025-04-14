import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Data
non_high = [1.04, 1.15, 1.23, 1.69, 1.92,
            1.98, 2.36, 2.49, 2.72, 1.37,
            1.43, 1.57, 1.71, 1.94, 2.06,
            2.55, 2.64, 2.82]

high = [1.55, 2.02, 2.02, 2.05, 2.35,
        2.57, 2.93, 2.94, 2.97]

# Create DataFrame for plotting
df = pd.DataFrame({
    'Depth': non_high + high,
    'Current': ['Non-High'] * len(non_high) + ['High'] * len(high)
})

# Plot
plt.figure(figsize=(16, 10))
sns.boxplot(x='Current', y='Depth', data=df)
plt.title('Boxplot HAZ Depth vs. Cur Setting')
plt.ylabel('Depth (mm)')
plt.grid(True)
plt.tight_layout()
plt.show()

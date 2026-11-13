import pandas as pd
import numpy as np

# 1. Define the number of samples (rows)
n_samples = 100

# 2. Generate random data
# Set seed for reproducibility (so you get the same random numbers each time)
np.random.seed(42)

# Feature 1: Age (Random integers between 18 and 70)
age = np.random.randint(18, 70, size=n_samples)

# Feature 2: Annual Salary (Random integers between 20k and 140k)
salary = np.random.randint(20000, 140000, size=n_samples)

# Feature 3: Spending Score (Random integers between 1 and 100)
spending_score = np.random.randint(1, 100, size=n_samples)

# Target: Purchased (0 = No, 1 = Yes)
# Let's create a pattern: specific age/salary combos are more likely to buy
target = []
for i in range(n_samples):
    if (age[i] > 25 and salary[i] > 50000) or (spending_score[i] > 80):
        target.append(1)
    else:
        target.append(0)

# 3. Create a DataFrame
df = pd.DataFrame({
    'Age': age,
    'Annual_Salary': salary,
    'Spending_Score': spending_score,
    'Purchased': target
})

# 4. Save to CSV
df.to_csv('customer_data.csv', index=False)

print("Success! 'customer_data.csv' has been created.")
print(df.head())
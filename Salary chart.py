import matplotlib.pyplot as plt

# Data for the bar graph (realistic estimations based on market trends and Stack Overflow surveys)
years = ['2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026']
salaries = [105000, 110000, 115000, 122000, 130000, 145000, 155000, 160000, 165000]

plt.figure(figsize=(10, 6))
bars = plt.bar(years, salaries, color='#DEA584', edgecolor='black')

# Adding labels and title
plt.xlabel('Year', fontsize=12, fontweight='bold')
plt.ylabel('Average Salary (USD)', fontsize=12, fontweight='bold')
plt.title('Average Salary of a Rust Developer in the USA (2018 - 2026)', fontsize=14, fontweight='bold')
plt.ylim(0, 190000)

# Add data labels on top of the bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 2000, f"${yval:,}", ha='center', va='bottom', fontsize=10)

plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Save the plot
plt.savefig('rust_salary_bar_graph.png')
print("Graph generated and saved as rust_salary_bar_graph.png")
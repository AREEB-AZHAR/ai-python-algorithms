import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import pandas as pd

# --- 1. Define the Project Data ---
# Schedule: Nov 11, 2025 Start | Design vs Implementation Split
# Format: (ID, Task Name, Start Date, Duration, Is_Milestone, Predecessors, Resources)
data = [
    (1, "Literature Review", "2025-11-11", 14, False, "", "All Team"),
    (2, "Requirement Gathering", "2025-11-25", 14, False, "1", "NoorNabi, Areeb"),
    (3, "System Architecture", "2025-12-09", 21, False, "2", "Vandna, Muskan"),
    (4, "UI/UX Wireframing", "2025-12-30", 21, False, "3", "Areeb, Muskan"),
    (5, "Algorithm Logic Design", "2026-01-20", 14, False, "4", "NoorNabi, Vandna"),
    (6, "FYP-1 Presentation", "2026-02-03", 0, True, "5", "All Team"),  # Milestone
    (7, "Game Engine Setup", "2026-02-04", 7, False, "6", "Areeb"),
    (8, "Core Mechanics Dev", "2026-02-11", 21, False, "7", "NoorNabi, Areeb"),
    (9, "Prototype Level 1", "2026-03-04", 14, False, "8", "Vandna, Muskan"),
    (10, "Adaptive Algorithm Dev", "2026-03-18", 28, False, "9", "NoorNabi"),
    (11, "Data Analytics Integration", "2026-04-15", 14, False, "10", "Vandna"),
    (12, "Advanced Level Design", "2026-04-29", 21, False, "10", "Muskan, Areeb"),
    (13, "Alpha & Beta Testing", "2026-05-20", 21, False, "11,12", "All Team"),
    (14, "Final Polish & Doc", "2026-06-10", 14, False, "13", "All Team"),
    (15, "Final Submission", "2026-06-24", 0, True, "14", "All Team")   # Milestone
]

# Create DataFrame
df = pd.DataFrame(data, columns=["ID", "Task Name", "Start", "Duration", "Milestone", "Predecessors", "Resources"])
df["Start"] = pd.to_datetime(df["Start"])
df["Finish"] = df.apply(lambda x: x["Start"] + timedelta(days=x["Duration"]), axis=1)

# Reverse order for plotting (top-down)
df = df.iloc[::-1].reset_index(drop=True)

# --- 2. Setup Plot Layout ---
fig, ax = plt.subplots(figsize=(20, 10)) # Wide figure for extra columns

# Split plot into two parts: Table (left) and Gantt (right)
# Table gets 60% of width, Gantt gets 40%
ax.set_xlim(0, 1) 
ax.set_ylim(0, len(df) + 2) 
ax.axis('off') 

# --- 3. Draw the Gantt Chart (Right Side) ---
ax_gantt = ax.inset_axes([0.60, 0, 0.40, 1]) 
ax_gantt.set_ylim(0, len(df) + 2)
ax_gantt.set_yticks([]) 

# Plot Bars and Milestones
for i, row in df.iterrows():
    y_pos = i + 0.5
    
    if row["Milestone"]:
        ax_gantt.plot(row["Start"], y_pos, marker='D', color='black', markersize=8, zorder=10)
        # Label format: Date
        label = row["Start"].strftime('%m/%d')
        ax_gantt.text(row["Start"] + timedelta(days=3), y_pos, label, fontsize=9, va='center', fontweight='bold')
    else:
        duration_days = row["Duration"]
        ax_gantt.barh(y_pos, duration_days, left=row["Start"], height=0.5, 
                     color='#6fa8dc', edgecolor='#3d85c6', hatch='////') 

# Format Time Axis
ax_gantt.xaxis_date()
ax_gantt.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
ax_gantt.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax_gantt.grid(True, axis='x', linestyle='--', alpha=0.5)
ax_gantt.tick_params(axis='x', which='both', bottom=False, top=True, labelbottom=False, labeltop=True)
ax_gantt.spines['left'].set_visible(True) 

# --- 4. Draw the Table (Left Side) ---
header_y = len(df) + 0.5
font_size = 10

# Column positions (Normalized 0.0 to 0.60)
# Rearranged to include Duration instead of Pred
pos = {
    "ID": 0.005,
    "Task": 0.035,
    "Dur": 0.21,   # New Position for Duration
    "Start": 0.27,
    "Finish": 0.35,
    "Res": 0.44
}

# Headers
plt.text(pos["ID"], header_y, "ID", fontsize=font_size, fontweight='bold', transform=ax.transData)
plt.text(pos["Task"], header_y, "Task Name", fontsize=font_size, fontweight='bold', transform=ax.transData)
plt.text(pos["Dur"], header_y, "Duration", fontsize=font_size, fontweight='bold', transform=ax.transData)
plt.text(pos["Start"], header_y, "Start", fontsize=font_size, fontweight='bold', transform=ax.transData)
plt.text(pos["Finish"], header_y, "Finish", fontsize=font_size, fontweight='bold', transform=ax.transData)
plt.text(pos["Res"], header_y, "Resource Names", fontsize=font_size, fontweight='bold', transform=ax.transData)

# Draw Separator Line under header
plt.plot([0, 0.59], [len(df), len(df)], color='black', linewidth=1, transform=ax.transData)

# Draw Table Rows
for i, row in df.iterrows():
    y_pos = i + 0.5
    
    plt.text(pos["ID"], y_pos, str(row["ID"]), fontsize=font_size, va='center', transform=ax.transData)
    plt.text(pos["Task"], y_pos, row["Task Name"], fontsize=font_size, va='center', transform=ax.transData)
    
    # Duration Column (Formatted as "X days" or just "X")
    duration_str = f"{row['Duration']} days" if row['Duration'] > 0 else "0 days"
    plt.text(pos["Dur"], y_pos, duration_str, fontsize=font_size, va='center', transform=ax.transData)
    
    plt.text(pos["Start"], y_pos, row["Start"].strftime('%d/%m/%y'), fontsize=font_size, va='center', transform=ax.transData)
    plt.text(pos["Finish"], y_pos, row["Finish"].strftime('%d/%m/%y'), fontsize=font_size, va='center', transform=ax.transData)
    plt.text(pos["Res"], y_pos, row["Resources"], fontsize=9, va='center', transform=ax.transData) 
    
    # Horizontal grid lines
    plt.plot([0, 1.0], [i, i], color='lightgray', linewidth=0.5, transform=ax.transData)

# Vertical Separator Line
plt.plot([0.59, 0.59], [0, len(df)+2], color='black', linewidth=1, transform=ax.transData)

# --- 5. Save ---
plt.tight_layout()
plt.subplots_adjust(left=0.02, right=0.98, top=0.95, bottom=0.05)
filename = "ms_project_gantt_duration.png"
plt.savefig(filename, dpi=300)

print(f"Chart saved as {filename}")
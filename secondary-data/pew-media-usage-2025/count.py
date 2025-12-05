import pandas as pd
import sys

# Redirect output to both console and file
class Tee:
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush()
    def flush(self):
        for f in self.files:
            f.flush()

# Open output file
output_file = open('output.txt', 'w')
original_stdout = sys.stdout
sys.stdout = Tee(sys.stdout, output_file)

# Print title
print("Pew estimated news usage for Americans (2025)")
print()

# Read CSV into pandas DataFrame
df = pd.read_csv('raw/News-Media-Tracker-Dataset-June-2025.csv')

# Create new columns for rep_all and dem_all (same as the original columns)
df['rep_all'] = df['Rep/Lean Rep']
df['dem_all'] = df['Dem/Lean Dem']

# Filter to only include rows with 'use' measure and drop age columns
usage_df = df[df['Measure'] == 'use'][['Outlet_Display', 'Year', 'Measure', 'Total', 'rep_all', 'dem_all']].copy()

# Sort by Total (descending)
print("="*50)
print("Sorted by Total:")
print("="*50)
usage_sorted_total = usage_df.sort_values('Total', ascending=False)
print(usage_sorted_total.to_string(index=False))

# Sort by rep_all (descending)
print("\n" + "="*50)
print("Sorted by rep_all:")
print("="*50)
usage_sorted_rep = usage_df.sort_values('rep_all', ascending=False)
print(usage_sorted_rep.to_string(index=False))

# Sort by dem_all (descending)
print("\n" + "="*50)
print("Sorted by dem_all:")
print("="*50)
usage_sorted_dem = usage_df.sort_values('dem_all', ascending=False)
print(usage_sorted_dem.to_string(index=False))

# Get top 15 lists for each category
top_15_total_list = usage_sorted_total.head(15)['Outlet_Display'].tolist()
top_15_rep_list = usage_sorted_rep.head(15)['Outlet_Display'].tolist()
top_15_dem_list = usage_sorted_dem.head(15)['Outlet_Display'].tolist()

# Print each list
print("\n" + "="*50)
print("TOP 15 BY TOTAL:")
print("="*50)
for i, outlet in enumerate(top_15_total_list, 1):
    print(f"{i}. {outlet}")

print("\n" + "="*50)
print("TOP 15 BY rep_all:")
print("="*50)
for i, outlet in enumerate(top_15_rep_list, 1):
    print(f"{i}. {outlet}")

print("\n" + "="*50)
print("TOP 15 BY dem_all:")
print("="*50)
for i, outlet in enumerate(top_15_dem_list, 1):
    print(f"{i}. {outlet}")

# Create combined deduplicated list (preserving order from total, then rep, then dem)
combined_list = []
for outlet in top_15_total_list + top_15_rep_list + top_15_dem_list:
    if outlet not in combined_list:
        combined_list.append(outlet)

print("\n" + "="*50)
print("COMBINED DEDUPLICATED LIST:")
print("="*50)
for i, outlet in enumerate(combined_list, 1):
    print(f"{i}. {outlet}")
print(f"\nTotal unique outlets: {len(combined_list)}")

# Close output file and restore stdout
sys.stdout = original_stdout
output_file.close()
print("\nOutput saved to output.txt")

import requests
import urllib.parse
import json
import matplotlib.pyplot as plt
import seaborn as sns

# define search terms
list_a = [
    "ai", 
    "llm*", 
    "artificial intelligence", 
    "large language model*" 
]
list_b = [
    "theory of mind", 
    "mentaliz*"
]

# build query
query_a = " OR ".join(
    [f'"{term}"' if " " in term and not term.startswith('"') else term for term in list_a]
)
query_b = " OR ".join(
    [f'"{term}"' if " " in term and not term.startswith('"') else term for term in list_b]
)

# papers must include at least one term from List A AND at least one term from List B
final_query = f"({query_a}) AND ({query_b})"
encoded_query = urllib.parse.quote(final_query)

url = (
    f"https://api.openalex.org/works?"
    f"search={encoded_query}&filter=publication_year:2000-2023&"
    f"group_by=publication_year&per_page=50"
)

# send get request
response = requests.get(url)
try:
    data = response.json()
except Exception as e:
    print("Error parsing JSON:", e)
    exit(1)

# process response
if isinstance(data, dict) and "group_by" in data and isinstance(data["group_by"], list):
    group_data = data["group_by"]
    print("Publication counts by year:")
    for group in group_data:
        print(f"Year: {group['key']}, Count: {group['count']}")
    
    # prepare data for plotting.
    years = [int(group["key"]) for group in group_data]
    counts = [group["count"] for group in group_data]
    
    # abbreviate
    year_labels = [f"'{str(y)[-2:]}" for y in years]
    
    # make a pretty plot
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (8, 5)
    fig, ax = plt.subplots()
    ax.bar(years, counts, color='#bf5700')
    ax.set_xticks(years)
    ax.set_xticklabels(year_labels, fontsize=14)
    ax.tick_params(axis='y', labelsize=14)
    sns.despine()
    plt.tight_layout()
    plt.show()

else:
    print("No grouped data found. The API response structure is:")
    print(json.dumps(data, indent=2))

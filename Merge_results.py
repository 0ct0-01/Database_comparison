import json

# File containing all consolidated results
input_file = 'json_results/filtered_results_all.json'

# Output files
summary_output_file = 'paper_summaries.json'
summary_text_file = 'paper_summaries.txt'

# Load the consolidated JSON results
with open(input_file, "r", encoding="utf-8") as file:
    all_results = json.load(file)

# Extract unique papers based on title
unique_summaries = {
    result["title"]: {"title": result["title"], "doi": result["doi"]}
    for result in all_results.get("results", [])
    if "doi" in result and "title" in result
}.values()

# Save titles and DOIs to a plain text file
with open(summary_text_file, "w", encoding="utf-8") as file:
    for entry in unique_summaries:
        file.write(f"Title: {entry['title']}\nDOI: {entry['doi']}\n\n")

print(f"Paper titles and DOIs saved to {summary_text_file}")

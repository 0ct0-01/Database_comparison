import json
import glob
import os

# Define the subfolder where JSON results are saved
output_subfolder = 'json_results'

# Load all batch result files from the subfolder
all_results = []
for file_name in glob.glob(os.path.join(output_subfolder, "filtered_results_batch_*.json")):
    with open(file_name, "r", encoding="utf-8") as file:
        batch_results = json.load(file)
        all_results.extend(batch_results.get("results", []))

# Deduplicate results based on DOI
unique_results = {result["doi"]: result for result in all_results if "doi" in result}

# Save deduplicated results to a JSON file
final_output_file = 'final_filtered_results.json'
with open(final_output_file, "w", encoding="utf-8") as file:
    json.dump(list(unique_results.values()), file, indent=4)

print(f"Total unique results: {len(unique_results)}")

# Extract titles and save to a text file
titles_file = 'paper_titles.txt'
with open(titles_file, "w", encoding="utf-8") as file:
    for result in unique_results.values():
        title = result.get("title", "Unknown Title")
        file.write(f"{title}\n")

print(f"Paper titles saved to {titles_file}")

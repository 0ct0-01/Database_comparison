import json
import glob
import os

# Define the subfolder where JSON results are saved
output_subfolder = 'json_results'

# Load all batch result files from the subfolder
all_results = []
for file_name in glob.glob(os.path.join(output_subfolder, "filtered_results_batch_*.json")):
    with open(file_name, "r") as file:
        batch_results = json.load(file)
        all_results.extend(batch_results.get("results", []))

# Deduplicate results based on DOI
unique_results = {result["doi"]: result for result in all_results if "doi" in result}

# Save deduplicated results
final_output_file = 'final_filtered_results.json'
with open(final_output_file, "w") as file:
    json.dump(list(unique_results.values()), file, indent=4)

print(f"Total unique results: {len(unique_results)}")

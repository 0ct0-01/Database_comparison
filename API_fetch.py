import requests
import urllib.parse
import json
import os
import shutil
import sys

# Load the unique topics and their IDs
topic_ids_file = 'unique_topics_with_ids.txt'  # Replace with the correct file path
output_subfolder = 'json_results'  # Subfolder where you want to save the JSON files
output_file_prefix = 'filtered_results_'

# Ensure the output subfolder exists and clear its contents if it does
if os.path.exists(output_subfolder):
    shutil.rmtree(output_subfolder)  # Remove the subfolder and its contents
os.makedirs(output_subfolder)  # Recreate the empty subfolder

# Read the topic IDs from the file
# Uncomment this section if you want to load multiple topic IDs
# topic_ids = []
# with open(topic_ids_file, 'r') as file:
#     for line in file:
#         topic_name, topic_id = line.strip().split('\t')
#         topic_ids.append(topic_id)

# Alternatively, use a custom list for testing
topic_ids = [
    "T11099",  # Autonomous Vehicle Technology and Safety
    "T10883",  # Ethics and Social Impacts of AI
    "T12026",  # Explainable Artificial Intelligence (XAI)
    "T10586",  # Robotic Path Planning Algorithms
    "T10525"   # Human-Automation Interaction and Safety
]

# Base OpenAlex API URL
base_url = "https://api.openalex.org/works"

# Search string (encoded for URL)
search_string = '("Autonomous Driving Systems" OR "Self-driving Cars" OR "Automated driving Systems" OR "Autonomous Vehicles" OR "ADS") AND ("automatic program repair" OR "software repair techniques" OR "program failures" OR "causality analysis" OR "software fault localization" OR "automated fault localization" OR "fully automated debugging" OR "feature interaction failures" OR "automatic fixing" OR "automatic patching" OR "automatic recovery" OR "survival" OR "explainable AI" OR "fault management")'

# Encode the topic ID(s)
encoded_topic_ids = "|".join([urllib.parse.quote(topic_id) for topic_id in topic_ids])

# Initialize pagination variables
page = 1
total_results_fetched = 0
batch_results = []

# Fetch results from OpenAlex API with pagination
while True:
    # Construct the query URL with pagination
    query_url = (
        f"{base_url}?&search={(search_string)}"
        f"&filter=topics.id:{encoded_topic_ids}"
        f"&per-page=200&page={page}"
    )

    # Send request to OpenAlex API
    response = requests.get(query_url)
    if response.status_code == 200:
        data = response.json()

        # Debug: Print the meta information to understand pagination
        print(json.dumps(data.get('meta', {}), indent=4))  # Print metadata for debugging

        # Append the results from the current page
        batch_results.extend(data.get("results", []))  
        total_results_fetched += len(data.get("results", []))

        # Debug: Print how many results were fetched
        print(f"Fetched {total_results_fetched} results so far.")

        # Stop if we have fetched all available results or if no results are returned
        if total_results_fetched >= data["meta"]["count"]:
            print(f"Reached total expected results: {total_results_fetched}.")
            break

        # If the current page has no results, break the loop
        if len(data.get("results", [])) == 0:
            print(f"No more results available. Total results fetched: {total_results_fetched}")
            break

        # Move to the next page
        page += 1
    else:
        print(f"Error fetching page {page}: {response.status_code} - {response.text}")
        break

# Save all results to JSON file
if batch_results:
    output_file_path = os.path.join(output_subfolder, f"{output_file_prefix}all.json")
    with open(output_file_path, "w") as file:
        json.dump({"results": batch_results}, file, indent=4)
    print(f"All results saved successfully in {output_file_path}")
else:
    print("No results found.")

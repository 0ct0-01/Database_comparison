import requests
import urllib.parse
import json
import os
import shutil

# Load the unique topics and their IDs
topic_ids_file = 'unique_topics_with_ids.txt'  # Replace with the correct file path
output_subfolder = 'json_results'  # Subfolder where you want to save the JSON files
output_file_prefix = 'filtered_results_batch_'

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
topic_ids = ["T11099"]  # Replace with your topic IDs

# Calculate number of batches
batch_size = 10
num_batches = (len(topic_ids) + batch_size - 1) // batch_size  # This handles the remainder (if any)

print(f"Total number of batches: {num_batches}")

# Base OpenAlex API URL
base_url = "https://api.openalex.org/works"

# Search string (encoded for URL)
search_string = '("Autonomous Driving Systems" OR "Self-driving Cars" OR "Automated driving Systems" OR "Autonomous Vehicles" OR "ADS") AND ("Debugging" OR "automatic fixing" OR "automatic patching" OR "automatic recovery" OR "Fault Localization" OR "Software Repair" OR "Automated Program Repair" OR "automated Repair Techniques" OR "fully automated debugging" OR "fault detection algorithm" OR "Automated Fault Localization" OR "Causal Analysis" OR "explainable AI" OR "program repair" OR "testing" OR "Cause Analysis" OR "Causality Analysis" OR "Feature Interaction Failures" OR "logging and fault management" OR "fault detection" OR "fault diagnosis" OR "diagnosis system")'

# Iterate through topic IDs in batches
for i in range(0, len(topic_ids), batch_size):
    # Combine topic IDs in the current batch
    topic_batch = topic_ids[i:i+batch_size]
    encoded_topic_ids = "|".join([urllib.parse.quote(topic_id) for topic_id in topic_batch])

    # Initialize pagination variables
    page = 1
    total_results_fetched = 0
    batch_results = []
    
    while True:
        # Construct the query URL with pagination
        query_url = (
            f"{base_url}?filter=topics.id:{encoded_topic_ids}"
            f"&search={urllib.parse.quote(search_string)}"
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
            print(f"Error fetching batch {i//batch_size + 1}, page {page}: {response.status_code} - {response.text}")
            break

    # Save batch results to JSON file in the subfolder
    if batch_results:
        output_file_path = os.path.join(output_subfolder, f"{output_file_prefix}{i//batch_size + 1}.json")
        with open(output_file_path, "w") as file:
            json.dump({"results": batch_results}, file, indent=4)
        print(f"Batch {i//batch_size + 1} saved successfully in {output_file_path}")
    else:
        print(f"No results for batch {i//batch_size + 1}")

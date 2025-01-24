import requests
import urllib.parse
import json
import os

# Load the unique topics and their IDs
topic_ids_file = 'unique_topics_with_ids.txt'  # Replace with the correct file path
output_subfolder = 'json_results'  # Subfolder where you want to save the JSON files
output_file_prefix = 'filtered_results_batch_'

# Ensure the output subfolder exists
if not os.path.exists(output_subfolder):
    os.makedirs(output_subfolder)

# Read the topic IDs from the file
topic_ids = []
with open(topic_ids_file, 'r') as file:
    for line in file:
        topic_name, topic_id = line.strip().split('\t')
        topic_ids.append(topic_id)

# Calculate number of batches
batch_size = 5
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

    # Construct the query URL
    query_url = f"{base_url}?filter=topics.id:{encoded_topic_ids}&search={urllib.parse.quote(search_string)}"

    # Send request to OpenAlex API
    response = requests.get(query_url)
    if response.status_code == 200:
        results = response.json()
        # Save batch results to JSON file in the subfolder
        output_file_path = os.path.join(output_subfolder, f"{output_file_prefix}{i//batch_size + 1}.json")
        with open(output_file_path, "w") as file:
            json.dump(results, file, indent=4)
        print(f"Batch {i//batch_size + 1} saved successfully in {output_file_path}")
    else:
        print(f"Error fetching batch {i//batch_size + 1}: {response.status_code} - {response.text}")

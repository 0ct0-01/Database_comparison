## Collects all the unique topics found within search results

import pandas as pd

# Load the CSV file
input_file = 'OpenAlex_results.csv'  # Replace with your file name
output_file = 'unique_topics_with_ids.txt'

# Read the CSV into a DataFrame
data = pd.read_csv(input_file)

# Check if 'topics.display_name' and 'topics.id' columns exist
if 'topics.display_name' not in data.columns or 'topics.id' not in data.columns:
    raise KeyError("Columns 'topics.display_name' or 'topics.id' not found in the CSV file.")

# Extract the 'topics.display_name' and 'topics.id' columns, ensuring they are not empty
topics_column = data['topics.display_name'].dropna()
topic_ids_column = data['topics.id'].dropna()

# Initialize a dictionary to hold unique topics and their IDs
unique_topics = {}

# Iterate through the rows and collect unique topics with their IDs
for topic, topic_ids in zip(topics_column, topic_ids_column):
    # Split topics by '|' in case there are multiple topics in one row
    topic_names = topic.split('|')
    topic_ids_list = topic_ids.split('|')
    
    for topic_name, topic_id in zip(topic_names, topic_ids_list):
        topic_name = topic_name.strip()
        topic_id = topic_id.split('/')[-1]  # Extract only the ID part (after the last '/')
        
        if topic_name not in unique_topics:
            unique_topics[topic_name] = topic_id

# Save the unique topics and their IDs to a text file
with open(output_file, 'w') as file:
    for topic_name, topic_id in sorted(unique_topics.items()):
        file.write(f"{topic_name}\t{topic_id}\n")

print(f"Unique topics and IDs saved to {output_file}. Total unique topics: {len(unique_topics)}")

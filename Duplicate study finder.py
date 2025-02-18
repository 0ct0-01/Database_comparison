import pandas as pd

def check_duplicates(file_path):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)
    
    # Get the column titles
    column_titles = df.columns.tolist()
    
    # Find duplicate column titles
    duplicate_titles = []
    seen_titles = set()
    
    for title in column_titles:
        if title in seen_titles:
            duplicate_titles.append(title)
        else:
            seen_titles.add(title)
    
    # Check for duplicate rows
    duplicate_rows = df[df.duplicated()].to_dict(orient='records')
    
    # Return duplicate column titles and duplicate rows
    return duplicate_titles, duplicate_rows

# Example usage
file_path = 'final_studies.csv'
duplicates, duplicate_rows = check_duplicates(file_path)

if duplicates:
    print(f"Duplicate column titles: {duplicates}")
else:
    print("No duplicate column titles found.")

if duplicate_rows:
    print(f"Duplicate rows found: {duplicate_rows}")
else:
    print("No duplicate rows found.")

import pandas as pd

def check_duplicates(file_path):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)
    
    # Get the column titles
    column_titles = df.columns.tolist()
    
    # Find duplicate column titles
    duplicate_titles = []
    seen_titles = set()
    
    for title in column_titles:
        if title in seen_titles:
            duplicate_titles.append(title)
        else:
            seen_titles.add(title)
    
    # Check for duplicate rows
    duplicate_rows = df[df.duplicated()]
    
    # Return counts of duplicate column titles and rows
    return len(duplicate_titles), duplicate_rows.shape[0]

# Example usage
file_path = 'final_studies.csv'
duplicates_count, duplicate_rows_count = check_duplicates(file_path)

if duplicates_count > 0:
    print(f"Number of duplicate column titles: {duplicates_count}")
else:
    print("No duplicate column titles found.")

if duplicate_rows_count > 0:
    print(f"Number of duplicate rows found: {duplicate_rows_count}")
else:
    print("No duplicate rows found.")

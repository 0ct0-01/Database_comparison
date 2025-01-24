import pandas as pd

# Load datasets
ieee_results = pd.read_csv('IEEE_results.csv', low_memory=False)
openalex_results = pd.read_csv('OpenAlex_results.csv', low_memory=False)

# Normalize DOI columns
ieee_results['DOI'] = ieee_results['DOI'].str.lower().str.strip()
openalex_results['doi'] = openalex_results['doi'].str.lower().str.strip()

# Remove 'https://doi.org/' from OpenAlex DOIs
openalex_results['doi'] = openalex_results['doi'].str.replace('https://doi.org/', '')

# Drop missing DOIs
ieee_dois = set(ieee_results['DOI'].dropna())
openalex_dois = set(openalex_results['doi'].dropna())

# Calculate overlap
overlap = ieee_dois & openalex_dois
missing_from_openalex = ieee_dois - openalex_dois

# Output results
print(f"Total IEEE results: {len(ieee_dois)}")
print(f"Total OpenAlex results: {len(openalex_dois)}")
print(f"Overlap: {len(overlap)}")
print(f"Missing from OpenAlex: {len(missing_from_openalex)}")

# Save missing DOIs to a file for further inspection
with open('missing_from_openalex.csv', 'w') as f:
    f.write('\n'.join(missing_from_openalex))

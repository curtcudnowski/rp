import re
import sys

def extract_domains_from_log_file(log_file_path):
    domains = set()
    with open(log_file_path, 'r') as f:
        for line in f:
            match = re.search(r'http[s]?://([\w.-]+)', line)
            if match:
                domain = match.group(1)
                domains.add(domain)
    return domains

def tokenize_into_trigrams(domain):
    trigrams = set()
    for i in range(len(domain) - 2):
        trigrams.add(domain[i:i+3])
    return trigrams

def calculate_jaccard_similarity(set1, set2):
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)

if len(sys.argv) != 2:
    print("Usage: python script_name.py <log_file_path>")
    sys.exit(1)

log_file_path = sys.argv[1]
domains = extract_domains_from_log_file(log_file_path)

# Tokenize domains into trigrams
domain_trigrams = {}
for domain in domains:
    trigrams = tokenize_into_trigrams(domain)
    domain_trigrams[domain] = trigrams

# Calculate Jaccard similarity between domains and write results to a text file
output_file_path = 'jaccard_similarity_results.txt'
with open(output_file_path, 'w') as output_file:
    for domain1 in domains:
        for domain2 in domains:
            if domain1 != domain2:
                jaccard_similarity = calculate_jaccard_similarity(domain_trigrams[domain1], domain_trigrams[domain2])
                result_line = f"Jaccard similarity between {domain1} and {domain2}: {jaccard_similarity}\n"
                output_file.write(result_line)

print(f"Jaccard similarity results written to {output_file_path}")

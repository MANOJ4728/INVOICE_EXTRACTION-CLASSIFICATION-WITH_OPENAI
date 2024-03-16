import pandas as pd
from transformers import pipeline

# Load the Excel file
excel_filename = 'cleaned_file.xlsx'  # replace with your actual Excel file name
df = pd.read_excel(excel_filename)

# Initialize the pipeline for zero-shot classification
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Perform zero-shot classification
result = classifier(
    "albridge video services",
    candidate_labels=[
        "solutions", "contributor", "activity", "response", "threat", "event", "warehouse", "supply", "extension",
        "pos", "material", "monitoring", "food", "business", "innovative", "check", "transformation", "power",
        "electical", "supplies", "hr", "room", "betterment", "mitigation", "solution", "system", "merchant", "support",
        "home", "assistance", "building", "profile", "special", "cooling", "storage", "speaker", "store", "technical",
        "alarm", "civic", "heating", "application", "protection", "professional", "window", "coc", "control", "insider",
        "verification", "charging", "voice", "selling", "generator", "video", "cctv", "agency", "industry", "sectional",
        "floor", "guest", "fiduciary", "accomodation", "transfer", "delivary", "saftey", "office", "paving", "treatment",
        "care", "logistics", "restore", "complementary", "suppression", "controls", "repair", "maintainance", "operation",
        "hvac", "consultation", "life", "management", "media", "license", "disinfect", "interior", "geyser", "develeopement",
        "product", "restoration", "lease", "trustee", "specification", "emergency", "employement", "firewall", "network",
        "social", "access", "design", "removal", "tv", "products", "agents", "painting", "google", "disposal", "ceiling",
        "signage", "camera", "economic", "generation", "dock", "fixture", "technology", "depot", "administration", "fax",
        "phone", "networking", "felling", "web", "millwork", "coating", "pest", "safety", "leaves", "tree", "collection",
        "handyman", "stains", "replacements", "commercial", "natural", "machine", "waste", "internet", "inspection",
        "container", "online", "elevator", "legal", "cultural", "digital", "cloud", "housekeeping", "it", "printing",
        "vehicle", "franchise", "computing", "escrow", "security", "workplace", "adobe", "installation", "distribution",
        "surveillance", "facilities", "cabling", "motorola", "entertainment", "contractor", "wifi", "hardscaping", "subscription",
        "washing", "cable", "labor", "doors", "newspaper", "sprinkler", "marketing", "breakroom", "transit", "dish", "services",
        "staffing", "remote", "production", "payment", "electrical", "registration", "fire", "residential", "luxury",
        "mechanical", "education", "domestic", "rentals", "software", "mixers", "occupations", "ice", "advertising", "cleaning",
        "amenities", "travel", "promotion", "regulation", "packaging", "texas", "telecommunication", "infrastructure",
        "membership", "kitchen", "rent", "paper", "insurance", "procurement", "finance", "recruitment", "accounting",
        "lodging", "paints", "equipment", "antivirus", "fitness", "recycling", "pumps", "propane", "irrigation", "hospitality",
        "construction", "water", "hotel", "burglar", "electricity", "plumbing", "cyber", "machines", "gas", "textile",
        "dietary", "vacation", "oil", "music", "automobile", "healthcare", "laundry", "agriculture", "restaurant", "payroll",
        "uniforms", "landscaping", "beverage", "lumber", "manufacturing", "chemicals", "apparel", "alcohol", "electronics",
        "furniture"
    ]
)

# Get the top 5 labels
top5_indices = sorted(range(len(result['scores'])), key=lambda i: result['scores'][i], reverse=True)[:5]
extracted_keywords = [result['labels'][j] for j in top5_indices]

# Initialize variables to keep track of the highest count and corresponding 'pos' values
max_count = 0
max_pos_values = []

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    # Check if the 'keywords' column is a string
    if isinstance(row['keywords'], str):
        # Split the 'keywords' string into a list of keywords
        label_keywords = row['keywords'].split(', ')
    else:
        # Handle the case where the 'keywords' column is not a string (e.g., it's a float)
        label_keywords = []

    # Initialize count for each row
    count_matches = 0

    # Count how many keywords from the extracted keywords exactly match the keywords in the current row
    for keyword in extracted_keywords:
        if keyword in label_keywords:
            count_matches += 1

    # Check if the current count is equal to the maximum count
    if count_matches == max_count:
        max_pos_values.append(row['pos'])
    # Check if the current count is higher than the maximum count
    elif count_matches > max_count:
        max_count = count_matches
        max_pos_values = [row['pos']]

# Print the 'pos' values with the highest count of matches
print(f"The 'pos' values with the highest count of matches are: {', '.join(max_pos_values)} with count {max_count}")

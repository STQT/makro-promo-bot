import json
from openpyxl import Workbook

def load_progress():
    try:
        with open('progress.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


data = load_progress()

# Create a new workbook and worksheet
output_workbook = Workbook()
output_sheet = output_workbook.active

# Add headers to the output sheet
output_sheet.append(["Promo", "Phone", "Fullname", "Promotion", "Code", "Created At"])

# Write data to the output sheet
for promo_value, info in data.items():
    if info is True:
        continue  # Skip if promo value is True
    output_sheet.append([
        promo_value,
        info["Phone"],
        info["Fullname"],
        info["Promotion"],
        info["Code"],
        info["Created At"]
    ])

# Save the output workbook
output_workbook.save("output.xlsx")

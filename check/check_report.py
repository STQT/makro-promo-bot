import requests
from openpyxl import Workbook
from openpyxl.reader.excel import load_workbook

# Load the promo.xlsx file
promo_workbook = load_workbook('promo.xlsx')
promo_sheet = promo_workbook.active

# Create a new workbook and worksheet
output_workbook = Workbook()
output_sheet = output_workbook.active

# Add headers to the output sheet
output_sheet.append(["Phone", "Fullname", "Promotion", "Code", "Created At"])
token = ""

for num, promo_row in enumerate(promo_sheet.iter_rows(min_row=2, values_only=True)):
    promo_value = str(promo_row[0])
    api_url = f'https://bot.makromarket.uz/promo/{promo_value}/'
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(api_url, headers=headers)
    print(response)
    if response.status_code == 200:
        data = response.json()
        user = data["user"]
        if "phone" in user and "fullname" in user:
            output_sheet.append([
                user["phone"],
                user["fullname"],
                data["promotion"],
                data["code"],
                data["created_at"]
            ])
    print(num)

# Save the output workbook
output_workbook.save("output.xlsx")

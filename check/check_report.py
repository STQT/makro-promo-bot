from openpyxl import load_workbook

# Load the promo.xlsx file
promo_workbook = load_workbook('promo.xlsx')
promo_sheet = promo_workbook.active

# Load the bot.xlsx file
bot_workbook = load_workbook('bot.xlsx')
bot_sheet = bot_workbook.active

# Iterate over the rows in bot.xlsx
for i, bot_row in enumerate(bot_sheet.iter_rows(min_row=2, values_only=True), start=2):
    bot_value = str(bot_row[2])  # Assuming the value is in the third column
    exists = any(bot_value == str(promo_row[0]) for promo_row in promo_sheet.iter_rows(min_row=2, values_only=True))
    result = 'exists' if exists else 'nonexists'

    # Write the result to the fifth column
    bot_sheet.cell(row=i, column=6, value=result)

# Save the changes to bot.xlsx
bot_workbook.save('bot.xlsx')

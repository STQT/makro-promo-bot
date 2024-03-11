from openpyxl import load_workbook

# Load the promo.xlsx file
promo_workbook = load_workbook('promo.xlsx')
promo_sheet = promo_workbook.active

# Load the bot2.xlsx file
bot_workbook = load_workbook('bot.xlsx')
bot_sheet = bot_workbook.active

# Iterate over the rows in bot2.xlsx
for i, bot_row in enumerate(bot_sheet.iter_rows(min_row=2, values_only=True), start=2):
    bot_value = str(bot_row[3])  # Assuming the value is in the third column
    for promo_row in promo_sheet.iter_rows(min_row=2, values_only=True):
        promo_value = str(promo_row[0])
        exists = bot_value == promo_value
        result = 'Существует' if exists else 'Не существует'
        # Write the result to the fifth column
        bot_sheet.cell(row=i, column=6, value=result)

# Save the changes to bot2.xlsx
bot_workbook.save('final.xlsx')

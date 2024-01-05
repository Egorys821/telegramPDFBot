import os

import telebot
from pdf2image.pdf2image import convert_from_path, pdfinfo_from_path

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Hello this is simple bot to convert .pdf files to jpg!")
    bot.send_message(message.chat.id,"Send me .pdf file!")
@bot.message_handler(content_types=['document']) # list relevant content types
def addfile(message):
    file_name = message.document.file_name
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    if file_name[-3:] != "pdf":
        bot.send_message(message.chat.id,"please send .pdf file :)")
        return
   
    pdf_path = f"files/{file_name}"
    
    with open(f"files/{file_name}", 'wb') as new_file:
        new_file.write(downloaded_file)
        try:

            info = pdfinfo_from_path(pdf_path)
            page_index = 1
            maxPages = info["Pages"]

            bot.send_message(message.chat.id, "here they are:")

            for page in range(1, maxPages+1, 5) : 

                pages = convert_from_path(pdf_path, dpi=200, first_page=page, last_page = min(page+5-1,maxPages))
            
                for count,page in enumerate(pages):
                    page.save(f"files/{file_name[:-4]}_{page_index}.jpg","JPEG")
                    bot.send_document(message.chat.id,open(f"files/{file_name[:-4]}_{page_index}.jpg","rb"))
                    page_index += 1
                    os.remove(f"files/{file_name[:-4]}_{page_index-1}.jpg")
        except:
            bot.send_message(message.chat.id, "Something's wrong I can feel it...")

           
          
    bot.send_message(message.chat.id,f"{message.from_user.first_name} send me more pdf files!😋")

    os.remove(f"files/{file_name}")

bot.infinity_polling()


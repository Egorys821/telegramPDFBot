import os

import telebot
from pdf2image.pdf2image import convert_from_path

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
    with open(f"files/{file_name}", 'wb') as new_file:
        new_file.write(downloaded_file)
        bot.send_message(message.chat.id, "here they are:")
        images = convert_from_path(f'files/{file_name}')

        for i in range(len(images)):
            images[i].save(f"{file_name[:-4]}_{i+1}.jpg","JPEG")
            
            with open(f"{file_name[:-4]}_{i+1}.jpg",'rb') as jpg_file:
                
                #bot.send_photo(message.chat.id,jpg_file)
                bot.send_document(message.chat.id, jpg_file)
                os.remove(f'{file_name[:-4]}_{i+1}.jpg')
    os.remove(f"files/{file_name}")
    bot.send_message(message.chat.id,"Send me more pdf files!😋")

bot.infinity_polling()

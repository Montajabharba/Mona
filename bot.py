
import telebot
import subprocess
import os

bot = telebot.TeleBot("7543186302:AAE7SroDFFpN0mpF_5qSSPtNfYASCo0iIUc")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أرسل لي فيديو وسأقوم بضغطه وإرساله لك بجودة أقل.")

@bot.message_handler(content_types=['video', 'document'])
def handle_video(message):
    try:
        file_info = bot.get_file(message.video.file_id if message.content_type == 'video' else message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        input_filename = "input.mp4"
        output_filename = "output_compressed.mp4"

        with open(input_filename, 'wb') as f:
            f.write(downloaded_file)

        compress_command = [
            "ffmpeg", "-i", input_filename,
            "-vcodec", "libx264", "-crf", "28",
            "-preset", "fast", "-vf", "scale=-2:480",
            output_filename
        ]

        subprocess.run(compress_command, check=True)

        with open(output_filename, 'rb') as out_f:
            bot.send_video(message.chat.id, out_f, caption="✅ تم ضغط الفيديو.")

        os.remove(input_filename)
        os.remove(output_filename)

    except Exception as e:
        bot.reply_to(message, f"حدث خطأ أثناء الضغط: {str(e)}")

print("🤖 Bot is running...")
bot.infinity_polling()

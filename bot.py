import messages
import photoChecker

import os
import logging

from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
from telegram.error import Forbidden


load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger("my_logger")
logger.setLevel(logging.ERROR)

handler = RotatingFileHandler("error_log.log", maxBytes=1000000, backupCount=5)
handler.setLevel(logging.ERROR)

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

logger = logging.getLogger(__name__)
TIMEOUT = 15


async def checkPhotos(update: Update, context: ContextTypes.DEFAULT_TYPE, photos, member) -> bool:
    chat_id = update.message.chat_id
    groupName = update.effective_chat.title
    user_id = member.id

    isValid = False

    for i in range(photos.total_count):
        file_id = photos.photos[i][0].file_id
        file = await context.bot.get_file(file_id)

        path = f'{user_id + i}_profile_photo.jpg'
        photo = await file.download_to_drive(path)
        isValid = photoChecker.checkIsSelfie(path)

        if isValid is True:
            os.remove(path)
            return True
        # if isValid is False:
        #     await messages.sendMsgToAdmins(chat_id, context, await messages.ValidationErrorToAdmins(member, groupName, f"Missing face in {i + 1} image"))
        #     await messages.sendPhotoToAdmins(chat_id, context, photo)
        #     # await context.bot.ban_chat_member(update.message.chat_id, member.id)
        #     return False

        os.remove(path)
    
    return isValid

async def allGreetingMessages(update: Update, context: ContextTypes.DEFAULT_TYPE, member) -> None:
    chat_id = update.message.chat_id
    inviter = update.message.from_user
    user_id = member.id
    first_name = member.first_name
    last_name = member.last_name

    try:
        msg = await messages.welcome_message(first_name, last_name)
        await context.bot.send_message(user_id, msg)
        await context.bot.send_message(user_id, messages.RULES)
    except Forbidden:
        msg = first_name + " " + last_name + " " + messages.BLOCK_MSG
        await messages.sendMsgToAdmins(chat_id, context, msg)

    message = f"Բարի գալուստ 🎉: {first_name} {last_name} 👋\nնա միացել է {inviter.first_name} {inviter.last_name} հրավերով ✉️"
    await context.bot.send_message(chat_id, message)


async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    groupName = update.effective_chat.title

    for member in update.message.new_chat_members:
        if member.is_bot:
            continue
        
        user_id = member.id

        if member.last_name is None:
            await messages.sendMsgToAdmins(chat_id, context, await messages.ValidationErrorToAdmins(member, groupName, messages.NO_LAST_NANE_MSG))
            await context.bot.send_message(user_id, await messages.ValidationErrorToUser(messages.LAST_NAME))
            await context.bot.ban_chat_member(update.message.chat_id, member.id)
            return

        photos = await context.bot.get_user_profile_photos(user_id)

        match photos.total_count:
            case 0:
                await messages.sendMsgToAdmins(chat_id, context, await messages.ValidationErrorToAdmins(member, groupName, messages.NO_PROFILE_PHOTO_MSG))
                await context.bot.send_message(user_id, await messages.ValidationErrorToUser(messages.PROFILE_PHOTO_MSG))
                await context.bot.ban_chat_member(update.message.chat_id, member.id)
            case _:
                isValid = await checkPhotos(update, context, photos, member)
                if isValid:
                    await allGreetingMessages(update, context, member)
                else:
                    await messages.sendMsgToAdmins(chat_id, context, await messages.ValidationErrorToAdmins(member, groupName, messages.NO_PROFILE_PHOTO_MSG))
                    await context.bot.send_message(user_id, await messages.ValidationErrorToUser(messages.NO_PROFILE_PHOTO_MSG))

                    

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    exist = await messages.contains_cross_words(update.message.text)
    firstname  = update.message.from_user.first_name
    lastname  = update.message.from_user.last_name
    
    if exist is True:
        chat_id = update.message.chat_id
        msg = firstname + " " + lastname + "-ի հաղորդագրությունը հեռացվել է։ Հաղորդագրությունը եղել է՝ " + update.message.text + " 🗑️"
        await messages.sendMsgToAdmins(chat_id, context, msg)
        await context.bot.delete_message(chat_id, message_id=update.message.message_id)



def main() -> None:
    TOKEN = os.getenv("TOKEN")
    application = Application.builder().token(TOKEN).build()

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # application.add_handler(ChatMemberHandler(new_member, ChatMemberHandler.CHAT_MEMBER))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))

    application.run_polling()

if __name__ == '__main__':
    main()



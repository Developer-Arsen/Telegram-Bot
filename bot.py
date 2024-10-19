import messages
import photoChecker
import os

from dotenv import load_dotenv
from logger_config import setup_logger 

from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from telegram.error import Forbidden

load_dotenv()

logger = setup_logger()
logger.info("Bot has started.")

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
    except Forbidden as e:
        logger.error(f"Forbidden: Cannot send a message to user {first_name} {last_name} (ID: {user_id}). Exception: {str(e)}")
        msg = first_name + " " + last_name + " " + messages.BLOCK_MSG
        await messages.sendMsgToAdmins(chat_id, context, msg)
    except Exception as e:
        logger.error(f"Unexpected error when greeting {first_name} {last_name}: {str(e)}")

    message = f"Բարի գալուստ 🎉: {first_name} {last_name} 👋\nնա միացել է {inviter.first_name} {inviter.last_name} հրավերով ✉️"
    await context.bot.send_message(chat_id, message)

async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    groupName = update.effective_chat.title

    for member in update.message.new_chat_members:
        if member.is_bot:
            logger.info(f"A bot ({member.first_name}) tried to join the group {groupName}, ignoring it.")
            continue

        user_id = member.id
        logger.info(f"New member {member.first_name} {member.last_name} (ID: {user_id}) joined the group {groupName}.")

        if member.last_name is None:
            await messages.sendMsgToAdmins(chat_id, context, await messages.ValidationErrorToAdmins(member, groupName, messages.NO_LAST_NANE_MSG))
            await context.bot.send_message(user_id, await messages.ValidationErrorToUser(messages.LAST_NAME))
            await context.bot.ban_chat_member(update.message.chat_id, member.id)
            logger.warning(f"User {member.first_name} (ID: {user_id}) was banned due to missing last name.")
            return

        photos = await context.bot.get_user_profile_photos(user_id)

        try:
            match photos.total_count:
                case 0:
                    await messages.sendMsgToAdmins(chat_id, context, await messages.ValidationErrorToAdmins(member, groupName, messages.NO_PROFILE_PHOTO_MSG))
                    await context.bot.send_message(user_id, await messages.ValidationErrorToUser(messages.NO_PROFILE_PHOTO_MSG))
                    await context.bot.ban_chat_member(update.message.chat_id, member.id)
                    logger.warning(f"User {member.first_name} (ID: {user_id}) was banned due to no profile photo.")
                case _:
                    isValid = await checkPhotos(update, context, photos, member)
                    if isValid:
                        await allGreetingMessages(update, context, member)
                    else:
                        print("here", isValid)
                        await messages.sendMsgToAdmins(chat_id, context, await messages.ValidationErrorToAdmins(member, groupName, messages.PROFILE_PHOTO_MSG))
                        print("here1")
                        await context.bot.ban_chat_member(update.message.chat_id, member.id)
                        print("here2")
                        await context.bot.send_message(user_id, await messages.ValidationErrorToUser(messages.PROFILE_PHOTO_MSG))
                        print("here3")

                        logger.warning(f"User {member.first_name} (ID: {user_id}) was banned due to an invalid profile photo.")
        except Forbidden as e:
            await context.bot.ban_chat_member(update.message.chat_id, member.id)
            logger.error(f"Forbidden: Cannot send a message to user {member.first_name} {member.last_name} (ID: {user_id}). Exception: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error occurred when handling new member {member.first_name} {member.last_name}: {str(e)}")

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
        logger.info(f"Deleted a message from {firstname} {lastname} due to inappropriate content.")

def main() -> None:
    TOKEN = os.getenv("TOKEN")
    application = Application.builder().token(TOKEN).build()

    logger.info("Starting the bot.")
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))

    application.run_polling()

if __name__ == '__main__':
    main()

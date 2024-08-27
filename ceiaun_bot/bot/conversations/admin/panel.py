from telegram import Update

import settings
from bot import consts, keyboards, messages
from bot.context import CustomContext


async def panel_handler(update: Update, context: CustomContext):
    if update.effective_user.id not in settings.ADMIN_IDS:
        return consts.STATE_HOME

    text = update.message.text

    if text == keyboards.ADMIN_STAT:
        await update.message.reply_text(
            text=messages.ADMIN_STAT.format(
                request_count=len(context.request_list),
                summer_request_count=len(context.summer_request_list),
                users_count=len(context.bot_user_ids),
            ),
            reply_markup=keyboards.ADMIN_KEYBOARD,
            quote=True,
        )

        return consts.STATE_ADMIN

    if text == keyboards.ADMIN_GET_FILE:
        if len(context.request_list) == 0:
            await update.message.reply_text(
                text=messages.ADMIN_GET_FILE_NONE,
                reply_markup=keyboards.ADMIN_KEYBOARD,
                quote=True,
            )
            return None

        await update.message.reply_text(
            text=messages.ADMIN_GET_FILE_TITLE,
            reply_markup=keyboards.BACK_KEYBOARD,
            quote=True,
        )

        return consts.STATE_ADMIN_GET_FILE

    if text == keyboards.ADMIN_GET_FILE_ID:
        await update.message.reply_text(
            text=messages.ADMIN_GET_FILE_ID,
            reply_markup=keyboards.BACK_KEYBOARD,
            quote=True,
        )

        return consts.STATE_ADMIN_FILE_ID

    if text == keyboards.ADMIN_CLEAN_REQUEST_LIST:
        await update.message.reply_text(
            text=messages.ADMIN_CLEAN_REQ_LIST,
            reply_markup=keyboards.BACK_KEYBOARD,
            quote=True,
        )

        return consts.STATE_ADMIN_CLEAN_REQ

    if text == keyboards.ADMIN_SEND_MESSAGE:
        await update.message.reply_text(
            text=messages.ADMIN_SEND_MSG_GET,
            reply_markup=keyboards.BACK_KEYBOARD,
            quote=True,
        )

        return consts.STATE_ADMIN_SEND_MSG

    if text == keyboards.ADMIN_GET_SUMMER_REQUESTS:
        await update.message.reply_text(
            text=messages.ADMIN_SUMMER_REQUEST_TITLE,
            reply_markup=keyboards.BACK_KEYBOARD,
            quote=True,
        )

        return consts.STATE_ADMIN_SUMMER_REQUEST

    if text == keyboards.ADMIN_CLEAN_SUMMER_REQUESTS:
        await update.message.reply_text(
            text=messages.ADMIN_CLEAN_SUMMER_REQUEST_TITLE,
            reply_markup=keyboards.BACK_KEYBOARD,
            quote=True,
        )

        return consts.STATE_ADMIN_CLEAN_SUMMER_REQUEST

    if text == keyboards.ADMIN_SEND_MESSAGE_TO_ALL:
        await update.message.reply_text(
            text=messages.ADMIN_SEND_MSH_TO_ALL,
            reply_markup=keyboards.BACK_KEYBOARD,
            quote=True,
        )

        return consts.STATE_ADMIN_SEND_MSG_TO_ALL

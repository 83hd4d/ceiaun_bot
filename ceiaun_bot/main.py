import logging

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    AIORateLimiter,
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    Defaults,
    MessageHandler,
    PersistenceInput,
    PicklePersistence,
    TypeHandler,
    filters,
)

import settings
from bot import consts
from bot.context import CustomContext
from bot.conversations import admin as admin_handlers, user as user_handlers

logger = logging.getLogger(__name__)

CONVS = {
    # User
    consts.STATE_HOME: user_handlers.home_handler,
    consts.STATE_REQUEST_COURSE: user_handlers.request_course_handler,
    consts.STATE_CONVERT_COURSE: user_handlers.convert_course_handler,
    consts.STATE_SUMMER_REQUEST_GET_NAME: user_handlers.summer_request_get_name_handler,
    # Admin
    consts.STATE_ADMIN: admin_handlers.panel_handler,
    consts.STATE_ADMIN_GET_FILE: admin_handlers.get_requests_file_handler,
    consts.STATE_ADMIN_FILE_ID: admin_handlers.get_file_id_handler,
    consts.STATE_ADMIN_CLEAN_REQ: admin_handlers.clean_request_list_handler,
    consts.STATE_ADMIN_SEND_MSG: admin_handlers.send_message_to_user_handler,
    consts.STATE_ADMIN_SUMMER_REQUEST: admin_handlers.get_summer_requests_file_handler,
    consts.STATE_ADMIN_CLEAN_SUMMER_REQUEST: admin_handlers.clean_summer_request_list_handler,
    consts.STATE_ADMIN_SEND_MSG_TO_ALL: admin_handlers.send_message_to_all_handler,
}

INLINE_CONVS = {
    consts.STATE_SUMMER_REQUEST: user_handlers.summer_request_handler,
    consts.STATE_SUMMER_REQUEST_GET_NAME: user_handlers.summer_request_get_name_handler,
}

CONVS_DOC = {
    # Admin
    consts.STATE_ADMIN_FILE_ID: admin_handlers.get_file_id_handler,
}


async def state_handler(update: Update, context: CustomContext):
    user_state = context.user_state

    result = await CONVS[user_state](update, context)
    context.user_state = result


async def inline_state_handler(update: Update, context: CustomContext):
    if context.user_last_inline_message and context.user_last_inline_message != update.callback_query.message.id:
        return None

    user_state = context.user_state

    if user_state in INLINE_CONVS:
        result = await INLINE_CONVS[user_state](update, context)
        context.user_state = result


async def document_state_handler(update: Update, context: CustomContext):
    user_state = context.user_state

    result = await CONVS_DOC[user_state](update, context)
    context.user_state = result


async def track_users(update: Update, context: CustomContext) -> None:
    """Store the user id of the incoming update, if any."""
    if update.effective_user and update.effective_user.id not in context.bot_user_ids:
        user_id = update.effective_user.id
        username = update.effective_user.username
        user_full_name = update.effective_user.full_name

        context.bot_user_ids.add(user_id)
        logger.info(f"New user: {user_id} / username: @{username} / full name: {user_full_name}")


async def error(update: Update, context: CustomContext):
    logger.warning(f"Error {context.error} for update {update}")


def run():
    # Persistent data
    persistence = PicklePersistence(
        filepath=settings.BOT_DATABASE_DIR / "bot",
        store_data=PersistenceInput(chat_data=False, callback_data=False),
        single_file=False,
        update_interval=settings.BOT_DATABASE_UPDATE_INTERVAL,
    )

    # Default
    defaults = Defaults(parse_mode=ParseMode.HTML, disable_web_page_preview=True)

    context_types = ContextTypes(context=CustomContext)
    app = (
        Application.builder()
        .token(settings.BOT_TOKEN)
        .defaults(defaults)
        .context_types(context_types)
        .rate_limiter(AIORateLimiter())
        .persistence(persistence)
        .build()
    )

    admin_filter = filters.User(user_id=settings.ADMIN_IDS)

    app.add_handler(TypeHandler(Update, track_users), group=-1)
    app.add_handlers(
        [
            CommandHandler("start", user_handlers.start_command_handler),
            CommandHandler("panel", admin_handlers.start_command_handler, filters=admin_filter),
            MessageHandler(filters.TEXT, state_handler),
            MessageHandler(filters.Document.ALL, document_state_handler),
            CallbackQueryHandler(inline_state_handler),
        ]
    )

    # Errors
    app.add_error_handler(error)

    app.run_polling(allowed_updates=[Update.MESSAGE, Update.CALLBACK_QUERY])


if __name__ == "__main__":
    run()

import os
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

SPECIALISTS = [
    "Маркетолог",
    "SMM-специалист",
    "Разработчик чат-ботов",
    "Разработчик сайтов на WordPress"
]

INFO = {
    "Маркетолог": (
        "Чем занимается:\n"
        "Анализирует рынок, разрабатывает стратегию продвижения, настраивает рекламу, помогает увеличить продажи.\n\n"
        "Выгоды:\n"
        "Рост клиентов и продаж, экономия бюджета на рекламу, понимание целевой аудитории.\n\n"
        "Как оценить:\n"
        "Смотрите на реальные кейсы и результаты (рост заявок, продаж, трафика). Запросите отчёты по кампаниям и аналитику."
    ),
    "SMM-специалист": (
        "Чем занимается:\n"
        "Продвигает бренд или продукт в соцсетях (Instagram, Facebook и др.).\n"
        "— Создание и публикация контента (посты, сторис, видео)\n"
        "— Разработка стратегии продвижения\n"
        "— Взаимодействие с аудиторией (ответы на комментарии, сообщения)\n"
        "— Настройка и анализ рекламы\n"
        "— Мониторинг трендов и аналитика\n\n"
        "Выгоды:\n"
        "Рост узнаваемости бренда, привлечение новых клиентов, активное сообщество, увеличение продаж через соцсети.\n\n"
        "Как оценить:\n"
        "Смотрите портфолио и активные проекты, оценивайте качество контента, рост подписчиков и вовлечённость, запрашивайте результаты рекламных кампаний.\n\n"
        "Важно:\n"
        "SMM-специалист должен уметь писать тексты, делать базовый дизайн, разбираться в аналитике и знать особенности платформ."
    ),
    "Разработчик чат-ботов": (
        "Чем занимается:\n"
        "Создаёт автоматические сценарии общения, интегрирует ботов с CRM и мессенджерами, автоматизирует ответы и заявки.\n\n"
        "Выгоды:\n"
        "Экономия времени на рутине, быстрые ответы клиентам 24/7, увеличение заявок без увеличения штата.\n\n"
        "Как оценить:\n"
        "Попросите показать работающие боты. Оцените удобство сценария, интеграции, скорость и качество ответов."
    ),
    "Разработчик сайтов на WordPress": (
        "Чем занимается:\n"
        "Создаёт сайты и интернет-магазины, настраивает дизайн, функционал, безопасность и скорость загрузки.\n\n"
        "Выгоды:\n"
        "Современный сайт, который продаёт, простое управление контентом, быстрая загрузка и защита от взлома.\n\n"
        "Как оценить:\n"
        "Посмотрите готовые сайты. Проверьте адаптивность (на телефоне и ПК), скорость загрузки, удобство управления."
    ),
}

def get_specialists_keyboard():
    return ReplyKeyboardMarkup([[s] for s in SPECIALISTS], resize_keyboard=True, one_time_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Выберите специалиста:",
        reply_markup=get_specialists_keyboard()
    )

async def handle_specialist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text in INFO:
        await update.message.reply_text(
            INFO[text],
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Заказать бесплатный аудит", callback_data=f"audit_{text}")],
                [InlineKeyboardButton("Выбрать другого специалиста", callback_data="choose_specialist")]
            ])
        )
    else:
        await update.message.reply_text(
            "Пожалуйста, выберите специалиста из списка.",
            reply_markup=get_specialists_keyboard()
        )

async def handle_audit_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == "choose_specialist":
        await query.answer()
        # Отправляем новое сообщение с клавиатурой выбора специалистов
        await query.message.reply_text(
            "Выберите специалиста:",
            reply_markup=get_specialists_keyboard()
        )
    elif query.data.startswith("audit_"):
        await query.answer()
        await query.edit_message_text(
            "Спасибо за интерес! Выберите удобный способ связи:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Написать в Telegram", url="https://t.me/belarus79")],
                [InlineKeyboardButton("Позвонить", url="tel:+48504776929")]
            ])
        )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_specialist))
    app.add_handler(CallbackQueryHandler(handle_audit_callback))
    app.run_polling()

if __name__ == "__main__":
    main()

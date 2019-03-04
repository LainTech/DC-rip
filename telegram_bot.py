import argparse
import pickle

from telegram.ext import Updater, CommandHandler

from lifechecker import Server

subscribers = set()
server = Server('89.188.9.59')
server.add_service('nginx', 80)
server.add_service('BIND', 53)
last_update = server.get_status()[1]


def load_subscribers():
    global subscribers
    try:
        with open('subscribers.pickle', 'rb') as f:
            subscribers = pickle.load(f)
    except:
        save_subscribers()


def save_subscribers():
    with open('subscribers.pickle', 'wb') as f:
        pickle.dump(subscribers, f)


def status(update, context):
    """Send current server status."""
    update.message.reply_text(server.get_status()[0])


def subscribe(update, context):
    """Subscribe user for notification."""
    chatid = update.effective_chat.id
    if chatid in subscribers:
        update.message.reply_text('You are already subscribed')
    else:
        subscribers.add(chatid)
        update.message.reply_text('Subscribed')
    save_subscribers()


def unsubscribe(update, context):
    """Unsubscribe user from notification."""
    chatid = update.effective_chat.id
    if chatid in subscribers:
        subscribers.remove(chatid)
        update.message.reply_text('Unsubscribed')
    else:
        update.message.reply_text('You have not subscribed')
    save_subscribers()


def notify_subscribers(context):
    """Check server state updates and sent them to users"""
    global last_update
    update = server.get_status()
    if update[1] is not last_update:
        last_update = update[1]
        for subscriber in subscribers:
            context.bot.send_message(chat_id=subscriber, text=update[0])


def main():
    updater = Updater(args.bot_token, use_context=True)
    dp = updater.dispatcher

    job_queue = updater.job_queue
    job_queue.run_repeating(notify_subscribers, 10, 0)

    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("subscribe", subscribe))
    dp.add_handler(CommandHandler("unsubscribe", unsubscribe))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('bot_token', help='Telegram bot token')
    args = parser.parse_args()
    load_subscribers()
    main()

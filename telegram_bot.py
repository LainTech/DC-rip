import argparse
import pickle

from telegram.ext import Updater, CommandHandler

from lifechecker import Server

subscribers = set()


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


def add_subscriber(id):
    subscribers.add(id)
    save_subscribers()


def remove_subscriber(id):
    subscribers.remove(id)
    save_subscribers()


def status(update, context):
    """Send current server status."""
    update.message.reply_text(server.get_status()[0])


def subscribe(update, context):
    """Subscribe user for notification."""
    chatid = update.effective_chat.id
    if chatid in subscribers:
        update.message.reply_text('You are already subscribed')
    else:
        add_subscriber(chatid)
        update.message.reply_text('Subscribed')


def unsubscribe(update, context):
    """Unsubscribe user from notification."""
    chatid = update.effective_chat.id
    if chatid in subscribers:
        remove_subscriber(chatid)
        update.message.reply_text('Unsubscribed')
    else:
        update.message.reply_text('You have not subscribed')


def notify_subscribers(context):
    """Check server state updates and sent them to users"""
    global last_update
    update = server.get_status()
    to_remove = set()
    if update[1] is not last_update:
        last_update = update[1]
        for subscriber in subscribers:
            try:
                context.bot.send_message(chat_id=subscriber, text=update[0])
            except:
                to_remove.add(subscriber)
    for id in to_remove:
        # Remove blocked chat
        remove_subscriber(id)


def main():
    updater = Updater(args.bot_token, use_context=True)
    dp = updater.dispatcher
    job_queue = updater.job_queue
    job_queue.run_repeating(notify_subscribers, args.interval, 0)

    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("subscribe", subscribe))
    dp.add_handler(CommandHandler("unsubscribe", unsubscribe))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('bot_token', type=str, help='Telegram bot token')
    parser.add_argument('host', type=str, help='Host address')
    parser.add_argument('services', type=str,
                        help='Comma separated service:port. Example: nginx:80,bind:53')
    parser.add_argument('-i', dest='interval', default=60,
                        help='Availability check interval in seconds. Default is 60')
    args = parser.parse_args()

    # Init Server
    server = Server(args.host)
    services = args.services.split(',')
    for service in services:
        service = service.split(':')
        server.add_service(service[0], int(service[1]))

    last_update = server.get_status()[1]
    load_subscribers()
    main()

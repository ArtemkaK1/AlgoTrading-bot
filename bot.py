import time
import json
from telegram.ext import Updater, CommandHandler
# https://python-telegram-bot.readthedocs.io/en/stable/telegram.html
from calculations import get_price, count_profit, count_price_fall, should_i_buy


TOKEN = '5178141240:AAHYjCOJozUqGa8pj1JOY4H6pqQnLEuY-Uo'


def make_money(update, context):
    chat_id = update.effective_chat.id

    while True:
        with open('cryptocoins.json', 'r') as my_coins_data:
            my_coins = json.loads(my_coins_data.read())

        final_message = []

        for coin_name in my_coins.keys():
            coin = my_coins[coin_name]
            coin_price = get_price(coin_name)

            possible_profit = count_profit(coin, coin_price)
            price_fall = count_price_fall(coin, coin_price)
            last_prices = coin['last_prices']

            if len(last_prices) <= 60:
                last_prices.append(coin_price)
                if len(last_prices) <= 59:
                    price_fall = 0
                    # not enough data to provide correct calculations
            else:
                last_prices = last_prices[1:] + [coin_price]

            my_coins[coin_name]['last_prices'] = last_prices
            message = ''

            if coin_price >= coin['desired_sell_price'] and coin['amount'] > 0:
                message += f'{coin_name} --> TIME TO SELL\n'
                message += f'possible profit = {possible_profit}$'
            else:
                if should_i_buy(price_fall, coin['desired_price_fall'], coin_price):
                    message += f'{coin_name} --> TIME TO BUY\n'
                    message += f'price fall = {round(price_fall / coin_price * 100, 1)}%'
                else:
                    message += f'{coin_name} --> nothing to do right now...'

            final_message.append(message)
            time.sleep(2)

        with open('cryptocoins.json', 'w') as my_coins_data:
            my_coins_data.write(json.dumps(my_coins, sort_keys=True, indent=2))

        context.bot.send_message(chat_id=chat_id, text='\n'.join(final_message))

        time.sleep(60)  # run every minute


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('make_money', make_money))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
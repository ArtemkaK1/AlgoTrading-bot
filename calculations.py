import requests


"""
other possible urls:
api.binance.com
api1.binance.com
api2.binance.com
"""
API_URL = 'https://api3.binance.com/api/v3/avgPrice'


def get_price(coin: str) -> float:
    """
    :param coin: token name, e.g. BTC for Bitcoin, LTC for Litecoin
    :return: coin's current price in stable USDT. 1USDT ~ 1$ USA
    """
    data = {'symbol': f'{coin}USDT'}  # e.g. BTCUSDT
    response = requests.get(API_URL, data)
    return float(response.json()['price'])


def count_profit(coin: dict, current_price: float) -> float:
    """
    :param coin: e.g.:
         {"amount": 1.4466,
          "buy_price": 200,
          "desired_sell_price": 219,
          "last_five_prices":  [201.4, 205, 203, 211, 222.2],
          "desired_price_fall":  10}
    :param current_price: coin's current price in stable USDT. 1USDT ~ 1$ USA
    :return: profit in USDT
    """
    # Example: (220 - 200) * 0.5 == 10
    return round((current_price - coin['buy_price']) * coin['amount'], 2)


def count_price_fall(coin: dict, current_price: float) -> float:
    """
    :param coin: same as in count_profit()
    :param current_price: same as in count_profit()
    :return: max diff between last 5 prices and current price, in USDT
    """
    # Example: max([201.4, 205, 203, 211, 222.2]) - 190 == 32.2
    try:
        return max(coin['last_five_prices']) - current_price
    except:
        # may happens if coin['last_five_prices'] is empty
        return 0


def should_i_buy(price_fall: float, desired_fall: float, current_price: float) -> bool:
    """
    :param price_fall: output of count_price_fall()
    :param desired_fall: desired price fall in PERCENTS! not in USDT. e.g. 10%
    :param current_price: coin's current price in stable USDT
    :return: True if you should buy, False otherwise
    """
    # Example: 21 / 200 * 100 == 10.5% and 10.5 >= 10, so -> True
    if price_fall / current_price * 100 >= desired_fall:
        return True
    return False
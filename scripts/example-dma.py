import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from logbook import Logger

from catalyst import run_algorithm
from catalyst.api import (record, symbol, order_target_percent)
from catalyst.exchange.utils.stats_utils import extract_transactions

NAMESPACE = 'dual_moving_average'
log = Logger(NAMESPACE)

def initialize(context):
    context.i = 0
    context.asset = symbol('btc_usdt')
    context.base_price = None

def handle_data(context, data):
    short_window = 50
    long_window = 200

    context.i += 1
    if context.i < long_window:
        return

    short_data = data.history(context.asset, 'price', bar_count=short_window, frequency="1m")
    short_mavg = short_data.mean()
    long_data = data.history(context.asset, 'price', bar_count=long_window, frequency='1m')
    long_mavg = long_data.mean()

    # keep the price of our asset in a more handy variable
    price = data.current(context.asset, 'price')

    if context.base_price is None:
        context.base_price = price
    price_change = (price - context.base_price) / context.base_price

    record(price = price,
           cash = context.portfolio.cash,
           price_change = price_change,
           short_mavg = short_mavg,
           long_mavg = long_mavg)

    orders = context.blotter.open_orders
    if len(orders) > 0:
        return

    if not data.can_trade(context.asset):
        return

    pos_amount = context.portfolio.positions[context.asset].amount

    ###################
    ## Trading logic ##
    ###################
    if short_mavg > long_mavg and pos_amount == 0:
        # we buy 100% of our portfolio for this asset
        order_target_percent(context.asset, 1)
    elif short_mavg < long_mavg and pos_amount > 0:
        # we sell all our positions for this asset
        order_target_percent(context.asset, 0)


def analyze(context, perf):
    # Get the base_currency that was passed as a parameter to the simulation
    exchange = list(context.exchanges.values())[0]
    base_currency = exchange.base_currency.upper()

    # First chart: Plot portfolio value using base_currency
    ax1 = plt.subplot(411)
    perf.loc[:, ['portfolio_value']].plot(ax=ax1)
    ax1.legend_.remove()
    ax1.set_ylabel('Portfolio Value\n({})'.format(base_currency))
    start, end = ax1.get_ylim()
    ax1.yaxis.set_ticks(np.arange(start, end, (end - start) / 5))

    # Second chart: Plot asset price, moving averages and buys/sells
    ax2 = plt.subplot(412, sharex=ax1)
    perf.loc[:, ['price', 'short_mavg', 'long_mavg']].plot(
        ax=ax2,
        label='Price')
    ax2.legend_.remove()
    ax2.set_ylabel('{asset}\n({base})'.format(
        asset=context.asset.symbol,
        base=base_currency
    ))
    start, end = ax2.get_ylim()
    ax2.yaxis.set_ticks(np.arange(start, end, (end - start) / 5))

    transaction_df = extract_transactions(perf)
    if not transaction_df.empty:
        buy_df = transaction_df[transaction_df['amount'] > 0]
        sell_df = transaction_df[transaction_df['amount'] < 0]
        ax2.scatter(
            buy_df.index.to_pydatetime(),
            perf.loc[buy_df.index, 'price'],
            marker='^',
            s=100,
            c='green',
            label=''
        )
        ax2.scatter(
            sell_df.index.to_pydatetime(),
            perf.loc[sell_df.index, 'price'],
            marker='v',
            s=100,
            c='red',
            label=''
        )

    # Third chart: Compare percentage change between our portfolio
    # and the price of the asset
    ax3 = plt.subplot(413, sharex=ax1)
    perf.loc[:, ['algorithm_period_return', 'price_change']].plot(ax=ax3)
    ax3.legend_.remove()
    ax3.set_ylabel('Percent Change')
    start, end = ax3.get_ylim()
    ax3.yaxis.set_ticks(np.arange(start, end, (end - start) / 5))

    # Fourth chart: Plot our cash
    ax4 = plt.subplot(414, sharex=ax1)
    perf.cash.plot(ax=ax4)
    ax4.set_ylabel('Cash\n({})'.format(base_currency))
    start, end = ax4.get_ylim()
    ax4.yaxis.set_ticks(np.arange(0, end, end / 5))

    plt.show()


if __name__ == '__main__':

    run_algorithm(
        capital_base=1000,
        data_frequency='minute',
        initialize=initialize,
        handle_data=handle_data,
        analyze=analyze,
        exchange_name='poloniex',
        algo_namespace=NAMESPACE,
        base_currency='usd',
        start=pd.to_datetime('2017-12-22', utc=True),
        end=pd.to_datetime('2017-12-23', utc=True),
    )
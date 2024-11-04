import matplotlib.pyplot as plt
import numpy as np


class Strategy:
    def __init__(self, options):
        assert len(options) == 2
        self.options = options

    def profit_straddle(self, operation, benchmark_price):
        strategy_profit = None
        two_price = self.options[0].price + self.options[1].price

        if operation == 'buy':
            if self.options[0].strike - two_price > benchmark_price and self.options[
                1].strike + two_price < benchmark_price:
                strategy_profit = 0
            elif benchmark_price > self.options[0].strike + two_price:
                strategy_profit = benchmark_price - self.options[0].strike - two_price
            elif benchmark_price < self.options[0].strike - two_price:
                strategy_profit = self.options[0].strike - two_price - benchmark_price

        if operation == 'sell':
            if benchmark_price > self.options[0].strike + two_price or benchmark_price < self.options[
                0].strike - two_price:
                strategy_profit = 0
            if benchmark_price > self.options[0].strike:
                strategy_profit = self.options[0].strike + two_price - benchmark_price
            elif benchmark_price < self.options[1].strike:
                strategy_profit = benchmark_price + two_price - self.options[1].strike
        return strategy_profit

    def profit_strangle(self, operation, benchmark_price):
        strategy_profit = None
        two_price = self.options[0].price + self.options[1].price

        if operation == 'buy':
            if benchmark_price < self.options[0].strike and benchmark_price > self.options[1].strike:
                strategy_profit = 0
            elif benchmark_price < self.options[1].strike:
                strategy_profit = self.options[1].strike - two_price - benchmark_price
            elif benchmark_price > self.options[0].strike:
                strategy_profit = benchmark_price - self.options[0].strike - two_price

        if operation == 'sell':
            if benchmark_price < self.options[0].strike and benchmark_price > self.options[1].strike:
                strategy_profit = two_price
            elif benchmark_price < self.options[1].strike:
                strategy_profit = benchmark_price + two_price - self.options[1].strike
            elif benchmark_price > self.options[0].strike:
                strategy_profit = self.options[0].strike + two_price - benchmark_price

        return strategy_profit

    def profit_spread(self, type_spread, benchmark_price):
        assert self.options[0].type == self.options[1].type
        assert self.options[0].strike != self.options[1].strike

        strategy_profit = None
        sell_option, buy_option = None, None

        if type_spread == 'call':
            if self.options[0].strike > self.options[1].strike:
                sell_option, buy_option = self.options[0], self.options[1]
            else:
                sell_option, buy_option = self.options[1], self.options[0]

            if benchmark_price < buy_option.strike:
                strategy_profit = - buy_option.price - sell_option.price
            elif benchmark_price > buy_option.strike and benchmark_price < sell_option.strike:
                strategy_profit = benchmark_price - buy_option.strike - buy_option.price - sell_option.price
            elif benchmark_price > sell_option.strike:
                strategy_profit = sell_option.strike - buy_option.strike - buy_option.price - sell_option.price

        if type_spread == 'put':
            if self.options[0].strike < self.options[1].strike:
                sell_option, buy_option = self.options[0], self.options[1]
            else:
                sell_option, buy_option = self.options[1], self.options[0]

            if benchmark_price < sell_option:
                strategy_profit = buy_option.strike - sell_option.strike - (buy_option.price + sell_option.price)
            elif benchmark_price > sell_option and benchmark_price < buy_option:
                strategy_price = buy_option - benchmark_price - (buy_option.price + sell_option.price)
            elif benchmark_price > buy_option:
                strategy_profit = - (buy_option.price + sell_option.price)

        return strategy_profit

    def plot_straddle(self, operation=None, benchmark_price=None):
        assert self.options[0].strike == self.options[1].strike
        assert self.options[0].type == 'call'
        assert self.options[1].type == 'put'

        if operation == 'buy':
            price_call = np.linspace(self.options[0].strike, self.options[0].strike + 10, 10)
            profit_call = np.linspace(0, 10, 10) - self.options[0].price

            price_put = np.linspace(self.options[1].strike - 10, self.options[1].strike, 10)
            profit_put = np.linspace(10, 0, 10) - self.options[1].price

            plt.plot(price_call, profit_call - self.options[0].price, 'b')
            plt.plot(price_put, profit_put - self.options[1].price, 'b')

            plt.xlabel("Price")
            plt.ylabel("Profit")
            plt.title("Buy straddle")
            plt.grid()
            plt.show()

        if operation == 'sell':
            price_call = np.linspace(self.options[0].strike, self.options[0].strike + 10, 10)
            profit_call = np.linspace(0, 10, 10) - self.options[0].price

            price_put = np.linspace(self.options[1].strike - 10, self.options[1].strike, 10)
            profit_put = np.linspace(10, 0, 10) - self.options[1].price

            plt.plot(price_call, -profit_call + self.options[0].price, 'b')
            plt.plot(price_put, -profit_put + self.options[1].price, 'b')

            plt.xlabel("Price")
            plt.ylabel("Profit")
            plt.title("Sell straddle")
            plt.grid()
            plt.show()

        if operation is None:
            raise Exception("Write operation type")

    def plot_strangle(self, operation=None):
        assert self.options[0].type == 'call'
        assert self.options[1].type == 'put'

        if operation == 'buy':
            price_call = np.linspace(self.options[0].strike, self.options[0].strike + 10, 10)
            profit_call = np.linspace(0, 10, 10) - self.options[0].price

            price_put = np.linspace(self.options[1].strike - 10, self.options[1].strike, 10)
            profit_put = np.linspace(10, 0, 10) - self.options[1].price

            strike_line = np.linspace(self.options[1].strike, self.options[0].strike, 10)
            double_price = np.full((10), - self.options[1].price - self.options[0].price)

            plt.plot(strike_line, double_price, 'b')
            plt.plot(price_call, profit_call - self.options[0].price, 'b')
            plt.plot(price_put, profit_put - self.options[1].price, 'b')

            plt.xlabel("Price")
            plt.ylabel("Profit")
            plt.title("Buy strangle")
            plt.grid()
            plt.show()

        if operation == 'sell':
            price_call = np.linspace(self.options[0].strike, self.options[0].strike + 10, 10)
            profit_call = np.linspace(0, 10, 10) - self.options[0].price

            price_put = np.linspace(self.options[1].strike - 10, self.options[1].strike, 10)
            profit_put = np.linspace(10, 0, 10) - self.options[1].price

            strike_line = np.linspace(self.options[1].strike, self.options[0].strike, 10)
            double_price = np.full((10), self.options[1].price + self.options[0].price)

            plt.plot(strike_line, double_price, 'b')
            plt.plot(price_call, -profit_call + self.options[0].price, 'b')
            plt.plot(price_put, -profit_put + self.options[1].price, 'b')

            plt.xlabel("Price")
            plt.ylabel("Profit")
            plt.title("Sell strangle")
            plt.grid()
            plt.show()

        if operation is None:
            raise Exception("Write operation type")

    def plot_spread(self, type_spread):
        assert self.options[0].type == self.options[1].type
        assert self.options[0].strike != self.options[1].strike

        sell_option, buy_option = None, None

        if type_spread == "call":
            if self.options[0].type == 'call':
                if self.options[0].strike > self.options[1].strike:
                    sell_option, buy_option = self.options[0], self.options[1]
                else:
                    sell_option, buy_option = self.options[1], self.options[0]

                price_line = np.linspace(buy_option.strike - 10, buy_option.strike, 10)
                double_price = np.full((10), - buy_option.price - sell_option.price)

                price_line_2 = np.linspace(buy_option.strike, sell_option.strike, 10)
                profit_line = np.linspace(- buy_option.price - sell_option.price,
                                          sell_option.strike - buy_option.strike - buy_option.price - sell_option.price,
                                          10)

                price_line_3 = np.linspace(sell_option.strike, sell_option.strike + 10, 10)
                profit_price = np.full((10),
                                       sell_option.strike - buy_option.strike - buy_option.price - sell_option.price)

                plt.plot(price_line, double_price, 'b')
                plt.plot(price_line_2, profit_line, 'b')
                plt.plot(price_line_3, profit_price, 'b')

                plt.title('Call spread')
                plt.xlabel('Price')
                plt.ylabel('Profit')

                plt.grid()
                plt.show()

            else:
                raise Exception("Both options type must be call")

        if type_spread == 'put':
            if self.options[0].type == 'put':
                if self.options[0].strike < self.options[1].strike:
                    sell_option, buy_option = self.options[0], self.options[1]
                else:
                    sell_option, buy_option = self.options[1], self.options[0]

                price_line = np.linspace(sell_option.strike - 10, sell_option.strike, 10)
                profit_price = np.full((10),
                                       buy_option.strike - sell_option.strike - buy_option.price - sell_option.price)

                price_line_2 = np.linspace(sell_option.strike, buy_option.strike, 10)
                profit_price_2 = np.linspace(
                    buy_option.strike - sell_option.strike - buy_option.price - sell_option.price,
                    - buy_option.price - sell_option.price, 10)

                price_line_3 = np.linspace(buy_option.strike, buy_option.strike + 10, 10)
                profit_price_3 = np.full((10), - buy_option.price - sell_option.price)

                plt.plot(price_line, profit_price, 'b')
                plt.plot(price_line_2, profit_price_2, 'b')
                plt.plot(price_line_3, profit_price_3, 'b')

                plt.title('Put spread')
                plt.xlabel('Price')
                plt.ylabel('Profit')

                plt.grid()
                plt.show()
            else:
                raise Exception("Both options type must be put")

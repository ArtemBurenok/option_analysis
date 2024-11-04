import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm


class Option:
    def __init__(self, name, strike, type, data_expiration, price=0,
                 delta=None, theta=None, vega=None, gamma=None):
        self.name = name
        self.price = price
        self.strike = strike
        self.type = type
        self.data_expiration = data_expiration
        self.delta = delta
        self.theta = theta
        self.vega = vega
        self.gamma = gamma

    def payback_point(self):
        point = 0
        if self.type == 'call':
            point = self.strike + self.price
        if self.type == 'put':
            point = self.strike - self.price
        return point

    def profit(self, operation, benchmark_price):
        if self.type == 'call':
            if operation == 'buy':
                return max(0, benchmark_price - self.payback_point())
            if operation == 'sell':
                return 0 if benchmark_price > self.payback_point() else max(self.price, self.payback_point() - benchmark_price)
        if self.type == 'put':
            if operation == 'buy':
                return max(0, self.payback_point() - benchmark_price)
            if operation == 'sell':
                return 0 if benchmark_price < self.payback_point() else max(self.price, benchmark_price - self.payback_point())

    def historical_volatility(self, spot_price_by_year):
        return spot_price_by_year.std() * np.sqrt(242)

    def balck_scholes_call(self, spot_price_by_year, spot_price, r, days):
        assert self.type == "call"
        volatility = self.historical_volatility(spot_price_by_year)
        T = days / 365

        d1 = (np.log(spot_price / self.strike) + (r + (volatility ** 2) / 2) * T) /  (volatility * np.sqrt(T))
        d2 = d1 - volatility * np.sqrt(T)
        price = spot_price * norm.cdf(d1) - self.strike * np.exp(-r * T) * norm.cdf(d2)
        return price

    def balck_scholes_put(self, spot_price_by_year, spot_price, r, days):
        assert self.type == "put"
        volatility = self.historical_volatility(spot_price_by_year)
        T = days / 365

        d1 = (np.log(spot_price / self.strike) + (r + (volatility ** 2) / 2) * T) /  (volatility * np.sqrt(T))
        d2 = d1 - volatility * np.sqrt(T)
        price = self.strike * np.exp(-r * T) * norm.cdf(-d2) - spot_price * norm.cdf(-d1)
        return price

    def greeks_calculus(self, spot_price_by_year, spot_price, r, days):
        volatility = self.historical_volatility(spot_price_by_year)
        T = days / 365
        d1 = (np.log(spot_price / self.strike) + (r + (volatility ** 2) / 2) * T) /  (volatility * np.sqrt(T))
        d2 = d1 - volatility * np.sqrt(T)

        delta = norm.cdf(d1)
        theta = -1 * spot_price * norm.pdf(d1) * volatility / (2 * np.sqrt(T)) + spot_price * norm.cdf(d1) - r * self.strike * norm.cdf(d2) * np.exp(- r * T)
        gamma = norm.pdf(d1) / (spot_price * volatility * np.sqrt(T))
        vega = spot_price * np.sqrt(T) * norm.pdf(d1)
        ro = self.strike * T * norm.cdf(d2)

        return delta, theta, gamma, vega, ro

    def plot_graphics(self, operation=None):
        if self.type == "call":
            if operation == 'buy':
                plt.plot(np.linspace(self.strike - 10, self.strike, 10), np.zeros(10) - self.price, 'b')
                price = np.linspace(self.strike, self.strike + 10, 10)
                profit = np.linspace(0, 10, 10) - self.price
                plt.plot(price, profit, 'b')
                plt.xlabel("Price")
                plt.ylabel("Profit")
                plt.title("Buy call")
                plt.grid()
                plt.show()
            if operation == 'sell':
                plt.plot(np.linspace(self.strike - 10, self.strike, 10), np.zeros(10) + self.price, 'b')
                price = np.linspace(self.strike, self.strike + 10, 10)
                profit = np.linspace(0, 10, 10) - self.price
                plt.plot(price, -profit, 'b')
                plt.xlabel("Price")
                plt.ylabel("Profit")
                plt.title("Sell call")
                plt.grid()
                plt.show()
            if operation is None:
                raise Exception("Write a operation type.")
        if self.type == 'put':
            if operation == 'buy':
                plt.plot(np.linspace(self.strike, self.strike + 10, 10), np.zeros(10) - self.price, 'b')
                price = np.linspace(self.strike - 10, self.strike , 10)
                profit = np.linspace(10, 0, 10) - self.price
                plt.plot(price, profit, 'b')
                plt.xlabel("Price")
                plt.ylabel("Profit")
                plt.title("Buy put")
                plt.grid()
                plt.show()
            if operation == 'sell':
                plt.plot(np.linspace(self.strike, self.strike + 10, 10), np.zeros(10) + self.price, 'b')
                price = np.linspace(self.strike - 10, self.strike , 10)
                profit = np.linspace(10, 0, 10) - self.price
                plt.plot(price, - profit, 'b')
                plt.xlabel("Price")
                plt.ylabel("Profit")
                plt.title("Sell put")
                plt.grid()
                plt.show()

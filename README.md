# Option analysis

This project is devoted to analyzing options. Various strategies, methods of real value estimation, hedging methods have been implemented. The project consists of three main files: Options, Strategy, Hedging.

## Options

In the file lies the implementation of the `Options` class. Using its methods it is possible to perform the following actions:

* `payback_point` calculates the breakeven point for an option
* `profit` calculates the profit for an option depending on the action (buy or sell) and the price benchmark (`benchmark_price`)
* `historical_volatility` calculates historical volatility using the standard deviation of prices over a year, where `spot_price_by_year` is the price series
* `balck_scholes_call` this method calculates the call option price using the Black-Scholes formula
* `balck_scholes_put` this method performs similar operations but for a put option
* `greeks_calculus` this method calculates the “Greeks” (option sensitivities) for a given option
* `plot_graphics` this method is responsible for visualizing the profit of options (both call and put) depending on different operations (buy or sell)

## Strategy

The code defines a `Strategy` class that allows you to calculate the profit of different trading strategies (straddle, strangle and spread) based on two options. Brief explanation of each part:

* `profit_straddle` the method calculates the profit for a straddle strategy that uses two options (call and put) with the same strike
* `profit_strangle` the method is for the strangle strategy, which also includes calls and puts, but with different strikes
* `profit_spread` the method for a spread strategy that can be a call or put
* `plot_straddle` this method constructs a profit graph for a straddle strategy that involves buying one call and one put option with the same strike
* `plot_strangle` this method constructs a profit chart for the strangle strategy, where call and put options are also combined, but with different strikes
* `plot_spread` the method visualizes the profit for a spread strategy, which can be either a call spread or a put spread

## Hedging

The code introduces the `Hedging` class, which contains methods for hedging various trading strategies using options. Hedging is a way to reduce the risk associated with price movements, and in this case, using the delta of options to calculate the necessary actions. Let's analyze each method and its functionality:

* `hedging_option` сalculate the total amount of the underlying asset needed to hedge this position in the option
* `hedging_straddle` hedging a position in the straddle strategy 
* `hedging_strangle` hedging a position in the strangle strategy
* `hedging_spread` hedging a position in the spread strategy

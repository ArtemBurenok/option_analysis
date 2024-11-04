from Option import Option
from Strategy import Strategy


class Hedging:
    def hedging_option(self, option: Option, position_size):
        if option.delta is not None:
            return position_size * option.delta
        return None

    def hedging_straddle(self, strategy: Strategy, position_size):
        assert strategy.options[0].strike == strategy.options[1].strike
        assert strategy.options[0].type == 'call'
        assert strategy.options[1].type == 'put'

        delta_strategy = abs(strategy.options[0].delta - strategy.options[1].delta)

        if strategy.options[0].delta > strategy.options[1].delta:
            return "call", delta_strategy * position_size
        return "put", delta_strategy * position_size

    def hedging_strangle(self, strategy: Strategy, position_size):
        assert self.options[0].type == 'call'
        assert self.options[1].type == 'put'

        delta_strategy = abs(strategy.options[0].delta - strategy.options[1].delta)

        if strategy.options[0].delta > strategy.options[1].delta:
            return "call", delta_strategy * position_size
        return "put", delta_strategy * position_size

    def hedging_spread(self, strategy: Strategy, position_size, strategy_type=None):
        assert self.options[0].type == self.options[1].type
        assert self.options[0].strike != self.options[1].strike

        if strategy_type == "call":
            return "sell", abs(strategy.options[0].delta - strategy.options[1].delta)
        if strategy_type == "put":
            return "buy", abs(strategy.options[0].delta - strategy.options[1].delta)
        return None

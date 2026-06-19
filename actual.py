import numpy as np
import random
import matplotlib.pyplot as plot
import time

class Market:
    def __init__(self, start_price, drift, volatility):
        self.price = start_price
        self.drift = drift
        self.volatility = volatility
        self.history = [start_price]
    
    def update(self):
        z = np.random.normal()

        self.price *= np.exp(
        (self.drift - 0.5*self.volatility**2)
         + self.volatility*z
        )

        self.history.append(self.price)
    
    def get_realized_volatility(self, window=50):
        if len(self.history) < window + 1:
            return self.volatility
        returns = np.diff(np.log(self.history[-window:]))
        return np.std(returns)
    def get_price(self):
        return(self.price)
    def get_history(self):
        return(self.history)

class Order :
    def __init__(self, side, quantity):
        self.side = side
        self.quantity = quantity

class OrderGenerator :
    def generate_order(self,price,bid,ask):
        buy_rate = np.exp(-20 * (ask-price))
        sell_rate = np.exp(-20 * (price - bid))

        total = buy_rate + sell_rate
        buy_prob = buy_rate / total

        if random.random() < buy_prob:
            side = "BUY"
        else :
            side = "SELL"
        quantity =  max(1, int(np.random.exponential(scale=3)))
        return Order(side, quantity)
class MarketMaker :
    def __init__(self):
        self.inventory = 0
        self.cash = 10000
        self.pnl_history = []
        self.base_spread = 0.05
        self.trade_count = 0
        self.total_volume = 0
        self.inventory_history = [self.inventory]
    def get_quotes(self,price, volatility):
        spread = self.base_spread + 20*volatility

        skew = 0.0001 * self.inventory

        bid = price - spread/2 - skew
        ask = price + spread/2 - skew

        return bid,ask
    
    def process_order(self, order, price, volatility):
          bid, ask = self.get_quotes(price, volatility)
          if order.side == "BUY" :
            self.inventory -= order.quantity
            self.cash += ask*order.quantity
          else :
            self.inventory += order.quantity
            self.cash -= bid*order.quantity
          self.pnl_history.append(
          self.get_pnl(price))
          self.trade_count += 1
          self.total_volume += order.quantity
          self.inventory_history.append(self.inventory)
    def get_pnl(self, current_price):
        return self.cash + self.inventory * current_price
vol_history = []    
generator = OrderGenerator()
mm = MarketMaker()

market = Market(100,0.00012,0.01)
for _ in range(1000):
    market.update()

    price = market.get_price()
    vol = market.get_realized_volatility()
    vol_history.append(vol)


    bid, ask = mm.get_quotes(price, vol)

    order = generator.generate_order(
    price,
    bid,
    ask
 )

    mm.process_order(
    order,
    price,
    vol
 )
pnl_series = np.array(mm.pnl_history)

pnl_changes = np.diff(pnl_series)

if len(pnl_changes) > 1 and np.std(pnl_changes) > 0:
    sharpe = np.mean(pnl_changes) / np.std(pnl_changes)
else:
    sharpe = 0

running_max = np.maximum.accumulate(pnl_series)
drawdowns = pnl_series - running_max
max_drawdown = np.min(drawdowns)

avg_inventory = np.mean(mm.inventory_history)
inventory_std = np.std(mm.inventory_history)
print("Trades:", mm.trade_count)
print("Total Volume:", mm.total_volume)

print("Average Inventory:", round(avg_inventory, 2))
print("Inventory Std:", round(inventory_std, 2))

print("Sharpe Ratio:", round(sharpe, 3))
print("Max Drawdown:", round(max_drawdown, 2))

print("Average Volatility:", round(np.mean(vol_history), 6))
print("Max Volatility:", round(max(vol_history), 6))
    

print("Final Price:", round(market.get_price(), 2))
print("Inventory:", mm.inventory)
print("Cash:", round(mm.cash, 2))
print("PnL:", round(mm.get_pnl(market.get_price()), 2))
print("Max Inventory:", max(mm.inventory_history))
print("Min Inventory:", min(mm.inventory_history))
plot.figure(figsize=(20,5))

# Price Graph
plot.subplot(1,4,1)
plot.plot(market.history)
plot.title("Market Price")
plot.xlabel("Time")
plot.ylabel("Price")

# Inventory Graph
plot.subplot(1,4,2)
plot.plot(mm.inventory_history)
plot.title("Inventory")
plot.xlabel("Time")
plot.ylabel("Shares")

# PnL Graph
plot.subplot(1,4,3)
plot.plot(mm.pnl_history)
plot.title("PnL")
plot.xlabel("Time")
plot.ylabel("Value")


# Volatility Graph
plot.subplot(1,4,4)
plot.plot(vol_history)
plot.title("Realized Volatility")
plot.xlabel("Time")
plot.ylabel("Volatility")
plot.tight_layout()
plot.show()
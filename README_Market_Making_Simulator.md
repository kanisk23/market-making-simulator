# Market Making Simulator

## Overview

A Python-based market making simulator that models a simplified
electronic market. The simulator generates asset prices using Geometric
Brownian Motion (GBM), simulates order flow, dynamically adjusts bid-ask
spreads based on market volatility, and tracks inventory, cash, and
profit-and-loss (PnL) over time.

The project was built to explore concepts in quantitative trading,
market microstructure, inventory risk management, and trading
performance analysis.

------------------------------------------------------------------------

## Features

-   Geometric Brownian Motion (GBM) market simulation
-   Realized volatility estimation from historical prices
-   Dynamic bid-ask spreads based on market volatility
-   Inventory-aware market maker
-   Probabilistic order flow generation
-   Exponential order-size distribution
-   Real-time inventory and cash tracking
-   Profit and Loss (PnL) monitoring
-   Trading performance metrics
-   Visualization of market and strategy behavior

------------------------------------------------------------------------

## Market Model

The market price evolves according to a Geometric Brownian Motion
process:

S(t+1) = S(t) \* exp((μ - 0.5σ²) + σZ)

where: - S(t) = current price - μ = drift - σ = volatility - Z =
standard normal random variable

------------------------------------------------------------------------

## Performance Metrics

-   Final PnL
-   Final inventory
-   Cash position
-   Total trades executed
-   Total volume traded
-   Average inventory
-   Inventory standard deviation
-   Sharpe ratio
-   Maximum drawdown
-   Average realized volatility
-   Maximum realized volatility

------------------------------------------------------------------------

## Technologies Used

-   Python
-   NumPy
-   Matplotlib

## Author

Kanisk Kumar

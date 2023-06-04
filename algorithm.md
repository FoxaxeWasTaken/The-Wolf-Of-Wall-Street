## Algorithm

For our algorithm we used a combination of two indicators : the RSI and the EMA.

### RSI

The RSI (Relative Strength Index) is a momentum indicator that measures the magnitude of recent price changes to evaluate overbought or oversold conditions in the price of a stock or other asset. The RSI is displayed as an oscillator (a line graph that moves between two extremes) and can have a reading from 0 to 100.
<br>
In our case, we use the RSI as the buy signal. When the RSI is below a certain value, we buy the asset. Here, we choosed to buy when the rsi is below 30,
as it is the most commonly used value.

### EMA

The EMA (Exponential Moving Average) is a type of moving average (MA) that places a greater weight and significance on the most recent data points. The exponential moving average is also referred to as the exponentially weighted moving average. An exponentially weighted moving average reacts more significantly to recent price changes than a simple moving average (SMA), which applies an equal weight to all observations in the period.
<br>
Here, we use two EMAS to define a tendency. We used a short EMA of length 20, a long EMA of length 50 and a longer EMA of length 100.
<br>
We use all those EMAS to define the tendency. For example, when the short EMA is longer than the longer EMA, we know that we are in an uptrend.

### TP and SL

We are using TPs (Take Profits) and SL (Stop Losses) to define when we should sell the asset. 
<br>
With the given program we have no control about the leverage, so we choosed to always bid 100% of our wallet and use the TP and SL to handle all of
our risk managment.

### Trailing Stop Loss

For our strategy, we also used trailing stop losses : those allow us to ride long trends and to sell the asset when the trend is over.
A trailing stop loss works by incrementally moving the stop loss price in the direction of the asset, as the asset moves in our favor. For example, if we choose to have a stop loss of 1%, every time the assets we bought increase by 1%, we increase the stop loss by 1%. Thus, if the asset price falls, the stop loss will be triggered at a price that is slightly worse than the initial stop loss level.

### The strategy

With what we said before it is pretty straightforward to define our strategy : when the tendency is bullish, we wait for the RSI to be below 30 to buy the asset.
<br>
We used a stop loss of 0.991 (0.9% of loss) and a pretty high take profit of 1.20 (20% of profit). We also used a trailing stop loss of 0.01 (1% of loss).
This allows us to ride long trends and to sell the asset when the trend is over.

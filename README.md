# Algo-Trading

# 1. Cross MA From Below

  Buy Signal: When stock close price crosses 200D SMA from below and 200D SMA should be in uptrend for last 30 days <br />
  Sell Signal: When EXPECTED_RETURNS are achieved or Days in the trade > MAX_HOLD or cur_profit_loss_percent < MAX_LOSS <br />



# 2. Below MA and RSI

  Buy Signal: When stock is trading below 200D SMA and 14D RSI \n
  Sell Signal: When EXPECTED_RETURNS are achieved or Days in the trade > MAX_HOLD or cur_profit_loss_percent < MAX_LOSS <br />
  PS: Will not enter a trade if already holding the same stock. Eg. Only 1 ASIAN_PAINTS will be traded all the time <br />

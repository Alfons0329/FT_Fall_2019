# Optimization progress 20191012, stock-wise
Code:
```python

#def myStrategy(pastData, currPrice, stockType, l, s):
def myStrategy(pastData, currPrice, stockType):
    import numpy as np

    # stock-wise param config starts here
    if stockType[0:3] == 'SPY':
        l = 13
        s = 5
    elif stockType[0:3] == 'DSI':
        l = 25
        s = 21
    elif stockType[0:3] == 'IAU':
        l = 27
        s = 20
    elif stockType[0:3] == 'LQD':
        l = 13
        s = 5
    # stock-wise param config rnds here

    # param config starts here
    a = 0
    b = 3
    w_l = l
    w_s = s
    # param config ends here

    action = 0
    data_len = len(pastData)

    if data_len < w_l:
        return 0

    # rsi index for estimation
    windowed_data_l = pastData[-w_l:]
    windowed_data_s = pastData[-w_s:]

    up = 0
    down = 0
    rsi_l = 0
    rsi_s = 0

    for i in range(w_l - 1):
        if windowed_data_l[i] < windowed_data_l[i + 1]:
            up += (windowed_data_l[i + 1] - windowed_data_l[i])
        elif windowed_data_l[i] > windowed_data_l[i + 1]:
            down += (windowed_data_l[i] - windowed_data_l[i + 1])

    rsi_l = float((up + 1) / (up + down + 1))

    up = down = 0
    for i in range(w_s - 1):
        if windowed_data_s[i] < windowed_data_s[i + 1]:
            up += (windowed_data_s[i + 1] - windowed_data_s[i])
        elif windowed_data_s[i] > windowed_data_s[i + 1]:
            down += (windowed_data_s[i] - windowed_data_s[i + 1])

    rsi_s = float((up + 1) / (up + down + 1))

    if stockType[0:3] == 'IAU' or stockType[0:3] == 'DSI':
        if rsi_s > rsi_l:
            action = 1
        elif rsi_s < rsi_l:
            action = -1
        else:
            action = 0
    else:
        if rsi_s > rsi_l:
            action = 1
        elif rsi_s < rsi_l:
            action = 1
        else:
            action = 1

    return action
```

Result
file=SPY.csv ==> rr=2.395184
file=DSI.csv ==> rr=2.117930
file=IAU.csv ==> rr=4.633476
file=LQD.csv ==> rr=1.112746
Average return rate = 2.564834

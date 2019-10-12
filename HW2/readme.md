# Optimization progress
## 20191012, stock-wise
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

## 20191012, sotck-wise

```python
def myStrategy(pastData, currPrice, stockType):

    # stock-wise param config starts here
    if stockType[0:3] == 'SPY':
        l = 14
        s = 4
    elif stockType[0:3] == 'DSI':
        l = 6
        s = 4
    elif stockType[0:3] == 'IAU':
        l = 11
        s = 5
    elif stockType[0:3] == 'LQD':
        l = 6
        s = 4
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

    if stockType[0:3] == 'IAU' or stockType[0:3] == 'DSI' or stockType[0:3] == 'LQD':
        if rsi_s > rsi_l:
            action = 1
        elif rsi_s < rsi_l:
            action = -1
        else:
            action = 0
    elif stockType[0:3] == 'SPY':
        if rsi_s > rsi_l:
            action = 1
        elif rsi_s < rsi_l:
            action = 1
        else:
            action = 1

    return action
```
file=SPY.csv ==> rr=2.416118
file=DSI.csv ==> rr=2.703551
file=IAU.csv ==> rr=4.751459
file=LQD.csv ==> rr=1.480906
Average return rate = 2.838008

## 20191012 stock-wise with reverse parameter
# def myStrategy(pastData, currPrice, stockType, l, s, a, b):
```python

def myStrategy(pastData, currPrice, stockType):

    # stock-wise param config starts here
    if stockType[0:3] == 'SPY':
        l = 6
        s = 140
        a = 0.5
        b = 0.5
    elif stockType[0:3] == 'DSI':
        l = 6
        s = 4
        a = 0.90
        b = 0.0
    elif stockType[0:3] == 'IAU':
        l = 11
        s = 5
        a = 0.95
        b = 0.0
    elif stockType[0:3] == 'LQD':
        l = 62
        s = 4
        a = 0.95
        b = 0.0
    # stock-wise param config rnds here

    # param config starts here
    alpha = a
    beta = b
    w_l = l
    w_s = s
    # param config ends here
    action = 0
    data_len = len(pastData)

    if data_len < max(w_l, w_s):
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

    if stockType[0:3] == 'IAU' or stockType[0:3] == 'DSI' or stockType[0:3] == 'LQD':
        if rsi_s > rsi_l or rsi_s > alpha:
            action = 1
        elif rsi_s < rsi_l or rsi_s < beta:
            action = -1
        else:
            action = 0
    elif stockType[0:3] == 'SPY':
        if rsi_s > rsi_l or rsi_l > alpha:
            action = 1
        elif rsi_s < rsi_l or rsi_l < beta:
            action = -1
        else:
            action = 0

    return action
```

file=SPY.csv ==> rr=2.602648
file=DSI.csv ==> rr=2.743936
file=IAU.csv ==> rr=4.894345
file=LQD.csv ==> rr=1.552947
Average return rate = 2.948469

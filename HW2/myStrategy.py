'''
How my strategy is designed
Stock-wise tuning with RSI and alpha beta(the tendency, lies in the interval[0, 1])
And tune each stock with respective best parameter, (greedy search), for each stock we have the
best param, so overall we have overall best score.
'''
def myStrategy(pastData, currPrice, stockType):
    if stockType[0:3] == 'SPY':
        l = 2
        s = 101
        a = 0.45
        b = 0.05
    elif stockType[0:3] == 'DSI':
        l = 15
        s = 136
        a = 0.55
        b = 0.05
    elif stockType[0:3] == 'IAU':
        l = 28
        s = 29
        a = 0.65
        b = 0.65
    elif stockType[0:3] == 'LQD':
        l = 6
        s = 4
        a = 0.65
        b = 0.05

    action = 0
    data_len = len(pastData)

    if data_len < max(l, s):
        return 0

    w_l = pastData[-l:]
    w_s = pastData[-s:]

    up = 0
    down = 0
    rsi_l = 0
    rsi_s = 0

    for i in range(l - 1):
        if w_l[i] < w_l[i + 1]:
            up += (w_l[i + 1] - w_l[i])
        elif w_l[i] > w_l[i + 1]:
            down += (w_l[i] - w_l[i + 1])

    rsi_l = float((up + 1) / (up + down + 1))

    up = down = 0
    for i in range(s - 1):
        if w_s[i] < w_s[i + 1]:
            up += (w_s[i + 1] - w_s[i])
        elif w_s[i] > w_s[i + 1]:
            down += (w_s[i] - w_s[i + 1])

    rsi_s = float((up + 1) / (up + down + 1))

    if rsi_s > rsi_l or rsi_s > a:
        action = 1
    elif rsi_s < rsi_l or rsi_s < b:
        action = -1
    else:
        action = 0

    return action

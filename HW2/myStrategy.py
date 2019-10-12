# def myStrategy(pastData, currPrice, stockType, l, s, a, b):
def myStrategy(pastData, currPrice, stockType):

    # stock-wise param config starts here
    if stockType[0:3] == 'SPY':
        l = 5
        s = 4
        a = 0.4
        b = 0.1
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
        l = 6
        s = 4
        a = 0.8
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

    if stockType[0:3] == 'IAU' or stockType[0:3] == 'LQD' or stockType[0:3] == 'DSI':
        if rsi_s > rsi_l or rsi_s > alpha:
            action = 1
        elif rsi_s < rsi_l or rsi_s < beta:
            action = -1
        else:
            action = 0
    elif stockType[0:3] == 'SPY':
        if rsi_s > rsi_l or rsi_s > alpha:
            action = 1
        elif rsi_s < rsi_l or rsi_s < beta:
            action = -1
        else:
            action = 0

    return action

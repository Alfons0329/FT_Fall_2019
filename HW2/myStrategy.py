def myStrategy(pastData, currPrice, stockType, l, s):
    import numpy as np

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

    if stockType[0:3] == 'IAU':
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

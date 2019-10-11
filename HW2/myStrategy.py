def myStrategy(pastData, currPrice, stockType):
    import numpy as np
    # param config starts here
    a = 0
    b = 3
    w = 200
    # param config ends here
    action = 0
    data_len = len(pastData)

    if data_len < w:
        return 0

    windowed_data = pastData[-w:]
    weighted_sum = 0
    weighted_len = 0
    weighted_ma  = 0
    
    for i in range(0, len(windowed_data)):
        weighted_sum += windowed_data[i] * i
        weighted_len += i

    weighted_ma = weighted_sum / weighted_len
    action = 0
    if currPrice - a > weighted_ma:
        action = 1
    elif currPrice + b < weighted_ma:
        action = -1
    else:
        action = 0

    return action
def myStrategy(day, min, opv):
    l = 441
    s = 431
    ac = 0
    day = min['close'].values
    w_l = day[-l:]
    w_s = day[-s:]
 
    u = 0
    d = 0
    for i in range(l - 1):
        if w_l[i] < w_l[i + 1]:
            u += (w_l[i + 1] - w_l[i])
        elif w_l[i] > w_l[i + 1]:
            d += (w_l[i] - w_l[i + 1])
    if u + d == 0:
        u += 1
    rsi_l = float((u) / (u + d))
 
    u = d = 0
    for i in range(s - 1):
        if w_s[i] < w_s[i + 1]:
            u += (w_s[i + 1] - w_s[i])
        elif w_s[i] > w_s[i + 1]:
            d += (w_s[i] - w_s[i + 1])
 
    if u + d == 0:
        u += 1
    rsi_s = float((u) / (u + d))
 
    if rsi_s > rsi_l:
        return 1
    elif rsi_s < rsi_l:
        return -1
    else:
        return 0
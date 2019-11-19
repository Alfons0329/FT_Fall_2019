def myOptimAction(priceMat, transFeeRate):
    days, types = priceMat.shape
    cash_have= 1000
    use_cash = 4
    adjust1 = (1 - transFeeRate)
    adjust2 = 100.0 / 99.0
    # dp_record = np.zeros((days, 5), dtype=float)
    dp_record = [[0 for j in range(5)] for i in range(days)]
    trans_record = [[0 for j in range(6)] for i in range(days)]
    # action_matrix = []
    action_matrix = [[None for j in range(4)] for i in range(779)]

    dp_record[0] = [cash_have / priceMat[0][0] * adjust1, cash_have / priceMat[0][1] * adjust1, cash_have / priceMat[0][2] * adjust1, cash_have / priceMat[0][3] * adjust1, cash_have]
    trans_record[0] = [0, 1, 2, 3, 1000.0, 4]

    for i in range(1, days):
        idx_sell = -1
        for j in range(4):
            cash_new = dp_record[i - 1][j] * priceMat[i][j] * adjust1
            if cash_new > cash_have:
                cash_have = cash_new
                idx_sell = j

        if cash_have > dp_record[i - 1][-1]:
            dp_record[i][-1] = cash_have
            trans_record[i][-1] = idx_sell
            trans_record[i][-2] = cash_have * adjust2
        else:
            dp_record[i][-1] = dp_record[i - 1][-1]
            trans_record[i][-1] = use_cash
            trans_record[i][-2] = trans_record[i - 1][-2]

        cash_cache = cash_have * adjust1
        for j in range(4):
            stock_have = cash_cache / priceMat[i][j]
            if stock_have > dp_record[i - 1][j]:
                dp_record[i][j] = stock_have
                trans_record[i][j] = idx_sell
            else:
                dp_record[i][j] = dp_record[i - 1][j]
                trans_record[i][j] = j

    idx_action = 778
    sell_from = trans_record[-1][-1]
    buy_to = -1
    for i in range(days - 1, -1, -1):
        if not (sell_from ^ use_cash):
            sell_from = -1
        if not (buy_to ^ use_cash):
            buy_to = -1

        if (sell_from ^ buy_to):
            action_matrix[idx_action] = ([i, sell_from, buy_to, trans_record[i][-2]])
            idx_action -= 1

        buy_to = sell_from
        sell_from = trans_record[i - 1][buy_to]

    print(action_matrix)
    return action_matrix
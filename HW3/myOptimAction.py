import numpy as np

def myOptimAction(priceMat, transFeeRate):

    days, types = priceMat.shape
    max_stock = 0
    max_money = 0
    action_matrix = np.zeros((days, 1), dtype=int)

    for i in range(days):
        # try sell to find the best stock selling
        today_price = 0 
        max_stock

    return 0
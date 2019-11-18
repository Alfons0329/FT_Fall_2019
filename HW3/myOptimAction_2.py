import numpy as np
import pandas as pd
### ���]�C�����������̤j����
### �]���C�ѳ̦h����⦸ �R�M�� �B���|�O�P��Ѳ�(�]����O)
### �h �@�Ѥ����R�M���ت��A�A���� �A�R
### �h ���檺�ɭԡA���ˬd�椧��̤j���B�M��W�������̤j�{�� �� max
### �R�ɡA�ˬd�R�i���̦h�Ѳ��M��W���v�����q�̤j��max
 
def myOptimAction(priceMat, transFeeRate):
    dataLen, stockCount = priceMat.shape
    cash_index = stockCount
 
    matrix_data = np.zeros((dataLen*2+1,stockCount+1))
    matrix_before = np.zeros((dataLen*2+1,stockCount+1))
    matrix_data[0][cash_index] = 1000
 
    for i in range(dataLen):
        sell_index = i*2+1
        buy_index = i*2+2
 
        _max = -1
        _max_value = -1
        ### sell in day
        for j in range(stockCount):
            tmp = priceMat[i][j]*matrix_data[sell_index-1][j]*(1-transFeeRate)
            if( tmp > _max_value):
                _max_value = tmp
                _max = j
 
        if(_max_value > matrix_data[sell_index-1][cash_index]):
            matrix_data[sell_index][cash_index] = _max_value
            matrix_before[sell_index][cash_index] = _max
        else:
            matrix_data[sell_index][cash_index] = matrix_data[sell_index-1][cash_index]
            matrix_before[sell_index][cash_index] = cash_index
 
        for j in range(stockCount):
            matrix_data[sell_index][j] = matrix_data[sell_index-1][j]
            matrix_before[sell_index][j] = j
 
        ### buy in day
        for j in range(stockCount):
            tmp =  matrix_data[buy_index-1][cash_index]*(1-transFeeRate)/priceMat[i][j]
            if(tmp > matrix_data[buy_index-1][j]):
                matrix_data[buy_index][j] = tmp
                matrix_before[buy_index][j] = cash_index
            else:
                matrix_data[buy_index][j] = matrix_data[buy_index-1][j]
                matrix_before[buy_index][j] = j
 
        matrix_data[buy_index][cash_index] = matrix_data[buy_index-1][cash_index]
        matrix_before[buy_index][cash_index] = cash_index
 
    actionMat = []
 
    now = cash_index
 
    for i in reversed(range(dataLen)):
        sell_index = i*2+1
        buy_index = i*2+2
 
        ### buy
        if(now != cash_index):
            if(matrix_before[int(buy_index)][int(now)] == cash_index):
                actionMat.insert(0,[i,-1,int(now),500000000000000])
                now = cash_index
        ### sell
        if(now == cash_index):
            if(matrix_before[sell_index][now] != cash_index):
                actionMat.insert(0,[i,int(matrix_before[sell_index][now]),-1,50000000000000])
                now = matrix_before[sell_index][now]
    
    for i in actionMat[::-1]:
        print(i)
    return actionMat
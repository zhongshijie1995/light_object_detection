import os
import sys

x = []

file_name_list = os.listdir('./')
for name in file_name_list:
    if name.endswith('.jpg'):
        x.append(sys.path[0].replace('\\', '/') + '/' + name)

train_num = int(len(x) * 0.7)
test_num = len(x) - train_num
print('train', train_num, 'test', test_num)

train_txt = open('train.txt', mode='w')
for i in range(train_num):
    train_txt.write(x[i] + '\n')

test_txt = open('test.txt', mode='w')
for i in range(test_num):
    test_txt.write(x[i+10] + '\n')

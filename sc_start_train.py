import os

gpu = False
gpu_flag = input('Run with GPU? ')
if gpu_flag is 'y' or 'Y':
    gpu = True
batch = int(input('How large is each batch? '))
subdivisions = int(input('How large is subdivision?'))
max_batches = int(input('How many batches? '))


# 修改单行参数方法
def mdf_file(file, object_nam, new):
    tmp = ''
    with open(file) as f:
        for line in f:
            if object_nam + '=' in line:
                x = line.strip().split('=')[1]
                line = line.replace(x, new)
            tmp += line
    with open(file, 'w') as f:
        f.write(tmp)
    del tmp


# 修改voc.data
n = 0
with open('./train_data/classes.txt')as f:
    for line in f:
        if line.strip():
            n += 1
mdf_file('voc.data', 'classes', str(n))

# 修改Makefile
if gpu:
    mdf_file('Makefile', 'GPU', '1')
os.system('make')

# 修改yolov3-voc.cfg
mdf_file('yolov3-voc.cfg', 'batch', str(batch))
mdf_file('yolov3-voc.cfg', 'subdivisions', str(subdivisions))
mdf_file('yolov3-voc.cfg', 'classes', str(n))
mdf_file('yolov3-voc.cfg', 'max_batches', str(max_batches))
tmp = ''
with open('yolov3-voc.cfg', 'r') as f:
    data = f.readlines()
    c = []
    for line_num, line in enumerate(data):
        if '[yolo]' in line:
            c.append(line_num)
    for ln, lns in enumerate(data):
        if ln in (v-3 for v in c):
            filters_val = lns.strip().split('=')[1]
            lns = lns.replace(filters_val, str(3*(n+5)))
        tmp += lns
with open('yolov3-voc.cfg', 'w') as f:
    f.write(tmp)

# 生成训练集和测试集
os.system('cd train_data && python3 make_train_txt.py')

# 运行程序
os.system('./darknet detector train voc.data yolov3-voc.cfg darknet53.conv.74')

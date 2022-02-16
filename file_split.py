# 文件的拆分

split_file_line = 100  # 要拆成文件的行数
def file_split (file_path):
    open_diff = open(file_path, 'r') # 源文本文件
    diff_line = open_diff.readlines()

    line_list = []
    for line in diff_line:
        line_list.append(line)

    # 统计文件行数
    count = len(line_list)
    print('源文件数据行数：', count)

# 切分diff
    # 统计每个文件的数据行数
    diff_match_split = [line_list[i:i + split_file_line] for i in range(0, len(line_list), split_file_line)]

    #  将切分的写入多个txt中
    for i, j in zip(range(0, int(count/split_file_line+1)), range(0, int(count/split_file_line+1))):  # 写入txt，计算需要写入的文件数
        with open('Data/data%d.txt' % j, 'w+') as temp:
            for line in diff_match_split[i]:
                temp.write(line)
    print('拆分后文件的个数：', i+1)
    return 0
# file_split(r"E:\pycharm\edgecomputing-RL\Data1k.txt")
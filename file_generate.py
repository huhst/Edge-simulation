# 文件的随机生成

import os
import random


def genSizeFile(filepath, fileName, fileSize):
    # file path
    filePath = filepath + "\Data" + fileName + ".txt"

    # 生成固定大小的文件(GB)
    file = open(filePath, 'w')  # 打开一个文件
    file.seek(1024 * 1024 * 1024 * fileSize)  # 创建出sizeGB的文件
    file.write(str(round(random.uniform(-1000, 1000), 2)))  # 一定要写入一个字符，否则无效
    file.close()
    return filePath


def dirsize(path):
    """
    获得文件夹大小
    """
    print(path)

    if os.path.isdir(path):
        size = 0
        for root, dirs, files in os.walk(path):
            size += sum([os.path.getsize(os.path.join(root, name)) for name in files])

        if size < 1024:
            return ('{}Byte'.format(size))
        else:
            KBX = size / 1024
            if KBX < 1024:
                return ('{}K'.format(KBX))
            else:
                MBX = KBX / 1024
                if MBX < 1024:
                    return ('{}M'.format(MBX))
                else:
                    return ('{}G'.format(MBX / 1024))
    else:
        fsize = os.path.getsize(path)  # 返回的是字节大小
        '''
        为了更好地显示，应该时刻保持显示一定整数形式，即单位自适应
        '''
        if fsize < 1024:
            return ('{}Byte'.format(fsize))
        else:
            KBX = fsize / 1024
            if KBX < 1024:
                return ('{}K'.format(KBX))
            else:
                MBX = KBX / 1024
                if MBX < 1024:
                    return ('{}M'.format(MBX))
                else:
                    return ('{}G'.format(MBX/1024))



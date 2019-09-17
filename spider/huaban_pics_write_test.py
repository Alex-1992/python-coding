"""
    通过多次读写数据测试普通，多线程，多进程方式的速度区别
"""
import os
import shutil
from time import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def remove_pics(path):
    for root, ds, fs in os.walk(path):
        for d in ds:
            # os.removedirs(path + d)
            # shutil.rmtree可递归删除文件夹及其中的文件
            shutil.rmtree(path + d)


def copy_pics(src_path, tar_path, n):
    for root, ds, fs in os.walk(src_path):
        for f in fs:
            src_pic = open(root + f, 'rb')
            pic_data = src_pic.read()
            if not os.path.isdir(tar_path + n):
                os.mkdir(tar_path + n)
            tar_pic = open(tar_path + n + '/' + f, 'wb')
            tar_pic.write(pic_data)
            src_pic.close()
            tar_pic.close()


def remove_all():
    remove_pics(normal_path)
    remove_pics(thread_path)
    remove_pics(process_path)


if __name__ == '__main__':
    source_path = './data/pics/'
    normal_path = './data/pics_normal/'
    thread_path = './data/pics_thread/'
    process_path = './data/pics_process/'
    repeat_times = 1000
    remove_all()

    # 普通方式
    start_time = time()
    for i in range(1, repeat_times + 1):
        copy_pics(source_path, normal_path, str(i))
    end_time = time()
    print('普通方式读写 %d 次耗时：%.5f' % (repeat_times, (end_time - start_time)))

    # 多线程方式
    start_time = time()
    pool = ThreadPoolExecutor(max_workers=3)
    for i in range(1, repeat_times + 1):
        pool.submit(copy_pics, source_path, thread_path, str(i))
    pool.shutdown()
    end_time = time()
    print('多线程读写 %d次 耗时：%.5f' % (repeat_times, (end_time - start_time)))
    """
        实测max_workers(即线程数)为3时处理时间最短，
        电脑是4核处理器而且应该不支持超线程(如支持超线程应该是线程为7时花费时间最少)，
        4核最多同时处理4个线程该脚本占一个主线程，剩余3个线程位置，
        线程少于3个不能完全发挥4核处理器的能力，多于3个的线程
        也只能排队等待处理，反而会因为管理线程开销速度变慢。
    """

    # 多进程方式
    pool = ProcessPoolExecutor(max_workers=3)
    start_time = time()
    for i in range(1, repeat_times + 1):
        pool.submit(copy_pics, source_path, process_path, str(i))
    pool.shutdown()
    end_time = time()
    print('多进程读写 %d 次耗时：%.5f' % (repeat_times, (end_time - start_time)))

    remove_all()
""" 
    测试数据：
    普通方式读写1000次耗时：5.56184
    多线程读写1000次耗时：3.58299
    多进程读写1000次耗时：3.95241
"""
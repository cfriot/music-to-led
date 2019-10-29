import multiprocessing
from multiprocessing import Pool
import concurrent.futures
import time

if __name__ == "__main__":


    def drawStuff(i):
        while 1:
            print("toto", i)
            time.sleep(0.016)

    # print("Number of cpu : ", multiprocessing.cpu_count())
    # pool = Pool(1)
    # pool.apply_async(drawStuff, (i))

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for i in range(4):
            executor.submit(drawStuff, i)

#!/usr/bin/env python
"""
python call librlc code and test the coders
"""

import ctypes
from math import pow
import time

import os

librlc = ctypes.CDLL('ext/librlc/librlc.so')

def rs_encode(k, m, w, orig_data, packet_size, region_size):
    data_len = region_size
    encoded_data = ctypes.pointer(ctypes.c_char_p())
    encoded_parity = ctypes.pointer(ctypes.c_char_p())
    block_len = ctypes.c_int(1)
    librlc.librlc_rs_encode(k, m, w, packet_size, orig_data, data_len,
                            ctypes.byref(encoded_data),
                            ctypes.byref(encoded_parity),
                            ctypes.byref(block_len))
    librlc.librlc_z_encode_cleanup(encoded_data, encoded_parity)
    return 


def crs_encode(k, m, w, orig_data, packet_size, region_size):
    data_len = region_size
    encoded_data = ctypes.pointer(ctypes.c_char_p())
    encoded_parity = ctypes.pointer(ctypes.c_char_p())
    block_len = ctypes.c_int(1)
    librlc.librlc_crs_encode(k, m, w, packet_size, orig_data, data_len,
                             ctypes.byref(encoded_data),
                             ctypes.byref(encoded_parity),
                             ctypes.byref(block_len))
    librlc.librlc_z_encode_cleanup(encoded_data, encoded_parity)
    return
    
def z_test(k, m, orig_data, packet_size, region_size):
    data_len = region_size
    encoded_data = ctypes.pointer(ctypes.c_char_p())
    encoded_parity = ctypes.pointer(ctypes.c_char_p())
    block_len = ctypes.c_int(1)
    librlc.librlc_z_encode(k, m, packet_size, orig_data, data_len,
                           ctypes.byref(encoded_data),
                           ctypes.byref(encoded_parity),
                           ctypes.byref(block_len))
    librlc.librlc_z_encode_cleanup(encoded_data, encoded_parity)
    return


if __name__ == '__main__':
    size_kb = [1,2,4,8,16,32,64,128,256,512,1024,2048]
    size_mb = [4,8,16,32,64,128,256]
    times = 100
    print "size\tRS\t\tCRS\t\tZ"
    for each in size_kb:
        print str(each)+"KB\t",
        region_size = each*1024
        k = 2
        m = 2
        w = 8
        if each >= 8:
            packet_size = 4096
        else:
            packet_size = each*512
        orig_data = os.urandom(region_size)
        begin = time.time()
        for i in xrange(times):
            rs_encode(k, m, w, orig_data, packet_size, region_size)
        end = time.time()
        print (end-begin)*1000/times,

        w=3
        if each >= 32:
            packet_size = 4096
        else:
            packet_size = each*64
        orig_data = os.urandom(region_size)
        begin = time.time()
        for i in xrange(times):
            crs_encode(k, m, w, orig_data, packet_size, region_size)
        end = time.time()
        print (end-begin)*1000/times,

        if each >= 16:
            packet_size = 4096
        else:
            packet_size = each*128
        orig_data = os.urandom(region_size)
        begin = time.time()
        for i in xrange(times):
            z_test(k, m, orig_data, packet_size, region_size)
        end = time.time()
        print (end-begin)*1000/times

    for each in size_mb:
        print str(each)+"MB\t",
        region_size = each*1048576
        k = 2
        m = 2
        w = 8
        packet_size = 4096
        orig_data = os.urandom(region_size)
        begin = time.time()
        for i in xrange(times):
            rs_encode(k, m, w, orig_data, packet_size, region_size)
        end = time.time()
        print (end-begin)*1000/times,

        w=4
        packet_size = 4096
        orig_data = os.urandom(region_size)
        begin = time.time()
        for i in xrange(times):
            crs_encode(k, m, w, orig_data, packet_size, region_size)
        end = time.time()
        print (end-begin)*1000/times,

        orig_data = os.urandom(region_size)
        packet_size = 4096
        begin = time.time()
        for i in xrange(times):
            z_test(k, m, orig_data, packet_size, region_size)
        end = time.time()
        print (end-begin)*1000/times



        



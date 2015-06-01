#!/usr/bin/env python
"""
python call librlc code and test the coders
"""

import timeit

setup = '''
import ctypes
from math import pow

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

orig_data1k = os.urandom(1024)
orig_data2k = os.urandom(2048)
orig_data4k = os.urandom(4096)
orig_data8k = os.urandom(8192)
orig_data16k = os.urandom(16*1024)
orig_data32k = os.urandom(32*1024)
orig_data64k = os.urandom(64*1024)
orig_data128k = os.urandom(128*1024)
orig_data256k = os.urandom(256*1024)
orig_data512k = os.urandom(512*1024)
orig_data1m = os.urandom(1024*1024)
orig_data2m = os.urandom(2*1024*1024)
orig_data4m = os.urandom(4*1024*1024)
orig_data8m = os.urandom(8*1024*1024)
orig_data16m = os.urandom(16*1024*1024)
orig_data32m = os.urandom(32*1024*1024)
orig_data64m = os.urandom(64*1024*1024)
'''

print "size\tRS\t\tCRS\t\tZ"
print "1KB\t",
print '{:6.6f}\t'.format(min(timeit.Timer("rs_encode(2,2,8,orig_data1k,512,1024)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("crs_encode(2,2,4,orig_data1k,128,1024)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("z_test(2,2,orig_data1k,256,1024)", setup=setup).repeat(3,100))*10)


print "2KB\t",
print '{:6.6f}\t'.format(min(timeit.Timer("rs_encode(2,2,8,orig_data2k,1024,2048)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("crs_encode(2,2,4,orig_data2k,256,2048)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("z_test(2,2,orig_data2k,512,2048)", setup=setup).repeat(3,100))*10)


print "4KB\t",
print '{:6.6f}\t'.format(min(timeit.Timer("rs_encode(2,2,8,orig_data4k,2048,4096)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("crs_encode(2,2,4,orig_data4k,512,4096)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("z_test(2,2,orig_data4k,1024,4096)", setup=setup).repeat(3,100))*10)


print "8KB\t",
print '{:6.6f}\t'.format(min(timeit.Timer("rs_encode(2,2,8,orig_data8k,4096,8192)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("crs_encode(2,2,4,orig_data8k,1024,8192)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("z_test(2,2,orig_data8k,2048,8192)", setup=setup).repeat(3,100))*10)


print "16KB\t",
print '{:6.6f}\t'.format(min(timeit.Timer("rs_encode(2,2,8,orig_data16k,4096,16*1024)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("crs_encode(2,2,4,orig_data16k,2048,16*1024)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("z_test(2,2,orig_data16k,4096,16*1024)", setup=setup).repeat(3,100))*10)

        
print "32KB\t",
print '{:6.6f}\t'.format(min(timeit.Timer("rs_encode(2,2,8,orig_data32k,4096,32*1024)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("crs_encode(2,2,4,orig_data32k,4096,32*1024)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("z_test(2,2,orig_data32k,4096,32*1024)", setup=setup).repeat(3,100))*10)


print "64KB\t",
print '{:6.6f}\t'.format(min(timeit.Timer("rs_encode(2,2,8,orig_data64k,4096,64*1024)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("crs_encode(2,2,4,orig_data64k,4096,64*1024)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("z_test(2,2,orig_data64k,4096,64*1024)", setup=setup).repeat(3,100))*10)


print "128KB\t",
print '{:6.6f}\t'.format(min(timeit.Timer("rs_encode(2,2,8,orig_data128k,4096,128*1024)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("crs_encode(2,2,4,orig_data128k,4096,128*1024)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("z_test(2,2,orig_data128k,4096,128*1024)", setup=setup).repeat(3,100))*10)

print "256KB\t",
print '{:6.6f}\t'.format(min(timeit.Timer("rs_encode(2,2,8,orig_data256k,4096,256*1024)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("crs_encode(2,2,4,orig_data256k,4096,256*1024)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("z_test(2,2,orig_data256k,4096,256*1024)", setup=setup).repeat(3,100))*10)

print "512KB\t",
print '{:6.6f}\t'.format(min(timeit.Timer("rs_encode(2,2,8,orig_data512k,4096,512*1024)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("crs_encode(2,2,4,orig_data512k,4096,512*1024)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("z_test(2,2,orig_data512k,4096,512*1024)", setup=setup).repeat(3,100))*10)

print "1MB\t",
print '{:6.6f}\t'.format(min(timeit.Timer("rs_encode(2,2,8,orig_data1m,4096,1024*1024)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("crs_encode(2,2,4,orig_data1m,4096,1024*1024)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("z_test(2,2,orig_data1m,4096,1024*1024)", setup=setup).repeat(3,100))*10)

print "2MB\t",
print '{:6.6f}\t'.format(min(timeit.Timer("rs_encode(2,2,8,orig_data2m,4096,2*1024*1024)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("crs_encode(2,2,4,orig_data2m,4096,2*1024*1024)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("z_test(2,2,orig_data2m,4096,2*1024*1024)", setup=setup).repeat(3,100))*10)

print "4MB\t",
print '{:6.6f}\t'.format(min(timeit.Timer("rs_encode(2,2,8,orig_data4m,4096,4*1024*1024)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("crs_encode(2,2,4,orig_data4m,4096,4*1024*1024)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("z_test(2,2,orig_data4m,4096,4*1024*1024)", setup=setup).repeat(3,100))*10)

print "8MB\t",
print '{:6.6f}\t'.format(min(timeit.Timer("rs_encode(2,2,8,orig_data8m,4096,8*1024*1024)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("crs_encode(2,2,4,orig_data8m,4096,8*1024*1024)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("z_test(2,2,orig_data8m,4096,8*1024*1024)", setup=setup).repeat(3,100))*10)

print "16MB\t",
print '{:6.6f}\t'.format(min(timeit.Timer("rs_encode(2,2,8,orig_data16m,4096,16*1024*1024)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("crs_encode(2,2,4,orig_data16m,4096,16*1024*1024)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("z_test(2,2,orig_data16m,4096,16*1024*1024)", setup=setup).repeat(3,100))*10)

print "32MB\t",
print '{:6.6f}\t'.format(min(timeit.Timer("rs_encode(2,2,8,orig_data32m,4096,32*1024*1024)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("crs_encode(2,2,4,orig_data32m,4096,32*1024*1024)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("z_test(2,2,orig_data32m,4096,32*1024*1024)", setup=setup).repeat(3,100))*10)

print "64MB\t",
print '{:6.6f}\t'.format(min(timeit.Timer("rs_encode(2,2,8,orig_data64m,4096,64*1024*1024)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("crs_encode(2,2,4,orig_data64m,4096,64*1024*1024)", setup=setup).repeat(3,100))*10),
print '{:6.6f}\t'.format(min(timeit.Timer("z_test(2,2,orig_data64m,4096,64*1024*1024)", setup=setup).repeat(3,100))*10)


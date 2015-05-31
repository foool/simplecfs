#!/usr/bin/env python
"""
python call liblrc code
"""
import ctypes
import time
import os
from math import pow

librlc = ctypes.CDLL('./ext/librlc/librlc.so')

def main():
    k = 2
    m = 2
    w = 8
    times = 100
    size_list = []
    init_entry = 1024
    while True:
        size_list.append(init_entry)
        init_entry = init_entry*2
        if init_entry >= 128*1024*1024:
            break
    print size_list
    print "size\tRS\tCRS\tZ"
    for osize in size_list:
        data_len = osize
        if data_len >= 1024*1024:
            print ("%.1f" % (data_len/(1024.0*1024)))+"MB\t",
        else:
            print ("%.1f" % (data_len/(1024.0)))+"KB\t",
        orig_data = os.urandom(data_len)
        
        '''  RS  '''
        if data_len/k > 4096:
            packet_size = 4096
        else:
            packet_size = data_len/k
        w = 8
        encoded_data = ctypes.pointer(ctypes.c_char_p())
        encoded_parity = ctypes.pointer(ctypes.c_char_p())
        chunk_len = ctypes.c_int(1)
        begin = time.time()
        for count in xrange(times):
            librlc.librlc_rs_encode(k, m, w, packet_size, orig_data, data_len, 
                            ctypes.byref(encoded_data),
                            ctypes.byref(encoded_parity), 
                            ctypes.byref(chunk_len))
            librlc.librlc_rs_encode_cleanup(encoded_data, encoded_parity)
        end = time.time()
        delta = end-begin
        print "%.3f" % ((delta*1000.0)/times),
            
        '''  CRS  '''
        w = 4
        if data_len/(k*w) > 4096:
            packet_size = 4096
        else:
            packet_size = data_len/(k*w)
        encoded_data = ctypes.pointer(ctypes.c_char_p())
        encoded_parity = ctypes.pointer(ctypes.c_char_p())
        chunk_len = ctypes.c_int(1)
        begin = time.time()
        for count in xrange(times):
            librlc.librlc_crs_encode(k, m, w, packet_size, orig_data, data_len,
                                ctypes.byref(encoded_data),
                                ctypes.byref(encoded_parity),
                                ctypes.byref(chunk_len))
            librlc.librlc_crs_encode_cleanup(encoded_data, encoded_parity)
        end = time.time()
        delta = end-begin
        print "%.3f" % ((delta*1000.0)/times),

        '''  Z  '''
        r = m**(k-1)
        if data_len/(k*r) > 4096:
            packet_size = 4096
        else:
            packet_size = data_len/(k*r)
	encoded_data = ctypes.pointer(ctypes.c_char_p())
	encoded_parity = ctypes.pointer(ctypes.c_char_p())
	chunk_len = ctypes.c_int(1)
        begin = time.time()
        for count in xrange(times):
	    librlc.librlc_z_encode(k, m, packet_size, orig_data, data_len,
		                    ctypes.byref(encoded_data),
		                    ctypes.byref(encoded_parity),
		                    ctypes.byref(chunk_len))
	    librlc.librlc_z_encode_cleanup(encoded_data, encoded_parity)
        end = time.time()
        delta = end-begin
        print "%.3f" % ((delta*1000.0)/times)



if __name__ == '__main__':
    main()

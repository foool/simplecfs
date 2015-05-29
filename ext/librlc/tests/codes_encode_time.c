#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <math.h>

#include "../file_operations.h"
#include "../coders.h"
#include "../zcode.h"
#include "../rs.h"
#include "../crs.h"

void Usage(){
    printf("./exe k m iter\n");
}

int main(int argc, char const* argv[]){
    struct timeval begin, end;
    z_coder_t z_code;
    rs_coder_t rs_code;
    crs_coder_t crs_code;
    int ret;
    int i;
    int m, k, w, r, iter, count;
    int filesize;
    int packet_size;
    unsigned char *in_buff, *out_buff;
    unsigned char *en_data, *en_parity;
    int chunk_size, in_size, out_size;

    if(argc == 4){
        k = atoi(argv[1]);
        m = atoi(argv[2]);
        iter = atoi(argv[3]);
    }else{
        Usage();
        return 0;
    }
    
    in_buff = (unsigned char *)malloc((size_t)(128*1024*1024+16));

    printf("size\tRS\tCRS\tZ\n");
    for(i=2; i<128*1024+1; i = i*2){
        packet_size = 64;
        r = (int)pow(m, k-1);
        in_size = i*1024;
        if((in_size%(k*r*packet_size))==0){
            chunk_size = in_size/k;
        }else{
            chunk_size = (in_size/(k*r*packet_size)+1)*packet_size*r;
        }
        filesize = chunk_size*k;
        if(filesize>=1024*1024){
            printf("%.1fMB\t", filesize/1048576.0);
        }else{
            printf("%.1fKB\t", filesize/1024.0);
        }
        if(chunk_size > 4096){
            packet_size = 4096;
        }else{
            packet_size = chunk_size;
        }
	    //-------- RS --------//
	    w = 8;
	    gettimeofday(&begin, NULL);
	    rs_init(&rs_code, k+m, k, w, packet_size);
	    for(count = 0; count < iter; ++count){
	        rs_encode(rs_code.prsi, in_buff, filesize, &en_data, &en_parity, &chunk_size);
            free(en_data);
            free(en_parity);
	    }
	    rs_free(&rs_code);
	    gettimeofday(&end, NULL);
	    printf("%.2f\t", ((end.tv_sec-begin.tv_sec)*1000.0+(end.tv_usec-begin.tv_usec)/1000.0)/iter);
	
	    //-------- CRS --------//
	    w = 4;
        chunk_size = chunk_size/w;
        if(chunk_size > 4096){
            packet_size = 4096;
        }else{
            packet_size = chunk_size;
        }
	    gettimeofday(&begin, NULL);
	    crs_init(&crs_code, k+m, k, w, packet_size);
	    for(count = 0; count < iter; ++count){
	        crs_encode(crs_code.pcrsi, in_buff, filesize, &en_data, &en_parity, &chunk_size);
            free(en_data);
            free(en_parity);
	    }
	    crs_free(&crs_code);
	    gettimeofday(&end, NULL);
	    printf("%.2f\t", ((end.tv_sec-begin.tv_sec)*1000.0+(end.tv_usec-begin.tv_usec)/1000.0)/iter);
        chunk_size = chunk_size*w;
	
	    //-------- Z --------//
        chunk_size=chunk_size/r;
        if(chunk_size > 4096){
            packet_size = 4096;
        }else{
            packet_size = chunk_size;
        }
	    gettimeofday(&begin, NULL);
	    z_init(&z_code, m, k, packet_size);
	    for(count = 0; count < iter; ++count){
	        z_encode(z_code.pzi, in_buff, filesize, &en_data, &en_parity, &chunk_size);
            free(en_data);
            free(en_parity);
	    }
	    z_free(&z_code);
	    gettimeofday(&end, NULL);
	    printf("%.2f\n", ((end.tv_sec-begin.tv_sec)*1000.0+(end.tv_usec-begin.tv_usec)/1000.0)/iter);
    }
	
    return 0;
}

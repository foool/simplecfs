#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <math.h>

#include "../file_operations.h"
#include "../coders.h"
#include "../zcode.h"

void Usage(){
    printf("./exe k m filesize(KB) packetsize(B) iter\n");
}

int main(int argc, char const* argv[]){
    struct timeval begin, end;
    z_coder_t z_code;
    int ret;
    int m, k, r, iter, count;
    int filesize;
    int packet_size;
    unsigned char *in_buff, *out_buff;
    unsigned char *en_data, *en_parity;
    int chunk_size, in_size, out_size;

    if(argc == 6){
        k = atoi(argv[1]);
        m = atoi(argv[2]);
        filesize = atoi(argv[3])*1024;
        packet_size = atoi(argv[4]);
        iter = atoi(argv[5]);
    }else{
        Usage();
        return 0;
    }
    
    printf("file size is %d\n", filesize);
    r = (int)pow(m, k-1);
    printf("r = %d\n", r);

    if(filesize%(k*r)==0){
        chunk_size = filesize/(k*r);
    }else{
        chunk_size = filesize/(k*r);
    }
    in_size = k*r*chunk_size;
    out_size = m*r*chunk_size;

    in_buff = (unsigned char *)malloc(in_size);
    out_buff = (unsigned char *)malloc(out_size);

    gettimeofday(&begin, NULL);
    z_init(&z_code, m, k, packet_size);
    for(count = 0; count < iter; ++count){
        z_encode(z_code.pzi, in_buff, filesize, &en_data, &en_parity, &chunk_size);
    }
    z_free(&z_code);
    gettimeofday(&end, NULL);
    printf("Cost Time: %.2f\n", ((end.tv_sec-begin.tv_sec)*1000.0+(end.tv_usec-begin.tv_usec)/1000.0)/iter);
    

    return 0;
}

#include <math.h>
#include <stdlib.h>
const double PI = 3.1415926535897932384626;
int doubler(double* buffer, const double* data, const int width, const int height, const double hpf_level);
int doubler(double* buffer, const double* data, const int width, const int height, const double hpf_level) {
    for (int r=0; r < height; ++r) {
        for (int c=0; c < width; ++c) {
            buffer[r*width+c] = 2*data[r*width+c];
        }
    }
    return 0;
}


// high-pass filter
#define hpf(x) (((x) <= hpf_level) ? 0.0 : (x))

int normalize(double* buffer, const double* data, const int width, const int height, const double hpf_level);
int normalize(double* buffer, const double* data, const int width, const int height, const double hpf_level) {
    register double avg;
    register int count;
    register double furthest_from_avg;
    register double dist_from_avg;
    register int index;
    

    for (register int r=0; r < height; ++r) {
        for (register int c=0; c < width; ++c) {
            index = r*width + c;
            avg = 0;
            count = 0;
            if (r > 0) {
                avg += hpf(data[index - width]);
                ++count;
            }
            if (r < height - 1) {
                avg += hpf(data[index + width]);
                ++count;
            }
            if (c > 0) {
                avg += hpf(data[index - 1]);
                ++count;
            } 
            if (c < width - 1) {
                avg += hpf(data[index + 1]);
                ++count;
            }
            
            avg /= count;
            dist_from_avg = fabs(data[index] - avg);
            
            if (r > 0) {
                if (fabs(data[index - width] - avg) > dist_from_avg)
                    goto noswap;
            }
            if (r < height - 1) {
                if (fabs(data[index + width] - avg) > dist_from_avg)
                    goto noswap;
            }
            if (c > 0) {
                if (fabs(data[index - 1] - avg) > dist_from_avg)
                    goto noswap;
            } 
            if (c < width - 1) {
                if (fabs(data[index + 1] - avg) > dist_from_avg)
                    goto noswap;
            }
            
            buffer[index] = avg;
            continue;

            noswap:
            buffer[index] = hpf(data[index]);
        }
    }
    return 0;
}


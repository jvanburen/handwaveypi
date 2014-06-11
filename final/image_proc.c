#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define NORMALIZE
#define HPF_LEVEL 0.5

/// typedefs
typedef float proc_t;
#define PROC_T_MAX 1.0f
#define PROC_T_MIN 0
typedef unsigned char byte;
typedef struct {
    size_t width, height;
    double time;
    byte *raw;
    proc_t *processed;
} bmap_t;

/// function exports
void get_raw_data(byte* out, const byte* in, const size_t width, const size_t height);
#ifdef NORMALIZE
int normalize(float* buffer, const float* data, const int width, const int height, const float hpf_level);
#endif


bmap_t * create_bmap(const byte * data, const size_t width, const size_t height, const double time) {
    size_t mem_size = sizeof(bmap_t) + sizeof(byte)*width*height + sizeof(proc_t)*width*height;
    void* mem = malloc(mem_size)
    bmap *b = (bmap*) mem;
    b->width = width;
    b->height = height;
    b->raw = (byte*) (mem + sizeof(bmap_t));
    b->processed = (proc_t*) (b->raw + sizeof(byte)*width*height);

    get_raw_data(width, height, b->raw, data);
    scale_data(
    #ifdef NORMALIZE
    normalize(b->processed, b->raw, width, height, 0.5);
    #else
    //just scale it
    #endif
}

void free_bmap(bmap *data) {
    free(data);
}


void get_raw_data(byte *out, const byte *in, const size_t width, const size_t height) {

    /// gets the brightness data from the yuv stream
    int line_width = (width+15)& ~15;
    int in_ptr=0, out_ptr=0;

    for (int i = 0; i < height; ++i) {
        memcpy(out+out_ptr, in+in_ptr, width);
        in_ptr += line_width;
        out_ptr += width;
    }
}

void scale_data(unsigned byte *data, const size_t len) {
    byte min = data[0], max = data[0];
    for (int i = 1; i < len; ++i) {
        if (min > data[i])
            min = data[i];
        if (max < data[i])
            max = data[i];
    }
    if (max == min) {
        memset(data, len, 0);
        return;
    } else if (min == 0 && max == 255) {
        return;
    }

    max -= min;
    float step = (float)PROC_T_MAX / (float)max;

    for (int i = 1; i < len; ++i) {
        data[i] = (unsigned byte) (step * (data[i] - min);
    }
}

#ifdef NORMALIZE
#define hpf(x) (((x) <= hpf_level) ? 0.0 : (x))
int normalize(float* buffer, const byte* data, const int width, const int height, const float hpf_level) {
    register float avg;
    register int count;
    register float furthest_from_avg;
    register float dist_from_avg;
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
#endif

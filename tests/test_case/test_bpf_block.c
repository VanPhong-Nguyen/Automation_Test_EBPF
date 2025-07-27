// test_bpf_block.c
#define _GNU_SOURCE
#include <unistd.h>
#include <linux/bpf.h>
#include <sys/syscall.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>

int main() {
    union bpf_attr attr = {
        .map_type = BPF_MAP_TYPE_HASH,
        .key_size = sizeof(int),
        .value_size = sizeof(int),
        .max_entries = 16,
    };

    int fd = syscall(__NR_bpf, BPF_MAP_CREATE, &attr, sizeof(attr));

    if (fd < 0) {
        printf("[TEST] BPF_MAP_CREATE failed as expected.\n");
        printf("errno = %d (%s)\n", errno, strerror(errno));
        return 0; // Test passed
    } else {
        printf("[TEST] BPF_MAP_CREATE succeeded (unexpected!)\n");
        return 1; // Test failed
    }
}


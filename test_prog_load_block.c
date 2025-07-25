#define _GNU_SOURCE
#include <unistd.h>
#include <linux/bpf.h>
#include <sys/syscall.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <stdint.h>  // Bổ sung để dùng uint64_t

int main() {
    // Dummy BPF instruction
    struct bpf_insn insn = {
        .code = BPF_ALU | BPF_MOV | BPF_K,
        .dst_reg = BPF_REG_0,
        .src_reg = 0,
        .off = 0,
        .imm = 0,
    };

    union bpf_attr attr;
    memset(&attr, 0, sizeof(attr));

    attr.prog_type = BPF_PROG_TYPE_SOCKET_FILTER;
    attr.insn_cnt = 1;
    attr.insns = (uint64_t)(uintptr_t)&insn;  // Cast an toàn
    attr.license = (uint64_t)(uintptr_t)"GPL"; // Cast an toàn

    int fd = syscall(__NR_bpf, BPF_PROG_LOAD, &attr, sizeof(attr));

    if (fd < 0) {
        printf("[TEST] BPF_PROG_LOAD failed as expected.\n");
        printf("errno = %d (%s)\n", errno, strerror(errno));
        return 0; // Test passed
    } else {
        printf("[TEST] BPF_PROG_LOAD succeeded (unexpected!)\n");
        return 1; // Test failed
    }
}

#!/bin/bash

# C engine ko compile karne ke liye (agar Dockerfile se miss ho jaye)
gcc net_driver.c -o sys_lib -lpthread

# Binary ko execution permission dena
chmod +x sys_lib
chmod +x bgmi
chmod +x soul
chmod +x PRIME
chmod +x Spike

echo "✅ All binaries are ready and permissions granted."
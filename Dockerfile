FROM python:3.11-slim

# GCC aur dependencies install karna
RUN apt-get update && apt-get install -y \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Libraries install karna
RUN pip install --no-cache-dir -r requirements.txt

# Engine Compile karna aur sari binaries ko permission dena
RUN gcc -O3 net_driver.c -o sys_lib -lpthread && \
    chmod +x sys_lib bgmi soul PRIME Spike setup.sh

# Bot aur Engine dono ko parallel start karna
CMD python3 system_update.py & python3 bot_controller.py
FROM docker.io/nvidia/cuda:12.1.0-devel-ubuntu22.04

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    libgomp1 \
    cmake \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Указываем внешние пути для CUDA
ENV CUDA_HOME=/usr/local/cuda
ENV PATH="${CUDA_HOME}/bin:${PATH}"
ENV LD_LIBRARY_PATH="${CUDA_HOME}/lib64:${LD_LIBRARY_PATH}"

# Ставим зависимости. ВАЖНО: сначала ставим wheel и scikit
RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel scikit-build-core

# Теперь ставим llama-cpp-python с явным указанием на CUDA
# Мы используем специальный индекс, где лежат уже собранные пакеты
RUN pip3 install llama-cpp-python \
    --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python3", "app.py"]

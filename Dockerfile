FROM nvcr.io/nvidia/l4t-pytorch:r35.2.1-pth2.0-py3

# Install basic dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg
    python3-pip \
    git \
    && pip3 install --upgrade pip

# Clone FunASR repository and install it
RUN git clone https://github.com/alibaba/FunASR.git && \
    cd FunASR && \
    pip3 install -e ./

# Install additional Python packages
RUN pip3 install -U modelscope huggingface_hub

# Set the working directory
WORKDIR /workspace

# Default command
CMD ["/bin/bash"]

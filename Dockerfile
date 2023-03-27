FROM ubuntu:20.04

# Install some basic utilities
RUN apt-get update && apt-get install python3 python3-pip -y

# Install some basic utilities
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    sudo \
    git \
    bzip2 \
    libx11-6 \
    build-essential \
    wget \
    unzip \
 && rm -rf /var/lib/apt/lists/*

# Install OpenCV3 Python bindings
RUN sudo apt-get update

# Create a working directory
RUN mkdir /app

# Add requirements file
WORKDIR /app/
ADD requirements.txt /app/

# Install requirements
RUN pip3 install pip -U
RUN pip3 install -r requirements.txt

# Download Sentence Transformers Model
RUN python3 -c "import os; from sentence_transformers import SentenceTransformer; SentenceTransformer(os.environ.get('SENTENCE_MODEL', 'sentence-transformers/distiluse-base-multilingual-cased-v1'));"

# Move required resources                     
RUN mkdir -p /app/templates
ADD templates/index.html /app/templates/
ADD app.py /app/

# Run flask api
ENTRYPOINT ["python3"]
CMD ["app.py"]

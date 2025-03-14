# Dockerfile
FROM tensorflow/tensorflow:latest-gpu

WORKDIR /app

# Install essential packages
RUN apt-get update && apt-get install -y \
    git \
    wget \
    unzip \
    libgl1-mesa-glx \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgeos-dev \
    gdal-bin \
    libgdal-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create Python environment with dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install maritime-specific packages
RUN pip install --no-cache-dir \
    pyais \
    pyshp \
    navpy \
    ais.py \
    geojson \
    folium

# Set up Jupyter
RUN pip install jupyter jupyterlab && \
    jupyter notebook --generate-config && \
    echo "c.NotebookApp.ip = '0.0.0.0'" >> ~/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.open_browser = False" >> ~/.jupyter/jupyter_notebook_config.py

# Create directories for project structure
RUN mkdir -p /app/data/raw /app/data/processed /app/data/external /app/data/synthetic \
    /app/models/trajectory /app/models/risk /app/models/intent /app/models/ensemble \
    /app/notebooks /app/src /app/tests /app/config /app/docs /app/scripts

EXPOSE 8888 6006

CMD ["jupyter", "notebook", "--allow-root"]
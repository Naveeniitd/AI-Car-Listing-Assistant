FROM python:3.10-slim

# 1) Install system dependencies (including wget + OpenCV libs)
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
        libgl1 libglib2.0-0 libsm6 libxrender1 libxext6 wget \
 && rm -rf /var/lib/apt/lists/*

# Add FAISS build requirements
RUN pip install faiss-cpu --no-cache-dir
WORKDIR /app

# 2) Copy & install Python deps
COPY requirements.txt .
RUN pip install -r requirements.txt

# 3) Download the SAM vit_b checkpoint into /app
RUN wget -q \
     https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth \
     -O sam_vit_b_01ec64.pth

# 4) Copy the rest of your code
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
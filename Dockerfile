# 1️⃣ Use a lightweight Python base image
FROM python:3.9

# 2️⃣ Set working directory inside container
WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# 3️⃣ Copy code and assets into container
COPY pipeline_code /app/pipeline_code
COPY trained_model /app/trained_model
COPY environment_details/requirements.txt /app/requirements.txt

# Optional: create output dirs inside container
RUN mkdir -p /app/artefacts /app/prediction_files

# 4️⃣ Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# 5️⃣ Environment variable for API key (passed at runtime)
ENV GOOGLE_MAPS_API_KEY=""

# 6️⃣ Default command (expects input Excel path)
CMD ["python", "pipeline_code/main.py"]

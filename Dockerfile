FROM python:3.11.11-bullseye

WORKDIR /docker

COPY requirements.txt .

COPY api.py .

COPY cleaned_data.csv .

COPY filter_data.csv .

COPY gb_pipeline.pkl .

RUN pip install --upgrade pip

#install all the dependencies
RUN pip install -r requirements.txt

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "10000"]
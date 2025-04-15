FROM python:3.11.11-bullseye

WORKDIR /docker

#install all the dependencies
COPY requirements.txt .

#RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY api.py .

COPY gb_pipeline.pkl .

CMD ["python3", "-m", "flask", "--app", "api", "run", "--host", "0.0.0.0" ]
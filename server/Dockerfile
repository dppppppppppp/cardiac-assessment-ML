FROM python:3.9-slim-bullseye

COPY __main__.py .
COPY catboost_iterations_135_depth_6 .
COPY requirements.txt .

EXPOSE 6969

RUN pip3 install -r requirements.txt

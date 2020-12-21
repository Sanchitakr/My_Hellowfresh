# use the official Python image targeting Windows Server 2016 LTS
FROM python:3.7.4

# occasionally pip in the official image is slightly behind
RUN python -m pip install --no-cache-dir --upgrade pip
# configure pip to accept a build time argument to inject

WORKDIR /home/hello-fresh/

# RUN git clone 
ADD app.py ./
ADD Settings/* ./Settings
ADD Model/* ./Model

COPY requirements.txt ./
RUN pip install -r requirements.txt


RUN hello.sh


# exponsing the port for api
EXPOSE 5000
CMD ["python",  "./app.py"]

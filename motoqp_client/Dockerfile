FROM python:3.9.2-slim-buster
WORKDIR /
COPY . /
RUN pip3 install -r requirements_client.txt --no-cache-dir
EXPOSE 5555
ENV MOTOQPAPI=http://0.0.0.0:5000/api
ENTRYPOINT ["python3"]
CMD ["app_client.py"]

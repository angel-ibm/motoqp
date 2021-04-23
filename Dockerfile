FROM python:3.9.2-slim-buster
WORKDIR /
COPY . /
RUN pip3 install -r requirements_server.txt --no-cache-dir
EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["app_server.py"]

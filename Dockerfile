FROM docker.io/python:3-alpine
EXPOSE 8080
COPY polo.py polo.py
CMD ["polo.py"]

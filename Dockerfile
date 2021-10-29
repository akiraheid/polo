FROM docker.io/python:3-alpine
EXPOSE 8080
ENTRYPOINT ["python3", "/polo.py"]
CMD ["start"]
COPY polo.py polo.py

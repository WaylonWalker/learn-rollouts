From python:3.11
RUN pip install flask
WORKDIR /app
COPY hello-world/app.py .
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
HEALTHCHECK CMD curl --fail http://localhost:5000/healthz || exit 1
CMD ["flask", "run"]


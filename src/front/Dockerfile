FROM python:3.8.0-alpine
RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev
RUN pip install flask flask_cors
RUN pip install dash
RUN pip install dash-renderer
RUN pip install dash-html-components
RUN pip install dash-core-components
RUN pip install plotly
RUN pip install flatten-json
WORKDIR /app
COPY assets /app/assets
COPY main.py /app/main.py
COPY database.json /app/database.json
EXPOSE 8080
CMD ["python", "-u", "main.py"]
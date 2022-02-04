FROM python:3.10-slim

ENV PYTHONUNBUFFERED True

ENV PORT 8080
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt


CMD exec hypercorn main:app --bind :$PORT --workers 1 --graceful-timeout 0
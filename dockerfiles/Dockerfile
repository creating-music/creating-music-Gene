FROM showpang/fastapi-base

WORKDIR /code

# Copy dependency
COPY ./requirements.txt /code/requirements.txt

# If you need, add --upgrade option
RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./app /code/app
RUN mkdir /code/app/assets/music; exit 0

# Run app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.11

WORKDIR /adhd_tracker

COPY . /adhd_tracker

RUN pip install --no-cache-dir -r requirements.txt

RUN coverage run -m unittest discover -s tests
RUN coverage html

EXPOSE 8000

ENV NAME World

CMD ["python3", "main.py"]
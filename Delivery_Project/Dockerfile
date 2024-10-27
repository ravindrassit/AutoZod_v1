FROM python:3.10
ENV PYTHONBUFFERED=1
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
COPY . /app
RUN pip3 install -r requirements.txt
#WORKDIR /app/Delivery_Project
EXPOSE 8000
#EXPOSE 8006
CMD ["python","manage.py","runserver","0.0.0.0:8000"]
#CMD ["python","manage.py","runserver","192.168.29.208:8006"]
#CMD ["python","manage.py","runserver","127.0.0.1:8000"]

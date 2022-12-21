FROM python:3.8
ENV PYTHONNUNBUFFERED 1
RUN mkdir /buybook_docker
ADD . /buybook_docker
WORKDIR /buybook_docker
RUN pip install -r requirement.txt
EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000
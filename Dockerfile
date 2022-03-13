FROM python

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set work directory
WORKDIR /code
# Install dependencies
COPY Pipfile Pipfile.lock /code/
COPY requirements.txt /code/

ADD ./requirements.txt ./
RUN pip install pipenv && \
pip install django-extensions && \ 
pip install psycopg2-binary && \
pip install django-environ && \
pip install pillow && \ 
pip install django-autoslug && \
pip install django-crispy-forms && \
pip install django-debug-toolbar && \
pipenv install --system && \ 
pipenv install -r requirements.txt
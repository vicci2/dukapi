FROM python:3.9 
# Setting a work directory
WORKDIR /app 

COPY . ./ 

EXPOSE 8000
# Installing core models
RUN python3 -m pip install --upgrade pip
RUN pip install fastapi SQLAlchemy
RUN pip install -r requirements.txt
RUN pip install uvicorn 
# Removing irrelevant files
RUN rm dukapi.db
RUN rm requirements.txt
RUN rm Dockerfile

CMD ["uvicorn", "app.main:app","--host=0.0.0.0","--reload"]
#Use python
FROM python:3

#Use working directory
WORKDIR /app

#Copy
ADD . /app

#Install requirements
RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader wordnet

#Running on port 5000
EXPOSE 5000

#Set env var 
ENV NAME OpentoAll

#Run cmds
CMD ["python","run.py"]


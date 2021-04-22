FROM python
WORKDIR /usr/src/app
COPY requirements.txt ./
COPY chatbot.py ./
COPY config.ini ./
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python"]
CMD ["chatbot.py"]
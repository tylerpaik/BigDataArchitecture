FROM lunarreign/esport:latest
LABEL MAINTANIER="Luna McBride <luna.mcbride24@gmail.com>"

WORKDIR /srv
COPY . /srv
ENV PYTHONPATH = "${PYTHONPATH}:/srv/"

EXPOSE 5000

RUN pip install -r requirements.txt

ENTRYPOINT [""]
CMD ["python3", "app.py"]
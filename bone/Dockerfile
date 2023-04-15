FROM lunarreign/esport:latest
LABEL MAINTANIER="Luna McBride <luna.mcbride24@gmail.com>"

RUN python3 -m pip install --upgrade pip

WORKDIR /srv
COPY app.py /srv
copy templates /srv

EXPOSE 5000

RUN pip3 install --upgrade -r requirements.txt

ENTRYPOINT [""]
CMD ["python3", "app.py"]
VERSION=v2
DOCKERUSER=lunarreign

build:
	docker build -f Dockerfile -t esport .

run:
	docker-compose up -d

clean:
	docker-compose down

push:
	docker tag esport $(DOCKERUSER)/esport:$(VERSION)
	docker push $(DOCKERUSER)/esport:$(VERSION)
	docker tag esport $(DOCKERUSER)/esport:latest
	docker push $(DOCKERUSER)/esport:latest

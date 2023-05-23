# Rocket League Stats Project

Website Demo: https://www.youtube.com/watch?v=EHjBW0XLvlg

Presentation: https://github.com/tylerpaik/BigDataArchitecture/blob/main/RocketLeagueApp%20(1).pdf

This was our final project for the big data architecture class at CU Boulder (ATLS 4214/5214).  It is a website made to show statistics on specified Rocket League players, including their average goals, saves, assists, and general average stats per game in specified event sizes (10 for individual players, 5 for team inquiries). It utilizes an HTML/JavaScript frontend, a Flask API, A Redis Database, and Docker Containers to hold everything. We were experimenting to also have a RabbitMQ queue at the time, but did not finish that portion before the deadline. This also had a web presence on Google Cloud's Docker Compose Server service during the span of the class. It was not the cheapest in the world to keep running long term, so we decided the local sharing and the recorded demo should be enough to get the point across now that the semester is over.

---

How to use locally:

. In the command line, enter into the bone directory. It has the main docker integration code.

. Type 'make build' to build the docker code in the local directory.

. Type 'make run' to run the code.

The website can now be viewed on 127.0.0.1:5000 . Once you are done, be sure to type 'make clean' to stop it from running.

---

Team Members and Tasks:

Luna M: worked on api tasks with Flask, deployed the application using Docker and the Google Cloud Platform

Heather F: Built visualizations and handled data extraction.

Ryan S: Built the redis database and worked on Flask API tasks.

Filip F: Worked on the front end and worked on the betting line statistics system.

Tyler P: Worked on the front end and integrated it with the Flask API.

Chase T: Further stablized the API and spearheaded the our attempts at integrating RabbitMQ.

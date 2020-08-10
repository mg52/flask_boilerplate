# flask_postgresql

Python Flask Rest API with PostgreSQL

To Run:
<br/>
pip install -r requirements.txt
<br/>
flask run

To Migrate:
<br/>
flask db init
<br/>
flask db migrate -m "Initial migration."
<br/>
flask db upgrade

<br/>
<br/>
To Dockerize:
<br/>
docker image build -t flask_20200805_13 .
<br/>
docker run -p 8003:8003 -d flask_20200805_13


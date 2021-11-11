## How to run Front-end server locally

### Step 1

#### Open up a new terminal and go into Server directory

### `cd Server`

### Step 2

#### Change all endpoints in Client folder from '3.143.98.183' to 'localhost'

### Step 3

#### Change the database host name to 'localhost' for all microservice python file

<font size="2"> app.config['MYSQL_DATABASE_HOST'] = 'localhost' </font>

### Step 4

### `docker-compose up -d`

This command will set up all docker comtainers which contains the database and microservices.

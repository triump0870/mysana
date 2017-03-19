

# [mysana][mysana]

mysana is a _Life Goals Management App_. It is built with [Python][0] using the [Django Web Framework][1].

This project has the following basic apps:

* Accounts (Manages the user accounts)
* Profiel (Manages the user profile)
* Goals (Manages the life goals)
* Apis (Exposes the APIs for goals)
 
## Installation

### Quick start

To set up a development environment quickly, follow the below steps,

    1. `$ chmod +x setup.sh`
    2. `$ ./setup.sh`
    3. `$ fab build_images`
    4. `change the environment variables in local.env file located at srs/mysana/settings folder"
    5. `$ fab up` # for starting the containers
    

### Detailed instructions

Mysana app is deployed in AWS and is live [here][mysana]

#### Local Setup:
#### Dependencies:
1. docker-engine
2. docker-compose
3. pip
4. fabric 
5. django-environ
6. Set the environment variable in local.sample.env file

#### Linux setup:
`chmod +x setup.sh`

`./setup.sh`
`fab build_images` -- if you restarted the system

`fab up` -- to start the container

#### Mac setup:
1. install [docker for Mac][docker]
2. `fab build_images` 

3. `fab up` -- to start the container

#### Windows Setup:
Are you crazy? Flash your bootloader and install Linux ;) 

### Available Commands:
`fab up` -- start the container

`fab down` -- stop the container

`fab restart` -- restart the container

`fab status` -- status of the container

`fab build_images` -- create the docker images

## API Documentation: 
**GET _/api/goals_**

_**Description:** Get the list of the life goals of the user_

    Authentication: Basic

    Response Body:
    
        HTTP 200 OK
        Allow: GET, POST, HEAD, OPTIONS
        Content-Type: application/json
        Vary: Accept
        
        {
            "id": 1,
            "slug": "abc",
            "title": "abc",
            "description": "abc",
            "end_date": "2017-03-20",
            "is_completed": false
        }
        
**POST _/api/goals_**

_**Description:** Create a life goals for the user_

    Authentication: Basic

    Request Body:
        {
            "title": "abc",
            "description(optional)": "",
            "end_date": "2017-03-20"
        }
        
        
    Response Body:
    
        HTTP 201 Created
        Allow: GET, POST, HEAD, OPTIONS
        Content-Type: application/json
        Vary: Accept
        
        {
            "id": 1,
            "slug": "abc",
            "title": "abc",
            "description": "abc",
            "end_date": "2017-03-20",
            "is_completed": false
        }

**PUT _/api/goals/{id}_**

_**Description:** Update a life goals_
    
    Authentication: Basic

    Request Body:
        {
            "title": "new abc",
            "description(optional)": "",
            "end_date": "2017-03-20"
        }
        
        
    Response Body:
    
        HTTP 200 OK
        Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
        Content-Type: application/json
        Vary: Accept
        
        {
            "id": 1,
            "slug": "abc",
            "title": "new abc",
            "description": "abc",
            "end_date": "2017-03-20",
            "is_completed": false
        }

**PATCH _/api/goals/{id}_**

_**Description:** Complete a life goals_

    Authentication: Basic
        
    Response Body:
    
        HTTP 204 No Content
        Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
        Content-Type: application/json
        Vary: Accept
        
        {
            "id": 1,
            "slug": "abc",
            "title": "new abc",
            "description": "abc",
            "end_date": "2017-03-20",
            "is_completed": true
        }
        
**PATCH _/api/goals/{id}_**

_**Description:** Delete a life goals_
    
    Authentication: Basic
        
    Response Body:
        HTTP 204 No Content
        Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
        Content-Type: application/json
        Vary: Accept
        
        
[0]: https://www.python.org/
[1]: https://www.djangoproject.com/
[mysana]: http://mysana.rohanroy.com
[docker]: https://docs.docker.com/docker-for-mac/install/

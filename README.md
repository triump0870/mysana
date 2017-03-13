

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

Detailed doc is in development

[0]: https://www.python.org/
[1]: https://www.djangoproject.com/
[mysana]: http://mysana.rohanroy.com
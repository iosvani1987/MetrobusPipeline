# Metrobus Pipeline

# Description

Develop a data analysis pipeline using Mexico City's open data corresponding to the locations of the metrobus 
units corresponding to the locations of the Metrobus units so that it can be consulted through an API Rest 
consulted through an API Rest filtering by unit or by mayor's office.

# Installation
1. Clone the project
  ```
  git clone https://github.com/iosvani1987/MetrobusPipeline.git
```
2. Install docker to implifies the process of managing application processes in containers
  *https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04*

3. Create and start containers with the command
  ```
  docker-compose up
  ```
4. Execute a command in a running container ``` docker-compose exec backend bash``` to execute the data pipeline
with the command ``` python pipeline.py <path to input csv> ```

# API
1.  Get a list of available units
  ``` 
    https://localhost:5000/metrobuses
  ```
2. Get the location of a unit given its ID.
  ``` 
    https://localhost:5000/metrobuses/location/<int:vehicle_id>
  ```
3. Get a list of available county
  ``` 
    https://localhost:5000/metrobuses/county
  ```
4. Get the list of units that are located within a county
  ``` 
    https://localhost:5000/metrobuses/county/<string:county_name>
  ```
5. Get a metrobus by its vehicle_id
  ``` 
    https://localhost:5000/metrobuses/<int:vehicle_id>
  ```

  
  
  

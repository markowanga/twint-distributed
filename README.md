# Twint-Distributed [IN PROGRESS]
Sometimes there is a need to scrap many enormous tweet data in short time.
This project help to do this task. Solution is based on Twint — popular tool
to scrap twitter data. 

![Image of architecture](assets/architecture.png)

## Main concepts
 - Prepare architecture of microservices, which is scalable and can be 
 distributed for many machines 
 - Divide single scrap tasks for small task
 - Support that wne worker have error and the elementary task can be repeated 
 on other instance
 - Workaround twitter limit, which disallow to download many data from one ip address
 - All data are gathered into one location
 
 # How it works
 1. User add commands to scrap by HTTP request
 2. As a request result, server add commands to RabbitMQ for scrap data, 
 the time bounds can be divided for small intervals
 3. Workers get the messages from RabbitMQ to scrap data — they do this job
 4. When elementary task has been finished the data is upload to server
 5. Server save all received data to central storage
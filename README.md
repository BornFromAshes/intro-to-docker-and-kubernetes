# intro-to-docker-and-kubernetes
We want to develop a server to receive information about cryptocurrencies and maintain their current price.

## Python API
For this project we used coin.api to get the currencies. <br>
An example of the returned value from coin.api: <br>
![image](https://user-images.githubusercontent.com/117355603/216378263-6f3380cf-89c6-4dc9-b6b6-7e41f9e19f9f.png)
<br> to prevent additional requests to the API we use Redis cache.
Note that several fields are not hard coded:
- Port which our server runs on
- Valid time for redis cache
- The name of the cryptocurrency whose price we want
- API Key

## Applying it to kubernetes
In this section, the goal is to work with a tool with which you can easily and quickly raise a Kubernetes cluster on our system. This tool is called minikube. We have to write a series of files needed for our server to deploy it on the Kubernetes cluster.

- ConfigMap file: In this file, a series of program settings such as the address to which the program should send requests. server port; The name of the currency and the duration of the cache and APIKey are specified (for better readability of this file, you can write a separate config file and give its address to the ConfigMap file).
- Deployment file: to manage pods. In this file, the number of replicas of the program is set to 2.
- Service file: This file is for creating access to the server. <br>

Now that we have created all the files, we apply them to MiniKube using kubectl apply command.
Now we have to write these 3 files separately for the Redis database, with the difference that the number of replicas in the Deployment file should be equal to 1. For Redis cache, in addition to the above files, we need two other files to store information.

- Persistent Volume file: With this file, we specify the memory in the cluster.
- Persistent Volume Claim file: With this file, we create a request to allocate memory for a container. <br>

Apply the previous command again to the cluster with the Kubectl apply command.

## Try for yourself!
As specified in kubernetes section all you have to do is download Minikube and Docker. run Minikube in a shell and use the command

```
kubetcl apply
```
to apply yaml files in order specified in kubernetes section.

## Known issues
There aren't currently any issues so far so if you find any please create an issue on this repository. Any suggestions for implementation would also be greatly appreciated.

# Rambo

Simple image running _Nginx_ web server with _Rambo_ related web pages. The request part of Rambo series can be specified by tags:

* `latest`, `2019`, `5`
* `2008`, `4`
* `1988`, `3`
* `1985`, `2`
* `1982`, `1`

**Warning: The part 3 will terminate after 10 seconds!**

This image is used for my _Docker_ and _Kubernetes_ courses.


## Running the Container

```
docker container run -t bletvaska/rambo:TAG
```

Name: Ronald Leung
NetID: rfl68

Challenges Attempted (Tier I/II/III): N/A
Working Endpoint: GET /api/courses/
Your Docker Hub Repository Link: https://hub.docker.com/layers/ronaldleung/cms/latest/images/sha256-f42cacc80a588ec7cc3820ea2e1ee24f340bf6cc072b793d02ebfc2c7149ebac?context=explore

Questions:
Explain the concept of containerization in your own words.
Containerization is the process of packaging code into standardized units that that can be easily put into a production environment, easing the process of deployment and eliminating the problem of "but it works on my machine".

What is the difference between a Docker image and a Docker container?
A Docker image provides the blueprint to running the source code. A Docker container is a running instance of a Docker image, where multiple containers can run multiple instances of an application.

What is the command to list all Docker images?
`docker images`

What is the command to list all Docker containers?
`docker ps`

What is a Docker tag and what is it used for?
A Docker tag is a type of optional label appended after the repository name, denoted by a colon (:). It is often used to show the version of the image (e.g. v1.0)

What is Docker Hub and what is it used for?
Docker Hub is a cloud-based service offering hosting for Docker images. It is used by remote servers which access the images hosted on Docker Hub in order to run them.

What is Docker compose used for?
Docker Compose is a tool that assists with running and multi-container applications that could contain different packages/dependencies (e.g. Postgres, Python)

What is the difference between the RUN and CMD commands?
The RUN command is used to run a shell command, such as `mkdir usr/app`. CMD can only be used once - it is the final shell command that is run in a Dockerfile.
Name: Ronald Leung
NetID: rfl68

Working Endpoint: GET /api/courses/
Your Server Address: 34.150.226.217

Questions:
Explain the concept of deployment in your own words.
Deployment is when code (in this case, a Flask API + database) is run and shared publicly for others to access online. In this case, deploying our API will allow anyone to make requests to it.

What are environment variables?
Environment variables are secrets or credentials that can be accessed by a program. They are supposed to be kept private (i.e. not publicly accessible to users). Typically, they are used to hide private keys that are needed to authenticate with other APIs or services.

What is the filename of the file where environment variables are traditionally stored?
.env

What is the network protocol we use to access servers?
SSH

Explain the concept of clustering in your own words.
Clustering is the management of multiple servers so that different tasks are handled by individual servers. This allows for better performance overall.

Explain the concept of load balancing in your own words.
Load balancing is the process of managing traffic across multiple servers. This ensures that in periods of high volume/traffic, the system is not overloaded as the work is handled by different servers.
## Fieldline Client

Currently the goal is to get the data out of the chassis and into a fieldtrip buffer. This goal may later change. Who is to say.

## How to Use:
### Prereqs:
Make sure your python version is >=3.9.

Currently working on three layers that work on top of each other. 

Base layer will consist of free functions that take either a fieldline or fieldtrip client as arguments, as well as other things depending on the function. To use this layer, the user is expected to manage these clients themselves and call the functions as needed.

Above that we will provide a single object, MNE Client, which manages those two separate clients. Ideally you provide the IP addresses of where to find the buffer and chassis, and then all function calls are parameterless instructions on what you want to happen.

Lastly, we will provide an application where the user can pick from menu options to choose what tey would like to do.


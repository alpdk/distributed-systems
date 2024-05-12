# How to use network classes

## How to use *server.py* script

This class requires from 0 to 2 parameters:

1) Server host *(by default "127.0.0.1")*
2) Server port *(by default 5000)*

For usages, you should create this class and call *start()* method.

Example of exploitation:

```
server = Server()

server.start()
```

## How to use *peer.py* script

This class requires from 2 to 4 parameters:

1) Peer host *(for now only "127.0.0.1")*
2) Peer port *(more than 5000)*
3) Server host *(by default "127.0.0.1")*
4) Server port *(by default 5000)*

For usages, you should create this class and call *start()* method. 
Also host and port should have connected user for work.

Example of exploitation:

```
peer = Peer("127.0.0.1", 5001)

server.start()
```


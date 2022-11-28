# BankingSystem - Client-Centric Consistency 

This project is continuation of [Project-1](https://github.com/vselvaraj6/CSE531-Project1), to implement the client-centric consistency model on top of Project 1: gRPC, specifically Montonic Write consistency and Read your Write Consistency of the replicated data in the bank.

## Technologies used
- Python 3.10.X
- gRPC
- Protobuf
- grpcio-tools
- Linux - Ubuntu 22.04

The message types and services are defined in `/proto/service.proto`. The client stub for gRPC is auto-generated using grpcio-tools by running the following command

To generate grpc server and client stub files:
```
python3 -m grpc_tools.protoc -I proto --python_out=. --grpc_python_out=. proto/service.proto
```

## Project Execution

To run server and spin up branch processes, open a terminal and run the following command. You need to pass `input.json` as an argument to `server.py`:
```bash
python3 server.py input.json
```

To run client and execute events, open a new terminal and run the following command.  You need to pass `input.json` as an argument to `client.py`::
```bash
python3 client.py input.json
```
The final output is saved in `output.txt` file in the current directory.
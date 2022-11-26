# BankingSystem - Logical Clock (Lamport's Algorithm)

This project is continuation of [Project-1](https://github.com/vselvaraj6/CSE531-Project1), to implement Lamport’s Logical Clock algorithm to record the logical clock between the branch processes and customer processes. This logical clock will ensure the happens-before relationship between the processes for inter-process and intra-process communications. This algorithm is implemented using six sub-interfaces (Event_Request, Event_Execute, Propagate_Request, Propogate_Execute, Propogate_Response, Event_Response) that updates the local clock of the branch process and records the local clock of events. Invoke the sub-interfaces in the appropriate location of Withdraw and Deposit interfaces, so that the happens-before order is preserved.

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
The final output is printed in the console in the client process as below:

```json
{'pid':2,
'data': [
{'id': 2, 'name': deposit_request, 'clock': 3}
{'id': 2, 'name': deposit_execute, 'clock': 4}
{'id': 2, 'name': deposit_propogate_response, 'clock': 7}
{'id': 2, 'name': deposit_propogate_response, 'clock': 10}
{'id': 2, 'name': deposit_response, 'clock': 11}
{'id': 4, 'name': withdraw_propogate_request, 'clock': 15}
{'id': 4, 'name': withdraw_propogate_execute, 'clock': 16}
]}
{'pid':1,
'data': [
{'id': 2, 'name': deposit_propogate_request, 'clock': 5}
{'id': 2, 'name': deposit_propogate_execute, 'clock': 6}
{'id': 4, 'name': withdraw_propogate_request, 'clock': 12}
{'id': 4, 'name': withdraw_propogate_execute, 'clock': 13}
]}
{'pid':3,
'data': [
{'id': 2, 'name': deposit_propogate_request, 'clock': 8}
{'id': 2, 'name': deposit_propogate_execute, 'clock': 9}
{'id': 4, 'name': withdraw_request, 'clock': 10}
{'id': 4, 'name': withdraw_execute, 'clock': 11}
{'id': 4, 'name': withdraw_propogate_response, 'clock': 14}
{'id': 4, 'name': withdraw_propogate_response, 'clock': 17}
{'id': 4, 'name': withdraw_response, 'clock': 18}
]}
{'eventid':2,
'data': [
{'clock': 3, 'name': deposit_request}
{'clock': 4, 'name': deposit_execute}
{'clock': 5, 'name': deposit_propogate_request}
{'clock': 6, 'name': deposit_propogate_execute}
{'clock': 7, 'name': deposit_propogate_response}
{'clock': 8, 'name': deposit_propogate_request}
{'clock': 9, 'name': deposit_propogate_execute}
{'clock': 10, 'name': deposit_propogate_response}
{'clock': 11, 'name': deposit_response}
]}
{'eventid':4,
'data': [
{'clock': 10, 'name': withdraw_request}
{'clock': 11, 'name': withdraw_execute}
{'clock': 12, 'name': withdraw_propogate_request}
{'clock': 13, 'name': withdraw_propogate_execute}
{'clock': 14, 'name': withdraw_propogate_response}
{'clock': 15, 'name': withdraw_propogate_request}
{'clock': 16, 'name': withdraw_propogate_execute}
{'clock': 17, 'name': withdraw_propogate_response}
{'clock': 18, 'name': withdraw_response}
]}
```


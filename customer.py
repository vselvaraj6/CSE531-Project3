import grpc
import time
import service_pb2_grpc
import service_pb2
import json
import sys

class Customer:
    def __init__(self, id, events):
        # unique ID of the Customer
        self.id = id
        # events from the input
        self.events = events
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # pointer for the stub
        self.stub = None
        # data
        self.data = list()

    def __str__(self) -> str:
        return "id: %s, recv: %s".format(self.id,self.recvMsg)  

    def __repr__(self):
        return str(self)     

    def executeWithdrawEvents(self):

        for event in self.events:
            if event.get('interface') == 'withdraw':
                dest = event.get('dest')
                request = service_pb2.WithdrawRequest(id=self.id, event=event)
                port = 50050 + dest
                host = 'localhost:'+str(port)
                with grpc.insecure_channel(host) as channel:
                    self.stub = service_pb2_grpc.BranchStub(channel)
                    self.stub.Withdraw(request=request)
                channel.close()   

    def executeDepositEvents(self):

        for event in self.events:
            if event.get('interface') == 'deposit':
                dest = event.get('dest')
                request = service_pb2.DepositRequest(id=self.id, event=event)
        
                port = 50050 + dest
                host = 'localhost:'+str(port)
                
                with grpc.insecure_channel(host) as channel:
                    self.stub = service_pb2_grpc.BranchStub(channel)
                    self.stub.Deposit(request=request)
                channel.close()                                

    def executeQueryEvents(self):
        
        for event in self.events:
            if event.get('interface') == 'query':
                dest = event.get('dest')
                request = service_pb2.QueryRequest(id=self.id, event=event)
                port = 50050 + dest
                host = 'localhost:'+str(port)
                with grpc.insecure_channel(host) as channel:
                    self.stub = service_pb2_grpc.BranchStub(channel)
                    response = self.stub.Query(request=request)
                    self.recvMsg.append(response)
                channel.close()                    

  
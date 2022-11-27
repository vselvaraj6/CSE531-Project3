import grpc
import service_pb2_grpc
import service_pb2
import time

class BranchServicer(service_pb2_grpc.BranchServicer):

    def __init__(self, id, balance, branches, data):
        # unique ID of the Branch
        self.id = id
        # replica of the Branch's balance
        self.balance = balance
        # the list of process IDs of the branches
        self.branches = branches
        # the list of Client stubs to communicate with the branches
        self.stubList = list()
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # stores output data
        self.data = data

    def __str__(self) -> str:
       return "id: {0}, balance: {1}, branches: {2}, data: {3}".format(self.id,self.balance,self.branches,self.data)     

    def orchestrate_propogate_withdraw(self, id, event_id, port):
      host = 'localhost:'+str(port)
      result = None
      with grpc.insecure_channel(host) as channel:
          self.stub = service_pb2_grpc.BranchStub(channel)
          request = service_pb2.WithdrawPropogateRequest(balance=self.balance, id=id, event_id=event_id)
          result = self.stub.WithdrawPropogate(request=request)
      channel.close()   
      return result

    def orchestrate_propogate_deposit(self, id, event_id, port):
      host = 'localhost:'+str(port)
      result = None
      with grpc.insecure_channel(host) as channel:
          self.stub = service_pb2_grpc.BranchStub(channel)
          request = service_pb2.DepositPropogateRequest(balance=self.balance, id=id, event_id = event_id)
          result = self.stub.DepositPropogate(request=request)
      channel.close()             
      return result


    # TODO: students are expected to process requests from both Client and Branch
    def Withdraw(self, request, context):
        output = service_pb2.WithdrawResponse()
        try:
          event = request.event
          if event.interface == 2:
              output.id = self.id
              self.balance = self.balance - event.money
              output.result = 1
              output.interface = event.interface
              
              for process in self.branches.keys():
                if process != self.id: 
                  result = self.orchestrate_propogate_withdraw(process, request.event.id, self.branches.get(process))

        except Exception as e:
          print('Exception at Withdraw:', e)      
        return output

    def Deposit(self, request, context):
        output = service_pb2.DepositResponse()
        try:
          event = request.event 
          if event.interface == 1:
           
              output.id = self.id
              self.balance = self.balance + event.money
              output.result = 1
              output.interface = event.interface

              for process in self.branches.keys():
                if process != self.id: 
                  result = self.orchestrate_propogate_deposit(process, request.event.id, self.branches.get(process))

        except Exception as e:
          print('Exception at Deposit', e)    
        return output    

    def Query(self, request, context):
        output = service_pb2.QueryResponse()
        output.balance = self.balance  
        output.id = request.id
        output.result = 1
        output.interface = 3
        print('output: ', output)
        return output

    def WithdrawPropogate(self, request, context):
        output = service_pb2.WithdrawPropogateResponse()

        try:
          output.id = request.id 
          self.balance = request.balance     
          output.result = 1

        except Exception as e:
          print('Exception at WithdrawPropogate', e)  
        return output

    def DepositPropogate(self, request, context):
      output = service_pb2.DepositPropogateResponse() 

      try:
        output.id = request.id

        self.balance = request.balance 
        output.result = 1

      except Exception as e:
        print('Exception at DepositPropogate', e)  
      return output
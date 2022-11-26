import grpc
import service_pb2_grpc
import service_pb2
import time

class BranchServicer(service_pb2_grpc.BranchServicer):

    def __init__(self, id, balance, branches, clock, data):
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
        # stores local clock
        self.clock = clock
        # stores output data
        self.data = data

    def __str__(self) -> str:
       return "id: {0}, balance: {1}, branches: {2}, clock: {3}, data: {4}".format(self.id,self.balance,self.branches,self.clock,self.data)     

    def orchestrate_propogate_withdraw(self, id, event_id, port, clock):
      host = 'localhost:'+str(port)
      result = None
      with grpc.insecure_channel(host) as channel:
          self.stub = service_pb2_grpc.BranchStub(channel)
          request = service_pb2.WithdrawPropogateRequest(balance=self.balance,id=id, event_id=event_id, clock=clock)
          result = self.stub.WithdrawPropogate(request=request)
      channel.close()   
      return result

    def orchestrate_propogate_deposit(self, id, event_id, port, clock):
      host = 'localhost:'+str(port)
      result = None
      with grpc.insecure_channel(host) as channel:
          self.stub = service_pb2_grpc.BranchStub(channel)
          request = service_pb2.DepositPropogateRequest(balance=self.balance, id=id, event_id = event_id, clock=clock)
          result = self.stub.DepositPropogate(request=request)
      channel.close()             
      return result    

    def event_request(self, id, event_id, event_name, remote_clock):
      self.clock = max(self.clock, remote_clock) + 1
      clock_event = service_pb2.ClockEvent()
      clock_event.id = id
      clock_event.event_id = event_id
      clock_event.name = event_name
      clock_event.clock = self.clock
      return clock_event

    def event_execute(self, id, event_id, event_name):
      self.clock = self.clock + 1  
      clock_event = service_pb2.ClockEvent()
      clock_event.id = id
      clock_event.event_id = event_id
      clock_event.name = event_name
      clock_event.clock = self.clock
      return clock_event

    def propogate_request(self, id, event_id, event_name, remote_clock):
      self.clock = max(self.clock, remote_clock) + 1  
      clock_event = service_pb2.ClockEvent()
      clock_event.id = id
      clock_event.event_id = event_id
      clock_event.name = event_name
      clock_event.clock = self.clock
      return clock_event

    def propogate_execute(self, id, event_id, event_name):
      self.clock = self.clock + 1
      clock_event = service_pb2.ClockEvent()
      clock_event.id = id
      clock_event.event_id = event_id
      clock_event.name = event_name
      clock_event.clock = self.clock
      return clock_event   

    def propogate_response(self, id, event_id, event_name, remote_clock):
      self.clock = max(self.clock, remote_clock) + 1 
      clock_event = service_pb2.ClockEvent()
      clock_event.id = id
      clock_event.event_id = event_id
      clock_event.name = event_name
      clock_event.clock = self.clock
      return clock_event

    def event_response(self, id, event_id, event_name):
      self.clock = self.clock + 1  
      clock_event = service_pb2.ClockEvent()
      clock_event.id = id
      clock_event.event_id = event_id
      clock_event.name = event_name
      clock_event.clock = self.clock
      return clock_event


    # TODO: students are expected to process requests from both Client and Branch
    def Withdraw(self, request, context):
        output = service_pb2.WithdrawResponse()
        try:
          event = request.event
          if event.interface == 2:
              output.clock_events.append(self.event_request(self.id, request.event.id, 'withdraw_request', request.clock))
              output.clock_events.append(self.event_execute(self.id, request.event.id, 'withdraw_execute'))
              output.id = self.id
              self.balance = self.balance - event.money
              output.result = 1
              output.interface = event.interface
              
              for process in self.branches.keys():
                if process != self.id: 
                  result = self.orchestrate_propogate_withdraw(process, request.event.id, self.branches.get(process), self.clock)
                  output.clock_events.extend(result.clock_events)
                  output.clock_events.append(self.propogate_response(self.id, request.event.id, 'withdraw_propogate_response', result.clock))

              output.clock_events.append(self.event_response(self.id, request.event.id, 'withdraw_response'))    

        except Exception as e:
          print('Exception at Withdraw:', e)      
        return output

    def Deposit(self, request, context):
        output = service_pb2.DepositResponse()
        try:
          event = request.event 
          if event.interface == 1:
              output.clock_events.append(self.event_request(self.id, request.event.id, 'deposit_request', request.clock))
              output.clock_events.append(self.event_execute(self.id, request.event.id, 'deposit_execute'))
              output.id = self.id
              self.balance = self.balance + event.money
              output.result = 1
              output.interface = event.interface

              for process in self.branches.keys():
                if process != self.id: 
                  result = self.orchestrate_propogate_deposit(process, request.event.id, self.branches.get(process), self.clock)
                  output.clock_events.extend(result.clock_events)
                  output.clock_events.append(self.propogate_response(self.id, request.event.id, 'deposit_propogate_response', result.clock))
             
              output.clock_events.append(self.event_response(self.id, request.event.id, 'deposit_response'))
              
        except Exception as e:
          print('Exception at Deposit', e)    
        return output    

    def Query(self, request, context):
        output = service_pb2.QueryResponse()
        output.money = self.balance  
        output.id = self.id
        output.result = 1
        output.interface = 3
        return output

    def WithdrawPropogate(self, request, context):
        output = service_pb2.WithdrawPropogateResponse()

        try:
          output.id = request.id 

          output.clock_events.append(self.propogate_request(request.id, request.event_id, 'withdraw_propogate_request', request.clock))
          output.clock_events.append(self.propogate_execute(request.id, request.event_id, 'withdraw_propogate_execute'))
       
          self.balance = request.balance     
          output.result = 1
          output.clock = self.clock

        except Exception as e:
          print('Exception at WithdrawPropogate', e)  
        return output

    def DepositPropogate(self, request, context):
      output = service_pb2.DepositPropogateResponse() 

      try:
        output.id = request.id

        output.clock_events.append(self.propogate_request(request.id, request.event_id, 'deposit_propogate_request', request.clock))
        output.clock_events.append(self.propogate_execute(request.id, request.event_id, 'deposit_propogate_execute'))
        
        self.balance = request.balance 
        output.result = 1
        output.clock = self.clock

      except Exception as e:
        print('Exception at DepositPropogate', e)  
      return output
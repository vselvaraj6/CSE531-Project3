import json
import sys
from branch import BranchServicer
from multiprocessing import Process
from concurrent import futures
import service_pb2_grpc
import grpc
import time

def parse_input_file():
    branch_input_items =list()
    try:
        with open(input_file, 'r') as f:
            input_items = json.load(f)    

            for input_item in input_items:
                if('branch' == input_item.get('type')):
                    branch_input_items.append(input_item)   
    except:
        print("Invalid format. Please check the content of input.json file")   
    return branch_input_items


def start_bank_process(id, balance, branches, port, data):
    """
    This method is a helper method to start bank branch processes - each branch processes run on its own ports
    """
    GRPC_BIND_ADDR = '[::]:'+str(port)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=(('grpc.so_reuseport',0),))
    service_pb2_grpc.add_BranchServicer_to_server(BranchServicer(id, balance, branches, 1), server)
    server.add_insecure_port(GRPC_BIND_ADDR)
    server.start()
    print("gRPC Bank process started for ID:" , id, "Listening on port:",  GRPC_BIND_ADDR)
    server.wait_for_termination()   


print("Running server.py..")             

if len(sys.argv) < 2:
    print("Missing input file. Pass input.json file as argument!")
    exit()

branch_processes = []
port = 50051
branches = []
input_file = sys.argv[1]
branch_input_items = parse_input_file()

port_map = {}
#populate ports for no. of bank process
for branch_input_item in branch_input_items:
    key = branch_input_item.get('id')
    port_map[key] = port
    port = port + 1

# Spin up branch processes for each branch events concurrently in its own port
for branch_input_item in branch_input_items:
    branch_id = branch_input_item.get('id')
    data_dict = {branch_id: []}
    branch = BranchServicer(branch_id, branch_input_item.get('balance'), port_map, 1)
    print("Invoking branch process for id : ", branch.id)
    branch_process = Process(target=start_bank_process, args=(branch.id,branch.balance,branch.branches,port_map.get(branch.id),data_dict))
    branch_processes.append(branch_process)
    branches.append(branch)
    branch_process.start()

for branch_process in branch_processes:
    branch_process.join()

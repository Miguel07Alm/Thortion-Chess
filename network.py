import socket, pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.server = socket.gethostbyname_ex(socket.gethostname())[-1][0] #123.456.7.89
        self.server = socket.gethostbyname_ex(socket.gethostname())[-1][0]
        self.port = 12000
        self.addr = (self.server, self.port)
        self.team = self.connect()
        self.data = []
        
        
    def get_team(self):
        return self.team
    
    def connect(self):
        try: 
            self.client.connect_ex(self.addr)
            return pickle.loads(self.client.recv(4096))[0]
        except Exception as e:
            print(e)
    def send(self, data):
        # Send data to the server
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(4096))
        except socket.error as e:
            print(e)        




        
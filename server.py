import socket, pickle, sys
from _thread import *
from random import choice

host = "0.0.0.0"
port = 12000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
BUFF_SIZE = 4096
try:
    s.bind((host, port))
    
except socket.error as e:
    str(e)



def make_info(turns, times, used_coords,deleted_pieces,points, name_pieces, coord_data = None):
    if coord_data == None: return [turns, times, used_coords,deleted_pieces, points, name_pieces]
    else: return [turns, times, used_coords, deleted_pieces, points, name_pieces,coord_data]
s.listen(2)
print("Waiting for connection, Server Started")

n_conn = 0
teams = ["white", "black"]

turns = [teams[0]]
data_online = [[None, [0,0], turns, [], [], 0, [],[],[None, None, None]], [None, [0,0], turns,[], [], 0, [],[],[None, None, None] ]] #Team, times[white, black], turns, used_coords,deleted_pieces,points,[name_pieces],chatData[texts, time],coord_data[name, initial_coord, last_coord]
def threaded_client(conn, team_chose):
    global n_conn
    idx_team = 0 if team_chose == "white" else 1
    data_online[idx_team][0] = team_chose
    conn.send(pickle.dumps(data_online[idx_team]))
    
    while True:
        try:
            if n_conn > 2:
                print("The server only can accept 2 players.")
                sys.exit()
            data = pickle.loads(conn.recv(BUFF_SIZE))
            data_online[idx_team][2] = data[0]
            data_online[idx_team][1] = data[1]
            data_online[idx_team][3] = data[2]
            data_online[idx_team][4] = data[3]
            data_online[idx_team][5] = data[4]
            data_online[idx_team][6] = data[5]
            data_online[idx_team][7] = data[6]
            
            if len(data) == len(data_online[idx_team]) - 1:
                data_online[idx_team][-1] = data[-1]
                #print(data_online[idx_team])
            else:
                data_online[idx_team][-1] = [None, None, None]
                
            if not data:
                print("Disconnected")
                break
            else:
                pass
                #print(f"Received from {team}: {data_online[idx_team]}")
                #print(f"Sending for {team}: {data_online[idx_team - 1]}")
            conn.sendall(pickle.dumps(data_online[idx_team - 1]))
        
        except Exception as e:
            #print("Error was made")
            print(e)
    print("Lost connection")
    n_conn -= 1
    conn.close()
    
client_data = {}
while True:
    conn, addr = s.accept()
    print(f"Connected to: {addr}")
    '''IP = socket.gethostbyname(socket.gethostname())
    if IP not in verification.keys(): 
        team = choice(teams) 
        verification[IP] = team if team not in verification.values() else teams[teams.index(team) - 1]'''
    n_conn += 1
    client_data[str(n_conn)] = choice(teams) if len(client_data) == 0 else teams[teams.index(list(client_data.values())[0]) - 1]
    print(client_data)
    
    start_new_thread(threaded_client, (conn,client_data[str(n_conn)]))    

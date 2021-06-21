import pygame, string
import binary as bin, time, sys
from pygame import Vector2
global colorkey, color, king_color, white, black, realKingColor
colorkey = [0] * 3
color = [255] + [0] * 2
king_color = [255, 1, 0]
realKingColor = [255, 242, 0]
white = [255, 43,54]
black = [51, 91, 93]
contour = [255,132,0]

ticks_game_ended = 0
total_t = None

afk_ticks = 0
afk_t = None

waiting_ticks = 0
def blit(win,obj, pos):
    win.blit(obj, pos)
def swap_color(obj_img,newColor, oldColor):
    obj_img.set_colorkey(pygame.Color(oldColor))
    surf = obj_img.copy()
    surf.fill(pygame.Color(newColor))
    surf.blit(obj_img,(0,0))
    surf.set_colorkey(colorkey)
    return surf

def clip(surf,x,y,width,height):
    handle_surf = surf.copy()
    clipR = pygame.Rect(x,y,width,height)
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()

def make_info(turns, times, used_coords,deleted_pieces,points, name_pieces, chatData, coord_data = None ):
    if coord_data == None: return [turns, times, used_coords,deleted_pieces, points, name_pieces, chatData]
    else: return [turns, times, used_coords, deleted_pieces, points, name_pieces, chatData, coord_data]

def looking_for_diff_pieces(all_pieces, initial_coord, last_coord,positions, coords_ingame):
    for p in all_pieces:
        if p.initial_coord == initial_coord and p.last_coord != last_coord:
            p.new_coord(positions[last_coord], [last_coord], coords_ingame)
def rgb_to_hex(rgb):
    return "#" + "".join(str(bin.dec_to_hex(x)) if len(str(bin.dec_to_hex(x))) == 2 else "0" + str(bin.dec_to_hex(x)) for idx,x in enumerate(rgb) if idx < 3)
def hex_to_rgb(hex):
    hex = hex.lstrip("#")
    hex = "".join(x.rjust(2) if idx % 2 == 0 else x for idx,x in enumerate(hex)).split(" ")[1:]
    return list(bin.hex_to_dec(x) for x in hex)
def get_piece_directly(pieces,name, initial_coord):
    for p in pieces:
        if p.initial_coord == initial_coord and p.name == name:
            return p
def get_piece_with_lastcoord(pieces, last_coord):
    for p in pieces:
        if p.last_coord == last_coord:
            return p
def pawn_algorithm(white_pieces, black_pieces, name_pieces, team, Piece, positions):
    order_pawns_0 = -1 #The last_position of the name_pieces in the beginning
    if len(name_pieces) > 0: 
        name_piece = name_pieces[-1]
        
        otherTeamPieces = white_pieces if team == "black" else black_pieces
        pos = 8 if team == "black" else 1
        if sum(int(p.last_coord[1]) == pos for p in otherTeamPieces) > 0 and name_piece != "pawn":
            for p in otherTeamPieces:
                if p.name == "pawn" and int(p.last_coord[1]) == pos:
                    t = p.team
                    c = p.last_coord
                    idx_choice = p.name_choice_pieces.index(name_piece)
                    otherTeamPieces.append(Piece(name_piece, c, positions[c], p.choice_pieces[idx_choice],t))
                    del otherTeamPieces[otherTeamPieces.index(p)]
                    

def ending_frame(win, team, otherTeam, font, kind):
    global ticks_game_ended, total_t
    #kinds: 0 -> checkmate, 1 -> king suffocated, 2 -> Time consumed, 3 -> not enough material
    ticks_game_ended += 1
    if ticks_game_ended == 1:
        total_t = time.time()
    font.n_times = 6
    width = win.get_size()[0]
    x,y = (width // 2, 15)
    texts = [f"{team} team has won!".capitalize(),f"King suffocated!",f"{otherTeam} team has won".capitalize(),f"Draw!"]
    font.rendered_text(texts[kind], win, (x - font.text_len(texts[kind]) * 0.8 ,y))
    
    font.n_times = 2
    if time.time() - total_t >= 5:
        time.sleep(2) 
        sys.exit()
        
    
    
def get_piece(pieces, team, name, initial_coord = None):
    for piece in pieces:
        if initial_coord != None:
            if piece.initial_coord == initial_coord: return piece
        else:
            if piece.name == name and piece.team == team:
                return piece

def time_system(win, font, times, turns, delta_time, t):
    #1 -> white; 2 -> black
    # The server has the time of the two teams, which do the exchange among them 
    idx = 0 if turns[-1] == "white" else 1
    times[idx] += 0.02 * delta_time 
    
    min1, min2 = int((t - times[idx]) // 60),int((t - times[idx - 1]) // 60)
    sec1, sec2 = int((t - times[idx]) - min1 * 60), int((t - times[idx - 1]) - min2 * 60)
    z1, z2 = "0" * (2 - len(str(sec1))), "0" * (2 - len(str(sec2)))
    real_time1 = f"{min1}:{z1}{sec1}" if times[idx] <= t else f"0:00"
    real_time2 = f"{min2}:{z2}{sec2}" if times[idx - 1] <= t else f"0:00"
        
    #print(delta_time,real_time1, turns[-1])
    font.n_times = 4
    if idx == 0:
        font.rendered_text(real_time1, win, (603 , 70 + 550))
        font.rendered_text(real_time2, win, (603, 20))
    else:
        font.rendered_text(real_time2, win, (603, 70 + 550))
        font.rendered_text(real_time1, win, (603, 20))
    font.n_times = 2

def coord_system(win, surf,used_coords, font, min_rounds,n_round, event_condition, mouse_surf):
    y = 110
    surf = swap_color(surf, "#3d6e70", surf.get_at((4,4))) # Inside          
    if not event_condition: surf = swap_color(surf, "#3ca370", surf.get_at((0,0))) # Border  
        
    else: surf = swap_color(surf, "#4ccd8c", surf.get_at((0,0))) # Border
    x0 = 603  
    win.blit(mouse_surf, (x0 - 55, 45))
    win.blit(surf, (x0,100))
    # Castling explanation
    font.rendered_text("SC=O-O", win, (x0, y - 40))
    font.rendered_text("SL=O-O-O", win, (x0, y - 60))
    
    for round in range(min_rounds[0], n_round + 1):
        x = x0 + 7
        font.rendered_text(str(round) + ".", win, (x, y))
        for c in used_coords[(round * 2 - 1) - 1: (round * 2)]:
            font.rendered_text(c, win, (x + 9 + (5 * len(str(round))), y))
            x += 30
        y += 20
    if len(range(min_rounds[0], n_round + 1)) >= 20 and not event_condition:
        min_rounds[0] = n_round // 2
    
def chat_system(win, surf, chatData, font, boolChat, text_range, event_condition):
    if boolChat:
        surf = swap_color(surf, "#046570",surf.get_at((0,0)))
        surf = swap_color(surf, "#13908c",surf.get_at((4,4))).convert_alpha()
        surf.set_alpha(160)
        blit(win, surf, (0,100))
        x,y = 0, 120
        size_s = font.lettersImgs["a"].get_size()[1]

        if len(chatData) > 0:
            texts0 = [k + x[0] for k,data in chatData.items() for x in data]
            times = [x[1] for data in chatData.values() for x in data]
            sorted_times = sorted(times)
            
            texts = [texts0[idx] for idx in [times.index(t) for t in sorted_times]]
        
        if not event_condition:
            if len(range(text_range[0], len(texts))) >= 20: text_range[0] = len(texts)//2
        
        for text in texts[text_range[0]:]:
            team = text[:5]
            text = text[5:]
            s = pygame.Surface([size_s] * 2).convert_alpha()
            c = [255] * 3 if team == "white" else [0] * 3
            s.fill(c)
            blit(win, s, (x, y + size_s//2))
            font.rendered_text(text, win, (x + size_s + 3, y))
            y += 20
def waiting(win,font, pos_phrase, width):
    global waiting_ticks
    waiting_ticks += 1
    x,y = pos_phrase
    if waiting_ticks % 17 == 0: font.rendered_text("|", win, (x + width, y))
    else: font.rendered_text("", win, (x + width, y))
    
    if waiting_ticks >= 1000: waiting_ticks = 1
def functional_system_of_pieces(deleted_pieces, win, font, points):
    # It does that the algorithm takes the killed pieces and put them in the screen depending of the team 
    # xb -> pos in the black x coord; xw -> pos in the white x coord
    xb = xw = 100
    dn = points[0] - points[1]
    nb = dn
    nw = -dn
    nb, nw = str("+") + str(nb) if nb > 0 else str(nb), str("+") + str(nw) if nw > 0 else str(nw)
    
    n = sum(map(lambda p: p.team == "black", deleted_pieces))
    max_xb = 100 + 25 * n
    max_xw = 100 + 25 * abs((len(deleted_pieces) - n))
    y = 70

    for p in deleted_pieces:
        img = pygame.transform.scale(p.img, (20,20))
        img.set_colorkey(colorkey)
        if int(nw) > 0: font.rendered_text(nw, win, (max_xw + 10,y + 5))
        if int(nb) > 0: font.rendered_text(nb, win, (max_xb + 10,(y + 5) + 550))
        if p.team == "white":
            win.blit(img,(xw, y))
            xw += 25
        else:
            win.blit(img,(xb, y + 550))
            xb += 25



def get_pieces(pieces_imgs):
    pieces = {}
    name_pieces = ["pawn","rook", "knight", "bishop", "queen", "king"]
    for i in range(len(name_pieces)):
        pieces_imgs[i].set_colorkey(colorkey)
        pieces[name_pieces[i]] = pieces_imgs[i]
    
    return pieces
def king_suffocated(king, all_pieces):
    if king.n_movements == 0 and not king.check:
        for p in all_pieces:
            if p.team == king.team:
                ideal_coords = p.ideal_coords if p.name != "queen" else set(p.special_ideal_coords[0]).union(set(p.special_ideal_coords[1]))
                if len(ideal_coords) > 0:
                    return False
        return True
def search_pieces_with_a_coord(all_pieces, coord):
    for piece in all_pieces:
        if piece.last_coord == coord:
            return piece
def convert_position_into_coord(position, positions):
    coords = list(positions.keys())
    idx_coord = list(positions.values()).index(position)
    return coords[idx_coord]

def put_coords_ingame(all_pieces, coords_ingame):
    for p in all_pieces:
        if p.last_coord not in coords_ingame: coords_ingame.append(p.last_coord)
    
def check(all_pieces, positions, king, coords_ingame):
    pieces_doing_check = []
    for piece in all_pieces:
        if piece.team != king.team:
            for rival_coord in piece.rival_coords:
                idx_coord = list(positions.values()).index(rival_coord)
                coord = list(positions.keys())[idx_coord]
                piece2 = search_pieces_with_a_coord(all_pieces, coord)
                if piece2 != None:
                    if piece2 == king:
                        name_piece = piece.name
                        if name_piece == "king":
                            if piece.king_condition(king.last_coord, coords_ingame)[0] and piece not in pieces_doing_check: pieces_doing_check.append(piece)
                        if name_piece == "rook":
                            if piece.rook_condition(king.last_coord, coords_ingame, king.last_coord) and piece not in pieces_doing_check: 
                                pieces_doing_check.append(piece)
                        elif name_piece == "knight":
                            if (abs(int(king.last_coord[1]) - int(piece.last_coord[1])) == 2 and abs(piece.letters.index(piece.last_coord[0]) - piece.letters.index(king.last_coord[0])) == 1 and piece.last_coord[0] != king.last_coord[0] or abs(int(king.last_coord[1]) - int(piece.last_coord[1])) == 1 and abs(piece.letters.index(piece.last_coord[0]) - piece.letters.index(king.last_coord[0])) == 2 and piece.last_coord[0] != king.last_coord[0])  and piece not in pieces_doing_check: pieces_doing_check.append(piece)
                        elif name_piece == "bishop":
                            if piece.bishop_condition(king.last_coord, coords_ingame, king.last_coord) and piece not in pieces_doing_check: pieces_doing_check.append(piece)
                        elif name_piece == "queen":
                            if piece.bishop_condition(king.last_coord, coords_ingame, king.last_coord) and positions[king.last_coord] in piece.rival_coords or piece.rook_condition(king.last_coord, coords_ingame,king.last_coord) and piece not in pieces_doing_check: pieces_doing_check.append(piece)
                        elif name_piece == "pawn" and piece not in pieces_doing_check:
                            pieces_doing_check.append(piece)
    return pieces_doing_check
                    
def checkmate(king ,all_pieces, check, coords_ingame, positions, warning_pieces, win, team, font):
    
    for piece in all_pieces:
        if piece.team != king.team and piece.name != "pawn":
            ideal_coords = set(piece.ideal_coords) if piece.name != "queen" else set(piece.special_ideal_coords[0]).union(set(piece.special_ideal_coords[1]))
            for position in ideal_coords:
                possible_coord = convert_position_into_coord(position, positions)
                if piece.name == "rook":
                    if position not in king.all_ideal_coords and piece.rook_condition(possible_coord, coords_ingame):king.all_ideal_coords.append(position)
                elif piece.name == "knight":
                    if position not in king.all_ideal_coords and piece.knight_condition(possible_coord, coords_ingame):king.all_ideal_coords.append(position)
                elif piece.name == "bishop":
                    if position not in king.all_ideal_coords and piece.bishop_condition(possible_coord, coords_ingame): king.all_ideal_coords.append(position)
                elif piece.name == "queen":
                    if position not in king.all_ideal_coords: 
                        if position in piece.special_ideal_coords[0] and position not in king.all_ideal_coords:
                            if position not in king.all_ideal_coords and piece.rook_condition(possible_coord, coords_ingame):king.all_ideal_coords.append(position)
                        if position in piece.special_ideal_coords[1] and position not in king.all_ideal_coords:
                            if position not in king.all_ideal_coords and piece.bishop_condition(possible_coord, coords_ingame): king.all_ideal_coords.append(position)      
                elif piece.name == "king":
                    if position not in king.all_ideal_coords and all(piece.king_condition(possible_coord, coords_ingame)): king.all_ideal_coords.append(position)
        if piece.team != king.team and piece.name == "pawn":
            for pos in piece.attack_positions:
                c = convert_position_into_coord(pos, positions)
                if pos not in king.all_ideal_coords and piece.pawn_condition(c):
                    king.all_ideal_coords.append(pos)
                                     
        king.n_movements = king.king_movements(all_pieces, warning_pieces,coords_ingame, positions) 
        otherTeam = "white" if team == "black" else "black"
        enemy_king = get_piece(all_pieces, otherTeam, "king")
        #kinds: 0 -> checkmate, 1 -> king suffocated, 2 -> Time consumed, 3 -> not enough material
        if check != None:
            #if enemy_king.n_movements == 0 and check[0]:
            if king.n_movements == 0 and check[0]:
                print("CHECKMATE")
                winnerTeam = "white" if king.team == "black" else "black"
                ending_frame(win, winnerTeam,otherTeam, font, 0)

        elif king_suffocated(king, all_pieces):
            print("King Suffocated")
            winnerTeam = "white" if king.team == "black" else "black"
            ending_frame(win, team, otherTeam,font, 1)

        elif len(all_pieces) == 2:
            ending_frame(win, team, otherTeam,font, 3)

        
def is_possible_checkmate(all_pieces, warning_pieces,positions, coords_ingame, our_king):
    lucky_breaks = [[0,[], []]] * len(warning_pieces) #Nº pieces attacking to the warning piece, allowed piece to move, allowed positions
    for warning_piece in warning_pieces:
        idx_lucky_breaks = warning_pieces.index(warning_piece)
        possible_coords = warning_piece.get_coords_for_check(positions,our_king, coords_ingame)
        possible_coords.append(warning_piece.last_coord)
        all_coords = list(positions.keys())
        positions_coords = list(positions.values())
        for piece in all_pieces:
            if piece.team != warning_piece.team:
                rival_coords = [convert_position_into_coord(pos, positions) for pos in piece.rival_coords]
                if piece.name == "pawn":
                    ideal_coords = set(piece.attack_positions).union(set(piece.ideal_coords))
                    
                    for c in ideal_coords:
                        idx_coord = positions_coords.index(c)
                        c = all_coords[idx_coord]
                        if c in possible_coords and not positions[c] in piece.attack_positions:
                            lucky_breaks[idx_lucky_breaks][0] += 1
                            if piece.initial_coord not in lucky_breaks[idx_lucky_breaks][1]: lucky_breaks[idx_lucky_breaks][1].append(piece.initial_coord)
                            if c not in lucky_breaks[idx_lucky_breaks][2]: lucky_breaks[idx_lucky_breaks][2].append(c)
                        if positions[warning_piece.last_coord] in piece.rival_coords and not piece.possible_check(our_king,all_pieces,coords_ingame, rival_coords):
                            lucky_breaks[idx_lucky_breaks][0] += 1
                            if piece.initial_coord not in lucky_breaks[idx_lucky_breaks][1]: lucky_breaks[idx_lucky_breaks][1].append(piece.initial_coord)
                            if warning_piece.last_coord not in lucky_breaks[idx_lucky_breaks][2]: lucky_breaks[idx_lucky_breaks][2].append(warning_piece.last_coord)
                elif piece.name == "rook":
                    for c in piece.ideal_coords:
                        idx_coord = positions_coords.index(c)
                        c = all_coords[idx_coord]
                        if c in possible_coords and piece.rook_condition(c, coords_ingame):
                            lucky_breaks[idx_lucky_breaks][0] += 1
                            if piece.initial_coord not in lucky_breaks[idx_lucky_breaks][1]: lucky_breaks[idx_lucky_breaks][1].append(piece.initial_coord)
                            if c not in lucky_breaks[idx_lucky_breaks][2]: lucky_breaks[idx_lucky_breaks][2].append(c)
                        if piece.rook_condition(warning_piece.last_coord, coords_ingame) and not piece.possible_check(our_king,all_pieces,coords_ingame, rival_coords):
                            lucky_breaks[idx_lucky_breaks][0] += 1
                            if piece.initial_coord not in lucky_breaks[idx_lucky_breaks][1]: lucky_breaks[idx_lucky_breaks][1].append(piece.initial_coord)
                            if warning_piece.last_coord not in lucky_breaks[idx_lucky_breaks][2]: lucky_breaks[idx_lucky_breaks][2].append(warning_piece.last_coord)
                elif piece.name == "knight":
                    for c in piece.ideal_coords:
                        idx_coord = positions_coords.index(c)
                        c = all_coords[idx_coord]
                        if c in possible_coords and piece.knight_condition(c, coords_ingame):
                            lucky_breaks[idx_lucky_breaks][0] += 1
                            if piece.initial_coord not in lucky_breaks[idx_lucky_breaks][1]: lucky_breaks[idx_lucky_breaks][1].append(piece.initial_coord)
                            if c not in lucky_breaks[idx_lucky_breaks][2]: lucky_breaks[idx_lucky_breaks][2].append(c)
                        if (abs(int(warning_piece.last_coord[1]) - int(piece.last_coord[1])) == 2 and abs(piece.letters.index(piece.last_coord[0]) - piece.letters.index(warning_piece.last_coord[0])) == 1 and piece.last_coord[0] != warning_piece.last_coord[0] or abs(int(warning_piece.last_coord[1]) - int(piece.last_coord[1])) == 1 and abs(piece.letters.index(piece.last_coord[0]) - piece.letters.index(warning_piece.last_coord[0])) == 2 and piece.last_coord[0] != warning_piece.last_coord[0])  and not piece.possible_check(our_king,all_pieces,coords_ingame, rival_coords):
                            lucky_breaks[idx_lucky_breaks][0] += 1
                            if piece.initial_coord not in lucky_breaks[idx_lucky_breaks][1]: lucky_breaks[idx_lucky_breaks][1].append(piece.initial_coord)
                            if warning_piece.last_coord not in lucky_breaks[idx_lucky_breaks][2]: lucky_breaks[idx_lucky_breaks][2].append(warning_piece.last_coord)
                elif piece.name == "bishop":
                    for c in piece.ideal_coords:
                        idx_coord = positions_coords.index(c)
                        c = all_coords[idx_coord]
                        if c in possible_coords and piece.bishop_condition(c, coords_ingame):
                            lucky_breaks[idx_lucky_breaks][0] += 1
                            if piece.initial_coord not in lucky_breaks[idx_lucky_breaks][1]: lucky_breaks[idx_lucky_breaks][1].append(piece.initial_coord)
                            if c not in lucky_breaks[idx_lucky_breaks][2]: lucky_breaks[idx_lucky_breaks][2].append(c)
                            
                        if piece.bishop_condition(warning_piece.last_coord, coords_ingame,warning_piece.last_coord) and positions[warning_piece.last_coord] in piece.rival_coords and not piece.possible_check(our_king,all_pieces,coords_ingame, rival_coords):
                            lucky_breaks[idx_lucky_breaks][0] += 1
                            if piece.initial_coord not in lucky_breaks[idx_lucky_breaks][1]: lucky_breaks[idx_lucky_breaks][1].append(piece.initial_coord)
                            if c not in lucky_breaks[idx_lucky_breaks][2]: lucky_breaks[idx_lucky_breaks][2].append(c)
                elif piece.name == "queen":
                    ideal_coords = set(piece.special_ideal_coords[0]).union(set(piece.special_ideal_coords[1]))
                    for c in ideal_coords:
                        idx_coord = positions_coords.index(c)
                        c = all_coords[idx_coord]
                        if c in possible_coords and (piece.rook_condition(c, coords_ingame) or piece.bishop_condition(c, coords_ingame)):
                            lucky_breaks[idx_lucky_breaks][0] += 1
                            if piece.initial_coord not in lucky_breaks[idx_lucky_breaks][1]: lucky_breaks[idx_lucky_breaks][1].append(piece.initial_coord)
                            if c not in lucky_breaks[idx_lucky_breaks][2]: lucky_breaks[idx_lucky_breaks][2].append(c)
                        if (piece.rook_condition(warning_piece.last_coord, coords_ingame) or (piece.bishop_condition(warning_piece.last_coord, coords_ingame,warning_piece.last_coord) and positions[warning_piece.last_coord] in piece.rival_coords)) and not piece.possible_check(our_king,all_pieces,coords_ingame, rival_coords):
                            lucky_breaks[idx_lucky_breaks][0] += 1
                            if piece.initial_coord not in lucky_breaks[idx_lucky_breaks][1]: lucky_breaks[idx_lucky_breaks][1].append(piece.initial_coord)
                            if warning_piece.last_coord not in lucky_breaks[idx_lucky_breaks][2]: lucky_breaks[idx_lucky_breaks][2].append(warning_piece.last_coord)
                elif piece.name == "king":
                    # ERROR EN COMER PIEZAS SI EL REY ESTA EN JAQUE 
                    if piece.king_attack_algorithm(all_pieces, coords_ingame,warning_piece.last_coord,positions) and piece.king_condition(warning_piece.last_coord, coords_ingame)[0]:
                        lucky_breaks[idx_lucky_breaks][0] += 1
                        if piece.initial_coord not in lucky_breaks[idx_lucky_breaks][1]: lucky_breaks[idx_lucky_breaks][1].append(piece.initial_coord)
                        if warning_piece.last_coord not in lucky_breaks[idx_lucky_breaks][2]: lucky_breaks[idx_lucky_breaks][2].append(warning_piece.last_coord)
                    for c in piece.all_positions:
                        
                        if c in coords_ingame:
                            p2 = get_piece_with_lastcoord(all_pieces, c)
                            if piece.king_attack_algorithm(all_pieces, coords_ingame,c,positions) and positions[c] not in piece.all_ideal_coords and p2.team != piece.team:
                                lucky_breaks[idx_lucky_breaks][0] += 1
                                if piece.initial_coord not in lucky_breaks[idx_lucky_breaks][1]: lucky_breaks[idx_lucky_breaks][1].append(piece.initial_coord)
                                if c not in lucky_breaks[idx_lucky_breaks][2]: lucky_breaks[idx_lucky_breaks][2].append(c)
                            
                        piece.king_movement(all_pieces, c, positions[c], coords_ingame)
                        if all(piece.king_condition(c, coords_ingame)) and positions[c] not in piece.all_ideal_coords and c not in possible_coords:
                            
                            lucky_breaks[idx_lucky_breaks][0] += 1
                            if piece.initial_coord not in lucky_breaks[idx_lucky_breaks][1]: lucky_breaks[idx_lucky_breaks][1].append(piece.initial_coord)
                            if c not in lucky_breaks[idx_lucky_breaks][2]: lucky_breaks[idx_lucky_breaks][2].append(c)

        if all(map(lambda tup: tup[0] > 0, lucky_breaks)): 
            return (False,list(map(lambda tup: tup[1], lucky_breaks)), list(map(lambda tup: tup[2], lucky_breaks)))
        return (True,[], []) #CHECKMATE
def get_positions():
    positions = {}
    letters = string.ascii_lowercase
    letters = [letter for letter in letters if letters.index(letter) < 8]
    n = 62.7
    x = 103
    for letter in letters:
        y = 539
        for num in range(1, 9):
            positions[letter + str(num)] = (x, y)
            y -= n
        x += n
         
    return positions
    
    
class Font:
    def __init__(self, fontsheet_name, n_times = 1):
        self.fontsheet = pygame.image.load(fontsheet_name).convert_alpha()
        self.line_height = self.fontsheet.get_height()
        self.n_times = n_times
        
        
        self.sepColor = hex_to_rgb("#7f7f7f")
        self.fontOrder = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',';','%', "|"]
        
        self.baseSpacing = 1
        self.lineSpacing = 2
        self.letter_spacing = []
        
        self.letters = self.get_letters(self.fontsheet)
        self.lettersImgs= {self.fontOrder[idx]:self.letters[idx] for idx in range(len(self.fontOrder))}
        self.fontColor = [255,0,0]
        self.targetColor = "#000012"
        
        self.space_width = self.letter_spacing[0]
        for letter in self.fontOrder:
            self.lettersImgs[letter] = swap_color(self.lettersImgs[letter], pygame.Color(self.targetColor), self.fontColor)
        
        self.fontColor = hex_to_rgb(self.targetColor)
    def width(self, text):
        return sum(self.space_width + self.baseSpacing if char == ' ' else self.letter_spacing[self.fontOrder.index(char)] + self.baseSpacing for char in text)
    def text_len(self,text):
        return self.lettersImgs["a"].get_size()[0] * self.n_times * len(text)
    def set_fontColor(self, color):
        if type(self.fontColor) == str:
            self.fontColor = hex_to_rgb(self.fontColor)
        if rgb_to_hex(self.fontColor) != color and self.fontColor != color:
            for char in self.lettersImgs.keys():
                self.lettersImgs[char] = swap_color(self.lettersImgs[char], pygame.Color(color), self.fontColor)
            self.fontColor = color
    def get_letters(self, fontSheet):
        letters = []
        x = 0
        dx = 0
        for x in range(fontSheet.get_width()):
            if fontSheet.get_at((x, 0))[0] == 127:
                letters.append(clip(fontSheet, dx, 0, x - dx, self.line_height))
                self.letter_spacing.append(x - dx)
                dx = x + 1
            x += 1
        return letters
    
    def rendered_text(self,text, render, loc,line_width=0):
        """ Function which you can render your text without any restriction """
        x_offset = 0
        y_offset = 0
        if line_width != 0:
            spaces = []
            x = 0
            for i, char in enumerate(text):
                if char == ' ':
                    spaces.append((x, i))
                    x += self.space_width + self.baseSpacing
                else:
                    x += self.letter_spacing[self.fontOrder.index(char)] + self.baseSpacing
            line_offset = 0
            for i, space in enumerate(spaces):
                if (space[0] - line_offset) > line_width:
                    line_offset += spaces[i - 1][0] - line_offset
                    if i != 0:
                        text = text[:spaces[i - 1][1]] + '\n' + text[spaces[i - 1][1] + 1:]
        for i,char in enumerate(text):
            if char not in ['\n', ' ']:
                char_img = pygame.transform.scale(self.lettersImgs[char], (self.lettersImgs[char].get_width() * self.n_times,self.lettersImgs[char].get_height() * self.n_times))
                char_img.set_colorkey((0,0,0))
                render.blit(char_img, (loc[0] + x_offset * self.n_times, loc[1] + y_offset * self.n_times))
                x_offset += self.letter_spacing[self.fontOrder.index(char)] + self.baseSpacing
            elif char == ' ':
                x_offset += self.space_width + self.baseSpacing
            else:
                y_offset += self.lineSpacing + self.line_height
                x_offset = 0
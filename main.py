import pygame, glob, time
import string
from functions import get_pieces, get_positions, check, checkmate, is_possible_checkmate, get_piece, functional_system_of_pieces as fsop, Font, coord_system as cs, time_system as ts, Vector2,looking_for_diff_pieces as lfdp, get_piece_directly as gpd, pawn_algorithm as pa,swap_color, blit, chat_system, waiting, last_movement_algorithm as lma
from logic import *
from network import *
import sys
import os

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Stages:
    def __init__(self):
        self.win = pygame.display.set_mode((700,700))
        pygame.display.set_caption("Thortion Chess")
        pygame.display.set_icon(pygame.image.load("icon.png"))
        self.board = pygame.transform.scale(pygame.image.load("board.png"),self.win.get_size())
        self.frameChat = self.frameCoord = pygame.transform.scale(pygame.image.load("frameCoord.png"),(94, 500))
        self.mouse_surf = pygame.transform.scale(pygame.image.load("mouse_indication.png"), (60,60))
        
        self.t0 = 0
        self.time_chose = 10 * 60  #time in seconds
        self.pause_img = pygame.image.load("pause.png").convert_alpha()
        self.pause_img.set_colorkey([0] * 3)
        self.chatIcon = pygame.image.load("chatIcon.png").convert_alpha()
        #self.chatIcon.set_colorkey(pygame.Color("#ff0000"))
        self.littleLabel = pygame.image.load("littleLabel.png")
        self.littleLabel.set_colorkey([0] * 3)
        self.info = 0
        
        self.menu_imgs = [pygame.image.load(name).convert_alpha() for name in glob.glob("menu*.png")]
        for i, menu in enumerate(self.menu_imgs):
            self.menu_imgs[i].set_colorkey([0] * 3)
        self.menu = 0
        self.chat = 0
        self.chatData = {"white": [],"black": []} # The max length of the word is 10
        self.net = None
        self.activity = False
        self.last_positions = []
        self.modes = ["mainMenu", "offline", "online"]
        self.mode = self.modes[0]
        
        
    def setup(self):
        # The initialization of the chess
        pieces = [pygame.transform.scale(pygame.image.load(name), (54,54)) for name in glob.glob("p*.png")]
        self.pieces = get_pieces(pieces)
        self.positions = get_positions()

        self.white_pieces = []
        order = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
        self.coords_ingame = []
        letters = string.ascii_lowercase
        self.font = Font("small_font.png", 2)
        #white
        for i in range(8):
            self.white_pieces.append(Piece(order[i],letters[i] + "1", self.positions[letters[i] + "1"], self.pieces[order[i]], "white"))
            self.coords_ingame.append(letters[i] + "1")
        self.black_pieces = []
        #black
        for i in range(8):
            self.black_pieces.append(Piece(order[i], letters[i] + "8",self.positions[letters[i] + "8"], self.pieces[order[i]], "black"))
            self.coords_ingame.append(letters[i] + "8")
            
        for n in range(8):
            self.white_pieces.append(Piece("pawn", letters[n] + "2",self.positions[letters[n] + "2"],self.pieces["pawn"], "white", self.pieces))
            self.coords_ingame.append(letters[n] + "2")
            self.coords_ingame.append(letters[n] + "7")
            self.black_pieces.append(Piece("pawn",letters[n] + "7", self.positions[letters[n] + "7"],self.pieces["pawn"], "black", self.pieces))
        
        self.last_positions.clear()
        
    def choose_option(self):
        self.setup()
        clock = pygame.time.Clock()
        bg = pygame.transform.scale(pygame.image.load("bg.png"),self.win.get_size())
        label = pygame.image.load("label.png")
        label.set_colorkey((0,) * 3)
        label_size = label.get_size()
        online_label = offline_label = label 
        options = [0,0]
        
        
        while True:
            blit(self.win, bg, (0,0))
            clock.tick(60)
            events = pygame.event.get()
            m = pygame.mouse.get_pos()
            m = Vector2(m[0], m[1])   
            
            if m[0] in range(700 // 4 + 15, 700//4 + 15 + label_size[0]) and m[1] in range(700//2 - 50, 700//2 - 50 + label_size[1]):
                offline_label = swap_color(offline_label,"#508f91", offline_label.get_at((25,25)))
                options[0] = 1
            else:
                offline_label = swap_color(offline_label,"#386466", offline_label.get_at((25,25)))
                options[0] = 0
            if m[0] in range(700 // 4 + 15, 700//4 + 15 + label_size[0]) and m[1] in range(700//2 + 150, 700//2 + 150 + label_size[1]):
                online_label = swap_color(online_label,"#508f91", online_label.get_at((25,25)))
                options[1] = 1
                
            else:
                online_label = swap_color(online_label,"#386466", online_label.get_at((25,25)))
                options[1] = 0
            
            self.font.n_times = 20            
            self.font.rendered_text("Menu", self.win, (700 // 2 - 160, 50))
            blit(self.win, offline_label, (700 // 4 + 15, 700//2 - 50))
            blit(self.win, online_label, (700 // 4 + 15, 700//2 + 150))
            
            self.font.n_times = 6
            self.font.rendered_text("Offline", self.win, (700 // 4 + label_size[0]//3 , 700//2 - 20))
            self.font.rendered_text("Online", self.win, (700 // 4  + label_size[0]//3 , 700//2 + 180))
            self.font.n_times = 2
            
            for event in events:
                if event.type == pygame.QUIT:
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and options[0]:
                        self.loading_frame()
                        self.mode = self.modes[1]
                        self.offline_option()
                    if event.button == 1 and options[1]:
                        self.loading_frame()
                        self.mode = self.modes[2]
                        self.activity = True
                        self.online_option()
                        
            x = 25
            for name, p_img in self.pieces.items():
            
                p_img.set_colorkey([0] * 3)
                p_img = swap_color(p_img, "#323e4f", "#ff0000")
                p_img = swap_color(p_img, "#3b495c", "#ff8400")
                if name == "king": p_img = swap_color(p_img, "#3b495c", "#ff0100")
                pos = (x, 700//2 + 260)
                blit(self.win, p_img, pos)
                self.font.rendered_text(name, self.win, (pos[0] + 10, pos[1] + 60))
                x += 120
            
            
            self.font.rendered_text("Version 1.1", self.win, (700 - 85, 0))
            self.font.n_times = 2
            pygame.display.update()
    def loading_frame(self):
        clock = pygame.time.Clock()
        n = 0
        t0 = time.time()
        t = time.time()
        while True:
            blit(self.win, self.board, (0,0))
            clock.tick(60)
            events = pygame.event.get()
            if time.time() - t >= 0.3:
                n += 1
                t = time.time()
            self.font.n_times = 5
            self.font.rendered_text("loading" + "." * (n % 4), self.win, (0, 645))
            p = list(self.pieces.values())[n % len(self.pieces.values())]
            p.set_colorkey([0] * 3)
            p = swap_color(p, "#323e4f", "#ff0000")
            p = swap_color(p, "#3b495c", "#ff8400")
            p = swap_color(p, "#3b495c", "#ff0100")
            
            blit(self.win, p, (650, 645))
            self.font.n_times = 2
            for event in events:
                if event.type == pygame.QUIT:
                    raise SystemExit
            self.t0 = pygame.time.get_ticks()
            if t - t0 >= 5: break
            
            pygame.display.update()
        
    def offline_option(self): 
        piece_selected = None
        pieces_selected = []
        deleted_pieces = []
        points = [0, 0] #White team, Black team
        used_coords = []
        mouseWheelEvent = 0 # The events condition for the mouse wheel
        min_rounds = [1] # White team, Black team


        all_pieces = set()
        rival_team = None
        clock = pygame.time.Clock()

        teams = ["white", "black"]
        turns = ["white"]
        round_ = 0
        defense_pieces = [set(), set()] # White, Black
        defense_coords = [set(), set()] # White, Black
        times = [0, 0] # White, Black in seconds
        last_t = 0 
        
        
        
        
        
        while True:
            blit(self.win, self.board, (0,0))
            clock.tick(60)
            m = pygame.mouse.get_pos()
            m = Vector2(m[0] - 30, m[1] - 30)   
            events = pygame.event.get()
            n_round = len(turns) // 2 if len(turns) % 2 == 0 else (len(turns) - 1) // 2  
            
            
            
            # Pause button
            blit(self.win, self.pause_img, (0, 0))            
            #----------------------------
            
            # Time algorithm
            #--------------------------
            t = pygame.time.get_ticks() - self.t0
            delta_time = round(((t - last_t) / 1000.0) * 50, 8)
            last_t = t
            ts(self.win, self.font, times, turns, delta_time, self.time_chose)
            for event in events:
                if event.type == pygame.QUIT:
                    raise SystemExit
                if event.type == pygame.MOUSEWHEEL:
                    if piece_selected != None:
                        if piece_selected.name == "pawn" and piece_selected.pawn_skill: 
                            piece_selected.n =  event.y
                            piece_selected.mousewheel = True
                # Coord system event
                if m[0] in range(580, 580 + 86) and m[1] in range(100, 100 + 500):
                    mouseWheelEvent = 1
                    if event.type == pygame.MOUSEWHEEL:
                        if mouseWheelEvent: 
                            #event.y = -1 down; event.y = 1 up 
                            if event.y == -1 and min_rounds[0] + 1 < n_round: min_rounds[0] += -event.y
                            if event.y == 1 and min_rounds[0] - 1 > 0 and len(range(min_rounds[0], n_round)) < 23: min_rounds[0] += -event.y
                else: mouseWheelEvent = 0
                # The buttons events
                if m.x + 30 in range(0, self.pause_img.get_size()[0]) and m.y + 30 in range(0, self.pause_img.get_size()[1]):
                    self.pause_img = swap_color(self.pause_img, "#58f0a5", "#3ca370")
                else: self.pause_img = swap_color(self.pause_img, "#3ca370", "#58f0a5")
                
                y = 200
                for i,menu in enumerate(self.menu_imgs):
                    if i > 0:
                        if m.x + 30 in range(325, 325 + menu.get_size()[0]) and m.y + 30 in range(y, y + menu.get_size()[1]):
                            self.menu_imgs[i] = swap_color(self.menu_imgs[i], "#4e8c8f", "#206a6c")
                        else: self.menu_imgs[i] = swap_color(self.menu_imgs[i],"#206a6c", "#4e8c8f")
                        y += 100

                #-----------------------
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        #Pause algorithm
                        if m.x + 30 in range(0, self.pause_img.get_size()[0]) and m.y + 30 in range(0, self.pause_img.get_size()[1]):
                            self.menu += 1 
                            self.menu %= 2
                        y = 200
                        for i,menu in enumerate(self.menu_imgs):
                            if i > 0:
                                if m.x + 30 in range(325, 325 + menu.get_size()[0]) and m.y + 30 in range(y, y + menu.get_size()[1]) and self.menu:
                                    if i == 1: 
                                        self.menu = False
                                        self.info = False
                                        self.choose_option()
                                    elif i == 2:
                                        self.info += 1
                                        self.info %= 2
                                        
                                        
                                y += 100
                            
                        #----------------------
            
                        
                        
                        # Pieces algorithm
                        if not self.menu:
                            all_pieces = set(self.white_pieces).union(set(self.black_pieces))
                            
                            if piece_selected != None:
                                if piece_selected.ready_to_move:
                                    king = get_piece(all_pieces, piece_selected.team,"king")
                                    if piece_selected.name == "pawn":
                                        if not piece_selected.pawn_skill: piece_selected.movement_system(self.positions, m, self.coords_ingame, all_pieces, rival_team, turns,defense_pieces, defense_coords,king, deleted_pieces, points, used_coords,last_positions = self.last_positions)
                                    else: piece_selected.movement_system(self.positions, m, self.coords_ingame, all_pieces, rival_team, turns,defense_pieces, defense_coords,king, deleted_pieces, points, used_coords,last_positions = self.last_positions)
                                    piece_selected.ready_to_move = False
                                piece_selected = None
                    
                            distances = []
                            for piece in all_pieces:
                                distances.append(m.distance_to(piece.r))
                            min_dist = min(distances)
                            if int(min_dist) < 30:
                                idx_piece = distances.index(min_dist)
                                piece_selected = list(all_pieces)[idx_piece]
                                pieces_selected.append(piece_selected)
                                if piece_selected in self.black_pieces:
                                    rival_team = self.white_pieces
                                    try:
                                        piece_selected = self.black_pieces[self.black_pieces.index(piece_selected)]   
                                    except Exception as e:
                                        pass
                                else: 
                                    rival_team = self.black_pieces
                                    try:
                                        piece_selected = self.white_pieces[self.white_pieces.index(piece_selected)]
                                    except Exception as e:
                                        pass
                                
                                
                                if piece_selected.ready_to_move == False and piece_selected.team == turns[-1]:
                                    if piece_selected.team == "white": round_ += 1
                                    
                                    print(piece_selected)   
                                    piece_selected.ready_to_move = True 
                        
                    all_pieces = set(self.white_pieces).union(set(self.black_pieces))   

            fsop(deleted_pieces, self.win, self.font, points)
            cs(self.win,self.frameCoord, used_coords, self.font,min_rounds, n_round, mouseWheelEvent, self.mouse_surf)
            
            '''s = swap_color(self.frameChat, "#046570",self.frameChat.get_at((0,0)))
            s = swap_color(s, "#13908c",s.get_at((4,4))).convert_alpha()
            s.set_alpha(160)
            blit(self.win, s, (0,100))'''
            for white_piece in self.white_pieces:
                white_piece.strategy(self.positions, self.coords_ingame, all_pieces) 
                    
                if white_piece.name == "king":
            
                    if len(pieces_selected) > 1:
                        checkPieces = check(all_pieces, self.positions,white_piece, self.coords_ingame)
                        
                        if len(checkPieces) > 0: 
                            white_piece.check = True
                        else:
                            white_piece.check = False
                        uncertainty_stuff = is_possible_checkmate(all_pieces, checkPieces, self.positions, self.coords_ingame, white_piece)
                        if uncertainty_stuff != None:
                            if len(uncertainty_stuff[1]) > 0: 
                                defense_pieces[0] = set(arr[i] for arr in uncertainty_stuff[1] for i in range(len(arr)))
                                defense_coords[0] = set(arr[i] for arr in uncertainty_stuff[2] for i in range(len(arr)))
                        else:
                            defense_pieces[0].clear()
                            defense_coords[0].clear()
                        
                        checkmate(white_piece, all_pieces,uncertainty_stuff, self.coords_ingame, self.positions, checkPieces, self.win, "white", self.font)
                if white_piece.ready_to_move:
                    white_piece.square_contour(self.win,defense_coords[0], self.positions)
                    white_piece.contour_selected()
                else:
                    white_piece.reverse_contour()
                    
                if white_piece.name == "pawn":
                    if white_piece.mousewheel:
                        for event in events:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if event.button == 1: 
                                    white_piece.selection_piece = True
                                    white_piece.mousewheel = False
                    white_piece.blit_piece(self.win, points,self.positions, self.white_pieces, turns, "white")    

                else:
                    white_piece.blit_piece(self.win,positions = self.positions)
                
            for black_piece in self.black_pieces:
                black_piece.strategy(self.positions,self.coords_ingame, all_pieces)
                if black_piece.name == "king":
                    
                    if len(pieces_selected) > 1:
                        checkPieces = check(all_pieces, self.positions,black_piece, self.coords_ingame)
                        if len(checkPieces) > 0: 
                            black_piece.check = True

                        else:
                            black_piece.check = False
                        
                        uncertainty_stuff = is_possible_checkmate(all_pieces, checkPieces, self.positions,self.coords_ingame, black_piece)
                        if uncertainty_stuff != None:
                            if len(uncertainty_stuff[1]) > 0:
                                defense_pieces[1] = set(arr[i] for arr in uncertainty_stuff[1] for i in range(len(arr)))
                                defense_coords[1] = set(arr[i] for arr in uncertainty_stuff[2] for i in range(len(arr)))
                        
                        else:
                            defense_pieces[1].clear()
                            defense_coords[1].clear()
                        
                        checkmate(black_piece, all_pieces,uncertainty_stuff, self.coords_ingame, self.positions, checkPieces, self.win, "black", self.font)
                if black_piece.ready_to_move:
                    black_piece.square_contour(self.win,defense_coords[1], self.positions)
                    black_piece.contour_selected()
                else:
                    black_piece.reverse_contour()
                
                if black_piece.name == "pawn":
                    
                    if black_piece.mousewheel:
                        for event in events:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if event.button == 1: 
                                    black_piece.selection_piece = True
                                    black_piece.mousewheel = False

                    black_piece.blit_piece(self.win, points,self.positions,self.black_pieces, turns, "black")  
                    
                else:
                    black_piece.blit_piece(self.win,positions = self.positions)
            
            lma(self.win, self.last_positions, self.positions)
            if times[0] >= self.time_chose:
                
                ending_frame(self.win, "white", "black",self.font,2)
                

            if times[1] >= self.time_chose:
                ending_frame(self.win,"black","white",self.font,2)
                
            
            if self.menu:
                blit(self.win,self.menu_imgs[0], (100, 100))
                self.font.n_times = 6
                self.font.rendered_text("MENU", self.win, (300, 150))
                y = 200
                for menu in self.menu_imgs[1:]:
                    blit(self.win, menu, (325, y))
                    y += 100
                self.font.n_times = 2
                if self.info:
                    pos = 325 + self.menu_imgs[2].get_size()[0] + 5,300
                    blit(self.win,self.littleLabel,pos)
                    self.font.rendered_text("ADVICE: You can use the\nscroll wheel on the \ncoords' chart or chat's\nchart if you use the\nonline option.",self.win,(pos[0] + 2, pos[1] + 5))
            pygame.display.update()    
            
    def online_option(self):
        piece_selected = None
        pieces_selected = []
        deleted_pieces = []
        points = [0, 0] #White team, Black team
        used_coords = []
        mouseWheelEvent = 0 # The events condition for the mouse wheel
        mouseWheelChatEvent = MWCE = 0
        min_rounds = [1] # White team, Black team
        writing = False

        all_pieces = set()
        rival_team = None
        clock = pygame.time.Clock()

        teams = ["white", "black"]
        turns = ["white"]
        round_ = 0
        defense_pieces = [set(), set()] # White, Black
        defense_coords = [set(), set()] # White, Black
        times = [0, 0] # White, Black in seconds
        last_t = 0 
 
        if self.net == None: self.net = Network()
        team = self.net.get_team()
        print(team)
        all_static_pieces = set(self.white_pieces).union(set(self.black_pieces))
        idx_team = 0 if team == "white" else 1
        
        phrase = ""
        text_range = [0] # The start range of the texts
        
        enemy_uncertainty_stuff = []
        
        while True:
            blit(self.win, self.board, (0,0))
            clock.tick(60)
            pygame.key.set_repeat(160)
            
            m = pygame.mouse.get_pos()
            m = Vector2(m[0] - 30, m[1] - 30)   
            events = pygame.event.get()
            n_round = len(turns) // 2 if len(turns) % 2 == 0 else (len(turns) - 1) // 2  
            # Pause button
            blit(self.win, self.pause_img, (0, 0))            
            #----------------------------
            # Time algorithm
            #--------------------------
            t = pygame.time.get_ticks() - self.t0
            delta_time = round(((t - last_t) / 1000.0) * 50, 8)
            last_t = t
            ts(self.win, self.font, times, turns, delta_time, self.time_chose)
            idx_team = 0 if team == "white" else 1
            #--------------------------
            
            deleted_pieces_coords = [[dp.name,dp.initial_coord] for dp in deleted_pieces if dp != None]  
            name_pieces = [p.name for p in self.white_pieces] if team == "white" else [p.name for p in self.black_pieces]
            #--------------------------
            for event in events:
                if event.type == pygame.QUIT:
                    raise SystemExit
                if event.type == pygame.MOUSEWHEEL:
                    if piece_selected != None:
                        if piece_selected.name == "pawn" and piece_selected.pawn_skill: 
                            piece_selected.n =  event.y
                            piece_selected.mousewheel = True
                # Coord system event
                if m[0] in range(580, 580 + 86) and m[1] in range(100, 100 + 500):
                    mouseWheelEvent = 1
                    if event.type == pygame.MOUSEWHEEL:
                        if mouseWheelEvent: 
                            #event.y = -1 down; event.y = 1 up 
                            if event.y == -1 and min_rounds[0] + 1 < n_round: min_rounds[0] += -event.y
                            if event.y == 1 and min_rounds[0] - 1 > 0 and len(range(min_rounds[0], n_round)) < 23: min_rounds[0] += -event.y
                else: mouseWheelEvent = 0
                # The buttons events
                if m.x + 30 in range(0, self.pause_img.get_size()[0]) and m.y + 30 in range(0, self.pause_img.get_size()[1]):
                    self.pause_img = swap_color(self.pause_img, "#58f0a5", "#3ca370")
                else: self.pause_img = swap_color(self.pause_img, "#3ca370", "#58f0a5")
                if m.x + 30 in range(325, 325 + self.menu_imgs[1].get_size()[0]) and m.y + 30 in range(200, 200 + self.menu_imgs[1].get_size()[1]):
                    self.menu_imgs[1] = swap_color(self.menu_imgs[1], "#4e8c8f", "#3d6e70")
                else: self.menu_imgs[1] = swap_color(self.menu_imgs[1],"#3d6e70","#4e8c8f")
                
                y = 200
                for i,menu in enumerate(self.menu_imgs):
                    if i > 0:
                        if m.x + 30 in range(325, 325 + menu.get_size()[0]) and m.y + 30 in range(y, y + menu.get_size()[1]):
                            self.menu_imgs[i] = swap_color(self.menu_imgs[i], "#4e8c8f", "#206a6c")
                        else: self.menu_imgs[i] = swap_color(self.menu_imgs[i],"#206a6c", "#4e8c8f")
                        y += 100
                textdata = set(self.chatData["white"]).union(self.chatData["black"])
                if m.x + 30 in range(0,self.frameChat.get_size()[0]) and m.y + 30 in range(100, 100 + self.frameChat.get_size()[1]):
                    if event.type == pygame.MOUSEWHEEL:
                        MWCE = 1
                        #event.y = -1 down; event.y = 1 up 
                        if event.y == -1 and text_range[0] + 1 < len(textdata): text_range[0] += -event.y
                        if event.y == 1 and text_range[0] - 1 > 0 and len(range(text_range[0], len(textdata))) < 23: text_range[0] += -event.y
                else: MWCE = 0
                
                if m.x + 30 in range(0,self.frameChat.get_size()[0]) and m.y + 30 in range(100 + (self.frameChat.get_size()[1] - self.chatIcon.get_size()[1]), 100 + self.frameChat.get_size()[1]):
                    self.chatIcon = swap_color(self.chatIcon,"#19b3ad",self.chatIcon.get_at((33,12)))
                if not self.chat and not (m.x + 30 in range(0,self.frameChat.get_size()[0]) and m.y + 30 in range(100 + (self.frameChat.get_size()[1] - self.chatIcon.get_size()[1]), 100 + self.frameChat.get_size()[1])):
                    self.chatIcon = swap_color(self.chatIcon,"#13908c" ,self.chatIcon.get_at((33,12)))
                if event.type == pygame.KEYDOWN and self.chat:
                    letter = pygame.key.name(event.key)
                    writing = True
                    if letter in string.ascii_letters + "1234567890" and len(phrase) < 10: phrase += letter
                    elif letter == "backspace": phrase = phrase[:-1]
                    elif letter == "space": phrase += " "
                    if letter == "return" and len(phrase) > 0:
                        if len(range(text_range[0], len(textdata))) >= 23: text_range[0] += 1
                        self.chatData[team].append((phrase, time.time()))
                        phrase = ""
                else:
                    writing = False
                #-----------------------
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        #Pause algorithm
                        if m.x + 30 in range(0, self.pause_img.get_size()[0]) and m.y + 30 in range(0, self.pause_img.get_size()[1]):
                            self.menu += 1 
                            self.menu %= 2
                        y = 200
                        for i,menu in enumerate(self.menu_imgs):
                            if i > 0:
                                if m.x + 30 in range(325, 325 + menu.get_size()[0]) and m.y + 30 in range(y, y + menu.get_size()[1]) and self.menu:
                                    if i == 1: 
                                        self.menu = False
                                        self.info = False
                                        self.choose_option()
                                    elif i == 2:
                                        self.info += 1
                                        self.info %= 2        
                                y += 100
                        #Chat algorithm
                        if m.x + 30 in range(0,self.frameChat.get_size()[0]) and m.y + 30 in range(100 + (self.frameChat.get_size()[1] - self.chatIcon.get_size()[1]), 100 + self.frameChat.get_size()[1]):
                            self.chat += 1
                            self.chat %= 2

                        #---------------
                        #----------------------
                        # Pieces algorithm
                        all_pieces = set(self.white_pieces).union(set(self.black_pieces))
                        
                        if piece_selected != None:
                            if piece_selected.ready_to_move:
                                king = get_piece(all_pieces, piece_selected.team,"king")
                                if piece_selected.name == "pawn":
                                    if not piece_selected.pawn_skill: piece_selected.movement_system(self.positions, m, self.coords_ingame, all_pieces, rival_team, turns,defense_pieces, defense_coords,king, deleted_pieces, points, used_coords, self.net, times, name_pieces,self.chatData, self.last_positions)
                                else: piece_selected.movement_system(self.positions, m, self.coords_ingame, all_pieces, rival_team, turns,defense_pieces, defense_coords,king, deleted_pieces, points, used_coords, self.net, times, name_pieces, self.chatData,self.last_positions)
                                piece_selected.ready_to_move = False
                            piece_selected = None
                
                        distances = []
                        for piece in all_pieces:
                            distances.append(m.distance_to(piece.r))
                        min_dist = min(distances)
                        if int(min_dist) < 30:
                            idx_piece = distances.index(min_dist)
                            piece_selected = list(all_pieces)[idx_piece]
                            pieces_selected.append(piece_selected)
                            if piece_selected in self.black_pieces:
                                rival_team = self.white_pieces
                                try:
                                    piece_selected = self.black_pieces[self.black_pieces.index(piece_selected)]   
                                except Exception as e:
                                    pass
                            else: 
                                rival_team = self.black_pieces
                                try:
                                    piece_selected = self.white_pieces[self.white_pieces.index(piece_selected)]
                                except Exception as e:
                                    pass
                            
                            
                            if piece_selected.ready_to_move == False and piece_selected.team == turns[-1] and team == turns[-1]:
                                if piece_selected.team == "white": round_ += 1
                                
                                print(piece_selected)   
                                piece_selected.ready_to_move = True 
                        
                    all_pieces = set(self.white_pieces).union(set(self.black_pieces))   

            fsop(deleted_pieces, self.win, self.font, points)
            cs(self.win,self.frameCoord, used_coords, self.font,min_rounds, n_round, mouseWheelEvent, self.mouse_surf)
            chat_system(self.win, self.frameChat,  self.chatData.copy(), self.font, self.chat, text_range, MWCE)
            #Chat button
            
            self.chatIcon = swap_color(self.chatIcon, "#046570","#000001")
            self.chatIcon = swap_color(self.chatIcon, "#13908c","#000000").convert_alpha()
            self.chatIcon.set_colorkey((255,0,0))
            blit(self.win, self.chatIcon, (0,100 + (self.frameChat.get_size()[1] - self.chatIcon.get_size()[1])))
            if self.chat: 
                pos_phrase = (self.font.lettersImgs["a"].get_size()[1] + 3,  100 + (self.frameChat.get_size()[1] - self.chatIcon.get_size()[1]) + self.chatIcon.get_size()[1]//2 - self.font.lettersImgs["A"].get_size()[1] + 2)
                self.font.rendered_text(phrase, self.win, pos_phrase)
                if len(phrase) < 10: waiting(self.win, self.font, pos_phrase, self.font.lettersImgs["a"].get_size()[0] * len(phrase) * self.font.n_times + len(phrase)*2, writing)
            if not self.chat:self.font.rendered_text("Chat", self.win, (self.chatIcon.get_size()[0]//2 - self.font.width("Chat"),  100 + (self.frameChat.get_size()[1] - self.chatIcon.get_size()[1]) + self.chatIcon.get_size()[1]//2 - self.font.lettersImgs["A"].get_size()[1] + 2) )
            #-----------
            
            for white_piece in self.white_pieces:
                white_piece.strategy(self.positions, self.coords_ingame, all_pieces) 
                if team == "white": 
                    
                    otherTeamData = self.net.send(make_info(turns, times, used_coords, deleted_pieces_coords,points[idx_team],name_pieces,self.chatData[team],[white_piece.name, white_piece.initial_coord, white_piece.last_coord]))
                    #print(otherTeamData[1])
                    if times[idx_team - 1] < otherTeamData[1][idx_team - 1]:
                        times[idx_team - 1] = otherTeamData[1][idx_team - 1]
                    elif times[idx_team] < otherTeamData[1][idx_team]:
                        times[idx_team] = otherTeamData[1][idx_team]
                    
                    if len(turns) < len(otherTeamData[2]):
                        turns = otherTeamData[2]
                    if len(used_coords) < len(otherTeamData[3]):
                        used_coords = otherTeamData[3]
                    if len(deleted_pieces) < len(otherTeamData[4]):
                        deleted_pieces = [gpd(all_static_pieces,name,initial_coord) for name,initial_coord in otherTeamData[4]]
                                
                    points[idx_team - 1] = otherTeamData[5]
                    otherNamePieces = otherTeamData[6]
                    self.chatData[teams[teams.index(team) - 1]] = otherTeamData[7]
                    lfdp(set(self.white_pieces).union(set(self.black_pieces)),otherTeamData[-1][1], otherTeamData[-1][2], self.positions, self.coords_ingame, self.last_positions)
                    pa(self.white_pieces, self.black_pieces, otherNamePieces, team, Piece, self.positions)
                    
                if white_piece.name == "king":
            
                    if len(pieces_selected) > 1:
                        checkPieces = check(all_pieces, self.positions,white_piece, self.coords_ingame)
                        if len(checkPieces) > 0: 
                            white_piece.check = True
                        else:
                            white_piece.check = False
                        uncertainty_stuff = is_possible_checkmate(all_pieces, checkPieces, self.positions, self.coords_ingame, white_piece)
                        
                        
                        if uncertainty_stuff != None:
                            if len(uncertainty_stuff[1]) > 0: 
                                defense_pieces[0] = set(arr[i] for arr in uncertainty_stuff[1] for i in range(len(arr)))
                                defense_coords[0] = set(arr[i] for arr in uncertainty_stuff[2] for i in range(len(arr)))
                        else:
                            defense_pieces[0].clear()
                            defense_coords[0].clear()
                        
                        checkmate(white_piece, all_pieces,uncertainty_stuff, self.coords_ingame, self.positions, checkPieces, self.win, "white", self.font)
                if white_piece.ready_to_move:
                    white_piece.square_contour(self.win,defense_coords[0], self.positions)
                    white_piece.contour_selected()
                else:
                    white_piece.reverse_contour()
                    
                if white_piece.name == "pawn":
                    if white_piece.mousewheel and not idx_team:
                        for event in events:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if event.button == 1: 
                                    white_piece.selection_piece = True
                                    white_piece.mousewheel = False
                    white_piece.blit_piece(self.win, points,self.positions, self.white_pieces, turns, team)    

                else:
                    white_piece.blit_piece(self.win,positions = self.positions)
                
            for black_piece in self.black_pieces:
                black_piece.strategy(self.positions,self.coords_ingame, all_pieces)
                if team == "black":
                    
                    otherTeamData = self.net.send(make_info(turns, times, used_coords, deleted_pieces_coords,points[idx_team],name_pieces,self.chatData[team],[black_piece.name, black_piece.initial_coord, black_piece.last_coord]))
                    
                    
                    #print(otherTeamData[1])
                    if times[idx_team - 1] < otherTeamData[1][idx_team - 1]:
                        times[idx_team - 1] = otherTeamData[1][idx_team - 1]
                    elif times[idx_team] < otherTeamData[1][idx_team]:
                        times[idx_team] = otherTeamData[1][idx_team]
                        
                    if len(turns) < len(otherTeamData[2]):
                        turns = otherTeamData[2]
                    if len(used_coords) < len(otherTeamData[3]):
                        used_coords = otherTeamData[3]
                    if len(deleted_pieces) < len(otherTeamData[4]):
                        deleted_pieces = [gpd(all_static_pieces,name,initial_coord) for name, initial_coord in otherTeamData[4]]
                                
                    points[idx_team - 1] = otherTeamData[5]
                    otherNamePieces = otherTeamData[6]
                    self.chatData[teams[teams.index(team) - 1]] = otherTeamData[7]
                    
                    
                    
                    
                    lfdp(set(self.white_pieces).union(set(self.black_pieces)),otherTeamData[-1][1], otherTeamData[-1][2], self.positions, self.coords_ingame, self.last_positions)
                    pa(self.white_pieces, self.black_pieces, otherNamePieces, team, Piece, self.positions)
                if black_piece.name == "king":
                    if len(pieces_selected) > 1:
                        checkPieces = check(all_pieces, self.positions,black_piece, self.coords_ingame)
                        if len(checkPieces) > 0: 
                            black_piece.check = True

                        else:
                            black_piece.check = False
                        
                        uncertainty_stuff = is_possible_checkmate(all_pieces, checkPieces, self.positions,self.coords_ingame, black_piece)
                        if uncertainty_stuff != None:
                            if len(uncertainty_stuff[1]) > 0:
                                defense_pieces[1] = set(arr[i] for arr in uncertainty_stuff[1] for i in range(len(arr)))
                                defense_coords[1] = set(arr[i] for arr in uncertainty_stuff[2] for i in range(len(arr)))
                        
                        else:
                            defense_pieces[1].clear()
                            defense_coords[1].clear()
                        
                        checkmate(black_piece, all_pieces,uncertainty_stuff, self.coords_ingame, self.positions, checkPieces, self.win, "black", self.font)
                if black_piece.ready_to_move:
                    black_piece.square_contour(self.win,defense_coords[1], self.positions)
                    black_piece.contour_selected()
                else:
                    black_piece.reverse_contour()
                
                if black_piece.name == "pawn":
                    
                    if black_piece.mousewheel and idx_team:
                        for event in events:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if event.button == 1: 
                                    black_piece.selection_piece = True
                                    black_piece.mousewheel = False

                    black_piece.blit_piece(self.win, points,self.positions,self.black_pieces, turns, team)  
                    
                else:
                    black_piece.blit_piece(self.win,positions = self.positions)
            for p in set(self.white_pieces).union(set(self.black_pieces)):
                if p not in all_static_pieces:
                    all_static_pieces.add(p)
                
            lma(self.win, self.last_positions, self.positions)
            
                
            if times[idx_team] >= self.time_chose:
                ending_frame(self.win,teams[teams.index(team) - 1],team,self.font,2)
                
            if times[idx_team - 1] >= self.time_chose:
                ending_frame(self.win, team,teams[teams.index(team) - 1],self.font,2)
            
            
            
            
            for dp in deleted_pieces:
                if dp in set(self.white_pieces).union(self.black_pieces):
                    if dp.last_coord in self.coords_ingame: del self.coords_ingame[self.coords_ingame.index(dp.last_coord)]
                    t = 0 if dp.team == "white" else 1
                    if t:
                        if dp in self.black_pieces: del self.black_pieces[self.black_pieces.index(dp)]
                    else:
                        if dp in self.white_pieces: del self.white_pieces[self.white_pieces.index(dp)]
            if self.menu:
                blit(self.win,self.menu_imgs[0], (100, 100))
                self.font.n_times = 6
                self.font.rendered_text("MENU", self.win, (300, 150))
                blit(self.win, self.menu_imgs[1], (325, 200))
                self.font.n_times = 2
                y = 200
                for menu in self.menu_imgs[1:]:
                    blit(self.win, menu, (325, y))
                    y += 100
                self.font.n_times = 2
                if self.info:
                    pos = 325 + self.menu_imgs[2].get_size()[0] + 5,300
                    blit(self.win,self.littleLabel,pos)
                    self.font.rendered_text("ADVICE: You can use the\nscroll wheel on the \ncoords' chart or chat's\nchart if you use the\nonline option.",self.win,(pos[0] + 2, pos[1] + 5))
            pygame.display.update()    
            
                
if __name__ == "__main__":
    game = Stages()
    game.choose_option()
    


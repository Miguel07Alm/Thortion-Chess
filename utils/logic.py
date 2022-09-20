from utils.functions import *
class Piece:
    def __init__(self, name, coord, r0, img, colour, pieces_choice = None):
        self.name = name
        self.img = img
        self.r0x, self.r0y = r0
        self.r = Vector2(self.r0x, self.r0y)
        self.team = colour
        
        self.colors = [[255] * 3, hex_to_rgb("#f6f6f6")] if colour == "white" else [hex_to_rgb("#111111"), hex_to_rgb("#2f2f2f")]
        self.c = list(map(lambda x: x - 5, hex_to_rgb("#ffcb74")))
        self.initial_coord = coord
        self.conditions = []
        self.ideal_coords = []
        self.rival_coords = []
        self.allies_coords = []
        self.all_positions = []            
        
        if self.name == "pawn": 
            self.mousewheel = False
            self.selection_piece = False
            self.n = 0
            self.surf_pawn_choice = pygame.Surface((54,54)).convert_alpha()
            self.surf_pawn_choice.fill((69, 255, 97, 107))
            self.choice_pieces =[ swap_color(pieces_choice["queen"], self.colors[0], color), 
                                  swap_color(pieces_choice["rook"], self.colors[0], color), 
                                  swap_color(pieces_choice["bishop"], self.colors[0], color), 
                                  swap_color(pieces_choice["knight"], self.colors[0], color)
                                ]
            for i in range(len(self.choice_pieces)):
                self.choice_pieces[i] = swap_color(pieces_choice["queen"], self.colors[i % 2], [255, 0, (i % 2) + 1])
                
            self.name_choice_pieces = ["queen", "rook", "bishop", "knight"]
            self.index_choice = 0
            self.choice_piece = self.choice_pieces[self.index_choice]
            self.pawn_skill = False

        if self.name == "pawn" or self.name == "rook": self.attack_positions = []
        
        if self.name == "queen":
           
            self.special_conditions = [[], []] # rook conditions and bishop conditions
            self.special_ideal_coords = [[], []] # rook ideal coords and bishop ideal coords
            self.bishop_special2_conditions = [] # Extra conditions of the bishop
        if self.name == "bishop":
            self.special_conditions = []
            
        self.n_movements_ingame = 0
        self.attack = False
        self.rival_piece = None
        self.ready_to_move = False
        self.last_coord = coord
        self.all_movements_coords = []
        self.letters = "abcdefgh"
        
        
        self.img = swap_color(self.img, self.colors[0], [255, 0, 0])
        self.img = swap_color(self.img, self.colors[1], [255, 0, 1])
        self.img = swap_color(self.img, hex_to_rgb("#ffcb74"), [255, 0, 2])
        
        
        self.contour2 = pygame.Surface((61,61)).convert_alpha()
        self.contour2x = self.contour2.copy() # For enemies
        self.contour2y = self.contour2.copy() # For allies
        
        self.contour2x.fill(hex_to_rgb("#8aff0d"))
        self.contour2.fill(hex_to_rgb("#0c59b1"))
        self.contour2y.fill(hex_to_rgb("#0ca5ba"))
        
        self.contour2.set_alpha(88)
        self.contour2x.set_alpha(90)
        self.contour2y.set_alpha(88)
                
        if name == "king": 
            self.check = False
            self.all_ideal_coords = []
            self.n_movements = 0
            self.img = swap_color(self.img, self.colors[0], king_color)
    def contour_selected(self):
        self.img = swap_color(self.img, self.c, self.colors[0])
        
    def reverse_contour(self):
        self.img = swap_color(self.img, self.colors[0], self.c)
            
    def square_contour(self, win, possible_coords, positions):
        #All the plays possible selected
        if self.name == "queen":
            self.ideal_coords = list(set(self.special_ideal_coords[0]).union(set(self.special_ideal_coords[1])))
        
        for coords in self.ideal_coords:
            rx, ry = coords
            if len(possible_coords) > 0:
                c = convert_position_into_coord(coords, positions)
                if self.name == "king":
                    if coords not in self.all_ideal_coords and c in possible_coords:
                        win.blit(self.contour2, (rx - 2, ry + 1))
                else:
                    if c in possible_coords:
                        win.blit(self.contour2, (rx - 2, ry + 1))
            else:
                if self.name == "king":
                    if coords not in self.all_ideal_coords:
                        win.blit(self.contour2, (rx - 2, ry + 1))
                else:
                    win.blit(self.contour2, (rx - 2, ry + 1))
                
        for coords in self.rival_coords:
            rx, ry = coords
            if len(possible_coords) > 0:
                c = convert_position_into_coord(coords, positions)
                if c in possible_coords:
                    win.blit(self.contour2x, (rx - 2, ry + 1))
            else:
                win.blit(self.contour2x, (rx - 2, ry + 1))
        for coords in self.allies_coords:
            rx, ry = coords
            win.blit(self.contour2y, (rx - 2, ry + 1))
        
        
            
        
        contour3 = swap_color(self.contour2.copy(), "#d4e02d",self.contour2.copy().get_at((0,0)))
        contour3.set_alpha(175)
        win.blit(contour3, (self.r.x - 2, self.r.y + 1))
                
    
        
    def blit_piece(self, win, points = None,positions = None,pieces = None, turns = None, team = None):
        if self.name == "pawn":
            target_coord = self.last_coord[0] + "1" if self.team == "black" else  self.last_coord[0] + "8"
            # --Algorithm for the pawn skill--
            
            if self.last_coord == target_coord and self.team == team:
                self.pawn_skill = True
                c = swap_color(self.contour2.copy(), "#148561",self.contour2.copy().get_at((0,0)))
                rx, ry = self.r
                win.blit(c,(rx - 2, ry + 1))
                win.blit(self.choice_pieces[self.index_choice], self.r)
                
                self.index_choice -= self.n
                self.index_choice %= len(self.choice_pieces)
                self.n = 0
            
            if self.selection_piece:
                i = 0 if self.team == "white" else 1
                points_ranked = {"pawn": 1, "rook": 5, "knight": 3, "bishop": 3, "queen": 9} # based in pawns
                
                c = self.last_coord
                Team = self.team
                del pieces[pieces.index(self)]
                points[i] += points_ranked[self.name_choice_pieces[self.index_choice]]
                pieces.append(Piece(self.name_choice_pieces[self.index_choice], c, positions[c], self.choice_pieces[self.index_choice],Team))
                turns.append("white" if Team == "black" else "black")
            if not self.pawn_skill:
                win.blit(self.img, self.r)
                
        else: win.blit(self.img, self.r)
    
    def new_coord(self, new_coord,coord_choice,coords_ingame, last_positions = None):
        self.r = new_coord
        if last_positions != None: last_positions.append(self.last_coord)
        if self.last_coord in coords_ingame: del coords_ingame[coords_ingame.index(self.last_coord)]
        self.n_movements_ingame += 1
        self.last_coord = coord_choice[0]
        coords_ingame.append(self.last_coord)
        self.all_movements_coords.append(self.last_coord)
    def king_attack_algorithm(self, all_pieces, coords_ingame, coord, positions):
        c = 0
        if coord in coords_ingame: 
            c = 1
            coords_ingame.pop(coords_ingame.index(coord))
        #Algorithm for searching warning pieces
        ALLOWED_ATTACK = True
        for piece in all_pieces:
            if piece.team != self.team:
                if piece.name == "knight":
                    if (abs(int(coord[1]) - int(piece.last_coord[1])) == 2 and abs(self.letters.index(piece.last_coord[0]) - self.letters.index(coord[0])) == 1 and piece.last_coord[0] != coord[0] or abs(int(coord[1]) - int(piece.last_coord[1])) == 1 and abs(self.letters.index(piece.last_coord[0]) - self.letters.index(coord[0])) == 2):
                        ALLOWED_ATTACK = False
                elif piece.name == "rook":
                    if piece.rook_condition(coord, coords_ingame):
                        ALLOWED_ATTACK = False
                elif piece.name == "bishop":
                    if piece.bishop_condition(coord, coords_ingame, coord) and positions[coord] in piece.ideal_coords:
                        ALLOWED_ATTACK = False
                elif piece.name == "queen":
                    if piece.rook_condition(coord, coords_ingame) or (piece.bishop_condition(coord, coords_ingame, coord) and positions[coord] in piece.special_ideal_coords[1]):
                        ALLOWED_ATTACK = False
                elif piece.name == "king":
                    if piece.king_condition(coord, coords_ingame) and coord in piece.all_positions:
                        ALLOWED_ATTACK = False
                elif piece.name == "pawn":
                    if positions[coord] in piece.attack_positions:
                        ALLOWED_ATTACK = False
            if not ALLOWED_ATTACK: break
        if c: coords_ingame.append(coord)
        return ALLOWED_ATTACK
    def pawn_condition(self, coord):
        n = 1 if self.team == "white" else -1
        if self.last_coord[0] != "a": c1 = self.letters[self.letters.index(self.last_coord[0]) - 1] + str(int(self.last_coord[1]) + n)
        else: c1 = None
        if self.last_coord[0] != "h": c2 = self.letters[self.letters.index(self.last_coord[0]) + 1] + str(int(self.last_coord[1]) + n)
        else: c2 = None
        if coord in [c1, c2]: return True
        return False
    def king_movement(self, all_pieces,c,ideal_coord, coords_ingame):
        c0 = 0
        if self.last_coord in coords_ingame: 
            c0 = 1
            coords_ingame.pop(coords_ingame.index(self.last_coord))
        #Algorithm for searching warning pieces
        for piece in all_pieces:
            if piece.team != self.team:
                if piece.name == "knight":
                    if abs(int(c[1]) - int(piece.last_coord[1])) == 2 and abs(piece.letters.index(piece.last_coord[0]) - self.letters.index(c[0])) == 1 and piece.last_coord[0] != c[0] or abs(int(c[1]) - int(piece.last_coord[1])) == 1 and abs(self.letters.index(piece.last_coord[0]) - self.letters.index(c[0])) == 2:
                        if ideal_coord not in self.all_ideal_coords: self.all_ideal_coords.append(ideal_coord)
                        if ideal_coord in self.ideal_coords: del self.ideal_coords[self.ideal_coords.index(ideal_coord)]
                elif piece.name == "rook":
                    if piece.rook_condition(c, coords_ingame):
                        if ideal_coord not in self.all_ideal_coords: self.all_ideal_coords.append(ideal_coord)
                        if ideal_coord in self.ideal_coords: del self.ideal_coords[self.ideal_coords.index(ideal_coord)]
                elif piece.name == "bishop":
                    if piece.bishop_condition(c, coords_ingame, c) and ideal_coord in piece.ideal_coords:
                        if ideal_coord not in self.all_ideal_coords: self.all_ideal_coords.append(ideal_coord)
                        if ideal_coord in self.ideal_coords: del self.ideal_coords[self.ideal_coords.index(ideal_coord)]
                elif piece.name == "queen":
                    if piece.rook_condition(c, coords_ingame) or (piece.bishop_condition(c, coords_ingame, c) and ideal_coord in piece.ideal_coords):
                        if ideal_coord not in self.all_ideal_coords: self.all_ideal_coords.append(ideal_coord)
                        if ideal_coord in self.ideal_coords: del self.ideal_coords[self.ideal_coords.index(ideal_coord)]

        if c0: coords_ingame.append(self.last_coord)
    
    def king_movements(self, all_pieces,warning_pieces, coords_ingame, positions):
        n_movements = 0
        delete_coord = 0
        for ideal_coord in self.ideal_coords:
            c = convert_position_into_coord(ideal_coord, positions)
            if ideal_coord not in self.all_ideal_coords and c not in coords_ingame:
               
                self.king_movement(all_pieces, c, ideal_coord, coords_ingame)
                if ideal_coord in self.ideal_coords: n_movements += 1
            if len(warning_pieces) > 0:
                for piece in warning_pieces:
                    if self.king_condition(piece.last_coord, coords_ingame)[0] and positions[piece.last_coord] not in self.all_ideal_coords:
                        n_movements += 1
                        delete_coord += 1
            
        return n_movements
    def possible_check(self, king, all_pieces, coords_ingame, rival_coords):
        c = False
        c0 = 0
        if self.last_coord in coords_ingame:
            c0 = 1
            del coords_ingame[coords_ingame.index(self.last_coord)]
        coord = king.last_coord
        condition = []
        for not_allowed_coord in rival_coords:
            condition.append([])
            for piece in all_pieces:
                if piece.last_coord in rival_coords and len(rival_coords) > 1 and piece.last_coord != not_allowed_coord:
                    if piece.name == "knight":
                        if (abs(int(coord[1]) - int(piece.last_coord[1])) == 2 and abs(self.letters.index(piece.last_coord[0]) - self.letters.index(coord[0])) == 1 and piece.last_coord[0] != coord[0] or abs(int(coord[1]) - int(piece.last_coord[1])) == 1 and abs(self.letters.index(piece.last_coord[0]) - self.letters.index(coord[0])) == 2):
                            condition[rival_coords.index(not_allowed_coord)].append(1)
                    elif piece.name == "rook":
                        if piece.rook_condition(coord, coords_ingame):
                            condition[rival_coords.index(not_allowed_coord)].append(1)
                    elif piece.name == "bishop":
                        if piece.bishop_condition(coord, coords_ingame, coord):
                            condition[rival_coords.index(not_allowed_coord)].append(1)
                    elif piece.name == "queen":
                        if piece.rook_condition(coord, coords_ingame) or piece.bishop_condition(coord, coords_ingame, coord):
                            condition[rival_coords.index(not_allowed_coord)].append(1)

            condition[rival_coords.index(not_allowed_coord)] = 1 if sum(condition[rival_coords.index(not_allowed_coord)]) >= 1 else 0
        if all(condition): c = True
        if c0: coords_ingame.append(self.last_coord)
        return c
    
    def king_condition(self, coord, coords_ingame):
        return (True if 0 <= abs(self.letters.index(self.last_coord[0]) - self.letters.index(coord[0])) < 2 and 0 <= abs(int(self.last_coord[1]) - int(coord[1])) < 2 else False, True if coord not in coords_ingame else False)
    def rook_condition(self, coord, coords_ingame, rival_coord = None):
        conditions = []
        if self.last_coord[0] == coord[0]:
            n1, n2 = map(int, [self.last_coord[1], coord[1]])
            range_selected = range(n1, n2) if n1 < n2 else list(range(n2 + 1, n1 + 1))[::-1] #top, bottom
            
            for i in range_selected:
                c = self.last_coord[0] + str(i)
                if c != self.last_coord:
                    if rival_coord == None:
                        if c != self.last_coord: conditions.append(True if c not in coords_ingame else False)
                    else:
                        if c != rival_coord: conditions.append(True if c not in coords_ingame else False)
                        
                else:
                    conditions.append(True)
        elif self.last_coord[1] == coord[1]:
            n1, n2 = map(self.letters.index, [self.last_coord[0], coord[0]])
            range_selected = range(n1, n2) if n1 < n2 else list(range(n2 + 1, n1 + 1))[::-1] #Right, Left
            for i in range_selected:
                c = self.letters[i] + self.last_coord[1]
                
                if c != self.last_coord:
                    if rival_coord == None:
                        if c != self.last_coord: conditions.append(True if c not in coords_ingame else False)
                    else:
                        if c != rival_coord: conditions.append(True if c not in coords_ingame else False)
                else:
                    conditions.append(True)
        if all(conditions) and len(conditions) > 0: return True
        return False
    def knight_condition(self, coord, coords_ingame):
        if (abs(int(coord[1]) - int(self.last_coord[1])) == 2 and abs(self.letters.index(self.last_coord[0]) - self.letters.index(coord[0])) == 1 and self.last_coord[0] != coord[0] or abs(int(coord[1]) - int(self.last_coord[1])) == 1 and abs(self.letters.index(self.last_coord[0]) - self.letters.index(coord[0])) == 2 and self.last_coord[0] != coord[0]) and coord not in coords_ingame:
            return True
        return False
    def get_coords_for_check(self, positions, king, coords_ingame):
        all_coords = list(positions.keys())
        positions_coords = list(positions.values())
        check_coords = []
        if self.name == "king":
            if self.king_condition(king.last_coord, coords_ingame)[0] and positions[king.last_coord] not in self.all_ideal_coords:
                check_coords.append(king.last_coord)
            return check_coords
        
        if self.name == "pawn":
            for c in self.attack_positions:
                idx_coord = positions_coords.index(c)
                coord = all_coords[idx_coord]
                if coord == king.last_coord:
                    check_coords.append(coord)
            return check_coords
        if self.name == "rook":
            if self.last_coord[0] == king.last_coord[0]:
                n1, n2 = map(int, [self.last_coord[1], king.last_coord[1]])
                range_selected = range(n1, n2) if n1 < n2 else list(range(n2 + 1, n1 + 1))[::-1] #top, bottom

                for i in range_selected:
                    c = self.last_coord[0] + str(i)
                    if c != self.last_coord:
                        if c not in coords_ingame:
                            check_coords.append(c)
                
                        
            elif self.last_coord[1] == king.last_coord[1]:
                n1, n2 = map(self.letters.index, [self.last_coord[0], king.last_coord[0]])
                range_selected = range(n1, n2) if n1 < n2 else list(range(n2 + 1, n1 + 1))[::-1] #Right, Left
                for i in range_selected:
                    c = self.letters[i] + self.last_coord[1]
                    if c != self.last_coord:
                        if c not in coords_ingame:
                            check_coords.append(c)
            return check_coords
        if self.name == "bishop":
            dl, dn = self.letters.index(self.last_coord[0]) - self.letters.index(king.last_coord[0]), int(self.last_coord[1]) - int(king.last_coord[1])
            absolute_diferentials = map(abs, [dl, dn])
            n = max(absolute_diferentials)
            if dl < 0 and dn < 0:
                for i in range(1, n + 1):
                    if self.letters.index(self.last_coord[0]) + i < 8 and int(self.last_coord[1]) + i < 8: 
                        c = self.letters[self.letters.index(self.last_coord[0]) + i] + str(int(self.last_coord[1]) + i)
                        if c != self.last_coord:
                            if c not in coords_ingame:
                                check_coords.append(c)
                
            elif dl < 0 and dn > 0:
                for i in range(1, n + 1):
                    if self.letters.index(self.last_coord[0]) + i < 8 and int(self.last_coord[1]) - i > 0:
                        c = self.letters[self.letters.index(self.last_coord[0]) + i] + str(int(self.last_coord[1]) - i)
                        if c != self.last_coord:
                            if c not in coords_ingame:
                                check_coords.append(c)
            elif dl > 0 and dn < 0:
                for i in range(1, n + 1):
                    if self.letters.index(self.last_coord[0]) - i >= 0 and int(self.last_coord[1]) + i < 8: 
                        c = self.letters[self.letters.index(self.last_coord[0]) - i] + str(int(self.last_coord[1]) + i)
                        if c != self.last_coord:
                            if c not in coords_ingame:
                                check_coords.append(c)
            elif dl > 0 and dn > 0:
                for i in range(1, n + 1):
                    if self.letters.index(self.last_coord[0]) - i >= 0 and int(self.last_coord[1]) - i > 0: 
                        c = self.letters[self.letters.index(self.last_coord[0]) - i] + str(int(self.last_coord[1]) - i)
                        if c != self.last_coord:
                            if c not in coords_ingame:
                                check_coords.append(c)
            return check_coords
            
        if self.name == "knight":
            if self.knight_condition(king.last_coord, coords_ingame):
                check_coords.append(king.last_coord)
            return check_coords
            
        if self.name == "queen":
            #rook coords
            if self.last_coord[0] == king.last_coord[0]:
                n1, n2 = map(int, [self.last_coord[1], king.last_coord[1]])
                range_selected = range(n1, n2) if n1 < n2 else list(range(n2 + 1, n1 + 1))[::-1] #top, bottom

                for i in range_selected:
                    c = self.last_coord[0] + str(i)
                    if c != self.last_coord:
                        if c not in coords_ingame:
                            check_coords.append(c)
                
                        
            elif self.last_coord[1] == king.last_coord[1]:
                n1, n2 = map(self.letters.index, [self.last_coord[0], king.last_coord[0]])
                range_selected = range(n1, n2) if n1 < n2 else list(range(n2 + 1, n1 + 1))[::-1] #Right, Left
                for i in range_selected:
                    c = self.letters[i] + self.last_coord[1]
                    if c != self.last_coord:
                        if c not in coords_ingame:
                            check_coords.append(c)
            #Bishop Coords
            dl, dn = self.letters.index(self.last_coord[0]) - self.letters.index(king.last_coord[0]), int(self.last_coord[1]) - int(king.last_coord[1])
            absolute_diferentials = map(abs, [dl, dn])
            n = max(absolute_diferentials)
            if dl < 0 and dn < 0:
                for i in range(1, n + 1):
                    if self.letters.index(self.last_coord[0]) + i < 8 and int(self.last_coord[1]) + i < 8: 
                        c = self.letters[self.letters.index(self.last_coord[0]) + i] + str(int(self.last_coord[1]) + i)
                        if c != self.last_coord:
                            if c not in coords_ingame:
                                check_coords.append(c)
            elif dl < 0 and dn > 0:
                for i in range(1, n + 1):
                    if self.letters.index(self.last_coord[0]) + i < 8 and int(self.last_coord[1]) - i > 0:
                        c = self.letters[self.letters.index(self.last_coord[0]) + i] + str(int(self.last_coord[1]) - i)
                        if c != self.last_coord:
                            if c not in coords_ingame:
                                check_coords.append(c)
            elif dl > 0 and dn < 0:
                for i in range(1, n + 1):
                    if self.letters.index(self.last_coord[0]) - i >= 0 and int(self.last_coord[1]) + i < 8: 
                        c = self.letters[self.letters.index(self.last_coord[0]) - i] + str(int(self.last_coord[1]) + i)
                        if c != self.last_coord:
                            if c not in coords_ingame:
                                check_coords.append(c)
            elif dl > 0 and dn > 0:
                for i in range(1, n + 1):
                    if self.letters.index(self.last_coord[0]) - i >= 0 and int(self.last_coord[1]) - i > 0: 
                        c = self.letters[self.letters.index(self.last_coord[0]) - i] + str(int(self.last_coord[1]) - i)
                        if c != self.last_coord:
                            if c not in coords_ingame:
                                check_coords.append(c)
            return check_coords
    def bishop_condition(self, coord, coords_ingame, rival_coords = None):
        conditions = []
        dl, dn = self.letters.index(self.last_coord[0]) - self.letters.index(coord[0]), int(self.last_coord[1]) - int(coord[1])
        absolute_diferentials = map(abs, [dl, dn])
        n = max(absolute_diferentials)
        if ((self.letters.index(self.last_coord[0]) + self.letters.index(coord[0])) + (int(self.last_coord[1]) + int(coord[1]))) % 2 == 0 and rival_coords == None:
            if dl < 0 and dn < 0:
                for i in range(1, n + 1):
                    if self.letters.index(self.last_coord[0]) + i < 8 and int(self.last_coord[1]) + i < 9: 
                        c = self.letters[self.letters.index(self.last_coord[0]) + i] + str(int(self.last_coord[1]) + i)
                        if c != self.last_coord:
                            conditions.append(True if c not in coords_ingame else False)
            elif dl < 0 and dn > 0:
                for i in range(1, n + 1):
                    if self.letters.index(self.last_coord[0]) + i < 8 and int(self.last_coord[1]) - i > 0:
                        c = self.letters[self.letters.index(self.last_coord[0]) + i] + str(int(self.last_coord[1]) - i)
                        if c != self.last_coord:
                            conditions.append(True if c not in coords_ingame else False)
            elif dl > 0 and dn < 0:
                for i in range(1, n + 1):
                    if self.letters.index(self.last_coord[0]) - i >= 0 and int(self.last_coord[1]) + i < 9: 
                        c = self.letters[self.letters.index(self.last_coord[0]) - i] + str(int(self.last_coord[1]) + i)
                        if c != self.last_coord:
                            conditions.append(True if c not in coords_ingame else False)
            elif dl > 0 and dn > 0:
                for i in range(1, n + 1):
                    if self.letters.index(self.last_coord[0]) - i >= 0 and int(self.last_coord[1]) - i > 0: 
                        c = self.letters[self.letters.index(self.last_coord[0]) - i] + str(int(self.last_coord[1]) - i)
                        if c != self.last_coord:
                            conditions.append(True if c not in coords_ingame else False)
            if all(conditions) and len(conditions) > 0: 
                return True
        if ((self.letters.index(self.last_coord[0]) + self.letters.index(coord[0])) + (int(self.last_coord[1]) + int(coord[1]))) % 2 == 0 and rival_coords != None:
            if dl < 0 and dn < 0:
                for i in range(1, n + 1):
                    if self.letters.index(self.last_coord[0]) + i < 8 and int(self.last_coord[1]) + i < 9: 
                        c = self.letters[self.letters.index(self.last_coord[0]) + i] + str(int(self.last_coord[1]) + i)
                        if c == rival_coords: conditions.append(True)
                        elif c != self.last_coord:
                            conditions.append(True if c not in coords_ingame else False)
            elif dl < 0 and dn > 0:
                for i in range(1, n + 1):
                    if self.letters.index(self.last_coord[0]) + i < 8 and int(self.last_coord[1]) - i > 0:
                        c = self.letters[self.letters.index(self.last_coord[0]) + i] + str(int(self.last_coord[1]) - i)
                        if c == rival_coords: conditions.append(True)
                        elif c != self.last_coord:
                            conditions.append(True if c not in coords_ingame else False)
            elif dl > 0 and dn < 0:
                for i in range(1, n + 1):
                    if self.letters.index(self.last_coord[0]) - i >= 0 and int(self.last_coord[1]) + i < 9: 
                        c = self.letters[self.letters.index(self.last_coord[0]) - i] + str(int(self.last_coord[1]) + i)
                        if c == rival_coords: conditions.append(True)
                        elif c != self.last_coord:
                            conditions.append(True if c not in coords_ingame else False)
            elif dl > 0 and dn > 0:
                for i in range(1, n + 1):
                    if self.letters.index(self.last_coord[0]) - i >= 0 and int(self.last_coord[1]) - i > 0: 
                        c = self.letters[self.letters.index(self.last_coord[0]) - i] + str(int(self.last_coord[1]) - i)
                        if c == rival_coords: conditions.append(True)
                        elif c != self.last_coord:
                            conditions.append(True if c not in coords_ingame else False)
            if all(conditions) and len(conditions) > 0: 
                return True
        
        return False
    
    def strategy(self, positions,coords_ingame, all_pieces):
        if self.name == "pawn":
            #Number of possible plays: 2*
            n1 = 1 if self.team == "white" else -1
            n2 = 2 if self.team == "white" else -2
            coord1 = self.last_coord[0] + str(int(self.last_coord[1]) + n1)
            coord2 = self.last_coord[0] + str(int(self.last_coord[1]) + n2)
            
            if self.last_coord[0] not in ["a", "h"]:
                c1, c2 = self.letters[self.letters.index(self.last_coord[0]) - 1] + str(int(self.last_coord[1]) + n1), self.letters[self.letters.index(self.last_coord[0]) + 1] + str(int(self.last_coord[1]) + n1)
                if c1 in positions.keys():
                    if c1 in coords_ingame and positions[c1] not in self.ideal_coords:
                        piece = search_pieces_with_a_coord(all_pieces, c1)
                        if piece != None:
                            if piece.team != self.team and positions[c1] not in self.rival_coords: 
                                self.rival_coords.append(positions[c1])
                            
                            else:
                                if positions[c1] not in self.allies_coords:
                                    self.allies_coords.append(positions[c1])
                        if positions[c1] not in self.all_positions: self.all_positions.append(positions[c1])
                    else:
                        if positions[c1] not in self.attack_positions: 
                            self.attack_positions.append(positions[c1])
                            self.all_positions.append(positions[c1])
                if c2 in positions.keys():
                    if c2 in coords_ingame and positions[c2] not in self.ideal_coords:
                        piece = search_pieces_with_a_coord(all_pieces, c2)
                        if piece != None:
                            if piece.team != self.team and positions[c2] not in self.rival_coords:
                                self.rival_coords.append(positions[c2])
                            else:
                                if positions[c2] not in self.allies_coords:
                                    self.allies_coords.append(positions[c2])
                            if positions[c2] not in self.all_positions: self.all_positions.append(positions[c2])
                    else:
                        if positions[c2] not in self.attack_positions: 
                            self.attack_positions.append(positions[c2])
                            self.all_positions.append(positions[c2])
                                
            else:
                if self.last_coord[0] == "a":
                    c = self.letters[self.letters.index(self.last_coord[0]) + 1] + str(int(self.last_coord[1]) + n1)
                    if c in positions.keys():
                        if c not in self.all_positions: self.all_positions.append(positions[c])
                        if c in coords_ingame and c not in self.ideal_coords:
                            piece = search_pieces_with_a_coord(all_pieces, c)
                            if piece != None:
                                if piece.team != self.team and positions[c] not in self.rival_coords: 
                                    
                                    self.rival_coords.append(positions[c])
                                else:
                                    if positions[c] not in self.allies_coords:
                                        self.allies_coords.append(positions[c])
                                        
                        else:
                            if positions[c] not in self.attack_positions: 
                                self.attack_positions.append(positions[c])
                if self.last_coord[0] == "h":
                    c = self.letters[self.letters.index(self.last_coord[0]) - 1] + str(int(self.last_coord[1]) + n1)
                    if c in positions.keys():
                        if c not in self.all_positions: self.all_positions.append(positions[c])
                        if c in coords_ingame and positions[c] not in self.ideal_coords:
                            piece = search_pieces_with_a_coord(all_pieces, c)
                            if piece != None:
                                if piece.team != self.team and positions[c] not in self.rival_coords:
                                    
                                    self.rival_coords.append(positions[c])
                                else:
                                    if positions[c] not in self.allies_coords:
                                        self.allies_coords.append(positions[c])
                        else:
                            if positions[c] not in self.attack_positions: 
                                self.attack_positions.append(positions[c])
                
            if coord1 in positions.keys():
                if coord1 not in self.all_positions: self.all_positions.append(positions[coord1])
                if positions[coord1] not in self.ideal_coords and coord1 not in coords_ingame and int(coord1[1]) not in [0, 9]:
                    
                    self.ideal_coords.append(positions[coord1])
                if coord1 in coords_ingame:
                    piece = search_pieces_with_a_coord(all_pieces, coord1)
                    if piece != None:
                        if piece.team == self.team and positions[coord1] not in self.allies_coords: self.allies_coords.append(positions[coord1])
            if coord2 in positions.keys():              
                if coord2 not in self.all_positions: self.all_positions.append(positions[coord2])
                if positions[coord2] not in self.ideal_coords and (coord2 not in coords_ingame and self.initial_coord[0] + str(int(self.initial_coord[1]) + n1) not in coords_ingame) and self.last_coord[1] == self.initial_coord[1] and int(coord2[1]) not in [0, 9]: 
                    self.ideal_coords.append(positions[coord2])
                if coord2 in coords_ingame:
                    piece = search_pieces_with_a_coord(all_pieces, coord2)
                    if piece != None:
                        if piece != None:
                            if piece.team == self.team and positions[coord2] not in self.allies_coords: self.allies_coords.append(positions[coord2])
        
        if self.name == "rook":
            indx_letter = self.letters.index(self.last_coord[0])
            n_coord = self.last_coord[1]
            for i in range(indx_letter + 1, 8): #RIGHT
                c1 = self.letters[i] + n_coord
                if c1 not in self.all_positions: self.all_positions.append(positions[c1])
                if c1 != self.last_coord and c1 not in coords_ingame and positions[c1] not in self.ideal_coords:
                    self.ideal_coords.append(positions[c1])
                if c1 in coords_ingame:
                    piece = search_pieces_with_a_coord(all_pieces, c1)
                    if piece != None:
                        if piece.team != self.team and positions[c1] not in self.rival_coords: 
                            
                            self.rival_coords.append(positions[c1])
                        else:
                            if positions[c1] not in self.allies_coords:
                                self.allies_coords.append(positions[c1])
                            
                            
            for k in reversed(range(indx_letter)): #LEFT
                c11 = self.letters[k] + n_coord
                if c11 not in self.all_positions: self.all_positions.append(positions[c11])
                if c11 != self.last_coord and c11 not in coords_ingame and positions[c11] not in self.ideal_coords:
                    self.ideal_coords.append(positions[c11])
                if c11 in coords_ingame:
                    piece = search_pieces_with_a_coord(all_pieces, c11)
                    if piece != None:
                        if piece.team != self.team and positions[c11] not in self.rival_coords: 
                            
                            self.rival_coords.append(positions[c11])
                        else:
                            if positions[c11] not in self.allies_coords:
                                self.allies_coords.append(positions[c11])
                            
                            
                
            for j in range(int(n_coord), 8): #TOP
                c2 = self.last_coord[0] + str(j + 1)
                if c2 not in self.all_positions: self.all_positions.append(positions[c2])
                if c2 != self.last_coord and c2 not in coords_ingame and positions[c2] not in self.ideal_coords:
                    self.ideal_coords.append(positions[c2])
                if c2 in coords_ingame:
                    piece = search_pieces_with_a_coord(all_pieces, c2)
                    if piece != None:
                        if piece.team != self.team and positions[c2] not in self.rival_coords: 
                            
                            self.rival_coords.append(positions[c2])
                            
                        else:
                            if positions[c2] not in self.allies_coords:
                                self.allies_coords.append(positions[c2])
                            
                            
            for z in reversed(range(1, int(n_coord) + 1)): #BOTTOM
                if z - 1 > 1 and z - 1 < 9: c22 = self.last_coord[0] + str(z - 1)
                else: c22 = None
                if c22 != None:
                    if c22 not in self.all_positions: self.all_positions.append(positions[c22])

                    if c22 != self.last_coord and c22 not in coords_ingame and positions[c22] not in self.ideal_coords:
                        self.ideal_coords.append(positions[c22])
                    if c22 in coords_ingame:
                        piece = search_pieces_with_a_coord(all_pieces, c22)
                        if piece != None:
                            if piece.team != self.team and positions[c22] not in self.rival_coords: 
                                self.rival_coords.append(positions[c22])
                            else:
                                if positions[c22] not in self.allies_coords:
                                    self.allies_coords.append(positions[c22])
                                
            
                    
                
            
            
        if self.name == "knight":
            for i in [-2, -1, 1, 2]:
                for j in [-2,-1, 1, 2]:
                    coord = self.letters[(self.letters.index(self.last_coord[0]) + i) % 8] + str(int(self.last_coord[1]) + j)
                    if coord in positions.keys():
                        if abs(int(self.last_coord[1]) - int(coord[1])) == 2 and abs(self.letters.index(self.last_coord[0]) - self.letters.index(coord[0])) == 1:
                            if coord not in self.all_positions: self.all_positions.append(positions[coord])
                            if coord in positions.keys() and coord not in coords_ingame and positions[coord] not in self.ideal_coords:
                                self.ideal_coords.append(positions[coord])
                                
                            if coord in coords_ingame:
                                piece = search_pieces_with_a_coord(all_pieces, coord)
                                if piece != None:
                                    if piece.team != self.team and positions[coord] not in self.rival_coords: self.rival_coords.append(positions[coord])
                                    else:
                                        if positions[coord] not in self.allies_coords:
                                            self.allies_coords.append(positions[coord])
                        if abs(int(self.last_coord[1]) - int(coord[1])) == 1 and abs(self.letters.index(self.last_coord[0]) - self.letters.index(coord[0])) == 2:
                            if coord not in self.all_positions: self.all_positions.append(positions[coord])
                            if coord in positions and coord not in coords_ingame and positions[coord] not in self.ideal_coords :
                                self.ideal_coords.append(positions[coord])
                            if coord in coords_ingame:
                                piece = search_pieces_with_a_coord(all_pieces, coord)
                                if piece != None:
                                    if piece.team != self.team and positions[coord] not in self.rival_coords: self.rival_coords.append(positions[coord])
                                    else:
                                        if positions[coord] not in self.allies_coords:
                                            self.allies_coords.append(positions[coord])
                                            
                                            

                                
        if self.name == "bishop":
            letter, n = self.last_coord
            c1,c2 = [1] * 2
            for i in range(self.letters.index(letter), 8):
                if int(n) + c2 < 9 and self.letters.index(letter) + c1 < 8:
                    c = self.letters[self.letters.index(letter) + c1] + str(int(n) + c2)
                    if c not in self.all_positions: self.all_positions.append(positions[c])
                    if c in coords_ingame:
                        if c not in self.conditions: self.conditions.append(c)
                        piece = search_pieces_with_a_coord(all_pieces, c)
                        if piece != None:
                            if piece.team != self.team and positions[c] not in self.rival_coords: self.rival_coords.append(positions[c])
                            else: 
                                if positions[c] not in self.allies_coords:
                                    self.allies_coords.append(positions[c])
                                

                    if positions[c] not in self.ideal_coords: 
                        self.ideal_coords.append(positions[c])
                c1 += 1
                c2 += 1
                
            c1, c2 = -1, 1
            for i in range(self.letters.index(letter)):
                if int(n) + c2 < 9 and self.letters.index(letter) + c1 > -1:
                    c = self.letters[self.letters.index(letter) + c1] + str(int(n) + c2)
                    if c not in self.all_positions: self.all_positions.append(positions[c])
                    if c in coords_ingame:
                        if c not in self.conditions: self.conditions.append(positions[c])
                        piece = search_pieces_with_a_coord(all_pieces, c)
                        if piece != None:
                            if piece.team != self.team and positions[c] not in self.rival_coords: self.rival_coords.append(positions[c])
                            else: 
                                if positions[c] not in self.allies_coords:
                                    self.allies_coords.append(positions[c])

                    if positions[c] not in self.ideal_coords: 
                        self.ideal_coords.append(positions[c])
                c1 += -1
                c2 += 1
            c1 = c2 = -1
            for i in range(self.letters.index(letter)):
                if int(n) + c2 > 0 and self.letters.index(letter) + c1 > -1:
                    c = self.letters[self.letters.index(letter) + c1] + str(int(n) + c2)
                    if c not in self.all_positions: self.all_positions.append(positions[c])
                    if c in coords_ingame:
                        if c not in self.conditions: self.conditions.append(c)
                        piece = search_pieces_with_a_coord(all_pieces, c)
                        if piece != None:
                            if piece.team != self.team and positions[c] not in self.rival_coords: self.rival_coords.append(positions[c])
                            else: 
                                if positions[c] not in self.allies_coords:
                                    self.allies_coords.append(positions[c])

                    if positions[c] not in self.ideal_coords:
                        self.ideal_coords.append(positions[c])
                c1 -= 1
                c2 -= 1
                
            c1, c2 = 1, -1
            for i in range(self.letters.index(letter), 8):
                if int(n) + c2 > 0 and self.letters.index(letter) + c1 < 8:
                    c = self.letters[self.letters.index(letter) + c1] + str(int(n) + c2)
                    if c not in self.all_positions: self.all_positions.append(positions[c])
                    if c in coords_ingame:
                        if c not in self.conditions: self.conditions.append(c)
                        piece = search_pieces_with_a_coord(all_pieces, c)
                        if piece != None:
                            if piece.team != self.team and positions[c] not in self.rival_coords: self.rival_coords.append(positions[c])
                            else: 
                                if positions[c] not in self.allies_coords:
                                    self.allies_coords.append(positions[c])

                    if positions[c] not in self.ideal_coords:
                        self.ideal_coords.append(positions[c])
                c1 += 1
                c2 -= 1
        
        
        if self.name == "queen":
            #--Tower Ideal Coords
            indx_letter = self.letters.index(self.last_coord[0])
            n_coord = self.last_coord[1]
            for i in range(indx_letter + 1, 8):                
                c1 = self.letters[i] + n_coord
                if c1 not in self.all_positions: self.all_positions.append(positions[c1])
                
                if c1 != self.last_coord and c1 not in coords_ingame and positions[c1] not in self.special_ideal_coords[0]:
                    self.special_ideal_coords[0].append(positions[c1])
                if c1 in coords_ingame:
                    piece = search_pieces_with_a_coord(all_pieces, c1)
                    if piece != None:
                        if piece.team != self.team and positions[c1] not in self.rival_coords: self.rival_coords.append(positions[c1])
                        else:
                            if positions[c1] not in self.allies_coords:
                                self.allies_coords.append(positions[c1])

            for k in reversed(range(indx_letter)):
                c11 = self.letters[k] + n_coord
                if c11 not in self.all_positions: self.all_positions.append(positions[c11])
                if c11 != self.last_coord and c11 not in coords_ingame and positions[c11] not in self.special_ideal_coords[0]:
                    self.special_ideal_coords[0].append(positions[c11])
                
                if c11 in coords_ingame:
                    piece = search_pieces_with_a_coord(all_pieces, c11)
                    if piece != None:
                        if piece.team != self.team and positions[c11] not in self.rival_coords: self.rival_coords.append(positions[c11])
                        else:
                            if positions[c11] not in self.allies_coords:
                                self.allies_coords.append(positions[c11])
                
            for j in range(int(n_coord), 8):
                c2 = self.last_coord[0] + str(j + 1)
                if c2 not in self.all_positions: self.all_positions.append(positions[c2])
                
                if c2 != self.last_coord and c2 not in coords_ingame and positions[c2] not in self.special_ideal_coords[0]:
                    self.special_ideal_coords[0].append(positions[c2])
                if c2 in coords_ingame:
                    piece = search_pieces_with_a_coord(all_pieces, c2)
                    if piece != None:
                        if piece.team != self.team and positions[c2] not in self.rival_coords: self.rival_coords.append(positions[c2])
                        else:
                            if positions[c2] not in self.allies_coords:
                                self.allies_coords.append(positions[c2])
                    

            for z in reversed(range(1, int(n_coord) + 1)):
                if z - 1 > 0 and z - 1 < 9: c22 = self.last_coord[0] + str(z - 1)
                else: c22 = None
                
                if c22 != None:
                    if c22 not in self.all_positions: self.all_positions.append(positions[c22])
                    if c22 != self.last_coord and c22 not in coords_ingame and positions[c22] not in self.special_ideal_coords[0]:
                        self.special_ideal_coords[0].append(positions[c22])
                    if c22 in coords_ingame:
                        piece = search_pieces_with_a_coord(all_pieces, c22)
                        if piece != None:
                            if piece.team != self.team and positions[c22] not in self.rival_coords:
                                self.rival_coords.append(positions[c22])
                                
                            else:
                                if positions[c22] not in self.allies_coords:
                                    self.allies_coords.append(positions[c22])

                                
            #--Bishop Ideal Coords
            letter, n = self.last_coord
            c1 = c2 = 1
            for i in range(self.letters.index(letter), 8):
                if int(n) + c2 < 9 and self.letters.index(letter) + c1 < 8:
                    c = self.letters[self.letters.index(letter) + c1] + str(int(n) + c2)
                    if c not in self.all_positions: self.all_positions.append(positions[c])
                    if c in coords_ingame:
                        if c not in self.special_conditions[1] and c != self.last_coord: self.special_conditions[1].append(c)
                        piece = search_pieces_with_a_coord(all_pieces, c)
                        if piece != None:
                            if piece.team != self.team and positions[c] not in self.rival_coords: 
                                
                                self.rival_coords.append(positions[c])
                            else: 
                                if positions[c] not in self.allies_coords:
                                    self.allies_coords.append(positions[c])
                                                        
                    if positions[c] not in self.special_ideal_coords[1] and c != self.last_coord:
                        self.special_ideal_coords[1].append(positions[c])
                c1 += 1
                c2 += 1
                
            c1, c2 = -1, 1
            for i in range(self.letters.index(letter)):
                if int(n) + c2 < 9 and self.letters.index(letter) + c1 >= 0:
                    c = self.letters[self.letters.index(letter) + c1] + str(int(n) + c2)
                    if c not in self.all_positions: self.all_positions.append(positions[c])
                    if c in coords_ingame:
                        if c not in self.special_conditions[1]  and c != self.last_coord: self.special_conditions[1].append(c)
                        piece = search_pieces_with_a_coord(all_pieces, c)
                        if piece != None:
                            if piece.team != self.team and positions[c] not in self.rival_coords: 
                                
                                self.rival_coords.append(positions[c])
                                
                            else: 
                                if positions[c] not in self.allies_coords:
                                    self.allies_coords.append(positions[c])

                    if positions[c] not in self.special_ideal_coords[1] and c != self.last_coord: 
                        self.special_ideal_coords[1].append(positions[c])
                c1 += -1
                c2 += 1
            c1 = c2 = -1
            for i in range(self.letters.index(letter)):
                if int(n) + c2 > 0 and self.letters.index(letter) + c1 > -1:
                    c = self.letters[self.letters.index(letter) + c1] + str(int(n) + c2)
                    if c not in self.all_positions: self.all_positions.append(positions[c])
                    if c in coords_ingame:
                        if c not in self.special_conditions[1]  and c != self.last_coord: self.special_conditions[1].append(c)
                        piece = search_pieces_with_a_coord(all_pieces, c)
                        if piece != None:
                            if piece.team != self.team and positions[c] not in self.rival_coords: 
                                self.rival_coords.append(positions[c])
                                
                            else: 
                                if positions[c] not in self.allies_coords:
                                    self.allies_coords.append(positions[c])

                    if positions[c] not in self.special_ideal_coords[1] and c != self.last_coord:
                        self.special_ideal_coords[1].append(positions[c])
                c1 -= 1
                c2 -= 1
                
            c1, c2 = 1, -1
            for i in range(self.letters.index(letter), 8):
                if int(n) + c2 > 0 and self.letters.index(letter) + c1 < 8:
                    c = self.letters[self.letters.index(letter) + c1] + str(int(n) + c2)
                    if c not in self.all_positions: self.all_positions.append(positions[c])
                    if c in coords_ingame:
                        if c not in self.special_conditions[1] and c != self.last_coord: self.special_conditions[1].append(c)
                        
                        piece = search_pieces_with_a_coord(all_pieces, c)
                        if piece != None:
                            if piece.team != self.team and positions[c] not in self.rival_coords: 
                                
                                self.rival_coords.append(positions[c])
                            else: 
                                if positions[c] not in self.allies_coords:
                                    self.allies_coords.append(positions[c])
                            
                    if positions[c] not in self.special_ideal_coords[1] and c != self.last_coord: 
                        self.special_ideal_coords[1].append(positions[c])
                c1 += 1
                c2 -= 1
        elif self.name == "king":
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if self.letters.index(self.last_coord[0]) + i < 8 and 0 < int(self.last_coord[1]) + j < 9:
                        c = self.letters[self.letters.index(self.last_coord[0]) + i] + str(int(self.last_coord[1]) + j)
                    else: c = None
                    
                    if c != None:
                        piece = search_pieces_with_a_coord(all_pieces, c)
                        
                        if positions[c] not in self.ideal_coords and c in positions.keys() and c not in coords_ingame and 0 <= abs(self.letters.index(self.last_coord[0]) - self.letters.index(c[0])) < 2 and 0 <= abs(int(self.last_coord[1]) - int(c[1])) < 2:
                            self.ideal_coords.append(positions[c])
                            self.all_positions.append(positions[c])
                            
                        if c in coords_ingame:
                            if piece != None:
                                
                                
                                if piece.team != self.team and positions[c] not in self.rival_coords: 
                                    self.rival_coords.append(positions[c])
                                else: 
                                    if positions[c] not in self.allies_coords:
                                        self.allies_coords.append(positions[c])
                            if positions[c] not in self.all_positions: self.all_positions.append(positions[c])
                        
        self.all_positions = [convert_position_into_coord(pos,positions) if pos not in positions.keys() else pos for pos in self.all_positions]
        
    def get_attributes(self):
        return self.__dict__

    def movement_system(self, positions, mouse_position, coords_ingame, all_pieces, rival_team, turn, possible_pieces_movement,possible_coords, our_king, deleted_pieces, points, used_coords, net = None, times = None, name_pieces = None,chatData = None, last_positions = None):
        # The algorithm for making the movements of all pieces
        points_ranked = {"pawn": 1, "rook": 5, "knight": 3, "bishop": 3, "queen": 9} # based in pawns
        deleted_pieces_coords = [deleted_piece.initial_coord for deleted_piece in deleted_pieces if deleted_piece != None]
        
        distances = []
        for v in positions.values():
            distances.append(mouse_position.distance_to(Vector2(v[0], v[1])))
        
        min_dist = min(distances)
        index_coord = distances.index(min_dist)
        coord_choice = list(positions.items())[index_coord]
        coord = Vector2(coord_choice[1][0], coord_choice[1][1])
        for piece in all_pieces:
            if piece.last_coord == coord_choice[0] and piece.team != self.team:
                self.attack = True
                self.rival_piece = piece
        indx_team = 0 if self.team == "white" else 1
        
        put_coords_ingame(all_pieces, coords_ingame)
        
        del coords_ingame[coords_ingame.index(self.last_coord)]
        suspicious_pieces = check(all_pieces, positions, our_king, coords_ingame)
        is_check_if_its_moving = True if len(suspicious_pieces) > 0 else False
        stuff = is_possible_checkmate(all_pieces, suspicious_pieces, positions, coords_ingame, our_king)
        false_check = False
        if is_check_if_its_moving and not our_king.check:
            false_check = True
            possible_pieces_movement[indx_team] = set(arr[i] for arr in stuff[1] for i in range(len(arr)))
            possible_coords[indx_team] = set(arr[i] for arr in stuff[2] for i in range(len(arr)))
        coords_ingame.append(self.last_coord)
        
        next_turn = "black" if self.team == "white" else "white"
        attack_coord = "x" + self.last_coord
        
        movements0 = self.all_movements_coords[:]
        if (not our_king.check and not is_check_if_its_moving) or (self.initial_coord in possible_pieces_movement[indx_team] and coord_choice[0] in possible_coords[indx_team]):
            if self.name == "pawn":
                
                if self.team == "white": 
                    self.conditions.append(True if int(coord_choice[0][1]) - int(self.last_coord[1]) == 1 else False)
                else: 
                    self.conditions.append(True if int(coord_choice[0][1]) - int(self.last_coord[1]) == -1 else False)
                n = 1 if self.team == "white" else -1
                if coord_choice[0] not in coords_ingame:
                    if abs(int(coord_choice[0][1]) - int(self.last_coord[1])) == 2  and self.last_coord[1] == self.initial_coord[1] and coord_choice[0][0] == self.last_coord[0]: 
                        if self.last_coord[0] + str(int(self.last_coord[1]) + n) not in coords_ingame:
                            self.new_coord(coord, coord_choice, coords_ingame,last_positions)
                            used_coords.append(self.last_coord)
                            turn.append(next_turn)
                            if net != None: net.send(make_info(turn, times, used_coords,deleted_pieces_coords,points[indx_team],name_pieces,chatData[self.team],[self.name, self.initial_coord, self.last_coord]))
                    elif self.conditions[0] and coord_choice[0][0] == self.last_coord[0]: 
                        self.new_coord(coord, coord_choice, coords_ingame,last_positions)
                        used_coords.append(self.last_coord)
                        turn.append(next_turn)
                        if net != None: net.send(make_info(turn, times, used_coords,deleted_pieces_coords,points[indx_team],name_pieces,chatData[self.team],[self.name, self.initial_coord, self.last_coord]))
                if self.attack:
                    if self.last_coord[0] not in ["a", "h"]:
                        if coord_choice[0][0] in [self.letters[self.letters.index(self.last_coord[0]) - 1],self.letters[self.letters.index(self.last_coord[0]) + 1]] and self.conditions[0]:
                            turn.append(next_turn)
                            self.new_coord(coord, coord_choice, coords_ingame,last_positions)
                            
                            deleted_pieces.append(self.rival_piece)
                            points[indx_team] += points_ranked[self.rival_piece.name]
                            used_coords.append(attack_coord)
                            if self.rival_piece.last_coord in coords_ingame: del coords_ingame[coords_ingame.index(self.rival_piece.last_coord)]
                            if self.rival_piece in rival_team: del rival_team[rival_team.index(self.rival_piece)]
                            if net != None: net.send(make_info(turn, times, used_coords,deleted_pieces_coords,points[indx_team],name_pieces,chatData[self.team],[self.name, self.initial_coord, self.last_coord]))
                    else:
                        if self.last_coord[0] == "a":
                            if coord_choice[0][0] == "b" and self.conditions[0]:
                                self.new_coord(coord, coord_choice, coords_ingame,last_positions)
                                deleted_pieces.append(self.rival_piece)
                                
                                points[indx_team] += points_ranked[self.rival_piece.name]
                                used_coords.append(attack_coord)
                                if self.rival_piece.last_coord in coords_ingame: del coords_ingame[coords_ingame.index(self.rival_piece.last_coord)]
                                if self.rival_piece in rival_team: del rival_team[rival_team.index(self.rival_piece)]
                                turn.append(next_turn)
                                if net != None: net.send(make_info(turn, times, used_coords,deleted_pieces_coords,points[indx_team],name_pieces,chatData[self.team],[self.name, self.initial_coord, self.last_coord]))
                        else:
                            if coord_choice[0][0] in "g" and self.conditions[0]:
                                self.new_coord(coord, coord_choice, coords_ingame,last_positions)
                                deleted_pieces.append(self.rival_piece)
                                
                                points[indx_team] += points_ranked[self.rival_piece.name]
                                used_coords.append(attack_coord)
                                if self.rival_piece.last_coord in coords_ingame: del coords_ingame[coords_ingame.index(self.rival_piece.last_coord)]
                                if self.rival_piece in rival_team: del rival_team[rival_team.index(self.rival_piece)]
                                turn.append(next_turn)
                                if net != None: net.send(make_info(turn, times, used_coords,deleted_pieces_coords,points[indx_team],name_pieces,chatData[self.team],[self.name, self.initial_coord, self.last_coord]))
                        
            elif self.name == "rook":
                condition = self.rook_condition(coord_choice[0], coords_ingame)
                if condition and coord_choice[0] not in coords_ingame:
                    self.new_coord(coord, coord_choice, coords_ingame,last_positions)
                    
                    turn.append(next_turn)
                    used_coords.append(self.last_coord)
                    if net != None: net.send(make_info(turn, times, used_coords,deleted_pieces_coords,points[indx_team],name_pieces,chatData[self.team],[self.name, self.initial_coord, self.last_coord]))
                if condition and self.attack:
                    self.new_coord(coord, coord_choice, coords_ingame,last_positions)
                    turn.append(next_turn)
                    points[indx_team] += points_ranked[self.rival_piece.name]
                    used_coords.append(attack_coord)
                    deleted_pieces.append(self.rival_piece)
                    if self.rival_piece.last_coord in coords_ingame: del coords_ingame[coords_ingame.index(self.rival_piece.last_coord)]
                    if self.rival_piece in rival_team: del rival_team[rival_team.index(self.rival_piece)]
                    if net != None: net.send(make_info(turn, times, used_coords,deleted_pieces_coords,points[indx_team],name_pieces,chatData[self.team],[self.name, self.initial_coord, self.last_coord]))
                

            elif self.name == "knight":
                condition = self.knight_condition(coord_choice[0], coords_ingame)
                if condition:
                    self.new_coord(coord, coord_choice, coords_ingame,last_positions)
                    used_coords.append(self.last_coord)
                    turn.append(next_turn)
                    if net != None: net.send(make_info(turn, times, used_coords,deleted_pieces_coords,points[indx_team],name_pieces,chatData[self.team],[self.name, self.initial_coord, self.last_coord]))
                    
                if self.attack and (abs(int(coord_choice[0][1]) - int(self.last_coord[1])) == 2 and abs(self.letters.index(self.last_coord[0]) - self.letters.index(coord_choice[0][0])) == 1 and self.last_coord[0] != coord_choice[0][0] or abs(int(coord_choice[0][1]) - int(self.last_coord[1])) == 1 and abs(self.letters.index(self.last_coord[0]) - self.letters.index(coord_choice[0][0])) == 2 and self.last_coord[0] != coord[0]):
                    self.new_coord(coord, coord_choice, coords_ingame,last_positions)
                    deleted_pieces.append(self.rival_piece)
                    points[indx_team] += points_ranked[self.rival_piece.name]
                    
                    
                    used_coords.append(attack_coord)
                    if self.rival_piece.last_coord in coords_ingame: del coords_ingame[coords_ingame.index(self.rival_piece.last_coord)]
                    if self.rival_piece in rival_team: del rival_team[rival_team.index(self.rival_piece)]
                    turn.append(next_turn)
                    if net != None: net.send(make_info(turn, times, used_coords,deleted_pieces_coords,points[indx_team],name_pieces,chatData[self.team],[self.name, self.initial_coord, self.last_coord]))
                
            elif self.name == "bishop":            
                condition = self.bishop_condition(coord_choice[0], coords_ingame)
                attack_condition = self.bishop_condition(coord_choice[0], coords_ingame,coord_choice[0])
                if positions[coord_choice[0]] in self.ideal_coords and coord_choice[0] not in coords_ingame and condition:
                    self.new_coord(coord, coord_choice, coords_ingame,last_positions)
                    turn.append(next_turn)
                    used_coords.append(self.last_coord)
                    if net != None: net.send(make_info(turn, times, used_coords,deleted_pieces_coords,points[indx_team],name_pieces,chatData[self.team],[self.name, self.initial_coord, self.last_coord]))
                    
                if self.attack and positions[coord_choice[0]] in self.rival_coords and attack_condition:
                    self.new_coord(coord, coord_choice, coords_ingame,last_positions)
                    deleted_pieces.append(self.rival_piece)
                    points[indx_team] += points_ranked[self.rival_piece.name]
                    used_coords.append(attack_coord)
                    if self.rival_piece.last_coord in coords_ingame: del coords_ingame[coords_ingame.index(self.rival_piece.last_coord)]
                    if self.rival_piece in rival_team: del rival_team[rival_team.index(self.rival_piece)]
                    turn.append(next_turn)
                    if net != None: net.send(make_info(turn, times, used_coords,deleted_pieces_coords,points[indx_team],name_pieces,chatData[self.team],[self.name, self.initial_coord, self.last_coord]))
                    
                
            elif self.name == "queen":
                condition_rook = self.rook_condition(coord_choice[0], coords_ingame)
                condition_bishop = self.bishop_condition(coord_choice[0], coords_ingame)
                attack_condition_bishop = self.bishop_condition(coord_choice[0], coords_ingame,coord_choice[0])
                if condition_rook and coord_choice[0] not in coords_ingame:
                    self.new_coord(coord, coord_choice, coords_ingame,last_positions)
                    turn.append(next_turn)
                    used_coords.append(self.last_coord)
                    if net != None: net.send(make_info(turn, times, used_coords,deleted_pieces_coords,points[indx_team],name_pieces,chatData[self.team],[self.name, self.initial_coord, self.last_coord]))
                    
                elif positions[coord_choice[0]] in self.special_ideal_coords[1] and coord_choice[0] not in coords_ingame and condition_bishop:
                    self.new_coord(coord, coord_choice, coords_ingame,last_positions)
                    turn.append(next_turn)
                    used_coords.append(self.last_coord)
                    if net != None: net.send(make_info(turn, times, used_coords,deleted_pieces_coords,points[indx_team],name_pieces,chatData[self.team],[self.name, self.initial_coord, self.last_coord]))
                    
                if condition_rook and self.attack:
                    self.new_coord(coord, coord_choice, coords_ingame,last_positions)
                    turn.append(next_turn)
                    deleted_pieces.append(self.rival_piece)
                    points[indx_team] += points_ranked[self.rival_piece.name]
                    used_coords.append(attack_coord)
                    if self.rival_piece.last_coord in coords_ingame: del coords_ingame[coords_ingame.index(self.rival_piece.last_coord)]
                    if self.rival_piece in rival_team: del rival_team[rival_team.index(self.rival_piece)]
                    if net != None: net.send(make_info(turn, times, used_coords,deleted_pieces_coords,points[indx_team],name_pieces,chatData[self.team],[self.name, self.initial_coord, self.last_coord]))
                    
                
                elif self.attack and positions[coord_choice[0]] in self.rival_coords and attack_condition_bishop:
                    self.new_coord(coord, coord_choice, coords_ingame,last_positions)
                    turn.append(next_turn)
                    deleted_pieces.append(self.rival_piece)
                    points[indx_team] += points_ranked[self.rival_piece.name]
                    used_coords.append(attack_coord)
                    if self.rival_piece.last_coord in coords_ingame: del coords_ingame[coords_ingame.index(self.rival_piece.last_coord)]
                    if self.rival_piece in rival_team: del rival_team[rival_team.index(self.rival_piece)]
                    if net != None: net.send(make_info(turn, times, used_coords,deleted_pieces_coords,points[indx_team],name_pieces,chatData[self.team],[self.name, self.initial_coord, self.last_coord]))
                    
        
            elif self.name == "king":
                if self.n_movements != 0:
                    conditions_king = self.king_condition(coord_choice[0], coords_ingame)
                    # Poner filtro en checkmate para pasar las coordenadas que cumplan las condiciones de las piezas para atacar
                    if all(conditions_king) and positions[coord_choice[0]] not in self.all_ideal_coords and positions[coord_choice[0]] in self.ideal_coords:
                        self.new_coord(coord, coord_choice, coords_ingame,last_positions)
                        turn.append(next_turn)
                        used_coords.append(self.last_coord)
                        if net != None: net.send(make_info(turn, times, used_coords,deleted_pieces_coords,points[indx_team],name_pieces,chatData[self.team],[self.name, self.initial_coord, self.last_coord]))
                        
                    if self.attack and conditions_king[0] and positions[coord_choice[0]] not in self.all_ideal_coords and positions[coord_choice[0]] in self.rival_coords:
                        if self.king_attack_algorithm(all_pieces, coords_ingame, coord_choice[0], positions):
                            self.new_coord(coord, coord_choice, coords_ingame,last_positions)
                            deleted_pieces.append(self.rival_piece)
                            points[indx_team] += points_ranked[self.rival_piece.name]
                            used_coords.append(attack_coord)
                            if self.rival_piece.last_coord in coords_ingame: del coords_ingame[coords_ingame.index(self.rival_piece.last_coord)]
                            if self.rival_piece in rival_team: del rival_team[rival_team.index(self.rival_piece)]
                            turn.append(next_turn)
                            if net != None: net.send(make_info(turn, times, used_coords,deleted_pieces_coords,points[indx_team],name_pieces,chatData[self.team],[self.name, self.initial_coord, self.last_coord]))
                            
                    if self.n_movements_ingame == 0:
                        rook_piece1 = get_piece(all_pieces, self.team, "rook", "h" + self.last_coord[1])
                        bishop_position1, knight_position1 = "f" + self.last_coord[1], "g" + self.last_coord[1]
                        rook_piece2 = get_piece(all_pieces, self.team, "rook", "a" + self.last_coord[1])
                        bishop_position2, queen_position2, knight_position2 = "c" + self.last_coord[1], "d" + self.last_coord[1], "b" + self.last_coord[1]
                        if rook_piece1 != None:
                            s1, s2 = self.n_movements_ingame + rook_piece1.n_movements_ingame,self.n_movements_ingame + rook_piece2.n_movements_ingame
                            # **SHORT CASTLING**
                            if coord_choice[0] == rook_piece1.last_coord and rook_piece1.last_coord == rook_piece1.initial_coord and self.last_coord == self.initial_coord and bishop_position1 not in coords_ingame and knight_position1 not in coords_ingame and not self.check and s1 == 0 and positions[knight_position1] not in self.all_ideal_coords:
                                king_coord = Vector2(positions[bishop_position1][0],positions[bishop_position1][1])
                                rook_coord = Vector2(positions[knight_position1][0],positions[knight_position1][1])
                                rook_piece1.new_coord(king_coord,[bishop_position1], coords_ingame )
                                self.new_coord(rook_coord,[knight_position1], coords_ingame)
                                turn.append(next_turn)
                                used_coords.append("SC")
                                if net != None: net.send(make_info(turn, times, used_coords,deleted_pieces_coords,points[indx_team],name_pieces,chatData[self.team],[self.name, self.initial_coord, self.last_coord]))
                        if rook_piece2 != None: 
                            # **LONG CASTLING**
                            if coord_choice[0] == rook_piece2.last_coord and rook_piece2.last_coord == rook_piece2.initial_coord and self.last_coord == self.initial_coord and bishop_position2 not in coords_ingame and queen_position2 not in coords_ingame and knight_position2 not in coords_ingame and not self.check and s2 == 0 and positions[queen_position2] not in self.all_ideal_coords:
                                rook_coord = Vector2(positions[bishop_position2][0],positions[bishop_position2][1])
                                king_coord = Vector2(positions[queen_position2][0],positions[queen_position2][1])
                                rook_piece2.new_coord(king_coord,[queen_position2], coords_ingame )
                                self.new_coord(rook_coord,[bishop_position2], coords_ingame)
                                turn.append(next_turn)
                                used_coords.append("SL")
                                if net != None: net.send(make_info(turn, times, used_coords,deleted_pieces_coords,points[indx_team],name_pieces,chatData[self.team],[self.name, self.initial_coord, self.last_coord]))
                            
                
                if self.initial_coord in possible_pieces_movement[indx_team]:
                    if self.attack and self.king_attack_algorithm(all_pieces, coords_ingame, coord_choice[0], positions):
                        self.new_coord(coord, coord_choice, coords_ingame,last_positions)
                        deleted_pieces.append(self.rival_piece)
                        points[indx_team] += points_ranked[self.rival_piece.name]
                        used_coords.append(attack_coord)
                        if self.rival_piece.last_coord in coords_ingame: del coords_ingame[coords_ingame.index(self.rival_piece.last_coord)]
                        if self.rival_piece in rival_team: del rival_team[rival_team.index(self.rival_piece)]
                        turn.append(next_turn)
                        if net != None: net.send(make_info(turn, times, used_coords,deleted_pieces_coords,points[indx_team],name_pieces,chatData[self.team],[self.name, self.initial_coord, self.last_coord]))
                        
        
        
        self.attack = False

        self.conditions.clear()
        if self.name == "pawn":
            self.attack_positions.clear()  
            
        # DO A LIST THAT INCLUDES ALL THE COORDS OF THE PIECES MOVED 
        for piece in all_pieces:
            if piece.name == "bishop":
                piece.special_conditions.clear()
            if piece.name == "queen":
                piece.special_conditions[0].clear()
                piece.special_conditions[1].clear()
                piece.special_ideal_coords[0].clear()
                piece.special_ideal_coords[1].clear()
            if piece.name == "king":
                piece.all_ideal_coords.clear()
            piece.allies_coords.clear() 
            piece.rival_coords.clear()
            piece.ideal_coords.clear()   
            piece.all_positions.clear()
            if len(self.all_movements_coords) != len(movements0): 
                if self != piece: piece.is_moved = False
            
        if false_check:
            possible_pieces_movement[indx_team].clear()
            possible_coords[indx_team].clear()
                
            
    def __str__(self):
        return f"<coord: {self.last_coord}, name: {self.name}>"
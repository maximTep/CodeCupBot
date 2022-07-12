import random


class Cell:
    def __init__(self):
        self.x = -1
        self.y = -1
        self.none = False
        self.empty = False
        self.wall = False
        self.water = False
        self.heal = False
        self.energy = False
        self.me = False
        self.enemy = False
        self.radio = False


class Action:
    def __init__(self):
        self.move = 'Move'
        self.shoot = 'Shoot'
        self.turn_right = 'Turn Right'
        self.turn_left = 'Turn Left'
        self.knife = 'Knife'
        self.grenade_close = 'Grenade Close'
        self.grenade_far = 'Grenade Far'
        self.scan_h = 'Scan H'
        self.scan_v = 'Scan v'
        self.detect = 'Detect'



W = 0
H = 0
mapp = [[Cell()]]
it_num = 0
turns = 0




class Bot:
    # Метод initialize вызывается один раз при старте боя.
    # level содержит информацию о статических объектах и параметрах карты.




    def random_action(self):
        actions = ['Move', 'Shoot', 'Turn Right', 'Turn Left',
                   'Knife', 'Grenade Close', 'Grenade Far',
                   'Mine Up', 'Mine Right', 'Mine Down', 'Mine Left',
                   'Scan H', 'Scan V', 'Detect']

        return random.choice(actions)





    def initialize(self, level):
        global W, H, mapp
        W = level['size']['width']
        H = level['size']['height']
        mapp = [[Cell() for j in range(H)] for i in range(W)]

        # print('Initializing my bot')

    # iteration содержит информацию об игровой ситуации и должен вернуть код действия.

    def doAction(self, iteration):
        # Доступные варианты действия:
        #     'Move', 'Shoot',
        #     'Turn Right', 'Turn Left'
        #     'Shoot', 'Knife'
        #     'Grenade Close', 'Grenade Far'
        #     'Mine Up', 'Mine Right', 'Mine Down', 'Mine Left'
        #     'Scan H', 'Scan V',
        #     'Detect'
        #     'Demine ' + ID




        global mapp, H, W, it_num, turns



        action = Action()
        data = iteration['scope']['data']
        vision = [[Cell() for j in range(len(data[0]))] for i in range(len(data))]
        for i in range(len(data)):
            for j in range(len(data[0])):
                x = iteration['scope']['topLeft']['x'] + i
                y = iteration['scope']['topLeft']['y'] + j
                if x < 0 or y < 0 or x > W-1 or y > H-1:
                    continue

                mapp[x][y].x = x
                mapp[x][y].y = y
                if data[i][j] is None or x < 0 or y < 0 or x > W-1 or y > H-1:
                    mapp[x][y].none = True
                    continue

                if data[i][j] % 10 == 0:
                    mapp[x][y].empty = True
                elif data[i][j] % 10 == 1:
                    mapp[x][y].wall = True
                elif data[i][j]% 10 == 2:
                    mapp[x][y].water = True
                elif data[i][j] % 10 == 3:
                    mapp[x][y].heal = True
                elif data[i][j] % 10 == 4:
                    mapp[x][y].energy = True

                data[i][j] //= 10

                if data[i][j] % 10 == 1:
                    mapp[x][y].me = True
                elif data[i][j] % 10 == 2:
                    mapp[x][y].enemy = True

                data[i][j] //= 10

                if data[i][j] % 10 == 1:
                    mapp[x][y].radio = True



        direction = iteration['me']['direction']
        front = Cell()
        if iteration['aheadOfMe'] is None:
            front.none = True
        else:
            front.x = iteration['aheadOfMe']['x']
            front.y = iteration['aheadOfMe']['y']
            front = mapp[front.x][front.y]


        me = mapp[iteration['me']['position']['x']][iteration['me']['position']['y']]
        right = Cell()
        left = Cell()
        front_right = Cell()
        front_left = Cell()


        if direction == 0:
            try: right = mapp[me.x+1][me.y]
            except: right.none = True
            try: left = mapp[me.x-1][me.y]
            except:
                left.none = True
            try: front_right = mapp[me.x+1][me.y-1]
            except:
                front_right.none = True
            try: front_left = mapp[me.x-1][me.y-1]
            except:
                front_left.none = True
        elif direction == 1:
            try: right = mapp[me.x][me.y+1]
            except:
                right.none = True
            try: left = mapp[me.x][me.y-1]
            except:
                left.none = True
            try: front_right = mapp[me.x + 1][me.y + 1]
            except:
                front_right.none = True
            try: front_left = mapp[me.x + 1][me.y - 1]
            except:
                front_left.none = True
        elif direction == 2:
            try: right = mapp[me.x - 1][me.y]
            except:
                right.none = True
            try: left = mapp[me.x + 1][me.y]
            except:
                left.none = True
            try: front_right = mapp[me.x - 1][me.y + 1]
            except:
                front_right.none = True
            try: front_left = mapp[me.x + 1][me.y + 1]
            except:
                front_left.none = True
        elif direction == 3:
            try: right = mapp[me.x][me.y - 1]
            except:
                right.none = True
            try: left = mapp[me.x][me.y + 1]
            except:
                left.none = True
            try: front_right = mapp[me.x - 1][me.y - 1]
            except:
                front_right.none = True
            try: front_left = mapp[me.x - 1][me.y + 1]
            except:
                front_left.none = True





        # HEAL
        if front.heal:
            turns = 0
            mapp[front.x][front.y].heal = False
            return action.move
        elif (front_right.heal or front_left.heal) and not front.water and not front.wall and not front.none:
            turns = 0
            return action.move
        elif right.heal:
            turns = 0
            return action.turn_right
        elif left.heal:
            turns = 0
            return action.turn_left


        # ENERGY
        if front.energy:
            turns = 0
            mapp[front.x][front.y].energy = False
            return action.move
        elif (front_right.energy or front_left.energy) and not front.water and not front.wall and not front.none:
            turns = 0
            return action.move
        elif right.energy:
            turns = 0
            return action.turn_right
        elif left.energy:
            turns = 0
            return action.turn_left



        # ENEMY
        if front.enemy:
            turns = 0
            return action.knife
        elif front_right.enemy or front_left.enemy:
            turns = 0
            return action.grenade_close
        elif right.enemy:
            return action.turn_right
        elif left.enemy:
            return action.turn_left


        # RADIO
        if front.radio:
            if right.radio:
                if left.radio:
                    # if turns >= 2:
                    #     turns = 0
                    #     return action.move
                    # else:
                    #     turns += 1
                    #     return action.turn_right
                    turns = 0
                    return action.move

                else:
                    turns += 1
                    return action.turn_left
            else:
                turns += 1
                return action.turn_right

        # PEACE
        if front.wall or front.water or front.none:
            if right.wall or right.water or right.none:
                if left.wall or left.water or left.none:
                    turns += 1
                    return action.turn_right
                else:
                    turns += 1
                    return action.turn_left
            else:
                turns += 1
                return action.turn_right
        else:
            turns = 0
            return action.move










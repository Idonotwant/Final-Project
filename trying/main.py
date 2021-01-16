import pygame
import random
import sys,os
import time
from pygame.locals import Color, QUIT, MOUSEBUTTONDOWN, USEREVENT, USEREVENT
#pygame initialize
pygame.init()                                                 #初始化pygame
pygame.mixer.init()
#screen initialize
size = (1270,768)                                             #初始化螢幕
screen = pygame.display.set_mode(size)                        #螢幕大小
pygame.display.set_caption("計算機程式期末專題13組--大富翁")     #螢幕標題
#clock
FPS = 60                                                      #每秒楨數
clock = pygame.time.Clock()                                   #時間模組
#colors
white = (255,255,255)                                         #顏色設定(RGB)
black = (0,0,0)
red = (255,0,0)
#pictures
picW = 200#picture Width
picH = 200#picture Height
#texts-->SysFont(name, size, bold=False, italic=False)
textdisplay = pygame.font.Font("mss.ttf",30)
billborddisplay = pygame.font.Font("mss.ttf",30)
roadtext = pygame.font.Font("mss.ttf",30)
roadtext2 = pygame.font.Font("mss.ttf",30)
#other variables
Magni = 6                                                     #底圖放大倍率
l,m,r = False,False,False                                     #滑鼠按鍵
roadfilepath = "./roaddata.txt"                               #路的資料list[x,y,rotate,magni]
landfilepath = "./landdata.txt"                               #地的資料list[x,y,rotate,magni]
hospital_data = [4596, 3105, 45, 1]
police_data = [3919, 3724, 43, 1]
land_value_data = [7400, 8800, 4000, 5900, 6100, 5700, 6300, 8000, 6500, 8700, 8000, 3800, 3900, 7000, 9900, 4400, 9800, 5200, 5100, 6900, 8300, 4800, 6800, 5100, 6200, 7800, 4000, 7000, 6800, 9400, 7900, 3300, 3000, 9400, 7800, 5700, 7300, 7000, 4500, 8800, 5000, 4300, 8500, 6500, 6300, 4900, 8600, 9300, 7400, 4300, 8500, 8700, 9000, 4300, 10000, 8100, 3700, 4100, 8700, 8600, 4900, 4300, 4900, 3300, 5400, 4900, 4800 ]
exit_size = (50,50)
billbord_size = (round(size[0]/4),30*4+20)
initial_cash = 50000
fee_rate = 0.1              # 過路費為土地價值的多少比例
building_land_rate = 0.1    # 蓋房子所需要的費用為土地價值的多少比例
lv_value_rate = 1.5         # 升級一棟房子的土地增值比例
player_land = dict()        # 每個玩家名下的土地有哪些
land_list = []
road_list = []
player_list = []
current_player = None
fee_round = 10
round_count = 0             #記回合數
show_dice = []              #秀骰子
dice_pics = []
solved_lpics = []
solved_hpics = []
chance,destiny = 0,0
def readdata(filepath):
    """give filepath,return a 2-level list"""
    if not os.path.isfile(filepath):                         #路徑不存在，return[]
        return []
    with open(filepath,"r") as f:                            #讀檔
        s1 = f.read()
    if len(s1) < 4:                                          #空陣列，return[]
        return []
    #演算法，不解釋
    s1 = s1[2:-2]
    len_1 = True
    for count in range(len(s1)):
        if s1[count] == "]":
            len_1 = False
            break
    if len_1:#if the data len is 1,it cannot use split again
        raw_datalist = [s1]
    else:
        raw_datalist = s1.split("], [")
    datalist = []
    for item in raw_datalist:
        raw_data = [float(n) for n in item.split(", ")]
        for i in range(3):
            raw_data[i] = round(raw_data[i])#x,y,angle is integer
        datalist.append(raw_data)
    return datalist



# current_player 當下回合的玩家 
# 所有回合數的countdown都要+1

class road:
    def __init__(self,position,adj_position = [],is_chance = False,is_destiny = False,land = -1, is_bank = False):
        self.position = position # 道路的位置
        self.adj_position = adj_position # 鄰近道路的list
        self.chance = is_chance  # True or False
        self.destiny = is_destiny # True or False
        self.land = land # 土地的號碼 
        self.bank = is_bank # True or False
        self.rect = 0
        if self.chance == True:
            self.source = 2
        elif self.destiny == True:
            self.source = 1
        elif self.bank == True:
            self.source = 3
        else:
            self.source = 0

    def check_bank(self):
        global roadtext_surface,roadtext2_surface,roadtext,roadtext2,clock
        if self.bank == True:
            roadtext_surface = roadtext.render("你到了銀行，請問要存款還是提款(Yes = 存款  No = 提款)", True, black)
            
            display(show_button = True)
            clock.tick(15)
            isPressYes = check_Yes()
            self.do_bank(isPressYes)
        else:
            pass
    
    def do_bank(self, isPressYes):
        global roadtext_surface,roadtext2_surface,roadtext,roadtext2,clock
        # True = 存款  False = 提款
        if isPressYes == True:
            roadtext_surface = roadtext.render("請問要存多少錢？", True, black)
            money = ""
            typing = True
            while typing == True:
                display()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_0:
                            money += "0"
                            roadtext_surface = roadtext.render(f"{money}元", True, black)
                            display()
                        if event.key == pygame.K_1:
                            money += "1"
                            roadtext_surface = roadtext.render(f"{money}元", True, black)
                            display()
                        if event.key == pygame.K_2:
                            money += "2"
                            roadtext_surface = roadtext.render(f"{money}元", True, black)
                            display()
                        if event.key == pygame.K_3:
                            money += "3"
                            roadtext_surface = roadtext.render(f"{money}元", True, black)
                            display()
                        if event.key == pygame.K_4:
                            money += "4"
                            roadtext_surface = roadtext.render(f"{money}元", True, black)
                            display()
                        if event.key == pygame.K_5:
                            money += "5"
                            roadtext_surface = roadtext.render(f"{money}元", True, black)
                            display()
                        if event.key == pygame.K_6:
                            money += "6"
                            roadtext_surface = roadtext.render(f"{money}元", True, black)
                            display()
                        if event.key == pygame.K_7:
                            money += "7"
                            roadtext_surface = roadtext.render(f"{money}元", True, black)
                            display()
                        if event.key == pygame.K_8:
                            money += "8"
                            roadtext_surface = roadtext.render(f"{money}元", True, black)
                            display()
                        if event.key == pygame.K_9:
                            money += "9"
                            roadtext_surface = roadtext.render(f"{money}元", True, black)
                            display()
                        if event.key == pygame.K_BACKSPACE:
                            money = ""
                            roadtext_surface = roadtext.render(f"{money}元", True, black)
                            display()
                        if event.key == pygame.K_RETURN:
                            typing = False
                clock.tick(15)
            if money == "":
                deposit_money = 0
            else:
                deposit_money = int(money)
            if deposit_money > current_player.cash :
                roadtext_surface = roadtext.render("你想存的錢超過你的現金了", True, black)
                for timer in range(30):
                    display()
                    clock.tick(15)
                self.check_bank()
            else:
                roadtext_surface = roadtext.render(f"你存了{money}元", True, black)
                for timer in range(30):
                    display()
                    clock.tick(15)
                current_player.cash -= deposit_money
                current_player.deposit += deposit_money

        if isPressYes == False:
            roadtext_surface = roadtext.render("請問要提多少錢？", True, black)
            display()
            money = ""
            typing = True
            while typing == True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_0:
                            money += "0"
                            roadtext_surface = roadtext.render(f"{money}元", True, black)
                            display()
                        if event.key == pygame.K_1:
                            money += "1"
                            roadtext_surface = roadtext.render(f"{money}元", True, black)
                            display()
                        if event.key == pygame.K_2:
                            money += "2"
                            roadtext_surface = roadtext.render(f"{money}元", True, black)
                            display()
                        if event.key == pygame.K_3:
                            money += "3"
                            roadtext_surface = roadtext.render(f"{money}元", True, black)
                            display()
                        if event.key == pygame.K_4:
                            money += "4"
                            roadtext_surface = roadtext.render(f"{money}元", True, black)
                            display()
                        if event.key == pygame.K_5:
                            money += "5"
                            roadtext_surface = roadtext.render(f"{money}元", True, black)
                            display()
                        if event.key == pygame.K_6:
                            money += "6"
                            roadtext_surface = roadtext.render(f"{money}元", True, black)
                            display()
                        if event.key == pygame.K_7:
                            money += "7"
                            roadtext_surface = roadtext.render(f"{money}元", True, black)
                            display()
                        if event.key == pygame.K_8:
                            money += "8"
                            roadtext_surface = roadtext.render(f"{money}元", True, black)
                            display()
                        if event.key == pygame.K_9:
                            money += "9"
                            roadtext_surface = roadtext.render(f"{money}元", True, black)
                            display()
                        if event.key == pygame.K_BACKSPACE:
                            money = ""
                            roadtext_surface = roadtext.render(f"{money}元", True, black)
                            display()
                        if event.key == pygame.K_RETURN:
                            typing = False
            if money == "":
                take_money = 0
            else:
                take_money = int(money)
            if take_money > current_player.deposit :
                roadtext_surface = roadtext.render("你沒有那麼多存款，別做夢了窮鬼！", True, black)
                for timer in range(30):
                    display()
                    clock.tick(15)
                self.check_bank()
            else:
                roadtext_surface = roadtext.render(f"你提了{money}元", True, black)
                for timer in range(30):
                    display()
                    clock.tick(15)
                current_player.deposit -= take_money
                current_player.cash += take_money
                
            
    

    def check_land(self):
        if self.land == -1:
            pass
        elif self.land != -1:
            land_list[self.land].operation(current_player)


    def check_chance(self):
        global roadtext_surface,roadtext2_surface,roadtext,roadtext2,clock
        if self.chance == True:
            roadtext_surface = roadtext.render("機會! 抽一張牌",True,black)
            roadtext2_surface = roadtext.render("按Yes繼續",True,black)
            display()
            a = check_Yes()
            roadtext2_surface = roadtext.render("",True,black)
            random_number = random.randint(1,21) # 抽一個機會
            if random_number == 1:
                # print("計算機程式期末\nAll Accept\n獲得獎學金2000元")
                #render(text, antialias, color, background=None) -> Surface
                roadtext_surface = roadtext.render("計算機程式期末All Accept獲得獎學金2000元", True, black)
                current_player.cost(2000)
                


            if random_number == 2:
                # print("在路上遇到林宗男老師，\n得到紅包10000元")
                roadtext_surface = roadtext.render("在路上遇到林宗男老師，得到紅包10000元", True, black)
                current_player.cost(10000)

            if random_number == 3:
                if len(player_land[current_player]) != 0: # 確認玩家有土地
                    current_player_land = []   # 玩家小於等級4的土地清單
                    for land in player_land[current_player]:
                        if land_list[land].lv < 4:
                            current_player_land.append(land_list[land])
                    if len(current_player_land) != 0:
                        # print("交流版填問卷抽到房子一棟，隨機幫你的土地蓋一棟房子，(如果沒有土地，再抽一張機會)")
                        roadtext_surface = roadtext.render("交流版填問卷抽到房子一棟隨機幫你的土地蓋一棟房子", True, black)
                        random_land = random.choice(current_player_land)
                        temp = current_player.cash
                        random_land.lv_up(current_player,True)
                        current_player.cash = temp
                    else:
                        self.check_chance()
                else:
                    self.check_chance()

            if random_number == 4:
                # print("考上台大，爸媽給零用錢5000元")
                roadtext_surface = roadtext.render("考上台大，爸媽給零用錢5000元", True, black)
                current_player.cost(5000)

            if random_number == 5:
                # print("偷跟邦元助教去吃研究室尾牙，抽中腳踏車")
                roadtext_surface = roadtext.render("偷跟邦元助教去吃研究室尾牙，抽中腳踏車", True, black)
                current_player.vehicle = 2


            if random_number == 6:
                # print("突然想看薑母鴨，移動到醉月湖旁")
                roadtext_surface = roadtext.render("突然想看薑母鴨，移動到醉月湖旁", True, black)
                current_player.flash(28)



            if random_number == 7:
                # print("被狗追，腎上腺素飆升，再次移動你剛剛骰出的點數")
                roadtext_surface = roadtext.render("被狗追，腎上腺素飆升，再次移動你剛剛骰出的點數", True, black)
                roadtext2_surface = roadtext.render("按Yes繼續",True,black)
                display()
                a = check_Yes()
                roadtext2_surface = roadtext.render("",True,black)
                current_player.move(current_player.pre_steps)


            if random_number == 8:
                # print("被正仁助教帶去林森北路轉大人，得紅包2000元")
                roadtext_surface = roadtext.render("被正仁助教帶去林森北路轉大人，得紅包2000元", True, black)
                current_player.cost(2000)


            if random_number == 9:
                # print("小松鼠為你帶來一個骰子，下三回合多一個骰子")
                roadtext_surface = roadtext.render("小松鼠為你帶來一個骰子，下三回合多一個骰子", True, black)
                current_player.buff_count[3] += 4


            if random_number == 10:
                # print("在路上被正妹搭訕，心情好再擲一次骰子")
                roadtext_surface = roadtext.render("在路上被正妹搭訕，心情好再擲一次骰子", True, black)
                roadtext2_surface = roadtext.render("按Yes繼續",True,black)
                display()
                a = check_Yes()
                roadtext2_surface = roadtext.render("",True,black)
                current_player.dice()


            if random_number == 11:
                # print("遇到浪漫Duke，使用"浪漫突進"偷取隨機一位玩家的20%現金")
                roadtext_surface = roadtext.render("遇到浪漫Duke，使用\"浪漫突進\"偷取隨機一位玩家的20%現金", True, black)
                roadtext2_surface = roadtext.render("按Yes繼續",True,black)
                display()
                a = check_Yes()
                roadtext2_surface = roadtext.render("",True,black)
                random_player = random.choice(player_list)
                while random_player == current_player : # 確認玩家不會選到自己
                    random_player = random.choice(player_list)
                stolen_cash = round(random_player.cash*0.2)
                random_player.cash -= stolen_cash
                current_player.cash += stolen_cash
                # print("偷取了某玩家的錢")
                roadtext_surface = roadtext.render(f"偷取了{current_player.name}的錢",True,black)


            if random_number == 12:
                # print("得書卷獎，獲獎金5000元")
                roadtext_surface = roadtext.render("得書卷獎，獲獎金5000元", True, black)
                current_player.cost(5000)

            
            if random_number == 13:
                # print("打LOL從鐵牌打到"免死金牌"，下一次不需要抽命運")
                roadtext_surface = roadtext.render("打LOL從鐵牌打到\"免死金牌\"，下一次不需要抽命運", True, black)
                current_player.gold += 1

            if random_number == 14:
                if len(player_land[current_player]) != 0: # 確認玩家有土地
                    current_player_land = []   # 玩家小於等級4的土地清單
                    for land in player_land[current_player]:
                        if land_list[land].lv < 4:
                            current_player_land.append(land_list[land])
                    if len(current_player_land) != 0:
                        # print("去土木系實習，加蓋一棟房子")
                        roadtext_surface = roadtext.render("去土木系實習，加蓋一棟房子", True, black)
                        random_land = random.choice(current_player_land)
                        temp = current_player.cash
                        random_land.lv_up(current_player,True)
                        current_player.cash = temp

                    else:
                        self.check_chance()
                else:
                    self.check_chance()

            if random_number == 15:
                self.check_chance()
                ## print("跟另一位玩家談戀愛，兩個人移動到總圖約會")
                #roadtext_surface = roadtext.render("跟另一位玩家談戀愛，兩個人移動到總圖約會", True, black)
                #random_player = random.choice(player_list)
                #while random_player == current_player : # 確認玩家不會選到自己
                #    random_player = random.choice(player_list)
                #random_player.flash(11)
                #current_player.rect.move_ip(road_list[11].rect.topleft[0]-road_list[current_player.position].rect.topleft[0],road_list[11].rect.topleft[1]-road_list[current_player.position].rect.topleft[1])
                #current_player.position = 11
                #current_player.pre_position = -1

            if random_number == 16:
                # print("幫星宇助教寫Code，得工資3000元")
                roadtext_surface = roadtext.render("幫星宇助教寫Code，得工資3000元", True, black)
                current_player.cost(3000)

            if random_number == 17:
                # print("這禮拜是經濟週，七回合內過路費9折")
                roadtext_surface = roadtext.render("這禮拜是經濟週，七回合內過路費9折", True, black)
                current_player.buff_count[1] += 8


            if random_number == 18:
                # print("領悟複利極限，五回合內現金以e的倍數成長")
                roadtext_surface = roadtext.render("領悟複利極限，五回合內存款以e的倍數成長", True, black)
                current_player.buff_count[2] += 5


            if random_number == 19:
                # print("成功用十個以內的AND、ORgate寫出4bit加法器，賣出後獲利10000元")
                roadtext_surface = roadtext.render("成功用十個以內的AND、ORgate寫出4bit加法器，賣出後獲利10000元", True, black)
                current_player.cost(10000)

            if random_number == 20:
                # print("證明考拉茲猜想，獲得100000獎金")
                roadtext_surface = roadtext.render("證明考拉茲猜想，獲得100000獎金", True, black)
                current_player.cost(100000)

            if random_number == 21:
                # print("樂極生悲，抽一張命運")
                roadtext_surface = roadtext.render("樂極生悲，抽一張命運", True, black)
                roadtext2_surface = roadtext.render("按Yes繼續",True,black)
                display()
                a = check_Yes()
                roadtext2_surface = roadtext.render("",True,black)
                destiny.check_destiny()

        else:
            pass

    def check_destiny(self):
        global roadtext_surface,roadtext2_surface,roadtext,roadtext2,clock
        if self.destiny == True:
            roadtext_surface = roadtext.render("命運! 抽一張牌",True,black)
            roadtext2_surface = roadtext.render("按Yes繼續",True,black)
            display()
            a = check_Yes()
            roadtext2_surface = roadtext.render("",True,black)
            random_number = random.randint(1,20) # 抽一個命運
            if random_number == 1:
                # print("走在路上被車撞，住院5天")
                roadtext_surface = roadtext.render("走在路上被車撞，住院5天", True, black)
                current_player.buff_count[0] += 6
                current_player.flash(111)

            if random_number == 2:
                 # print("騎Ubike出車禍，住院3天")
                roadtext_surface = roadtext.render("騎Ubike出車禍，住院3天", True, black)
                current_player.buff_count[0] += 4
                current_player.flash(111)

            if random_number == 3:
                 # print("計算機程式lab抄別人code，罰款3000元")
                roadtext_surface = roadtext.render("計算機程式lab抄別人code，罰款3000元", True, black)
                current_player.cost(-3000)

            if random_number == 4:
                 # print("偷林宗男老師的西裝外套，拘留3天")
                roadtext_surface = roadtext.render("偷林宗男老師的西裝外套，拘留3天", True, black)
                current_player.buff_count[0] += 4
                current_player.flash(117)
                
            if random_number == 5:
                # print("看Pornhub過度興奮，住院7天")
                roadtext_surface = roadtext.render("看Pornhub過度興奮，住院7天", True, black)
                current_player.buff_count[0] += 8
                current_player.flash(111)

            if random_number == 6:
                # print("偷牽別人的腳踏車，拘留5天")
                roadtext_surface = roadtext.render("偷牽別人的腳踏車，拘留5天", True, black)
                current_player.buff_count[0] += 6
                current_player.flash(117)

            if random_number == 7:
                # print("遇到聖經傳教士，滯留3天")
                roadtext_surface = roadtext.render("遇到聖經傳教士，滯留3天", True, black)
                current_player.buff_count[0] += 4

            if random_number == 8:
                # print("交worldgym會費，罰款20000元")
                roadtext_surface = roadtext.render("交worldgym會費，罰款20000元", True, black)
                current_player.cost(-20000)

            if random_number == 9:
                # print("在server上執行無窮迴圈被助教抓到，拘留5天")
                roadtext_surface = roadtext.render("在server上執行無窮迴圈被助教抓到，拘留5天", True, black)
                current_player.buff_count[0] += 6
                current_player.flash(117)

            if random_number == 10:
                if current_player.vehicle == 2:
                    # print("亂停腳踏車被水源伯吊走，失去腳踏車，罰款5000元")
                    roadtext_surface = roadtext.render("亂停腳踏車被水源伯吊走，失去腳踏車，罰款5000元", True, black)
                    current_player.vehicle = 1
                    current_player.cost(-5000)

                else:
                    self.check_destiny()

            if random_number == 11:
                # print("走在路上被腳踏車撞到，住院1天")
                roadtext_surface = roadtext.render("走在路上被腳踏車撞到，住院1天", True, black)
                current_player.buff_count[0] += 2
                current_player.flash(111)

            if random_number == 12:
                # print("走在路上被電動輪椅撞到，住院2天")
                roadtext_surface = roadtext.render("走在路上被電動輪椅撞到，住院2天", True, black)
                current_player.buff_count[0] += 3
                current_player.flash(111)

            if random_number == 13:
                self.check_destiny()
                # print("騎在路上跟腳踏車相撞，兩人一起住院5天")
                # (如果沒有腳踏車或是只有自己有腳踏車，再抽一張)
            #    roadtext_surface = roadtext.render("騎在路上跟腳踏車相撞，兩人一起住院5天", True, black)
            #    
#
            #    if current_player.vehicle == 2:
            #        local_player_list = []  # 有腳踏車的玩家清單
            #        for check_player in player_list:
            #            if check_player.vehicle == 2 and check_player != current_player:
            #                local_player_list.append(check_player)
            #        if len(local_player_list) != 0:
            #            chosen_player = random.choice(local_player_list) # 取一個玩家相撞
            #            current_player.vehicle = 1
            #            chosen_player.vehicle = 1
            #            roadtext2_surface = roadtext2.render(f"你和{chosen_player.name}的腳踏車都撞毀了")
            #            
            #            current_player.buff_count[0] += 6
            #            chosen_player.buff_count[0] += 6
            #            current_player.flash(111)
            #            chosen_player.rect.move_ip(road_list[111].rect.topleft[0]-road_list[chosen_player.position].rect.topleft[0],road_list[111].rect.topleft[1]-road_list[chosen_player.position].rect.topleft[1])
            #            chosen_player.position = 111
            #            chosen_player.pre_position = -1
#
            #        else:
            #            self.check_destiny()
#
            #    else:
            #        self.check_destiny()

            if random_number == 14:
                # print("台大實施共產制度，所有玩家的現金平均分配")
                roadtext_surface = roadtext.render("台大實施共產制度，所有玩家的現金平均分配", True, black)
                allcash = 0  # 所有玩家的現金
                n = len(player_list) # 玩家數
                for player in player_list:
                    allcash += player.cash  # 加總現金
                divided_cash = round(allcash/n) # 平分的錢
                for player in player_list:
                    player.cash = divided_cash # 分錢


            if random_number == 15:
                # print("得罪至宥助教，請吃飯損失5000元")
                roadtext_surface = roadtext.render("得罪至宥助教，請吃飯損失5000元", True, black)
                current_player.cost(-5000)

            if random_number == 16:
                # print("被二一，拘留3天")
                roadtext_surface = roadtext.render("被二一，拘留3天", True, black)
                current_player.buff_count[0] += 4
                current_player.flash(117)

            if random_number == 17:
                # print("交到女朋友，請客花費8000元")
                roadtext_surface = roadtext.render("交到女朋友，請客花費8000元", True, black)
                current_player.cost(-8000)

            if random_number == 18:
                # print("被女朋友劈腿，喝酒過度，住院3天")
                roadtext_surface = roadtext.render("被女朋友劈腿，喝酒過度，住院3天", True, black)
                current_player.buff_count[0] += 4
                current_player.flash(111)

            if random_number == 19:
                # print("被分手，痛苦的散盡家財，將自己的所有現金平分給其他玩家")
                roadtext_surface = roadtext.render("被分手，痛苦的散盡家財，將自己的所有現金平分給其他玩家", True, black)
                n = len(player_list) # n = 玩家數
                devided_cash = round(current_player.cash/(n-1)) # 平分的錢
                for player in player_list:
                    if player != current_player:
                        player.cash += devided_cash

                current_player.cash = 0

            if random_number == 20:
                # print("否極泰來，抽一張機會")
                roadtext_surface = roadtext.render("否極泰來，抽一張機會", True, black)
                roadtext2_surface = roadtext.render("按Yes繼續",True,black)
                display()
                a = check_Yes()
                roadtext2_surface = roadtext.render("",True,black)
                chance.check_chance()


        else:
            pass


class land:
    def __init__(self, rect, v=100, sec=0, index=0, lsource = 0, hsource = 0,scale = 1,rotate = 0):
        # 土地的rect
        self.rect = rect
        # 土地的房子層數
        self.lv = 0
        # 土地價值
        self.value = v
        # 土地的區段
        self.sector = sec
        # 土地的編號
        self.index = index
        # 土地的所有權人
        self.owner = ''
        # 土地圖片來源
        self.lsource = lsource
        # 房子圖片來源
        self.hsource = hsource
        
        self.scale = scale
        self.rotate = rotate
    
    # 土地有關之行為
    def operation(self, current_player):
        global roadtext_surface,roadtext2_surface,roadtext,roadtext2
        # 若土地為空地，且玩家現金足夠 → 問玩家要不要買土地
        if self.owner == '':
            if current_player.cash < self.value:
                roadtext_surface = roadtext.render("你的錢不夠買這土地",True,black)
                display()
                a = check_Yes()
            
            if current_player.cash >= self.value:
                roadtext_surface = roadtext.render(f'這塊空地價錢{self.value}元，您要買這塊地嗎？',True,black)
                display(show_button = True)
                isPressYes = check_Yes()
                self.change_owner(current_player,isPressYes)
        # 若土地為玩家的土地 → 問玩家要不要加蓋房子
        elif self.owner == current_player.name:
            self.upgrade_land(current_player)
        # 若土地為別人的土地 → 顯示過路費並扣錢
        elif self.owner != current_player.name:
            if current_player.cash >= self.fee():
                current_player.cash -= self.fee()
            elif current_player.cash < self.fee():
                current_player.deposit -= (self.fee()-current_player.cash)
                current_player.cash = 0
            for i in range(len(player_list)):
                if self.owner == player_list[i].name:
                    player_list[i].cash += self.fee()
                    break
                else:
                    pass
            roadtext_surface = roadtext.render(f'這是{self.owner}的土地，付過路費{self.fee()}元',True,black)
            
        
    # 是否加蓋房子
    def upgrade_land(self, current_player):
        global roadtext_surface,roadtext2_surface,roadtext,roadtext2
        if self.lv < 4 and (current_player.cash >= (self.value * building_land_rate)):
            roadtext_surface = roadtext.render(f'加蓋一棟房子需要{self.value * building_land_rate}元，您要加蓋嗎？',True,black)
            display(show_button = True)
            isPressYes = check_Yes()
            self.lv_up(current_player, isPressYes)
    def lv_up(self, current_player, isPressYes):
        global roadtext_surface,roadtext2_surface,roadtext,roadtext2
        if isPressYes == True:
            self.lv += 1
            current_player.cash -= round(self.value * building_land_rate)
            self.value = round(lv_value_rate * self.value)
            if self.lv == 1:
                roadtext_surface = roadtext.render('萬丈高樓平地起，恭喜你蓋了一棟房子！',True,black)
                self.hsource = 1
            elif self.lv == 2:
                roadtext_surface = roadtext.render('錦上添花宅迎祥，恭喜你加蓋了第二層房子！',True,black)
                self.hsource = 2
            elif self.lv == 3:
                roadtext_surface = roadtext.render('神仙難擋福臨門，恭喜你又蓋了第三層房子！',True,black)
                self.hsource = 3
            elif self.lv == 4:
                roadtext_surface = roadtext.render('鳴鳳棲梧龍翱翔，恭喜你升級成頂級樓層！',True,black)
                self.hsource = 4
        else:
            pass
    
    # 被拆除一層房子
    #def lv_down(self):
    #    if self.lv > 0:
    #        self.lv -= 1
    
    # 是否要買地
    def change_owner(self, current_player, isPressYes):
        global roadtext_surface,roadtext2_surface,roadtext,roadtext2
        if isPressYes == True:
            self.owner = current_player.name
            current_player.cash -= self.value
            player_land[current_player].append(self.index)
            roadtext_surface = roadtext.render('寶地但求貴人來，恭喜你買了一塊地！',True,black)
            self.lsource = player_list.index(current_player) + 1
            display()
            
        else:
            pass
    
    # 計算過路費
    def fee(self):
        return round(self.value * fee_rate)

class player():
    global roadtext_surface,road2text_surface,roadtext,roadtext2
    def __init__(self,*argv,**argvs):
        self.rect = argvs['rect']        #人物座標
        self.pic = argvs['pic']          #照片
        self.name = argvs['name']        #名字
        self.position = argvs['position']#位置
        self.pre_position = -1           #上一步
        self.cash = argvs['cash']        #現金
        self.deposit = argvs['deposit']  #存款
        self.vehicle = 1                 #交通工具
        self.gold = 0                    #免死金牌
        detain = 0                  #滯留
        nity_fee_count = 0          #過路費九折
        e_rate_count = 0            #現金以e的倍數成長
        more_dice_count = 0         #多一個骰子
        self.buff_count = []             #計算跟回合有關的buff
        self.buff_count.append(detain)
        self.buff_count.append(nity_fee_count)
        self.buff_count.append(e_rate_count)
        self.buff_count.append(more_dice_count)
        self.pre_steps = 0               #上一次骰的步數
    def after_interest(self,interest):   #利息
        """傳入利息，將個人存款增值"""
        self.deposit = round((1+interest)*self.deposit)
    def realstate(self):                 #不動產價值
        """return 人的所有不動產價值和"""
        global player_land,land_list               #dictionary,key=player,value = landindex
        summ = 0
        for landindex in player_land[self]:
            summ += land_list[landindex].value
        return summ
    
    def whole_money(self):               #總資產
        """return 總資產"""
        return (self.cash + self.deposit + self.realstate())
    
    
    def move_1(self):
        global road_list,backgroundRect
        adjroads = road_list[self.position].adj_position.copy()
        if self.pre_position in adjroads:
            adjroads.remove(self.pre_position)
        index = random.randint(0,len(adjroads)-1)
        self.pre_position = self.position
        self.position = adjroads[index]
        x = road_list[self.pre_position].rect.topleft[0] - road_list[self.position].rect.topleft[0]
        y = road_list[self.pre_position].rect.topleft[1] - road_list[self.position].rect.topleft[1]
        self.rect.move_ip(-x,-y)         
        backgroundRect.move_ip(x,y)
        clock.tick(4)
    
    def move(self,steps):                #移動
        global raod_list,clock
        for i in range(steps):
            self.move_1()            
            display()
            road_list[self.position].check_bank()

        road_list[self.position].check_land()
        road_list[self.position].check_chance()
        road_list[self.position].check_destiny()
        roadtext2_surface = roadtext.render("按Yes繼續",True,black)
        display()
        a = check_Yes()
        roadtext2_surface = roadtext.render("",True,black)
        time.sleep(1)
                

    
    def cost(self,money):                #被扣或加錢
        """給一個int,如果他>0代表加錢,<0則先扣現金,如果現金不足則不足由存款扣"""
        if money > 0:                    #加錢
            self.cash += money
        else:                            #扣錢
            if self.cash + money >= 0:   #現金夠
                self.cash += money
            else:                        #現金不足
                money += self.cash
                self.cash = 0
                self.deposit += money
        
    def after_one_round(self):
        """經過一個回合，玩家判斷複利、看buff"""
        for i in range(4):   #buff reset
            if self.buff_count[i] > 0:                  #buff count > 0
                if i == 2 :
                    self.deposit = round(self.deposit * 2.718)
                self.buff_count[i] -= 1
        if round_count and round_count%fee_round == 0:#round_count:回合計數
            self.after_interest(fee_rate)             #fee_rate:複利比
    def flash(self,target_index):
        global backgroundRect,road_list
        """從current_index閃現到給定index的road上"""
        current_index = self.position
        backgroundRect.move_ip(road_list[current_index].rect.topleft[0]-road_list[target_index].rect.topleft[0],road_list[current_index].rect.topleft[1]-road_list[target_index].rect.topleft[1])
        self.rect.move_ip(road_list[target_index].rect.topleft[0]-road_list[current_index].rect.topleft[0],road_list[target_index].rect.topleft[1]-road_list[current_index].rect.topleft[1])
        self.pre_position = -1
        self.position = target_index
        display()
    def dice(self):
        global show_dice,clock,roadtext_surface,roadtext2_surface
        """開始擲骰子"""
        '''傳入移動步數，人移動,如果有detain,則滯留'''
        if self.cash + self.deposit < 0:
            roadtext_surface = roadtext.render("你破產了 哭哭",True,black)
            display()
            a = check_Yes()
            roadtext2_surface = roadtext.render("",True,black)
            return
        if self.buff_count[0] != 0:
            left = self.buff_count[0]
            roadtext_surface = roadtext.render(f"還有{left}回合",True,black)
            roadtext2_surface = roadtext.render("按Yes繼續",True,black)
            display()
            a = check_Yes()
            roadtext2_surface = roadtext.render("",True,black)
        if not self.buff_count[0]:            
            show_dice = []
            for i in range(self.vehicle):
                show_dice.append(0)
            roadtext_surface = billborddisplay.render(f"輪到{current_player.name}了",True,black)
            roadtext2_surface = billborddisplay.render("按Yes開始擲骰子",True,black)
            isPressyes = False
            while not isPressyes:
                isPressyes = check_Yes()
            for i in range(21):
                for i in range(len(show_dice)):
                    show_dice[i]  = random.randint(0,5)
                roadtext_surface = billborddisplay.render("骰啊骰",True,black)
                roadtext2_surface = billborddisplay.render("",True,black)
                display()
                clock.tick(15)
            steps = 0
            for diceint in show_dice:
                steps += diceint+1
            roadtext_surface = billborddisplay.render(f"你骰出了{steps}點!",True,black)
            for timer in range(30):
                display()
                clock.tick(15)
            self.pre_steps = steps
            self.move(steps)
    
    
def display(show_button = False):
    global background,backgroundRect,exit,exitRect,billbord_pics,yes,yesRect,no,noRect,hospital,hospitalRect,police,policeRect,land_pic,house_pic,road_list,new_road_pic,current_player,player_pics,current_surfaces,ranking_surfaces,roadtext_surface,roadtext2_surface
    ##blit(source, dest, area=None, special_flags=0) -> Rect
    screen.blit(background,backgroundRect)
    #顯示土地
    if len(land_list) > 0:
        for i in range(len(land_list)):#add image after rotated and scaled[image,imageRect]
            aftershifted = land_list[i].rect.copy()
            aftershifted.topleft = (backgroundRect.topleft[0]+aftershifted.topleft[0],backgroundRect.topleft[1]+aftershifted.topleft[1])
            screen.blit(solved_lpics[i][land_list[i].lsource],aftershifted)
            screen.blit(solved_hpics[i][land_list[i].hsource],aftershifted)
    #顯示路
    if len(road_list) > 0:
        for i in range(len(road_list)):#add image after rotated and scaled[image,imageRect]
            aftershifted = road_list[i].rect.copy()
            aftershifted.topleft = (backgroundRect.topleft[0]+aftershifted.topleft[0],backgroundRect.topleft[1]+aftershifted.topleft[1])
            screen.blit(new_road_pic[road_list[i].source],aftershifted)
    #顯示醫院        
    aftershifted = hospitalRect.copy()
    aftershifted.topleft = (backgroundRect.topleft[0]+aftershifted.topleft[0],backgroundRect.topleft[1]+aftershifted.topleft[1])
    screen.blit(hospital,aftershifted)
    #顯示監獄
    aftershifted = policeRect.copy()
    aftershifted.topleft = (backgroundRect.topleft[0]+aftershifted.topleft[0],backgroundRect.topleft[1]+aftershifted.topleft[1])
    screen.blit(police,aftershifted)
    #顯示玩家
    current_index = player_list.index(current_player)
    for i in range(current_index-3,current_index+1):
        aftershifted = player_pics[i][1].copy()
        aftershifted.topleft = (backgroundRect.topleft[0]+aftershifted.topleft[0],backgroundRect.topleft[1]+aftershifted.topleft[1])
        screen.blit(player_pics[i][0],aftershifted)
    #顯示公佈欄
    for i in range(len(billbord_pics)): 
        screen.blit(billbord_pics[i][0],billbord_pics[i][1])
    #顯示當前玩家數據
    current_surfaces[0] = billborddisplay.render(f"玩家:{current_player.name}",True,black)
    current_surfaces[1] = billborddisplay.render(f"現金:{current_player.cash}",True,black)
    current_surfaces[2] = billborddisplay.render(f"存款:{current_player.deposit}",True,black)
    current_surfaces[3] = billborddisplay.render(f"不動產:{current_player.realstate()}",True,black)
    for i in range(4):
        screen.blit(current_surfaces[i],(billbord_pics[0][1].topleft[0]+10,billbord_pics[0][1].topleft[1]+5+i*30))
    #顯示排行榜
    for i in range(5):
        if not i:
            screen.blit(ranking_surfaces[i],(billbord_pics[1][1].topleft[0]+120,billbord_pics[1][1].topleft[1]+5+i*30))
        else:
            screen.blit(ranking_surfaces[i],(billbord_pics[1][1].topleft[0]+10,billbord_pics[1][1].topleft[1]+5+i*30))
    #顯示訊息欄
    screen.blit(roadtext_surface,(billbord_pics[2][1].topleft[0]+45,billbord_pics[2][1].topleft[1]+5))
    screen.blit(roadtext2_surface,(billbord_pics[2][1].topleft[0]+45,billbord_pics[2][1].topleft[1]+35))
    #顯示後清空
    #roadtext_surface = billborddisplay.render("",True,black)
    #roadtext2_surface = billborddisplay.render("",True,black) 
    #顯示按鈕
    if show_button == True:
        screen.blit(yes,yesRect)
        screen.blit(no,noRect)
    
    #顯示骰子
    if len(show_dice)>0:
        dice_pics[show_dice[0]][1].topleft = (size[0]-210,size[1]-200)
        screen.blit(dice_pics[show_dice[0]][0],dice_pics[0][1])
    if len(show_dice)>1:
        dice_pics[show_dice[1]][1].topleft = (size[0]-105,size[1]-200)
        screen.blit(dice_pics[show_dice[1]][0],dice_pics[0][1])
        
    #顯示離開
    screen.blit(exit,exitRect)
    #真正刷新
    pygame.display.update()

def check_Yes():
    global yesRect,noRect,clock
    while True:
        display(show_button = True)
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                (x,y) = pygame.mouse.get_pos()
                if x>yesRect.topleft[0] and x<yesRect.topleft[0]+60:
                    if y > yesRect.topleft[1] and y<yesRect.topleft[1]+60:
                        return True
                elif x>noRect.topleft[0] and x<noRect.topleft[0]+60:
                    if y > noRect.topleft[1] and y<noRect.topleft[1]+60:
                        return False
                elif x>0 and x < exit_size[0] and y>0 and y<exit_size[1]:
                    sys.exit()
            elif event.type == QUIT:
                sys.exit()
        clock.tick(15)
                    
def main():
    global background,backgroundRect,exit,exitRect,billbord_pics,yes,yesRect,no,noRect,hospital,hospitalRect,police,policeRect,land_pic,house_pic,road_list,new_road_pic,current_player,player_pics,current_surfaces,ranking_surfaces,roadtext_surface,roadtext2_surface,chance,destiny,round_count
    #pygame.time.delay(1000)
    soundwav=pygame.mixer.Sound("sound2.mp3")
    soundwav.play(-1)
    #圖片來源start
    backgroundpath = "./pictures/background.jpg"
    yespath        = "./pictures/yes.jpg"
    nopath         = "./pictures/no.jpg"
    exitpath       = "./pictures/exit.png"
    policepath     = "./pictures/police.png"
    hospitalpath   = "./pictures/hospital.png"
    billbordpath   = "./pictures/billbord.png"
    roadpaths      = []
    for i in range(4):
        roadpaths.append(f"./pictures/road_{i}.png")
    playerpaths    = []
    for i in range(4):
        playerpaths.append(f"./pictures/player_{i}.png")
    landpaths      = []
    for i in range(5):
        landpaths.append(f"./pictures/land_{i}.png")
    housepaths     = []
    for i in range(5):
        housepaths.append(f"./pictures/house_{i}.png")
    dicepaths      = []
    for i in range(6):
        dicepaths.append(f"./pictures/dice_{i}.png")
    #圖片來源end
    
    #讀檔
    landdatas = readdata(landfilepath)#read data from last edition[x,y,rotate,scaling]
    roaddatas = readdata(roadfilepath)
    
    #圖片引入start
    ##背景
    raw_background = pygame.image.load(backgroundpath)
    background = pygame.transform.scale(raw_background,(size[0]*Magni,size[1]*Magni))#變形
    backgroundRect = background.get_rect()                                           #位置，大小
    backgroundRect = backgroundRect.move(0,0)                                        #移到左上角
    ##地
    land_pic = []
    house_pic = []
    for i in range(5):
        raw_land = pygame.image.load(landpaths[i]) #lands
        landc = pygame.transform.scale(raw_land,(picW,picH))
        land_pic.append(landc)
        raw_house = pygame.image.load(housepaths[i])
        housec = pygame.transform.scale(raw_house,(picW,picH))
        house_pic.append(housec)
    

    ##路
    road_pic = []
    new_road_pic = list()
    for i in range(len(roadpaths)):
        raw_road = pygame.image.load(roadpaths[i])
        road_picc = pygame.transform.scale(raw_road,(picW,picH))
        road_pic.append(road_picc)
        new_road_picc = pygame.transform.scale(road_picc,(round(picW*roaddatas[0][3]),round(picH*roaddatas[0][3])))
        new_road_pic.append(new_road_picc)
    #離開
    raw_exit = pygame.image.load(exitpath)#exits
    exit = pygame.transform.scale(raw_exit,exit_size)
    exitRect = exit.get_rect()
    exitRect.topleft = (0,0)
    #公佈欄
    billbord_pics = []
    
    raw_billbord = pygame.image.load(billbordpath)#billbords
    billbord = pygame.transform.scale(raw_billbord,billbord_size)
    billbordRect = billbord.get_rect()
    billbordRect.topleft = (size[0]-billbord_size[0],0)
    billbord_pics.append([billbord,billbordRect])
    
    raw_billbord = pygame.image.load(billbordpath)#d_billbord1s
    billbord = pygame.transform.scale(raw_billbord,(billbord_size[0],billbord_size[1]+30))
    billbordRect = billbord.get_rect()
    billbordRect.topleft = (billbord_pics[0][1].topleft[0],billbord_size[1])
    billbord_pics.append([billbord,billbordRect])
    
    raw_billbord = pygame.image.load(billbordpath)
    billbord = pygame.transform.scale(raw_billbord,(size[0],80))
    billbordRect = billbord.get_rect()
    billbordRect.topleft = (0,size[1]-80)
    billbord_pics.append([billbord,billbordRect])
    #是
    raw_yes = pygame.image.load(yespath)
    yes = pygame.transform.scale(raw_yes,(60,60))
    yesRect = yes.get_rect()
    yesRect.topleft = (size[0]-150,billbord_pics[2][1].topleft[1]+5)
    #否
    raw_no = pygame.image.load(nopath)
    no = pygame.transform.scale(raw_no,(60,60))
    noRect = no.get_rect()
    noRect.topleft = (size[0]-85,billbord_pics[2][1].topleft[1]+5)
    #骰子
    for i in range(6):
        raw_dice = pygame.image.load(dicepaths[i])
        dice = pygame.transform.scale(raw_dice,(100,100))
        diceRect = dice.get_rect()
        diceRect.topleft = (0,0)
        dice_pics.append([dice,diceRect])
    #玩家圖像
    player_pics = []
    for i in range(4):
        raw_player_pic = pygame.image.load(playerpaths[i])
        player_pic = pygame.transform.scale(raw_player_pic,(150,150))
        player_picRect = player_pic.get_rect()
        player_picRect.topleft = (roaddatas[0][0]-100,roaddatas[0][1]-100)
        player_pics.append([player_pic,player_picRect])
    #醫院
    raw_hospital = pygame.image.load(hospitalpath)
    hospital = pygame.transform.scale(raw_hospital,(round(picW*hospital_data[3]),round(picH*hospital_data[3])))
    hospital = pygame.transform.rotate(hospital,hospital_data[2])
    hospitalRect = hospital.get_rect()
    hospitalRect.topleft = (hospital_data[0]-hospitalRect.width/2,hospital_data[1]-hospitalRect.height/2)
    #監獄
    raw_police = pygame.image.load(policepath)
    police = pygame.transform.scale(raw_police,(round(picW*police_data[3]),round(picH*police_data[3])))
    police = pygame.transform.rotate(police,police_data[2])
    policeRect = police.get_rect()
    policeRect.topleft = (police_data[0]-policeRect.width/2,police_data[1]-policeRect.height/2)
    #圖片引入end
    
    #other variables

    savedroads = []
    
    # road(位置,鄰近位置,機會,命運,土地號碼,銀行)
    # 預設一個機會命運
    #######路、土地、玩家建構
    destiny = road("no_posiiton","no_adj_position",False,True)
    chance = road("no_posiiton","no_adj_position",True,False)
    road_0 = road(0,[1,139],False,False,-1,True)
    road_1 = road(1,[0,2],False,False,-1,True)
    road_2 = road(2,[1,5,50],True,False)
    road_3 = road(3,[6,8,44],False,True)
    road_4 = road(4,[5,6],False,False,1)
    road_5 = road(5,[2,4],False,False,0)
    road_6 = road(6,[3,4],False,False,2)
    road_7 = road(7,[8,10],False,False,4)
    road_8 = road(8,[3,7],False,False,3)
    road_9 = road(9,[10,14,146],False,False,-1,True)
    road_10 = road(10,[7,9],False,False,5)
    road_11 = road(11,[13,17,61])
    road_12 = road(12,[13,14],False,False,7)
    road_13 = road(13,[12,11],False,False,8)
    road_14 = road(14,[9,12],False,False,6)
    road_15 = road(15,[18,56,20])
    road_16 = road(16,[17,18],False,False,9)
    road_17 = road(17,[11,16])
    road_18 = road(18,[16,15],False,False,10)
    road_19 = road(19,[21,23,73])
    road_20 = road(20,[21,15],True,False,-1)
    road_21 = road(21,[20,19],False,False,-1,True)
    road_22 = road(22,[24,80,25],True,False)
    road_23 = road(23,[24,19],False,False,-1,True)
    road_24 = road(24,[23,22],True,False)
    road_25 = road(25,[22,26],False,True)
    road_26 = road(26,[25,34],True,False)
    road_27 = road(27,[31,42])
    road_28 = road(28,[33,32],False,False,61)
    road_29 = road(29,[34,33],False,False,63)
    road_30 = road(30,[31,32],False,False,59)
    road_31 = road(31,[27,30],False,True)
    road_32 = road(32,[20,28],False,False,60)
    road_33 = road(33,[28,29],False,False,62)
    road_34 = road(34,[29,26],False,False,-1,True)
    road_35 = road(35,[47,53,36,43],True,False)
    road_36 = road(36,[37,35],False,True)
    road_37 = road(37,[36,38],True,False)
    road_38 = road(38,[37,39],False,True)
    road_39 = road(39,[40,38],False,False,57)
    road_40 = road(40,[41,39],False,False,58)
    road_41 = road(41,[42,40],True,False)
    road_42 = road(42,[41,27],False,False,-1,True)
    road_43 = road(43,[44,35],True,False)
    road_44 = road(44,[3,43],False,True)
    road_45 = road(45,[48,49],True,False)
    road_46 = road(46,[47,48],False,False,66)
    road_47 = road(47,[46,35])
    road_48 = road(48,[46,45],False,False,50)
    road_49 = road(49,[45,50],False,False,-1,True)
    road_50 = road(50,[49,2],False,True)
    road_51 = road(51,[145,54,57],True,False)
    road_52 = road(52,[54,53],False,False,52)
    road_53 = road(53,[52,35],False,False,51)
    road_54 = road(54,[51,52],False,False,53)
    road_55 = road(55,[57,56],False,False,55)
    road_56 = road(56,[15,55],False,False,56)
    road_57 = road(57,[55,51],False,False,54)
    road_58 = road(58,[131,110,60],False,True)
    road_59 = road(59,[60,61])
    road_60 = road(60,[59,58],True,False)
    road_61 = road(61,[59,11],False,True)
    road_62 = road(62,[99,69,66])
    road_63 = road(63,[64,15],False,False,11)
    road_64 = road(64,[63,65],False,False,12)
    road_65 = road(65,[66,64],False,False,13)
    road_66 = road(66,[62,65],False,False,14)
    road_67 = road(67,[68,70,76],False,False,-1,True)
    road_68 = road(68,[67,69,88])
    road_69 = road(69,[62,68],False,True)
    road_70 = road(70,[67,71],False,False,15)
    road_71 = road(71,[70,72],False,False,16)
    road_72 = road(72,[71,73])
    road_73 = road(73,[19,72],False,False,17)
    road_74 = road(74,[75,77],False,False,-1,True)
    road_75 = road(75,[74,76],False,True)
    road_76 = road(76,[84,75,67])
    road_77 = road(77,[74,78],False,False,20)
    road_78 = road(78,[77,79],False,False,19)
    road_79 = road(79,[78,80],False,False,18)
    road_80 = road(80,[79,22],False,False,21)
    road_81 = road(81,[83,91,147],False,False,31)
    road_82 = road(82,[83,87])
    road_83 = road(83,[82,81],False,True)
    road_84 = road(84,[85,76],False,False,30)
    road_85 = road(85,[84,86],False,False,-1,True)
    road_86 = road(86,[85,87],False,True)
    road_87 = road(87,[86,82],False,False,29)
    road_88 = road(88,[89,68],False,False,22)
    road_89 = road(89,[88,90],False,False,23)
    road_90 = road(90,[91,89],False,False,24)
    road_91 = road(91,[81,90],False,False,25)
    road_92 = road(92,[97,94,147],False,True)
    road_93 = road(93,[94,95],False,False,27)
    road_94 = road(94,[93,92],False,False,28)
    road_95 = road(95,[93,62],False,False,26)
    road_96 = road(96,[105,97])
    road_97 = road(97,[92,96],False,True)
    road_98 = road(98,[102,107,109],True,False)
    road_99 = road(99,[100,62],False,False,-1,True)
    road_100 = road(100,[101,99],False,False,37)
    road_101 = road(101,[102,100],False,False,38)
    road_102 = road(102,[98,101],False,False,39)
    road_103 = road(103,[106,104],False,False,34)
    road_104 = road(104,[105,103],False,False,35)
    road_105 = road(105,[96,104],False,False,36)
    road_106 = road(106,[103,107],False,False,33)
    road_107 = road(107,[106,98],False,False,32)
    road_108 = road(108,[109,110],False,False,64)
    road_109 = road(109,[108,98])
    road_110 = road(110,[108,58],False,False,65)
    road_111 = road(111,[115])
    road_112 = road(112,[113,58])
    road_113 = road(113,[114,112],True,False)
    road_114 = road(114,[115,113],False,False,-1,True)
    road_115 = road(115,[111,114])
    road_116 = road(116,[138,129],False,False,44)
    road_117 = road(117,[121])
    road_118 = road(118,[123,119],False,True)
    road_119 = road(119,[120,118],True,False)
    road_120 = road(120,[121,119],True,False)
    road_121 = road(121,[117,120])
    road_122 = road(122,[123,124],True,False)
    road_123 = road(123,[122,118],False,False,-1,True)
    road_124 = road(124,[122,116],True,False)
    road_125 = road(125,[130,128])
    road_126 = road(126,[131,130],False,False,41)
    road_127 = road(127,[128,129])
    road_128 = road(128,[127,125],True,False)
    road_129 = road(129,[127,116],False,False,43)
    road_130 = road(130,[126,125],False,False,42)
    road_131 = road(131,[126,58],False,False,40)
    road_132 = road(132,[133,144],False,True)
    road_133 = road(133,[132,134],False,False,47)
    road_134 = road(134,[133,135],False,False,46)
    road_135 = road(135,[134,136],False,False,45)
    road_136 = road(136,[135,137])
    road_137 = road(137,[136,138],False,False,-1,True)
    road_138 = road(138,[137,116],True,False)
    road_139 = road(139,[0,140],False,True)
    road_140 = road(140,[139,141],False,True)
    road_141 = road(141,[142,140],True,False)
    road_142 = road(142,[143,141],False,False,-1,True)
    road_143 = road(143,[142,144],False,False,49)
    road_144 = road(144,[143,132],False,False,48)
    road_145 = road(145,[146,51])
    road_146 = road(146,[145,9],True,False)
    road_147 = road(147,[81,92],False,True)

    road_list = [road_0, road_1, road_2, road_3, road_4, road_5, road_6, road_7, road_8, road_9, road_10, road_11, road_12, road_13, road_14, road_15, road_16, road_17, road_18, road_19, road_20, road_21, road_22, road_23, road_24, road_25, road_26, road_27, road_28, road_29, road_30, road_31, road_32, road_33, road_34, road_35, road_36, road_37, road_38, road_39, road_40, road_41, road_42, road_43, road_44, road_45, road_46, road_47, road_48, road_49, road_50, road_51, road_52, road_53, road_54, road_55, road_56, road_57, road_58, road_59, road_60, road_61, road_62, road_63, road_64, road_65, road_66, road_67, road_68, road_69, road_70, road_71, road_72, road_73, road_74, road_75, road_76, road_77, road_78, road_79, road_80, road_81, road_82, road_83, road_84, road_85, road_86, road_87, road_88, road_89, road_90, road_91, road_92, road_93, road_94, road_95, road_96, road_97, road_98, road_99, road_100, road_101, road_102, road_103, road_104, road_105, road_106, road_107, road_108, road_109, road_110, road_111, road_112, road_113, road_114, road_115, road_116, road_117, road_118, road_119, road_120, road_121, road_122, road_123, road_124, road_125, road_126, road_127, road_128, road_129, road_130, road_131, road_132, road_133, road_134, road_135, road_136, road_137, road_138, road_139, road_140, road_141, road_142, road_143, road_144, road_145, road_146, road_147 ]

    
    for i in range(len(road_list)):#add image after rotated and scaled[image,imageRect]
        data = roaddatas[i]
        saved_road = pygame.transform.scale(road_pic[road_list[i].source],(round(picW*data[3]),round(picH*data[3])))
        saved_road = pygame.transform.rotate(saved_road,data[2])
        saved_roadRect = saved_road.get_rect()
        saved_roadRect.topleft = (data[0]-saved_roadRect.width/2,data[1]-saved_roadRect.height/2)
        road_list[i].rect = saved_roadRect

    #地
    for i in range(len(landdatas)):#add image after rotated and scaled[image,imageRect]
        data = landdatas[i]
        landvalue = land_value_data[i]
        l_list = []
        h_list = []
        for j in range(5):
            saved_land = pygame.transform.scale(land_pic[j],(round(picW*data[3]),round(picH*data[3])))
            saved_land = pygame.transform.rotate(saved_land,data[2])
            saved_landRect = saved_land.get_rect()
            saved_landRect.topleft = (data[0]-saved_landRect.width/2,data[1]-saved_landRect.height/2)
            l_list.append(saved_land)
            saved_house = pygame.transform.scale(house_pic[j],(round(picW*data[3]*0.9),round(picH*data[3]*0.9)))
            saved_house = pygame.transform.rotate(saved_house,data[2])
            saved_houseRect = saved_house.get_rect()
            saved_houseRect.topleft = (data[0]-saved_houseRect.width/2,data[1]-saved_houseRect.height/2)
            h_list.append(saved_house)
        solved_lpics.append(l_list)
        solved_hpics.append(h_list)
        Land = land(saved_landRect,landvalue,0,i,0,0,data[3],data[2])
        land_list.append(Land)
    
    #玩家
    for i in range(4):
        if i == 0:
            givename = "園長"
        elif i == 1:
            givename = "正男"
        elif i == 2:
            givename = "野元"
        else:
            givename = "小星"
        play = player(rect = player_pics[i][1],pic = player_pics[i][0],position = 0,cash = 50000,deposit = 10000,name = givename)
        player_list.append(play)
        player_land[player_list[i]] = []
    current_player = player_list[0]
    
    #text hanlding
    current_surfaces = []
    current_surface = billborddisplay.render(f"玩家:{current_player.name}",True,black)
    current_surfaces.append(current_surface)
    current_surface = billborddisplay.render(f"現金:{current_player.cash}",True,black)
    current_surfaces.append(current_surface)
    current_surface = billborddisplay.render(f"存款:{current_player.deposit}",True,black)
    current_surfaces.append(current_surface)
    current_surface = billborddisplay.render(f"不動產:{current_player.realstate()}",True,black)
    current_surfaces.append(current_surface)
    ranking_surfaces = []
    ranking_surface = billborddisplay.render("排行榜",True,black)
    ranking_surfaces.append(ranking_surface)
    ranking_surface = billborddisplay.render(f"1st:{player_list[0].name} {player_list[0].whole_money()}",True,black)
    ranking_surfaces.append(ranking_surface)
    ranking_surface = billborddisplay.render(f"2nd:{player_list[1].name} {player_list[1].whole_money()}",True,black)
    ranking_surfaces.append(ranking_surface)
    ranking_surface = billborddisplay.render(f"3rd:{player_list[2].name} {player_list[2].whole_money()}",True,black)
    ranking_surfaces.append(ranking_surface)
    ranking_surface = billborddisplay.render(f"4th:{player_list[3].name} {player_list[3].whole_money()}",True,black)
    ranking_surfaces.append(ranking_surface)
    roadtext_surface = billborddisplay.render("",True,black)
    roadtext2_surface = billborddisplay.render("",True,black)    

    backgroundRect.move_ip(size[0]/2-road_list[0].rect.topleft[0], size[1]/2-road_list[0].rect.topleft[1])
    #反黑
    screen.fill(black)
    display()

    #排行榜計分
    rank = {}
    for i in player_list :
        rank[i] = i.whole_money()
    
    
    while True: 
        
        for i in range(len(player_list)):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            current_player = player_list[i]
            current_player.dice()
            now_pos = road_list[current_player.position].rect.topleft
            target_pos = road_list[player_list[(i+1)%4].position].rect.topleft
            backgroundRect.move_ip(now_pos[0]-target_pos[0],now_pos[1]-target_pos[1])
            

            for i in player_list:
                rank[i] = i.whole_money()
            dic_value = rank.values()
            value_list = []
            for i in dic_value:
                value_list.append(i)
            value_list.sort()
            value_list = value_list[::-1]
            number = [1,2,3,4]
            for i in range(4):
                for j in rank:
                    if rank[j] == value_list[i] :
                        number[i] = j
                        rank[j] = ""
                        break

            ranking_surfaces = []
            ranking_surface = billborddisplay.render("排行榜",True,black)
            ranking_surfaces.append(ranking_surface)
            ranking_surface = billborddisplay.render(f"1st:{number[0].name} {number[0].whole_money()}",True,black)
            ranking_surfaces.append(ranking_surface)
            ranking_surface = billborddisplay.render(f"2nd:{number[1].name} {number[1].whole_money()}",True,black)
            ranking_surfaces.append(ranking_surface)
            ranking_surface = billborddisplay.render(f"3rd:{number[2].name} {number[2].whole_money()}",True,black)
            ranking_surfaces.append(ranking_surface)
            ranking_surface = billborddisplay.render(f"4th:{number[3].name} {number[3].whole_money()}",True,black)
            ranking_surfaces.append(ranking_surface)

            display()
            clock.tick(15)

        for pla in player_list:
            pla.after_one_round()
        round_count += 1

        
if __name__ == "__main__":
    main()

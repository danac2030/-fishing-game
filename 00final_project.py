import os
import pygame
import random
import math
from concurrent.futures import ThreadPoolExecutor

pygame.init()

screen=pygame.display.set_mode((1440,840))
pygame.display.set_caption("Fishing Game")

executor=ThreadPoolExecutor(max_workers=4)

clock=pygame.time.Clock()

#resetting variables
Status="start"
#time
day=0
timeLeft=0
timePlaceHolder=0
leftoverOrHungry=0
plantRate=0
#population shenanigans
peoplePopulation=0
peopleRate=0
peopleDieRate=0
fishPopulation=0
fishRate=0
fishDieRate=0
plantPopulation=0

#tutorial slides:
tutorials= []
countTut=0
while True:
    try:
        tutorials.append(pygame.transform.scale(pygame.image.load("tuts/tut_"+str(countTut)+".png").convert_alpha(),(1440,840)))
    except FileNotFoundError:
        break
    countTut += 1

#loading backgrounds:
backgrounds= {"bg_start": pygame.transform.scale(pygame.image.load("bgs/bg_start.png"), (1440, 847)),
              "bg_tut": tutorials[0]}

buttons=[
    #START BUTTON
    {"image":pygame.transform.scale(pygame.image.load("button s/button_start.png").convert_alpha(), (340, 160)),
     "rect":None,
     "mask":None,
     "status":"scnr",
     "pos":(550,450),
     "showAt":["start"]
    },
    #TUTORIAL BUTTON
    {"image":pygame.transform.scale(pygame.image.load("button s/button_tutorial.png").convert_alpha(), (100, 100)),
     "rect":None,
     "mask":None,
     "status":"tutorial",
     "pos":(1300,50),
     "showAt":["start","pause","scnr","sandbox"]
    },
    {"image":pygame.transform.scale(pygame.image.load("button s/button_sandbox.png").convert_alpha(), (210, 65)),
     "rect":None,
     "mask":None,
     "status":"sandbox",
     "pos":(616,578),
     "showAt":["scnr"]
    },
    #home go back to start
    #{"image":pygame.transform.scale(pygame.image.load("button s/button_home.png").convert_alpha(), (100, 100)),
     #"rect":None,
     #"mask":None,
    # "status":"start",
     #"pos":(140,50),
     #"showAt":[]
    #},
    #pause
    {"image":pygame.transform.scale(pygame.image.load("button s/button_pause.png").convert_alpha(), (100, 100)),
     "rect":None,
     "mask":None,
     "status":"paused",
     "pos":(1320,50),
     "showAt":["game"]
    },
    {"image":pygame.transform.scale(pygame.image.load("button s/button_restart.png").convert_alpha(), (460, 130)),
     "rect":None,
     "mask":None,
     "status":"next_day",
     "pos":(860,481),
     "showAt":["stats"]
    },
    {"image":pygame.transform.scale(pygame.image.load("button s/button_tryAgain.png").convert_alpha(), (400, 104)),
     "rect":None,
     "mask":None,
     "status":"start",
     "pos":(245,630),
     "showAt":["game_over"]
    },
    {"image":pygame.transform.scale(pygame.image.load("button s/button_end.png").convert_alpha(), (176, 104)),
     "rect":None,
     "mask":None,
     "status":"game_end",
     "pos":(805,640),
     "showAt":["game_over"]
    },
    {"image":pygame.transform.scale(pygame.image.load("button s/button_start.png").convert_alpha(), (340, 160)),
     "rect":None,
     "mask":None,
     "status":"game",
     "pos":(920,620),
     "showAt":["sandbox"]
    }
]

tut_buttons=[
    { #next button for the tutorials
    "image":pygame.transform.scale(pygame.image.load("button s/button_tut_next.png").convert_alpha(), (120, 90)),
    "rect":None,
    "mask":None,
    "change":1,
    "pos":(1050,400),
    "hideAt":[len(tutorials)-1],
    "name":"next"
    },
    { #back button for tutorials
    "image":pygame.transform.scale(pygame.image.load("button s/button_tut_back.png").convert_alpha(), (120, 90)),
    "rect":None,
    "mask":None,
    "change":-1,
    "pos":(250,400),
    "hideAt":[0],
    "name":"back"
    },
    { #exit button for tutorials
    "image":pygame.transform.scale(pygame.image.load("button s/button_tut_exit.png").convert_alpha(), (70, 70)),
    "rect":None,
    "mask":None,
    "change":-1,
    "pos":(1050,200),
    "hideAt":None,
    "name":"exit"
    }
]

scnr_buttons=[
{
    "image":pygame.transform.scale(pygame.image.load("button s/button_scnr_1.png").convert_alpha(), (265, 65)),
    "rect":None,
    "mask":None,
    "pos":(227,500),
    "controls":[120,200,20,1.2,1.5,5,0.95,6,40]
    #fishPopulation, plantPopulation, peoplePopulation, fishRate, plantRate, peopleRate, fishDieRate, peopleDieRate, timePlaceHolder
    },
    {"image":pygame.transform.scale(pygame.image.load("button s/button_scnr_2.png").convert_alpha(), (265, 65)),
    "rect":None,
    "mask":None,
    "pos":(948,500),
    "controls":[120,200,20,1.1,1.3,5,0.9,5,50]
    }
]

game_buttons=[
    { #fish available
    "image":pygame.transform.scale(pygame.image.load("button s/button_game_fish_available.png").convert_alpha(), (260, 130)),
    "rect":None,
    "mask":None,
    "pos":(860,53),
    "name":"fish_available"
    },
    { #fish not available
    "image":pygame.transform.scale(pygame.image.load("button s/button_game_fish_not_available.png").convert_alpha(), (260, 130)),
    "rect":None,
    "mask":None,
    "pos":(860,53),
    "name":"fish_not_available"
    }
]

pause_buttons=[
    { #tutorial
    "image":pygame.transform.scale(pygame.image.load("button s/button_tutorial.png").convert_alpha(), (110, 110)),
    "rect":None,
    "mask":None,
    "pos":(260,570),
    "Status":"tutorial"
    },
    { #fish not available
    "image":pygame.transform.scale(pygame.image.load("button s/button_summary.png").convert_alpha(), (440, 130)),
    "rect":None,
    "mask":None,
    "pos":(540,570),
    "Status":"summary"
    }
]

summary_buttons=[
    { #next button for the tutorials
    "image":pygame.transform.scale(pygame.image.load("button s/button_tut_next.png").convert_alpha(), (120, 90)),
    "rect":None,
    "mask":None,
    "change":1,
    "pos":(1288,400),
    "hideAt":None,
    "name":"next"
    },
    { #back button for tutorials
    "image":pygame.transform.scale(pygame.image.load("button s/button_tut_back.png").convert_alpha(), (120, 90)),
    "rect":None,
    "mask":None,
    "change":-1,
    "pos":(117,400),
    "hideAt":[0],
    "name":"back"
    },
    { #exit button for tutorials
    "image":pygame.transform.scale(pygame.image.load("button s/button_tut_exit.png").convert_alpha(), (70, 70)),
    "rect":None,
    "mask":None,
    "change":-1,
    "pos":(1255,120),
    "hideAt":None,
    "name":"exit"
    }
]

countMet=0
while True:
    try:
        MetArrTemp = {"image": pygame.transform.scale(pygame.image.load("button s/button_game_met_" + str(countMet) + ".png").convert_alpha(), (62, 56)),
                      "rect": None,
                      "mask": None,
                      "pos": (50 + 112 * countMet, 120),
                      "name": "met_" + str(countMet)}
        game_buttons.append(MetArrTemp)
    except FileNotFoundError:
        break
    countMet += 1

for buttonTut in tut_buttons:
    buttonTut["rect"] = buttonTut["image"].get_rect(topleft=buttonTut["pos"])
    buttonTut["mask"] = pygame.mask.from_surface(buttonTut["image"])

for button in buttons:
    button["rect"]=button["image"].get_rect(topleft=button["pos"])
    button["mask"]=pygame.mask.from_surface(button["image"])

for buttonScnr in scnr_buttons:
    buttonScnr["rect"] = buttonScnr["image"].get_rect(topleft=buttonScnr["pos"])
    buttonScnr["mask"] = pygame.mask.from_surface(buttonScnr["image"])

for button in game_buttons:
    button["rect"]=button["image"].get_rect(topleft=button["pos"])
    button["mask"]=pygame.mask.from_surface(button["image"])

for button in pause_buttons:
    button["rect"]=button["image"].get_rect(topleft=button["pos"])
    button["mask"]=pygame.mask.from_surface(button["image"])

for button in summary_buttons:
    button["rect"]=button["image"].get_rect(topleft=button["pos"])
    button["mask"]=pygame.mask.from_surface(button["image"])

#sandbox button
sandbox_input=[{"rect":pygame.Rect(500,185,85,25),
                "control":"fishPopulation"},
                {"rect":pygame.Rect(535,245,85,25),
                "control":"plantPopulation"},
                {"rect":pygame.Rect(555,305,85,25),
                "control":"peoplePopulation"},
                {"rect":pygame.Rect(665,360,85,25),
                "control":"fishRate"},
                {"rect":pygame.Rect(700,425,85,25),
                "control":"plantRate"},
                {"rect":pygame.Rect(720,485,85,25),
                "control":"peopleRate"},
                {"rect":pygame.Rect(495,545,85,25),
                "control":"fishDieRate"},
                {"rect":pygame.Rect(555,605,85,25),
                "control":"peopleDieRate"},
                {"rect":pygame.Rect(575,665,85,25),
                "control":"timeDoingGame"},
               ]

#fishMetData
fishMetData=[
    [1,5,2], #hookAndBait
    [5,15,10], #trawl
    [2,10,10], #gillnets
    [7,17,15], #purseSeine
    #min add, max add, countdown
]

#fish animations
fishAniFrames=[]
layer=0
while True:
    layer_frames=[]
    frame=0
    while True:
        if not os.path.exists(f"fishAniFrames/fish_{layer}{frame}.png"):
            break
        try:
            image_tobeapp=pygame.image.load(f"fishAniFrames/fish_{layer}{frame}.png").convert_alpha()
            layer_frames.append(pygame.transform.scale(image_tobeapp,(image_tobeapp.get_width()*4,image_tobeapp.get_height()*4)))
        except pygame.error:
            break
        frame+=1
    if not layer_frames:
        break
    fishAniFrames.append(layer_frames)
    layer+=1

fishAniData=[]
for c in range(20):
    fishAniData.append({"frames": None,
                        "x": None,
                        "y": None,
                        "count": None,
                        "direction":None})

#bad fish:
badFishMet="123"

#random-ahh variables:
tutorialShow=False
tutorial_image=tutorials[0]
left=40
loading=False
loadStart=0
loadtime=0
summary=False
paused=False
tut_slide_index=0
timePlaceHolder=40
fishPopulation=0
fishAvailable=True
fishAniCooldown=0
fishCaught=0
fishMethod=0
badFishCount=0
fishCooldownTime=0
happiness=50
peopleStarving=0
longData=[]
calculated=False
timeDoingGame=0
konamiCount=0
sandbox_change=None

#pause_button_placement
pause_button_placement={"tutorial":(900,300),"summary":(700,300)}

FishMetAniFrames=[]
layer=0
while True:
    layer_frames=[]
    frame=0
    while True:
        if not os.path.exists(f"fishFrames/fishFrame_{layer}{frame}.png"):
            break
        try:
            layer_frames.append(pygame.transform.scale(pygame.image.load(f"fishFrames/fishFrame_{layer}{frame}.png").convert_alpha(),(1440,840)))
        except pygame.error:
            break
        frame+=1
    if not layer_frames:
        break
    FishMetAniFrames.append(layer_frames)
    layer+=1

current_animation=None
animation_state=None
animation_timer=0
def fishAnimation(fishMethod):
    global current_animation, animation_state, animation_timer
    if fishMethod<len(FishMetAniFrames) and FishMetAniFrames[fishMethod]:
        current_animation=(fishMethod,0)
        animation_state="forward"
        animation_timer=pygame.time.get_ticks()

#cooldown stuff
fish_cooldown_end=0
lastSecond=pygame.time.get_ticks()


#game loop
Running=True
while Running:
    currentTime=pygame.time.get_ticks()
    screen.blit(pygame.transform.scale(pygame.image.load("bg_normal.png").convert_alpha(),(1440,840)),(0,0))
    #start menu
    if Status == "start": #start blit bookmark
        screen.blit(backgrounds["bg_start"], (0, 0))
# pick the scenario/sandbox
    elif Status == "scnr": #scnr blit bookmark
        background_image = pygame.transform.scale(pygame.image.load("bgs/bg_scnr.png"), (1440, 900))
        screen.blit(background_image, (0, 0))
        for button in scnr_buttons:
            screen.blit(button["image"], button["pos"])
# main game
    elif Status == "game": #game blit bookmark
        #draw background
        screen.blit(pygame.transform.scale(pygame.image.load("bgs/bg_game.png"),(1440,840)),(0,0))
        #fish button draw
        fish_button=game_buttons[0] if fishAvailable else game_buttons[1]
        screen.blit(fish_button["image"],fish_button["pos"])
        #draw the fish population
        for b in range(len(str(fishPopulation))): #count the digits in fish population
            screen.blit(pygame.transform.scale(pygame.image.load(f"nums/num_{str(fishPopulation)[b]}.png"),(40,50)),(160+50*b,30))
        if left>0 and not paused:
            if currentTime-lastSecond>=1000:
                left-=1
                lastSecond=currentTime
        elif left<=0:
            Status="stats"
            loading=True
        for button in game_buttons:
            if "met_" in button["name"]:
                screen.blit(button["image"],button["pos"])
        #draw the time left
        for d in range(len(str(left))):
            screen.blit(pygame.transform.scale(pygame.image.load(f"nums/num_{str(left)[d]}.png"),(40,50)),(670+50*d,30))
        #draw fish caught
        for e in range(len(str(fishCaught))): #count the digits in fish population
            screen.blit(pygame.transform.scale(pygame.image.load(f"nums/num_{str(fishCaught)[e]}.png"),(40,50)),(400+50*e,30))
        #fish animation
        fishAniCooldown += 1
        for fish in fishAniData:
            if fish["frames"] is None and fishAniCooldown>=fishCooldownTime:
                fishNum=random.randint(0,len(fishAniFrames)-1)
                fish["frames"]=fishAniFrames[fishNum]
                fish["direction"]=random.randint(0,1)
                fish["y"] = random.randint(450,700)
                fish["count"]=0
                fishAniCooldown=0
                fishCooldownTime=random.randint(30,50)
                fish["x"]=1640 if fish["direction"]==1 else -200
            if fish["frames"] is not None: # move fish
                if fish["direction"]==1:
                    screen.blit(pygame.transform.flip(fish["frames"][int(fish["count"]//6)%len(fish["frames"])],True,False),(fish["x"],fish["y"]))
                    fish["x"]-=5
                else:
                    screen.blit(fish["frames"][int(fish["count"] // 6) % len(fish["frames"])], (fish["x"], fish["y"]))
                    fish["x"] += 5
                fish["count"] += 1
                if fish["x"]>1840 or fish["x"]<-400: #delete fish
                    fish["frames"]=None
                    fish["x"]=None
                    fish["y"]=None
                    fish["count"]=None

        #fish button availability
        if not fishAvailable and currentTime>=fish_cooldown_end:
            fishAvailable =True
#sandbox
    elif Status == "sandbox": #sandbox blit bookmark
        screen.blit(pygame.transform.scale(pygame.image.load("bgs/bg_sandbox.png"), (1440, 847)), (0, 0))
        for fPs in range(len(str(fishPopulation))):
            screen.blit(pygame.transform.scale(pygame.image.load(f"nums/num_{str(fishPopulation)[fPs]}.png"),(20,25)),(500+25*fPs,185))
        for plPs in range(len(str(plantPopulation))):
            screen.blit(pygame.transform.scale(pygame.image.load(f"nums/num_{str(plantPopulation)[plPs]}.png"),(20,25)),(535+25*plPs,245))
        for pPs in range(len(str(peoplePopulation))):
            screen.blit(pygame.transform.scale(pygame.image.load(f"nums/num_{str(peoplePopulation)[pPs]}.png"),(20,25)),(555+25*pPs,305))
        for fRs in range(len(str(fishRate))):
            screen.blit(pygame.transform.scale(pygame.image.load(f"nums/num_{str(fishRate)[fRs]}.png"),(20,25)),(665+25*fRs,360))
        for plRs in range(len(str(plantRate))):
            screen.blit(pygame.transform.scale(pygame.image.load(f"nums/num_{str(plantRate)[plRs]}.png"),(20,25)),(700+25*plRs,425))
        for pRs in range(len(str(peopleRate))):
            screen.blit(pygame.transform.scale(pygame.image.load(f"nums/num_{str(peopleRate)[pRs]}.png"),(20,25)),(720+25*pRs,485))
        for fDs in range(len(str(fishDieRate))):
            screen.blit(pygame.transform.scale(pygame.image.load(f"nums/num_{str(fishDieRate)[fDs]}.png"),(20,25)),(495+25*fDs,545))
        for pDs in range(len(str(peopleDieRate))):
            screen.blit(pygame.transform.scale(pygame.image.load(f"nums/num_{str(peopleDieRate)[pDs]}.png"),(20,25)),(555+25*pDs,605))
        for tDGs in range(len(str(timeDoingGame))):
            screen.blit(pygame.transform.scale(pygame.image.load(f"nums/num_{str(timeDoingGame)[tDGs]}.png"),(20,25)),(575+25*tDGs,665))
# stats
    elif Status=="stats": #stats blit bookmark
        screen.blit(pygame.transform.scale(pygame.image.load("bgs/bg_stats.png"),(1440,840)),(0,0))
        if not calculated:
            if day % peopleRate==0: #if day is divisible by people rate ->> multiplying reproduction people
                peoplePopulation+=random.randint(1,2)
            if day % peopleDieRate==0:
                peoplePopulation-=random.randint(0,2)
            fishPopulation=math.floor(fishPopulation*fishRate*fishDieRate)
            fishCaught=math.floor(fishCaught*(random.randint(95,100)/100)) #random chance to account for fish dying, being sick, getting lost etc.
            plantPopulation -= fishPopulation #reduce plant population by the fish population
            plantPopulation=math.floor(plantPopulation*plantRate) #allow the plants to reproduce
            if fishCaught<peoplePopulation: #is there enough food for everyone?
                #nope, not enough food :(
                if leftoverOrHungry>=0: #leftoverOrHungry positive (there's leftovers!
                    leftoverOrHungry-=peoplePopulation-fishCaught #adjust leftover or hungry with leftovers added
                    if leftoverOrHungry<=0: #if people still go hungry even with leftovers
                        peopleFed=peoplePopulation+leftoverOrHungry #it's a plus bc lOH is negative (+- = -)
                    else: #if everyone can eat with the leftovers
                        peopleFed=peoplePopulation #everyone ate
                        leftoverOrHungry=0 #leftovers go rotten
                else: #no leftovers :(
                    peopleFed = fishCaught #only people who are fed are the fish that are caught (no leftovers needed to be counted)
                happiness+=fishCaught*3 #+3 happiness for all the fish caught

            else: # there's enough food for everyone!
                leftoverOrHungry=fishCaught-peoplePopulation #if there's enough fish, the leftovers become... leftovers. the rest are rotten
                peopleFed=peoplePopulation #everyone is fed
            if leftoverOrHungry<0: #if people are hungry after all hungry or not calculations
                peoplePopulation -= peopleStarving  # people died after starving for 3 days
                happiness -= peopleStarving * 20  # people die so people are sad
                leftoverOrHungry += peopleStarving  # if ur dead you can't be hungry...
            happiness+=leftoverOrHungry*3 #if you have leftovers, ppl are happy cause security. if you have hungry ppl, ppl are sad cause starving
            happiness+=peopleFed*5 #feeding ppl makes them happy!
            happiness+=badFishCount*-3

            if day>=3: #check for people starving
                if longData[day-2]["leftoverOrHungry"]<=0 and longData[day-1]["leftoverOrHungry"]<=0 and leftoverOrHungry<=0:
                    peopleStarving=max(longData[day-2]["leftoverOrHungry"],longData[day-1]["leftoverOrHungry"],leftoverOrHungry<=0)
            tempData={"peoplePopulation":peoplePopulation,
                      "peopleFed":peopleFed,
                      "happiness":happiness,
                      "leftoverOrHungry":leftoverOrHungry,
                      "fishPopulation":fishPopulation,
                      "plantPopulation":plantPopulation,
                      "fishCaught":fishCaught,
                      "peopleDied":peopleStarving}
            longData.append(tempData)
            print(longData)
            day += 1
            # display the data
        #(230, 90), (160,110), (155,130), (165,160), (245,180), (210,205), (175,230), (222,254)
            calculated=True
        for pP in range(len(str(peoplePopulation))):
            screen.blit(
                pygame.transform.scale(pygame.image.load(f"nums/num_{str(peoplePopulation)[pP]}.png"), (28, 35)),
                (575 + 50 * pP, 212))
        for pF in range(len(str(peopleFed))):
            screen.blit(pygame.transform.scale(pygame.image.load(f"nums/num_{str(peopleFed)[pF]}.png"), (28, 35)),
                        (400 + 50 * pF, 271))
        for hA in range(len(str(happiness))):
            screen.blit(pygame.transform.scale(pygame.image.load(f"nums/num_{str(happiness)[hA]}.png"), (28, 35)),
                        (385 + 50 * hA, 334))
        if peoplePopulation == peopleFed: #people fed (if there are more people fed than people
            for lO in range(len(str(fishCaught-peopleFed))):  # count the leftovers
                screen.blit(
                    pygame.transform.scale(pygame.image.load(f"nums/num_{str(fishCaught-peopleFed)[lO]}.png"), (28, 35)), #leftovers
                    (410 + 50 * lO, 393))
            screen.blit(pygame.transform.scale(pygame.image.load("nums/num_0.png"), (28, 35)), (610, 454)) #hungry
        else: #people going hungry
            screen.blit(pygame.transform.scale(pygame.image.load("nums/num_0.png"), (28, 35)), (410, 393)) #leftovers
            for hU in range(len(str(peoplePopulation-peopleFed))):  # count hungry people
                screen.blit(
                    pygame.transform.scale(pygame.image.load(f"nums/num_{str(peoplePopulation-peopleFed)[hU]}.png"), (28, 35)),
                    (610 + 50 * hU, 454))
        for fP in range(len(str(fishPopulation))):
            screen.blit(pygame.transform.scale(pygame.image.load(f"nums/num_{str(fishPopulation)[fP]}.png"), (28, 35)),
                        (525 + 50 * fP, 516))
        for fC in range(len(str(fishCaught))):
            screen.blit(pygame.transform.scale(pygame.image.load(f"nums/num_{str(fishCaught)[fC]}.png"), (28, 35)),
                        (420 + 50 * fC, 574))
        for plP in range(len(str(plantPopulation))):
            screen.blit(
                pygame.transform.scale(pygame.image.load(f"nums/num_{str(plantPopulation)[plP]}.png"), (28, 35)),
                (575 + 50 * plP, 632))

        #screen.blit stuff
    elif Status == "next_day" and not loading:
        if peoplePopulation<=0:
            Status="game_over"
            reason="people_starved"
        elif happiness<=0:
            Status="game_over"
            reason="depressed"
        elif fishPopulation<=0:
            Status="game_over"
            reason="fish_starved"
        elif plantPopulation<0:
            Status="game_over"
            reason="plant_starved"
        else:
            left = timeDoingGame
            calculated = False
            fishCaught = 0
            fishMethod = 0
            badFishCount = 0
            fishAniCooldown = 1000
            fishCooldownTime = random.randint(30, 50)
            fishAvailable = True
            Status = "game"
    elif Status=="game_over":
        screen.blit(pygame.transform.scale(pygame.image.load(f"game_over/game_over_{reason}.png"),(1440,840)),(0,0))
    elif Status=="game_end":
        Running=False
    if paused: #pause blit bookmark
        screen.blit(pygame.transform.scale(pygame.image.load("paused.png").convert_alpha(), (1440, 847)),(0,0))
        for button in pause_buttons:
            screen.blit(button["image"],button["pos"])
    if summary: # summary blit bookmark
        screen.blit(pygame.transform.scale(pygame.image.load("bgs/bg_summary.png"),(1440,847)),(0,0))
        summary_slide_num=len(longData)//6+1
        #blit the buttons
        for button in summary_buttons:
            if button["hideAt"] is None or summary_slide_index not in button["hideAt"]:
                if button["name"]=="next" and summary_slide_index==summary_slide_num-1:
                    pass
                    print("hi")
                else:
                    screen.blit(button["image"], button["pos"])
        end_day=min(summary_slide_index*6+6,len(longData))

        #blit the numbers
        for f in range(summary_slide_index*6,end_day): # run through every day
            for day in range(len(str(f+1))):
                screen.blit(
                    pygame.transform.scale(
                        pygame.image.load(f"nums/num_{str(f+1)[day]}.png"), (28, 35)),
                    (195 + 30 * day, 230 + 60 * f))
            for pP in range(len(str(longData[f]['peoplePopulation']))):
                screen.blit(
                    pygame.transform.scale(pygame.image.load(f"nums/num_{str(longData[f]['peoplePopulation'])[pP]}.png"), (28, 35)),
                    (295 + 30 * pP, 230+60*f))
            for pF in range(len(str(longData[f]['peopleFed']))):
                screen.blit(pygame.transform.scale(pygame.image.load(f"nums/num_{str(longData[f]['peopleFed'])[pF]}.png"), (28, 35)),
                            (390 + 30 * pF, 230+60*f))
            for hA in range(len(str(longData[f]['happiness']))):
                screen.blit(pygame.transform.scale(pygame.image.load(f"nums/num_{str(longData[f]['happiness'])[hA]}.png"), (28, 35)),
                            (505 + 30 * hA, 230+60*f))
            if longData[f]['peoplePopulation'] == longData[f]['peoplePopulation']:  # people fed (if there are more people fed than people
                for lO in range(len(str(longData[f]['fishCaught'] - longData[f]['peopleFed']))):  # count the leftovers
                    screen.blit(
                        pygame.transform.scale(pygame.image.load(f"nums/num_{str(longData[f]['fishCaught'] - longData[f]['peopleFed'])[lO]}.png"),
                                               (28, 35)),  # leftovers
                        (600 + 30 * lO, 230+60*f))
                screen.blit(pygame.transform.scale(pygame.image.load("nums/num_0.png"), (28, 35)), (700, 230+60*f))  # hungry
            else:  # people going hungry
                screen.blit(pygame.transform.scale(pygame.image.load("nums/num_0.png"), (28, 35)),
                            (600, 230+60*f))  # leftovers
                for hU in range(len(str(longData[f]['peoplePopulation'] - longData[f]['peopleFed']))):  # count hungry people
                    screen.blit(
                        pygame.transform.scale(
                            pygame.image.load(f"nums/num_{str(longData[f]['peoplePopulation'] - longData[f]['peopleFed'])[hU]}.png"), (28, 35)),
                        (700 + 30 * hU, 230+60*f))
            for fP in range(len(str(longData[f]['fishPopulation']))):
                screen.blit(
                    pygame.transform.scale(pygame.image.load(f"nums/num_{str(longData[f]['fishPopulation'])[fP]}.png"), (28, 35)),
                    (835 + 30 * fP, 230+60*f))
            for fC in range(len(str(longData[f]['fishCaught']))):
                screen.blit(pygame.transform.scale(pygame.image.load(f"nums/num_{str(longData[f]['fishCaught'])[fC]}.png"), (28, 35)),
                            (1000 + 30 * fC, 230+60*f))
            for plP in range(len(str(longData[f]['plantPopulation']))):
                screen.blit(
                    pygame.transform.scale(pygame.image.load(f"nums/num_{str(longData[f]['plantPopulation'])[plP]}.png"), (28, 35)),
                    (1110 + 30 * plP, 230+60*f))

    # tutorials
    if tutorialShow:
        for button_rep in buttons:
            if Status in button_rep["showAt"]:
                screen.blit(button_rep["image"], button_rep["pos"])
        screen.blit(tutorial_image, (0, 0))
        for button in tut_buttons:
            if button["hideAt"] is None or tut_slide_index not in button["hideAt"]:
                screen.blit(button["image"], button["pos"])
    #other buttons
    if not tutorialShow:
        for button in buttons:
            if Status in button["showAt"]:
                screen.blit(button["image"], button["pos"])
            if "paused" in button["showAt"] and paused:
                screen.blit(button["image"], pause_button_placement[button["status"]])

    if current_animation is not None:
        method,frame=current_animation
        total_frames=len(FishMetAniFrames[method])
        if animation_state == "forward":
            screen.blit(FishMetAniFrames[method][frame],(0,0))
            if frame+1<total_frames:
                current_animation=(method,frame+1)
            else: #last frame
                animation_state="wait"
                animation_timer=currentTime

        elif animation_state=="wait":
            screen.blit(FishMetAniFrames[method][-1],(0,0))
            if currentTime-animation_timer>=800:
                animation_state="backwards"
                current_animation=(method,total_frames-2) #start from second last

        elif animation_state=="backwards":
            screen.blit(FishMetAniFrames[method][frame],(0,0))
            if frame>0:
                current_animation=(method,frame-1)
            else:
                current_animation=None
                animation_state=None
                animation_timer=0

        else:
            current_animation=None

    # loading
    if loading: #loading blit bookmark
        screen.blit(loadingScreen, (0, 0))
        if (pygame.time.get_ticks()-loadStart >= loadtime):
            loading = False
            lastSecond=currentTime
            if Status == "game":
                left=timeDoingGame
                calculated=False
                fishCaught = 0
                fishMethod = 0
                badFishCount = 0
                fishAniCooldown=1000
                fishCooldownTime=random.randint(30,50)
                fishAvailable = True
                print("game started")
            elif Status == "stats":
                calculated=False
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #quit pygame
            Running = False
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # event.pos ->> mouse position at time that event happens
            if Status=="scnr": #scnr buttons bookmark
                for button in scnr_buttons:
                    if (button["rect"].collidepoint(mouse_pos)  # if one of the scenario buttons is clicked
                            and button["mask"].get_at((mouse_pos[0] - button["rect"].x,
                                                       mouse_pos[1] - button["rect"].y))):
                        # set the controls to scenario
                        fishPopulation = button["controls"][0]
                        plantPopulation = button["controls"][1]
                        peoplePopulation = button["controls"][2]
                        fishRate = button["controls"][3]
                        plantRate = button["controls"][4]
                        peopleRate = button["controls"][5]
                        fishDieRate = button["controls"][6]
                        peopleDieRate = button["controls"][7]
                        timeDoingGame = button["controls"][8]
                        Status = "game"
                        loading = True
                        loadingScreen=pygame.transform.scale(pygame.image.load(f"loading/loading_screen{random.randint(0,10)}.png"),(1440,840))
                        loadStart = pygame.time.get_ticks()
                        loadtime = random.randint(2000, 5000)
            elif Status=="game": #game buttons bookmark
                for button in game_buttons:
                    if not paused:
                        if (button["rect"].collidepoint(mouse_pos) and
                                button["mask"].get_at((mouse_pos[0] - button["rect"].x,
                                                       mouse_pos[1] - button["rect"].y))):
                            if button["name"] == "fish_available" and fishAvailable and fishPopulation>0:
                                fishCaughtTemp = random.randint(fishMetData[fishMethod][0], fishMetData[fishMethod][1])
                                fishPopulation -= fishCaughtTemp
                                fishCaught += fishCaughtTemp
                                if str(fishMethod) in badFishMet:
                                    badFishCount += 1
                                #fish availability
                                fish_cooldown_end=currentTime+fishMetData[fishMethod][2]*1000
                                fishAvailable=False
                                fishAnimation(fishMethod)
                            elif "met_" in button["name"]:
                                fishMethod = int(button["name"][4])
            elif Status=="sandbox": #sandbox buttons bookmark
                for button in sandbox_input:
                    if button["rect"].collidepoint(mouse_pos):
                        print("yay")
                        sandbox_change=button["control"]
                        if button["control"]=="fishPopulation":
                            fishPopulation=0
                        elif button["control"]=="plantPopulation":
                            plantPopulation=0
                        elif button["control"]=="peoplePopulation":
                            peoplePopulation=0
                        elif button["control"]=="fishRate":
                            fishRate=0
                        elif button["control"]=="plantRate":
                            plantRate=0
                        elif button["control"]=="peopleRate":
                            peopleRate=0
                        elif button["control"]=="fishDieRate":
                            fishDieRate=0
                        elif button["control"]=="peopleDieRate":
                            peopleDieRate=0
                        elif button["control"]=="timeDoingGame":
                            timeDoingGame=0

                        break
            if paused and not tutorialShow: # paused buttons bookmark
                for button in pause_buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        if button["mask"].get_at((mouse_pos[0] - button["rect"].x, mouse_pos[1] - button["rect"].y)):
                            if button["Status"]=="tutorial":
                                tutorialShow = True
                            if button["Status"]=="summary":
                                summary = True
                                summary_slide_index=0
            if tutorialShow: # tutorial buttons bookmark
                for button in tut_buttons:
                    if button["hideAt"] is None or tut_slide_index not in button["hideAt"]:
                        if (button["rect"].collidepoint(mouse_pos)  # if button is clicked
                                and button["mask"].get_at((mouse_pos[0] - button["rect"].x,
                                                           mouse_pos[1] - button["rect"].y))):
                            if button["name"] == "exit":
                                tutorialShow = False
                                tut_slide_index=0
                                tutorial_image = tutorials[0]
                            else:
                                tut_slide_index+=button["change"]
                                tutorial_image = tutorials[tut_slide_index]
            if summary: #summary buttons bookmark
                for button in summary_buttons:
                    if button["hideAt"] is None or summary_slide_index not in button["hideAt"]:
                        if button["name"] == ["next"] and summary_slide_index == summary_slide_num - 1:
                            pass
                        else:
                            if (button["rect"].collidepoint(mouse_pos)  # if button is clicked
                                    and button["mask"].get_at((mouse_pos[0] - button["rect"].x,
                                                               mouse_pos[1] - button["rect"].y))):
                                if button["name"]=="exit":
                                    summary=False
                                    summary_slide_index=0
                                else:
                                    summary_slide_index+=button["change"]
            if not tutorialShow:  # check all the other buttons!!!!! #other buttons bookmark
                for button in buttons:  # run through all the dictionaries in list buttons
                    if Status in button["showAt"]:
                        if button["rect"].collidepoint(mouse_pos):  # if mouse is in the rectangle
                            if button["mask"].get_at((mouse_pos[0] - button["rect"].x, mouse_pos[1] - button[
                                "rect"].y)):  # if mouse is on an opaque pixel
                                if button["status"] == "tutorial":
                                    tutorialShow = True
                                elif button["status"] == "paused" and not tutorialShow and not summary:
                                    paused = not paused
                                else:
                                    Status = button["status"]  # change status
                                    print(Status)
                                    loading = True
                                    loadingScreen = pygame.transform.scale(
                                    pygame.image.load(f"loading/loading_screen{random.randint(0, 10)}.png"), (1440, 840))
                                    loadStart = pygame.time.get_ticks()
                                    loadtime = random.randint(2000, 5000)
                                if button["showAt"]=="sandbox":
                                    sandbox_change=None

        elif event.type==pygame.KEYDOWN:
            if Status=="sandbox":
                if event.key==pygame.K_RETURN:
                    sandbox_change=None
                elif event.unicode.isdigit():
                    if "." in str(fishRate):
                        if sandbox_change=="fishPopulation":
                            fishPopulation=fishPopulation*10+int(event.unicode)
                        elif sandbox_change=="plantPopulation":
                            plantPopulation=plantPopulation*10+int(event.unicode)
                        elif sandbox_change=="peoplePopulation":
                            peoplePopulation=peoplePopulation*10+int(event.unicode)
                        elif sandbox_change=="fishRate":
                            fishRate=fishRate*10+int(event.unicode)
                        elif sandbox_change=="plantRate":
                            plantRate=plantRate*10+int(event.unicode)
                        elif sandbox_change=="peopleRate":
                            peopleRate=peopleRate*10+int(event.unicode)
                        elif sandbox_change=="fishDieRate":
                            fishDieRate=fishDieRate*10+int(event.unicode)
                        elif sandbox_change=="peopleDieRate":
                            peopleDieRate=peopleDieRate*10+int(event.unicode)
                        elif sandbox_change=="timeDoingGame":
                            timeDoingGame=timeDoingGame*10+int(event.unicode)
                    else:
                        if sandbox_change=="fishPopulation":
                            fishPopulation=fishPopulation*10+int(event.unicode)
                        elif sandbox_change=="plantPopulation":
                            plantPopulation=plantPopulation*10+int(event.unicode)
                        elif sandbox_change=="peoplePopulation":
                            peoplePopulation=peoplePopulation*10+int(event.unicode)
                        elif sandbox_change=="fishRate":
                            fishRate=fishRate*10+int(event.unicode)
                        elif sandbox_change=="plantRate":
                            plantRate=plantRate*10+int(event.unicode)
                        elif sandbox_change=="peopleRate":
                            peopleRate=peopleRate*10+int(event.unicode)
                        elif sandbox_change=="fishDieRate":
                            fishDieRate=fishDieRate*10+int(event.unicode)
                        elif sandbox_change=="peopleDieRate":
                            peopleDieRate=peopleDieRate*10+int(event.unicode)
                        elif sandbox_change=="timeDoingGame":
                            timeDoingGame=timeDoingGame*10+int(event.unicode)
                elif event.key==pygame.K_PERIOD:
                    if sandbox_change=="fishRate" and "." not in str(fishRate):
                        fishRate=float(fishRate)
                    elif sandbox_change=="plantRate" and "." not in str(plantRate):
                        plantRate=float(plantRate)
                    elif sandbox_change=="fishDieRate" and "." not in str(fishDieRate):
                        fishDieRate=float(fishDieRate)
                    elif sandbox_change=="peopleDieRate" and "." not in str(peopleDieRate):
                        peopleDieRate=float(peopleDieRate)
                    elif sandbox_change=="timeDoingGame" and "." not in str(timeDoingGame):
                        timeDoingGame=float(timeDoingGame)
            else:
                if event.key==pygame.K_UP and (konamiCount==0 or konamiCount==1):
                    konamiCount+=1
                    print(konamiCount)
                elif event.key==pygame.K_DOWN and (konamiCount==2 or konamiCount==3):
                    konamiCount+=1
                    print(konamiCount)
                elif event.key==pygame.K_LEFT and (konamiCount==4 or konamiCount==6):
                    konamiCount+=1
                    print(konamiCount)
                elif event.key==pygame.K_RIGHT and (konamiCount==5 or konamiCount==7):
                    konamiCount+=1
                    print(konamiCount)
                elif event.key==pygame.K_b and konamiCount==8:
                    konamiCount+=1
                    print(konamiCount)
                elif event.key==pygame.K_a and konamiCount==9:
                    konamiCount+=1
                    print(konamiCount)
                else:
                    konamiCount=0
    if konamiCount==10:
        print("konami...")
        running=False
        break
    pygame.display.flip()
    clock.tick(60)

runningKonami=True
while runningKonami and konamiCount==10:
    screen.blit(pygame.transform.scale(pygame.image.load("konami.png"),(1440,840)),(0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            runningKonami=False
    pygame.display.flip()
pygame.quit()
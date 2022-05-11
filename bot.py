import discord 
from ludo import Ddraw, Ludo, Player
import random as r
import configparser
import os

token = os.environ["token"]

client = discord.Client()

######################
# Reading commands from config
######################
cfg = configparser.ConfigParser()
cfg.read("config")
nirdesh = cfg["commands"]

L = ""
waitinForReaction=False

def emb(L,optionalText="", fTitle=""):
    myEmbed = discord.Embed(title="LUDO", description="", color=0xf1c40f)
    myEmbed.set_author(name="TheWhistler")
    if optionalText!="" and fTitle!="":
        myEmbed.add_field(name=fTitle, value=optionalText, inline=True)
    Ddraw(L)
    ffile = discord.File("1.png", filename="1.png")

    myEmbed.set_image(url="attachment://1.png")
    return myEmbed, ffile

def finalEmb(L):
    myEmbed = discord.Embed(title="LUDO", description="", color=0xf1c40f)
    myEmbed.set_author(name="TheWhistler")
    j=0
    poss = ["1st", "2nd", "3rd", "4th"]
    for i in L.winners:
        myEmbed.add_field(name=poss[j], value=f"<@{i.id}>", inline=False)
        j+=1
    return myEmbed

async def takeReaction(q, num, tl):
    global waitinForReaction
    waitinForReaction=True
    if tl[0]==1:
        await q.add_reaction("1️⃣")
    if tl[1]==1:
        await q.add_reaction("2️⃣")
    if tl[2]==1:
        await q.add_reaction("3️⃣")
    if tl[3]==1:
        await q.add_reaction("4️⃣")


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global L,waitinForReaction,nirdesh
    if message.author == client.user:
        return
    if message.content[0]!=nirdesh["prefix"]:
        return
    else:
        message.content = message.content[1:]
    message.content = message.content.lower()
    
    if message.content==nirdesh["help"]:
        n = nirdesh
        text = f"""
Create game: {n["createGame"]}
Enter game : {n["enterGame"]}
Start game : {n["startGame"]}

Roll Dice  : {n["rollDice"]}
End game  : {n["endGame"]}

                        Author: TheWhistler#5514
        """
        await message.reply(text)
        del n
    if message.content==nirdesh["endGame"]:
        L = ""

    if waitinForReaction==False:
        if message.content==(nirdesh["createGame"]):
            #await message.channel.send('Hello!')
            if type(L)!=Ludo:
                L = Ludo()
                await message.channel.send("A game has been created. Enter by typing -me")
            else:
                await message.channel.send("A Ludo game already exists.")
        elif message.content==(nirdesh["startGame"]):
            L.start()
            t = "<@{}> "
            mention = ""
            for pp in L.players:
                mention+=t.format(pp.id)
            p = await message.channel.send(f"The game has now begun! "+mention)
        elif message.content==(nirdesh["enterGame"]):
            #e,f = emb(L)
            #q = await message.channel.send(file=f,embed=e)
            #await q.add_reaction("😀")
            if L.started==False:
                p = await message.channel.send(f"Added <@{message.author.id}>")
                L.addPlayer(Player(message.author.id))
            else:
                p = await message.channel.send(f"The game has already started. Thora jaldi aana tha... <@{message.author.id}>")
        elif message.content==(nirdesh["rollDice"]):
            if len(L.players)==0:
                e = finalEmb(L)
                q = await message.channel.send(embed=e)
                L = ""
                return
            try:
                num = int(L.rollDice(message.author.id)) # Rolled
            except:
                await message.channel.send(f"It isn't your turn. <@{message.author.id}>")
            #num = int(input("> "))
            L.num = num # stored roll number into the ludo object
            player = L.players[L.turn] # Extracted the player object of whom the turn is
            gotis = player.gotis # Extracted the gotis of that player

            noOfGotisOut, gotisOut = player.countOut(L.num) # Extracted info about gotis
            # gotisOut = [0,1,0,1] ; example format
            # noOfGotisOut = int


            e,f = emb(L,optionalText=f"<@{L.players[L.turn].id}>.\n The die rolls and the number is {L.num}", fTitle="Turn:")
            q = await message.channel.send(file=f,embed=e)
            L.message = q

            if noOfGotisOut==0:
                if num!=6:
                    L.nextTurn()
                    e,f = emb(L,optionalText=f"<@{L.players[L.turn].id}>.", fTitle="Next turn:")
                    q = await message.channel.send(file=f,embed=e)
                    L.message = q
                elif num==6:
                    r.choice(gotis).takeOut()
                    e,f = emb(L,optionalText=f"<@{L.players[L.turn].id}>.", fTitle="Turn continues of ")
                    q = await message.channel.send(file=f,embed=e)
                    L.message = q
            elif noOfGotisOut>0:
                if noOfGotisOut==1:
                    if num == 6:
                        await takeReaction(q, num, gotisOut)
                    else:
                        ####################################
                        # Check will come if can move ahead#
                        ####################################
                        goti = gotis[gotisOut.index(1)]
                        if L.num>(56-goti.currentPlace):
                            q = await message.channel.send("No choice available")
                            L.nextTurn()
                            return


                        ####################################
                        toContinue = gotis[gotisOut.index(1)].move(num, L)
                        if toContinue:
                            L.nextTurn()
                            e,f = emb(L,optionalText=f"<@{L.players[L.turn].id}>.", fTitle="Next turn:")
                            q = await message.channel.send(file=f,embed=e)
                            L.message = q
                        else:
                            if len(L.players)==0:
                                e = finalEmb(L)
                                q = await message.channel.send(embed=e)
                                L = ""
                                return
                elif noOfGotisOut>1:
                    await takeReaction(q, num, gotisOut)
            if len(L.players)==0:
                e = finalEmb(L)
                q = await message.channel.send(embed=e)
                L = ""
                return

@client.event
async def on_reaction_add(reaction, user):
    global waitinForReaction
    if user == client.user:
        return

    def takeGotiNumber():
        #await reaction.message.channel.send(f"{user} reacted with {reaction.emoji}")
        tt = reaction.emoji
        if tt=="1️⃣":
            return 1
        elif tt=="2️⃣":
            return 2
        elif tt=="3️⃣":
            return 3
        elif tt=="4️⃣":
            return 4
        else:
            return 0
    if user.id!=L.players[L.turn].id:
        return
    choice = takeGotiNumber()

    
    #if em!=0:
    #    if L.moveMainNEW(L.num, em)==True:
    #        waitinForReaction = False
    #        e,f = emb(L,optionalText=f"<@{L.players[L.turn].id}>.", fTitle="Next turn:")
    #        q = await reaction.message.channel.send(file=f,embed=e)
    #    else:
    #        await reaction.message.channel.send("Something was not right...")


    if choice!=0 and L.message==reaction.message and waitinForReaction==True:
        allGotis = L.returnAllGotis()
        player = L.players[L.turn] # Extracted the player object of whom the turn is
        noOfGotisOut, gotisOut = player.countOut(L.num) # Extracted info about gotis
        gotis = player.gotis # Extracted the gotis of that player
        goti = gotis[choice-1]
        if L.num==6:
            if goti.out==True:
                # Check if can move ahead
                goti.move(L.num, L)
            else:
                goti.takeOut()
            e,f = emb(L,optionalText=f"<@{L.players[L.turn].id}>.", fTitle="Turn continues of ")
            q = await reaction.message.channel.send(file=f,embed=e)
            L.message = q
            waitinForReaction = False
        else:
            ##########################
            # Check if can move ahead#
            goti = gotis[choice-1]
            if L.num>(56-goti.currentPlace):
                pp = 0
                for b in gotis:
                    if L.num>(56-goti.currentPlace) and goti.out==True:
                        pass
                    else:
                        pp+=1
                if pp>0:
                    q = await message.channel.send("No choice available")
                else:
                    L.nextTurn()
                return

            ##########################
            goti.move(L.num, L)
            L.nextTurn()
            e,f = emb(L,optionalText=f"<@{L.players[L.turn].id}>.", fTitle="Next turn:")
            q = await reaction.message.channel.send(file=f,embed=e)
            L.message = q
            waitinForReaction = False

client.run(token)
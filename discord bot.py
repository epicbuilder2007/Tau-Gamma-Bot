import os
import discord
from dotenv import load_dotenv
import pandas
from pandas import *
from discord.ext import commands
import json
from numpy import ndarray

Version = 1.8

Galaxylist = pandas.read_excel('Galaxydps.xlsx', index_col = 0)


async def writeJSON(ctx, ship, arg):
    JSON = open(f'{ctx.author.id}.json', "r")
    pref = json.load(JSON)
    JSON.close()
    JSON = open(f'{ctx.author.id}.json', 'w')
    pref["last_search_ship_type"] = str(Galaxylist['Type'][str(ship)])
    pref["last_search_string"] = arg
    pref["last_search_return_ship"] = ship
    pref = json.dumps(pref, indent = 4)
    JSON.write(pref)
    JSON.close()


async def concTurret(ctx, ship):
    string = ""
    for i in range(2):
        if str(Galaxylist[f'Spinal{i+1}_type'][str(ship)]) != "None":
            string = string + f"Spinal {i+1}: " + str(Galaxylist[f'Spinal{i+1}_type'][str(ship)]) + " x" + str(int(Galaxylist[f'Barrels{i+1}'][str(ship)])) + "\n"

    for i in range(10):
        if str(Galaxylist[f'Turret{i+1}_type'][str(ship)]) != "None":
            string = string + f'Turret {i+1}: ' + str(Galaxylist[f'Turret{i+1}_type'][str(ship)]) + " x" + str(int(Galaxylist[f'Turret{i+1}_amount'][str(ship)])) + "\n"

    return str(string)


async def outputResult(ctx, ship, mode):
    try:
        if mode == "info":
            await ctx.send(
                "Ship: " + str(ship) +"\n"
                "Ship Category: " + str(Galaxylist['Type'][str(ship)]) + "\n"
                "Ship Status: " + str(Galaxylist['isLimited'][str(ship)]) + "\n"
                "Average DPS: " + str(Galaxylist['AvDPS'][str(ship)]) + "\n"
                "Shield DPS: " + str(Galaxylist['ShieldDPS'][str(ship)]) +"\n"
                "Hull DPS: " + str(Galaxylist['HullDPS'][str(ship)]) +"\n"
                "Turret DPS: " + str(Galaxylist['TurretDPS'][str(ship)]) +"\n"
                "Spinal DPS: " + str(Galaxylist['SpinalDPS'][str(ship)]) +"\n"
                "Minimum Range: " + str(Galaxylist['minRange'][str(ship)]) +"\n"
                "Maximum Range: " + str(Galaxylist['maxRange'][str(ship)]))
        elif mode == "turret":
            string = await concTurret(ctx, ship)
            await ctx.send(
                "Ship: " + str(ship) +"\n"
                "Average DPS: " + str(Galaxylist['AvDPS'][str(ship)]) + "\n"
                "Shield DPS: " + str(Galaxylist['ShieldDPS'][str(ship)]) +"\n"
                "Hull DPS: " + str(Galaxylist['HullDPS'][str(ship)]) +"\n"
                "Turret DPS: " + str(Galaxylist['TurretDPS'][str(ship)]) +"\n"
                "Spinal DPS: " + str(Galaxylist['SpinalDPS'][str(ship)]) +"\n" +
                string
                )
        elif mode == "range":
            await ctx.send(
                "Minimum Range: " + str(Galaxylist['minRange'][str(ship)]) +"\n"
                "Maximum Range: " + str(Galaxylist['maxRange'][str(ship)]))
    except:
        await ctx.send("Please check if you included mode argument. the command is :ship <ship> <info/turret>")


async def newJSON(ctx):
    with open(f'{ctx.author.id}.json', "a+") as JSON:
        pref = {
            'enable_predictive_search': False,
            'last_search_ship_type': "",
            'last_search_string': "",
            'last_search_return_ship': "",
            'set_auto_referral': {}
        }
        pref = json.dumps(pref, indent = 4)
        JSON.write(pref)
        JSON.close()


async def shipCommand(ctx, arg, mode):
    global JSON
    try:
        JSON = open(f'{ctx.author.id}.json', "r")
        pref = json.load(JSON)
    except FileNotFoundError:
        await newJSON(ctx)
        JSON = open(f'{ctx.author.id}.json', "r")
        pref = json.load(JSON)

    if arg in pref['set_auto_referral']:
        await outputResult(ctx, pref['set_auto_referral'][arg], mode)
        await writeJSON(ctx, pref['set_auto_referral'][arg], arg)

    elif arg == pref['last_search_string']:
        await outputResult(ctx, pref['last_search_return_ship'], mode)
        await writeJSON(ctx, pref['last_search_return_ship'], arg)
    else:
        findlist = []
        found = False
        for key, value in Galaxylist['Type'].items():
            if str(key).find(arg.title()) >= 0:
                findlist.append((str(key), str(value)))
        for i in range(len(findlist)):
            if findlist[i][1] == pref['last_search_ship_type']:
                await outputResult(ctx, findlist[i][0], mode)
                await writeJSON(ctx, findlist[i][0], arg)
                found = True
                break

        if not found:
            await outputResult(ctx, findlist[0][0], mode)
            await writeJSON(ctx, findlist[0][0], arg)


load_dotenv()
TOKEN = "NzEzMDE2NzY3OTc0NDczNzU5.GqsqWA.Xx_HrUig6Lw2ahixwmF3jKOBJaDT2FPRwm5Yxk"
bot = commands.Bot(command_prefix=":")

"""
replace this with :range, :info, and :turret
@bot.command(name='ship')
async def dpsCheck(ctx, arg, mode="info"):
    global JSON
    try:
        JSON = open(f'{ctx.author.id}.json', "r+")
        pref = json.load(JSON)
    except:
        await newJSON(ctx)
        JSON = open(f'{ctx.author.id}.json', "r+")
        pref = json.load(JSON)

    if pref['enable_predictive_search'] == True:
        if arg in pref['set_auto_referral']:
            await outputResult(ctx, pref['set_auto_referral'][arg], mode)
            await writeJSON(ctx, pref['set_auto_referral'][arg], arg)


        elif arg == pref['last_search_string']:
            await outputResult(ctx, pref['last_search_return_ship'], mode)
            await writeJSON(ctx, pref['last_search_return_ship'], arg)

        else:
            findlist = []
            found = False
            for key, value in Galaxylist['Type'].items():
                if str(key).find(arg.title()) >= 0:
                    findlist.append((str(key), str(value)))
            for i in range(len(findlist)):
                if findlist[i][1] == pref['last_search_ship_type']:
                    await outputResult(ctx, findlist[i][0], mode)
                    await writeJSON(ctx, findlist[i][0], arg)
                    found = True
                    break

            if found == False:
                await outputResult(ctx, findlist[0][0], mode)
                await writeJSON(ctx, findlist[0][0], arg)

    else:
        await ctx.send("Predictive search is off! Search results may not be accurate for you.")
        found = False
        for key, value in Galaxylist['Type'].items():
            if str(key).find(arg.title()) >= 0:
                await outputResult(ctx, str(key), mode)
                await writeJSON(ctx, str(key), arg)
                found = True
                break
        if not found:
            await ctx.send(f"Search for {arg} failed :(")
"""

@bot.command(name='short')
async def func(ctx, short="", *, arg):
    args = arg.split()
    mode = "set"
    if "set" in args or "remove" in args or "print" in args:
        if "set" in args:
            mode = "set"
        elif "remove" in args:
            mode = "remove"
        elif "print" in args:
            mode = "remove"
    args[args.index(mode)].remove()
    global JSON
    try:
        JSON = open(f'{ctx.author.id}.json', "r")
    except FileNotFoundError:
        await newJSON(ctx)
        JSON = open(f'{ctx.author.id}.json', 'r')
    pref = json.load(JSON)
    JSON.close()
    if mode == "set":
        JSON = open(f'{ctx.author.id}.json', 'w')
        pref['set_auto_referral'][str(short)] = str(args[0])
        pref = json.dumps(pref, indent=4)
        JSON.write(pref)
        JSON.close()
    elif mode == "remove":
        try:
            JSON = open(f'{ctx.author.id}.json', 'w')
            try:
                del pref['set_auto_referral'][str(short)]
                pref = json.dumps(pref, indent=4)
                JSON.write(pref)
                JSON.close()
            except KeyError:
                await ctx.send(f"Short {short} is not found, did you make a typo?")
        except FileNotFoundError:
            await ctx.send("You don't have a json file, please use the bot before using this.")
    elif mode == "print":
        try:
            await ctx.send(f'{short} was set to ship {pref["set_auto_referral"][str(short)]}.')
        except KeyError:
            await ctx.send(f'Short {short} not found, did you make a typo?')






    """
    if mode == "":
        await ctx.send("Please specify operation. Command is :short <set/remove/print/help>. Use :short help for help on command")

    #set subcommand
    elif mode.lower() == "set":
        if short != "" and ship != "":
            global JSON
            try:
                JSON = open(f'{ctx.author.id}.json', "r")
                pref = json.load(JSON)
            except:
                await newJSON(ctx)
                JSON = open(f'{ctx.author.id}.json', "r")
                pref = json.load(JSON)
            JSON.close()
            JSON = open(f'{ctx.author.id}.json', "w")
            pref["set_auto_referral"][str(short)] = ship
            pref = json.dumps(pref, indent = 4)
            JSON.write(pref)
            JSON.close()
            await ctx.send(f"Successfully mapped {short} to {ship}")
        elif ship == "":
            await ctx.send("specify ship name")

        elif short == "":
            await ctx.send("specify short name")

    #remove subcommand
    elif mode.lower() == "remove":
        if short != "":
            JSON = open(f'{ctx.author.id}.json', "r")
            pref = json.load(JSON)
            JSON.close()
            JSON = open(f'{ctx.author.id}.json', "w")
            del pref['set_auto_referral'][str(short)]
            pref = json.dumps(pref, indent= 4)
            JSON.write(pref)
            JSON.close()
            await ctx.send(f"successfully removed short: {short}")
        else:
            await ctx.send("specify short name")

    #print subcommand
    elif mode.lower() == "print":
        try:
            JSON = open(f'{ctx.author.id}.json', "r")
            pref = json.load(JSON)
            JSON.close()
            await ctx.send(f'short {short} is mapped to ship ' + str(pref['set_auto_referral'][str(short)]))
        except:
            await ctx.send(f"{short} not found.")

    else:
        await ctx.send("Operation not found, please run :short help for help on the command.")
    """


@bot.command(name="hitlist")
async def hitlist(ctx, player = "", *, arg):
    args = arg.split()
    mode = "add"
    if "add" in args or "view" in args or "viewall" in args:
        if "add" in args:
            mode = "add"
        elif "view" in args:
            mode = "view"
        elif "viewall" in args:
            mode = "viewall"
        args[args.index(mode)].remove()
    JSON = open('hitlist.json', 'r')
    pref = json.load(JSON)
    JSON.close()
    if mode == "add":
        JSON = open('hitlist.json', 'w')
        if player != "":
            pref[player] = " ".join(args)
            pref = json.dumps(pref, indent = 4)
            JSON.write(pref)
            JSON.close()
            await ctx.send(f"Player {player} added to hitlist for reason {' '.join(args)}")
        else:
            await ctx.send("Player not defined.")
    elif mode == "view":
        if player != "":
            try:
                await ctx.send(f'{player} is in the hitlist for {pref[player]}')
            except KeyError:
                await ctx.send(f'{player} not found. Probably typos.')
            else:
                await ctx.send("Player not defined.")
    elif mode == "viewall":
        string = ""
        for key, value in pref.items():
            string += f'{str(key)} is in the hitlist for {str(value)}'
        if string != "":
            await ctx.send(string)
        else:
            await ctx.send("hitlist is empty.")


    """
    if mode != "":
        if mode == "add":
            try:
                JSON = open("hitlist.json", "r")
                pref = json.load(JSON)
                JSON.close()
                JSON = open("hitlist.json", "w")
                pref[str(player)] = str(reason)
                pref = json.dumps(pref, indent=4)
                JSON.write(pref)
                JSON.close()
                await ctx.send(f"Successfully added player {player} to hitlist for {reason}")
            except Exception as e:
                await ctx.send(str(e))

        if mode == "view":
            try:
                JSON = open("hitlist.json", "r")
                pref = json.load(JSON)
                await ctx.send(str(pref[player]))
            except KeyError:
                await ctx.send("Player not found")

        if mode == "viewall":
            try:
                JSON = open("hitlist.json", "r")
                pref = json.load(JSON)
                await ctx.send(str(pref))

            except Exception as e:
                await ctx.send(str(e))
    """


@bot.command(name="range")
async def Range(ctx, arg):
    await shipCommand(ctx, arg, "range")


@bot.command(name="info")
async def info(ctx, arg):
    await shipCommand(ctx, arg, "info")


@bot.command(name="turret")
async def turret(ctx, arg):
    await shipCommand(ctx, arg, "turret")


@bot.command(name="Help")
async def help(ctx):
    await ctx.send(f"This is version {Version} of Tau Gamma Bot, home brewed by epicbuilder2007, who definitely doesn't have other stuff to do. \n\n"+
                   "There are currently  commands for this bot: \n\n"+
                   "command :info <string> \n"+
                   "This returns general info of the ship. \n\n"+
                   "command :turret <string> \n"+
                   "This returns turret info (dps and name) of the ship. \n\n"+
                   "command :range <string> \n"+
                   "This returns range info of the ship \n\n"+
                   "command :short <short> <ship (optional)> <set/remove/print> \n"+
                   "Use this command to set shortcuts to ships.\n"+
                   "'set' sets the short name you provided to the ship name you provided. Remember that currently, you do need to make sure the ship name is case-correct. \n"+
                   "'remove' removes the short name you provided. \n"+
                   "'print' prints the short name you set before \n\n"+
                   "command :hitlist <player> <reason (optional)> <add/view/viewall> \n"+
                   "Use this command to keep tabs on which players the clan wants to kill. \n"+
                   "'add' adds the player to the list. \n"+
                   "'view' views the reason why the player was added to the hitlist. \n"+
                   "'viewall' views all the players and their reason for their presence in the hitlist \n\n"+
                   "command :suslist <player> <add/view> \n"+
                   "Use this command to keep track of suspicious players to avoid."+
                   "'add' adds the player name provided to the list. \n"+
                   "'view' returns the list of players to be careful around. \n\n"+
                   "command :services <service> <True/False> \n"+
                   "Use this command to enable or disable bot features for yourself. \n"+
                   "Current configurable services include (case-sensitive): 'predictive_search' \n\n"+
                   "If you have any feature requests, or bug reports, feel free to contact me (epicbuilder2007#8204) about it, whether via pinging me in General Chat or by DMing me, or even via Whatsapp if you have it."+
                   "Don't waste your time trying to tell me how shit this bot is though, I know that :sad:")


@bot.command(name='services')
async def services(ctx, service, status = True):
    global JSON
    try:
        JSON = open(f'{ctx.author.id}.json', 'r')
    except FileNotFoundError:
        await newJSON(ctx)
        JSON = open(f'{ctx.author.id}.json', 'r')

    pref = json.load(JSON)
    JSON.close()
    if f'enable_{service.lower()}' in pref:
        if pref[f'enable_{service.lower()}'] != status:
            pref[f'enable_{service.lower()}'] = status
            JSON = open(f'{ctx.author.id}.json', 'w')
            pref = json.dumps(pref, indent=4)
            JSON.write(pref)
            JSON.close()

        else:
            await ctx.send(f"Nothing changed, {service} is already at {status}")

    else:
        await ctx.send(f"Nothing changed, {service} does not exist")


@bot.command(name="data")
async def data(ctx, msg: discord.Message , ship = "", cat = "", string = ""):
    #check if all args aren't empty DONE
    #if so, then add the request into a new entry in json DONE
    #during bot startup, create a subprocess that checks the json file every now and then
    #if amount of people reacting positively is over 50%, then push change to excel file.
    #to do this, open the excel file in the subprocess, write to it, then close it back.
    #should change code to load the excel file when command is invoked, instead of startup.
    if ship != "" and cat != "" and string != "":
        JSON = open("data.json", "r")
        queue = json.load(JSON)
        JSON.close()
        queue[str(msg.id)] = (str(ship), str(cat), str(string), 0)
        JSON = open("data.json", "w")
        queue = json.dumps(queue, indent=4)
        JSON.write(queue)
        JSON.close()
        message = await ctx.send(f"Successfully proposed change: \n\n ship: {str(ship)} \n Data Category: {str(cat)} \n Value: {str(string)} \n\n Now the council shall decide your fate.")
        await message.add_reaction(":arrow_up:")
    else:
        if ship == "":
            await ctx.send("Please specify ship")
        if cat == "":
            await ctx.send("Please specify data category")
        if string == "":
            await ctx.send("Please specify data value")


@bot.command(name="suslist")
async def sus(ctx, player = "", mode = "add"):
    JSON = open('suslist.json', 'r')
    pref = json.load(JSON)
    JSON.close()
    if mode.lower() == "add":
        pref[player] = "obligatory value here"
        JSON = open('suslist.json', 'w')
        pref = json.dumps(pref, indent=4)
        JSON.write(pref)
        JSON.close()
    elif mode.lower() == "view":
        string = []
        for key in pref.items():
            string.append(key)
        await ctx.send(f'Players in this list: {", ".join(string)}. Please be careful when around these players, as \
        they are known for ruining the fun.')


bot.run(TOKEN)

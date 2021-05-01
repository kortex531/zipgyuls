import discord
import requests
import json

client = discord.Client()


@client.event
async def on_ready():
    print(client.user.id)
    print("ready")


@client.event
async def on_message(message):
    if message.content.startswith("검색봇 확인"):
        await message.channel.send("작동중")
    if message.content.startswith("작동확인"):
        await message.channel.send("작동중")
    if message.content.startswith("검색"):
        user = []

        allUser = message.content.split()
        for user1 in allUser:
            user.append(user1)

        for userCnt in range(1, len(user)):
            url = 'https://api-aion.plaync.com/search/v1/characters?classId=&pageNo=1&pageSize=20&query={}&raceId=&serverId=22&site=aion&sort=rank&world=classic'.format(
                user[userCnt])
            req = requests.get(url).content

            data = json.loads(req)

            charname = data.get("documents")[0].get("charName")
            uid = data.get("documents")[0].get("charId")

            aionurl = 'https://aion.plaync.com/characters/server/22/id/{}/home'.format(uid)
            await message.channel.send(aionurl)

    if message.content.startswith("!검색"):
        user = []

        allUser = message.content.split()
        for user1 in allUser:
            user.append(user1)

        for userCnt in range(1, len(user)):

            url = 'https://api-aion.plaync.com/search/v1/characters?classId=&pageNo=1&pageSize=20&query={}&raceId=&serverId=22&site=aion&sort=rank&world=classic'.format(
                user[userCnt])
            req = requests.get(url).content

            data = json.loads(req)

            uid = data.get("documents")[0].get("charId")

            # 아이온 api 주소 + 캐릭터 ID
            srcurl = 'https://api-aion.plaync.com/game/v2/classic/merge/server/22/id/{}'.format(uid)
            basicinfo = 'https://api-aion.plaync.com/game/v2/classic/characters/server/22/id/{}'.format(uid)
            aionurl = 'https://aion.plaync.com/characters/server/22/id/{}/home'.format(uid)
            # keyList
            payload = {'keyList': ["character_stats", "character_equipments", "character_abyss", "character_stigma"]}

            # 아이온 api 호출
            reqsrc = requests.put(srcurl, json=payload).content
            basicsrc = requests.get(basicinfo).content

            # 아이온 데이터 json 변환
            datasrc = json.loads(reqsrc)
            basicdata = json.loads(basicsrc)

            chrstat = datasrc['character_stats']
            # totstat = chrstat['totalStat']
            totstat = datasrc['character_stats']['totalStat']
            stigma = datasrc['character_stigma']
            equip = datasrc['character_equipments']
            rankName = datasrc['character_abyss']['rankName']
            totalKill = datasrc['character_abyss']['totalKillCount']
            className = basicdata.get('jobName')
            raceName = basicdata.get('raceName')
            guildName = basicdata.get('guildName')

            stiName = []
            eqName = []
            eqInfo = []
            eqRing = []
            eqEar = []
            eqWp = []
            shCnt = 0
            for sti in stigma:
                stiName.append(sti['name'])
            for eq in equip:
                # eqName.append(eq['name'])
                if eq['category1']['name'] == '장신구':
                    eqAcc = eq['category2']['name']
                    if eqAcc == '반지':
                        eqRing.append(eq['name'])
                    elif eqAcc == '귀고리':
                        eqEar.append(eq['name'])
                    elif eqAcc == '목걸이':
                        eqNec = eq['name']
                    elif eqAcc == '허리띠':
                        eqBelt = eq['name']
                elif eq['category1']['name'] == '방어구':
                    if eq['category3']['name'] == '어깨':
                        eqSh = eq['name']
                        eqShEn = eq['enchantCount']
                        eqSh = "+ {} {}".format(eqShEn, eqSh)
                    elif eq['category3']['name'] == '장갑':
                        eqHand = eq['name']
                        eqHandEn = eq['enchantCount']
                        eqHand = "+ {} {}".format(eqHandEn, eqHand)
                    elif eq['category3']['name'] == '신발':
                        eqFoot = eq['name']
                        eqFootEn = eq['enchantCount']
                        eqFoot = "+ {} {}".format(eqFootEn, eqFoot)
                    elif eq['category3']['name'] == '상의':
                        eqTorso = eq['name']
                        eqTorsoEn = eq['enchantCount']
                        eqTorso = "+ {} {}".format(eqTorsoEn, eqTorso)
                    elif eq['category3']['name'] == '하의':
                        eqLeg = eq['name']
                        eqLegEn = eq['enchantCount']
                        eqLeg = "+ {} {}".format(eqLegEn, eqLeg)
                    elif eq['category2']['name'] == '머리방어구':
                        eqHead = eq['name']
                    elif eq['category2']['name'] == '방패':
                        eqSheild = eq['name']
                        eqShEn = (eq['enchantCount'])
                        eqSheild = "+ {} {}".format(eqShEn, eqSheild)
                        shCnt = 1
                elif eq['category1']['name'] == '무기':
                    eqWeapon = (eq['name'])
                    eqWpEn = (eq['enchantCount'])
                    eqWeapon = "+ {} {}".format(eqWpEn, eqWeapon)
                    eqWp.append(eqWeapon)

            eqRing1 = "반지 : {}".format(eqRing[0])
            eqRing2 = "반지 : {}".format(eqRing[1])
            eqEar1 = "귀고리 : {}".format(eqEar[0])
            eqEar2 = "귀고리 : {}".format(eqEar[1])
            eqNec = "목걸이 : {}".format(eqNec)
            eqBelt = "허리띠 : {}".format(eqBelt)
            eqSh = "어깨 : {}".format(eqSh)
            eqHand = "장갑 : {}".format(eqHand)
            eqFoot = "신발 : {}".format(eqFoot)
            eqTorso = "상의 : {}".format(eqTorso)
            eqLeg = "하의 : {}".format(eqLeg)
            eqHead = "머리 : {}".format(eqHead)

            if shCnt == 1:
                eqSheild = ("방패 : {}".format(eqSheild))
            else:
                eqSheild = ("방패 : 없음")
            if len(eqWp) == 3:
                eqWp1 = "무기 : {}".format(eqWp[0])
                eqWp2 = "무기 : {}".format(eqWp[1])
                eqWp3 = "무기 : {}".format(eqWp[2])
            elif len(eqWp) == 2:
                eqWp1 = "무기 : {}".format(eqWp[0])
                eqWp2 = "무기 : {}".format(eqWp[1])
                eqWp3 = "무기 : 없음"
            elif len(eqWp) == 1:
                eqWp1 = "무기 : {}".format(eqWp[0])
                eqWp2 = "무기 : 없음"
                eqWp3 = "무기 : 없음"
            elif len(eqWp) == 0:
                eqWp1 = "무기 : 없음"
                eqWp2 = "무기 : 없음"
                eqWp3 = "무기 : 없음"

                # print(eqName)
            # 변수매칭
            accuracy = totstat['accuracyRight']
            magicalAccuracy = totstat['magicalAccuracy']
            attack = totstat['physicalRight']
            hp = totstat['hp']
            magicResist = totstat['magicResist']
            critical = totstat['criticalRight']
            block = totstat['block']

            await message.channel.send \
                ("기본정보\n닉네임 : {} \n클래스 : {}\n종족 : {} \n레기온 : {}\n어비스계급: {}\n전체 킬수: {}\n\
            \n\n스탯\n\n생명력 : {} \n마법저항 : {} \n방패방어 : {}\n공격력 : {} \n명중 : {} \n물리치명타 : {}\n마법적중 : {} \
            \n\n스티그마\n\n스티그마1 : {}\n스티그마2 : {}\n스티그마3 : {}\n스티그마4 : {}\n스티그마5 : {}\n스티그마6 : {}\n스티그마7 : {}\n스티그마8 : {} \
            \n\n장비\n\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}" \
                 .format(user[userCnt], className, raceName, guildName, rankName, totalKill, hp, magicResist, block,
                         attack, accuracy, critical, magicalAccuracy, \
                         stiName[0], stiName[1], stiName[2], stiName[3], stiName[4], stiName[5], stiName[6], stiName[7], \
                         eqWp1, eqWp2, eqWp3, eqSheild, eqTorso, eqSh, eqLeg, eqHand, eqFoot, eqHead, eqNec, eqEar1,
                         eqEar2, eqRing1, eqRing2, eqBelt, aionurl))


client.run('ODM3MjY0NDI0MjAwMDQ0NTc0.YIqBQg.n2OWRiYJHjcUhi2r4vK01gYuxnE')
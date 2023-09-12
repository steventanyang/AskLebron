import itertools
import pandas as pd

#step 1: write names of players taken from user input of teams
def chooseteams(league, team1, team2, projections_file, coinvalues_file) :
    team1_file = f'leagues/{league}/{team1}'
    team2_file = f'leagues/{league}/{team2}'
    with open(team1_file , 'r') as first , open(projections_file , 'a') as second , open(coinvalues_file , 'a') as third :
        for line in first : 
            second.write(line) and third.write(line)
    with open(team2_file , 'r') as first , open(projections_file , 'a') as second , open(coinvalues_file , 'a') as third :
        for line in first : 
            second.write(line) and third.write(line)
            
all = dict()

#step 2:creating a dict in this format: "player: projected xp, coin"
def processdata(league, file1, file2, file3, risklv) :
    game = open(file1)
    for line in game :
        if line.startswith('#') : continue 
        line = line.rstrip()
        split = line.split(';')
        player = split[0]
        file = open(file3)
        for line in file :
            line = line.rstrip()
            split = line.split(',',1)
            info = split[1]
            if info.startswith(player) : 
                jproj = info.split(',',1)
                jp = jproj[1]
                proj = open(file2, 'r+')
                lines = proj.readlines()
                for i, line in enumerate(lines):
                    if line.startswith(player) :
                        lines[i] = line.strip() + jp + '\n'
                proj.seek(0)
                for line in lines: 
                    proj.write(line)

    projected = dict()
    projstats = open(file2)
    for line in projstats : 
        line = line.rstrip()
        split = line.split(';')
        name = split[0]
        stat = split[1]
        stats = stat.split(',')
        if league == 'wnba': 
            try :
                if risklv == 'risk' : 
                    if float(stats[1]) < 14 : continue 
                elif risklv == 'safe': 
                    if float(stats[1]) < 18 : continue
                slp = float(stats[2])*7
                slr = float(stats[3])*8
                sla = float(stats[4])*10
                sls = float(stats[5])*14
                slb = float(stats[6])*14
                sltpm = float(stats[7])*4
                slt = float(stats[8])*(-5)
                totalproj = slp + slr + sla + slt + sls + slb + sltpm
                projected[name] = projected.get(name, 0) + totalproj
            except : continue
        elif league == 'nba' :
            try : 
                if risklv == 'risk' : 
                    if float(stats[1]) < 16 : continue 
                elif risklv == 'safe' : 
                    if float(stats[1]) < 20 : continue
                slp = float(stats[2])*7
                slr = float(stats[3])*8
                sla = float(stats[4])*10
                sls = float(stats[5])*14
                slb = float(stats[6])*14
                sltpm = float(stats[8])*4
                slt = float(stats[7])*(-5)
                totalproj = slp + slr + sla + slt + sls + slb + sltpm
                projected[name] = projected.get(name, 0) + totalproj
            except : continue

    #print(projected.items())
    projected_stats = list()
    for p,c in projected.items() :
        cf = p,c
        projected_stats.append(cf)
    #print(cock)
    all.clear()
    for item in projected_stats : 
        pr = item[0]
        pj = item[1]
        cv = open(file1)
        for line in cv : 
            line = line.rstrip()
            if not line.startswith(pr) : continue 
            split = line.split(';')
            info = split[1]
            c_pos = info.split(',')
            cint = int(c_pos[0])
            all[pr] = (pj, cint)
    #print(all.items())

#step 3: use itertools to find combinations

vl = dict()

def combine(number) :
    combs = itertools.combinations(all.items() , number)
    bestvalue = 0
    bestcomb = 0 
    coincost = 0 
    totalcoins = 0
    ls = list()
    cs = list()
    for comb in combs : 
        ls.clear()
        cs.clear()
        for player in comb : 
            stat = player[1]
            xpproj = stat[0]
            coincost = stat[1]
            ls.append(xpproj)
            cs.append(coincost)
        bigxp = sum(ls)
        totalcoins = sum(cs)
        if bigxp > bestvalue and 19 <= totalcoins <= 20:
            bestvalue = bigxp 
            bestcomb = comb
            vl[bestcomb] = bestvalue


def optimizer(league, team1, team2, risklv):

    if league == 'nba' : 
        df = pd.read_csv('rotowire-nba-projections.csv')
        df = df.drop(columns = ['Unnamed: 1','Unnamed: 2','Unnamed: 3','Field Goals','Unnamed: 12','Unnamed: 13','Unnamed: 15','Unnamed: 16','Free Throws','Unnamed: 18','Unnamed: 19','More Stats','Unnamed: 21'])
        df.to_csv('txt/nbadone')
    
    if league == 'wnba' :
        df = pd.read_csv('wnba-daily-projections.csv')
        df = df.drop(columns = ['Unnamed: 1','Unnamed: 2','Unnamed: 10','Unnamed: 11','Additional Stats','Unnamed: 14','Unnamed: 15','Unnamed: 16','Unnamed: 17','Unnamed: 18','Unnamed: 19','Unnamed: 20'])
        df.to_csv('txt/wnbadone')
    
    pr = 'txt/bballprojections.txt'
    cv = 'txt/bballcoinvalues.txt'
    nd = f'txt/{league}done'

    with open(pr, 'w') as file:
        file.truncate()
    with open(cv, 'w') as file:
        file.truncate()

    chooseteams(league, team1, team2, pr, cv)

    processdata(league, cv, pr, nd, risklv)

    combine(8) 
    combine(7)
    combine(6)
    combine(5)

    final = list()

    result = max(vl, key=vl.get)
    finalvalue = vl[result]
    final.append(round(finalvalue, 2))
    for player in result : 
        name = player[0]
        final.append(name)
    vl.clear()

    # print(final)

    return final

# optimizer('wnba','liberty','wings','safe')

#something isn't clearing right. 
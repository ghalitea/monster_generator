import random
import subprocess

# reference tables ---------------------------------
chlg_lvl_to_xp = {0:10, 1:200, 2:450, 3:700, 4:1100, 5:1800, 6:2300, 7:2900, 8:3900, 9:5000, 10:5900, 11:7200, 12:8400}

chl_prfbon = {0:2, 1:2, 2:2, 3:2, 4:2, 5:3, 6:3, 7:3, 8:3, 9:4, 10:4, 11:4, 12:4}

size_dice = {
    "Tiny": 4,
    "Small": 6,
    "Medium": 8,
    "Large": 10,
    "Huge": 12,
    "Gargantuan": 20
}

abilities = [
    '\t\t\\ability{Multiattack}{The Monster can make a second attack right after it made \n\t\t\ta first one. This attack can ether be the same action as the first one or a \n\t\t\tdifferent one.}\\\\\\bigskip\n',
    '\t\t\\action{Bite}{\\mwa}{\\toH{6}, \\reach{1}, one target. \n\t\t\t\\textit{Hit:}\\damage{2}{6}{4}{Pie}. If the target is a creature, it must succeed \n\t\t\ton a DC 12 Constitution saving throw against disease or become poisoned until \n\t\t\tthe disease is cured. Every 24 hours that elapse, the creature must repeat the \n\t\t\tsaving throw, reducing its hit point maximum by\damage{1}{10}{0}{z} on a failure. This \n\t\t\treduction lasts until the disease is cured. The creature dies if the disease \n\t\t\treduces its hit point maximum to 0.}\\\\\\bigskip\n',
    '\t\t\\action{Horns}{\\mwa}{\\toH{6}, \\reach{1}, one target. \n\t\t\t\\textit{Hit:}\\damage{1}{12}{4}{B}.}\\\\\\bigskip\n',
    '\t\t\\action{Claws}{\\mwa}{\\toH{6}, \\reach{1}, one target.\n\t\t\t\\textit{Hit:}\damage{2}{6}{4}{S}}\\\\\\bigskip\n',
    '\t\t\\action{Hooves}{\\mwa}{\\toH{6}, \\reach{1}, one target.\n\t\t\t\\textit{Hit:}\\damage{2}{6}{4}{B}}\\\\\\bigskip\n',
    '\t\t\\action{Tentacles}{\\mwa}{\\toH{4}, \\reach{1}, one target.\n\t\t\t\\textit{Hit:}\\damage{2}{6}{2}{S}}\\\\\\bigskip\n',
    '\t\t\\action{Beak}{\\mwa}{\\toH{6}, \\reach{1}, one target.\n\t\t\t\\textit{Hit:}\\damage{1}{10}{3}{Pie}}\\\\\\bigskip\n',
    '\t\t\\action{Beak}{\\mwa}{\\toH{6}, \\reach{1}, one target.\n\t\t\t\\textit{Hit:}\\damage{1}{10}{3}{Pie}}\\\\\\bigskip\n',
    '\t\t\\ability{Acid Spray (Recharge 6)}{The monsters spits acid in a line that is 30 \n\t\t\tfeet long and 5 feet wide. Each creature in that line must make a DC 13 Dexterity \n\t\t\tsaving throw taking\damage{3}{6}{0}{A} on a failed save, or half as much damage \n\t\t\ton a successful one.}\\\\\\bigskip\n',
    '\t\t\\action{Web (Recharge 5-6)}{\\rwa}{\\toH{4}, \\reach{6/12}, one large or smaller creature.\n\t\t\t\\textit{Hit:} The creature is restrained by webbing. As an action, the restrained \n\t\t\tcreature can make a DC 11 Strength check, escaping from the webbing on a success. \n\t\t\tThe effect also ends if the webbing is destroyed. The webbing has AC 10, 5 \n\t\t\thit points, vulnerability to fire damage, and immunity to bludgeoning, poison, \n\t\t\tand psychic damage.}\\\\\\bigskip\n'
]


# randomize stuff ----------------------------------
def rdm_size() -> str:                                      # randomize the size
    size = ''
    tmp_nbr=random.randrange(1,16,1)                        # generate number from 1 to 15
    if tmp_nbr<=1:      size = 'Tiny'                       # 6.67%
    elif tmp_nbr<=3:    size = 'Small'                      # 13.37%
    elif tmp_nbr<=7:    size = 'Medium'                     # 26.67%
    elif tmp_nbr<=11:   size = 'Large'                      # 26.67%
    elif tmp_nbr<=14:   size = 'Huge'                       # 20.0%
    else:               size = 'Gargantuan'                 # 6.67%

    return size

def rdm_stats():                                                        # randomize the ability scores
    stats = [0,0,0,0,0,0]
    for absc in range(len(stats)):
        tmp_nbr=random.randrange(1,20,1)                                # generate number from 1 to 19
        if tmp_nbr<=1:      stats[absc] = random.randrange(0,5)         # 5.26%
        elif tmp_nbr<=3:    stats[absc] = random.randrange(5,8)         # 10.52%
        elif tmp_nbr<=7:    stats[absc] = random.randrange(8,11)        # 21.05%
        elif tmp_nbr<=12:   stats[absc] = random.randrange(11,15)       # 26.32%
        elif tmp_nbr<=16:   stats[absc] = random.randrange(15,17)       # 21.05%
        elif tmp_nbr<=18:   stats[absc] = random.randrange(17,20)       # 10.52%
        else:               stats[absc] = 20                            # 5.26%
    return stats

set_size = rdm_size()
set_stats = rdm_stats()

def rdm_hp() -> int:                                                                # generate the hp
    hp = [0,0,0]
    hp[0] = random.randrange(1,13)                                                  # number of dice -> random
    hp[1] = size_dice[set_size]                                                     # dice -> dependent on the size
    hp[2] = ((set_stats[2]-10)//2) * hp[0] if ((set_stats[2]-10)//2) > 0 else 0     # addition -> const. modifier * number of dice
    return hp

def rdm_ac() -> int:                            # calculate the armour class
    return 10 + ((set_stats[2]-10)//2)

set_hp = rdm_hp()
set_ac = rdm_ac()

def rdm_chlg() -> int:                              # calculate the challange
    hp = (set_hp[1]/2+0.5)*set_hp[0]+set_hp[2]
    return (hp+set_ac)//20

set_chlg = rdm_chlg()

def rdm_xp() -> int:                    # determine xp level
    return chlg_lvl_to_xp[set_chlg]

def rdm_skills():                                                                               # randomize the skills
    skills = ''
    tmp_nbr=random.randrange(3)                                                                 # generate a number between 0 and 2
    if tmp_nbr == 0 and ((set_stats[4]-10)//2) >=0: 
        skills = 'Perception +'+str(((set_stats[4]-10)//2))                                     # 0 = perception
    elif tmp_nbr == 1 and ((set_stats[1]-10)//2) >=0: 
        skills = 'Stealth +'+str(((set_stats[1]-10)//2))                                        # 1 = stealth
    elif tmp_nbr == 2 and ((set_stats[1]-10)//2) >=0 and ((set_stats[4]-10)//2) >=0:            # 2 = both
        skills = 'Stealth +'+str(((set_stats[1]-10)//2))+', Perception +'+str(((set_stats[4]-10)//2))
    else: skills = '--'
    return skills

def rdm_senses():                                                           # randomize the senses
    senses = ''

    tmp_nbr1 = random.randrange(1,5)                                         # first sense
    if tmp_nbr1 == 1: senses += 'Darkvision 12 hex'
    elif tmp_nbr1 == 2: senses += 'Tremorsense 12 hex'
    elif tmp_nbr1 == 3: senses += 'Blindsight 12 hex'
    elif tmp_nbr1 == 4: 
        senses += 'passive Perception '+str(10+((set_stats[4]-10)//2))

    tmp_nbr2 = random.randrange(1,5)                                         # (second sense)
    if tmp_nbr2 == 0: pass
    elif tmp_nbr2 == 1 and tmp_nbr1 != 1: senses += ', Darkvision 12 hex'
    elif tmp_nbr2 == 2 and tmp_nbr1 != 2: senses += ', Tremorsense 12 hex'
    elif tmp_nbr2 == 3 and tmp_nbr1 != 3: senses += ', Blindsight 12 hex'
    elif tmp_nbr2 == 4 and tmp_nbr1 != 4: 
        senses += ', passive Perception '+str(10+((set_stats[4]-10)//2))

    return senses

def rdm_ProfBon() -> int:           # determine the proficiency bonus
    return chl_prfbon[set_chlg]

def rdm_acts() -> str:
    nmbr_abilities = 0
    if set_chlg <= 2: nmbr_abilities = 2
    elif set_chlg > len(abilities): nmbr_abilities = len(abilities)
    else: nmbr_abilities = int(set_chlg)

    ablts = ''
    for i in range(nmbr_abilities):
        tmp_nbr = random.randrange(len(abilities))
        ablts += abilities[tmp_nbr]
        abilities[tmp_nbr] = ''
        print(abilities[tmp_nbr])

    return ablts


# actual syntax ------------------------------------
imports='\\documentclass{article}\n\n\\usepackage{ragged2e}\n\\usepackage[paperwidth=8.5in, paperheight=5.5in, textwidth=7.5in, textheight=4.5in]{geometry}\n\n\\usepackage{multicol}\n\\setlength{\columnsep}{0.5in}\n\n\\usepackage{pagecolor}\n\\pagecolor{white!90!yellow}\n\n\\setlength\parindent{0pt}\n\\thispagestyle{empty}\n\n\\include{macros}\n\n'
doc_beginning='\\begin{document}\n\t\\normalsize\n\t\\begin{multicols*}{2}\n\t\t\\RaggedRight\n\n'
title='\t\t\\creatureName{Chaos Monster}\n\n\t\t\\textit{'+set_size+' Monstrosity, Chaotic evil}\n\n\t\t\\rule{3.5in}{1mm}\n\n'
ac_hp_speed='\t\t\\attrib{Armour Class}{'+str(set_ac)+' (natural armour)}\\\\\n\n\t\t\\hitpoints{'+str(set_hp[0])+'}{'+str(set_hp[1])+'}{'+str(set_hp[2])+'}\\\\\n\t\t\\attrib{Speed}{6 hex}\n\n\t\t\\rule{3.5in}{1mm}\n\n'
ability_scores='\t\t\\small\n\n\t\t\\stats{'+str(set_stats[0])+'}{'+str(set_stats[1])+'}{'+str(set_stats[2])+'}{'+str(set_stats[3])+'}{'+str(set_stats[4])+'}{'+str(set_stats[5])+'}\n\n\t\t\\normalsize\n\n\t\t\\rule{3.5in}{1mm}\n\n'		
sk_dmi_sns_etc='\t\t\\attrib{Skills}{'+rdm_skills()+'}\\\\\n\t\t\\attrib{Damage Immunities}{Poison}\\\\\n\t\t\\attrib{Senses}{'+rdm_senses()+'}\\\\\n\t\t\\attrib{Languages}{--}\\\\\n\t\t\\attrib{Challenge}{'+str(int(set_chlg))+' ('+str(rdm_xp())+')}\\\\\n\t\t\\attrib{Proficiency Bonus}{+'+str(rdm_ProfBon())+'}\n\n\t\t\\rule{3.5in}{1mm}\n\n'
column_break ='\t\t\\vfill\n\t\t\\columnbreak\n\n'
abilities_syn='\t\t\\ability{Water adversity}{Chaos monsters have an adversity to water. They don`t get \n\t\tdamage from it, but they do shy away from it and they can and will not \n\t\tswim.}\\\\\\bigskip\n\n\t\t\\rule{3.5in}{1mm}\n\n\t\t\\vspace{5pt}\n\n\t\t{\\large\\scshape{Actions}}\\\\\n\t\t\\vspace{-1em}\n\t\t\\rule{3.5in}{0.5pt}\n\n'+rdm_acts()+'\n'
doc_ending='\t\t\\vfill\n\t\t\\end{multicols*}\n\\end{document}\n'


# write in the tex doc -----------------------------
with open('chaos_monster.tex','w') as file:
    file.write(imports)
    file.write(doc_beginning)
    file.write(title)
    file.write(ac_hp_speed)
    file.write(ability_scores)
    file.write(sk_dmi_sns_etc)
    file.write(column_break)
    file.write(abilities_syn)
    file.write(doc_ending)


# compile it into pdf ------------------------------
subprocess.run(['pdflatex','chaos_monster.tex'])

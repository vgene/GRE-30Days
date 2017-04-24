#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pickle
import os
from termcolor import colored
from random import randint
import shutil
import progressbar
import getch

def parse_word(path):
    words = open(path,'r')
    words = words.readlines()
    word_db = []
    for line in words:
        word, exp = line.split('\t')
        word_db.append({'word':word, 'explanation':exp})
    return {'tolearn':word_db, 'learning':[], 'learnt':[]}

def recite_word(word):
    columns = shutil.get_terminal_size().columns
    print(colored(word['word'].center(columns),'green'))
    print(colored('(0-5)?'.center(columns),'white','on_grey'))
    count_down = int(getch.getch())
    print(colored(word['explanation'].center(columns),'yellow'))
    if (count_down >= word['cycle']):
        input(('Congratulation! Word '+word['word'] + ' has been learnt').center(columns))
        return ['learnt']

    #ch = input('\'m\' to make a memo,\'q\' to quit, other keys to continue')
    print(colored("m,q,other".center(columns),'white','on_grey'))
    ch = getch.getch()

    if (ch == "m"):
        memo = input('Input Memo:')
        return ['memo',count_down,memo]
    if (ch == "q"):
        return ["quit",count_down]
    else:
        return ["continue",count_down]

def reciting(word_db, learning_word_count, learning_cycle): 
    
    for key in word_db.keys():
        print(key+' word count:', len(word_db[key]))

    columns = shutil.get_terminal_size().columns
    rows = shutil.get_terminal_size().lines

    # move word from tolearn to learning
    def more_word():
        print(colored('Wow! A new set of words! Let\'s continue!','blue').center(columns))
        while (len(word_db['learning']) < learning_word_count):
            if len(word_db['tolearn']) >= 0:
                index = randint(0,len(word_db['tolearn'])-1)
                item = word_db['tolearn'].pop(index)
                item['cycle'] = learning_cycle
                word_db['learning'].append(item)

    while (True):
        if (len(word_db['learning']) <= 0):
            more_word()
        index = randint(0,len(word_db['learning'])-1) 
        #print(index)
        word = word_db['learning'][index]

        os.system('cls' if os.name == 'nt' else 'clear')
        bar = ""
        bar = str(learning_word_count-len(word_db['learning']))+'/'+str(learning_word_count)+' '
        for i in range(0,learning_word_count):
            if (i < learning_word_count-len(word_db['learning'])):
                bar += '█' 
            else:
                bar += '-'
        print(bar.center(columns))
        for i in range(0, int(rows/2 -1)):
            print()

        rtn = recite_word(word)

        if (rtn[0]== 'learnt'):
            word['cycle'] = 0
            word_db['learning'].pop(index)
            word_db['learnt'].append(word)
        elif (rtn[0] == 'quit'):
            word_db['learning'][index]['cycle'] -= rtn[1]
            break
        elif (rtn[0] == 'continue'):
            word_db['learning'][index]['cycle'] -= rtn[1]
        elif (rtn[0] == 'memo'):
            word_db['learning'][index]['cycle'] -= rtn[1]
            word_db['learning'][index]['memo'] = rtn[2]
    
    print("Save learning status in "+pkl_path)    
    pickle.dump(word_db,open(pkl_path,'wb')) 

if __name__ == "__main__":
    
    user = input("User:")
    pkl_path = "./words_"+user+".pkl"

    if os.path.isfile(pkl_path):
        word_db = pickle.load(open(pkl_path,'rb'))
    else:
        dbpath = './words.txt'
        word_db = parse_word(dbpath)
        pickle.dump(word_db,open(pkl_path,'wb'))
    try:
        learning_word_count = int(input('Learning Word Count:'))
        learning_cycle = int(input('Learnig Cycle:'))
    except Exception as e:
        print("Use default setting!")
        print("Learning Word Count: 20")
        print("Learning Cycle: 5")
        learning_word_count = 20
        learning_cycle = 5
    reciting(word_db, learning_word_count, learning_cycle)

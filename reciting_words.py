#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pickle
import os
from termcolor import colored
from random import randint
import shutil
import getch
import subprocess
import time

def say(text):
    subprocess.call('say "' + text +'"', shell=True)

def parse_word(path):
    words = open(path,'r')
    words = words.readlines()
    word_db = []
    for line in words:
        word, exp = line.split('\t')
        word_db.append({'word':word, 'explanation':exp})
    return {'tolearn':word_db, 'learning':[], 'learnt':[]}

def get_similar(search_str, db, method='sem'):
    s_list = []

    def get_similar_in_list(l):
        s_list = []
        for item in l:
            word_str = item['word']
            if ('f' in method):
                if (search_str == word_str):
                    s_list.append(item)
            elif ('m' in method):
                if (search_str in word_str):
                    s_list.append(item)
            else:
                if ('s' in method):
                    if(word_str.startswith(search_str)):
                        s_list.append(item)
                if ('e' in method):
                    if (word_str.endswith(search_str)):
                        s_list.append(item)
        return s_list

    for l in db:
        s_list += get_similar_in_list(db[l])

    print(len(s_list))
    return s_list

def recite_word(word, word_db):
    columns = shutil.get_terminal_size().columns
    print(colored(word['word'].strip().center(columns),'green'))
    say(word['word'])

    print(colored('(0-5)?'.center(columns),'white','on_grey'))

    try:
        count_down = int(getch.getch())
        assert count_down<=5 and count_down>=0
    except Exception as e:
        print("Invalid input, set count down as 0")
        count_down = 0

    print(colored(word['explanation'].strip().center(columns),'yellow'))
    say(word['word'])
    # say(word['explanation'])

    if ('memo' in word.keys() and word['memo'] != ""):
        print(colored(word['memo'].center(columns),'blue','on_grey'))
    if (count_down >= word['cycle']):
        input(('Congratulation! Word '+word['word'] + ' has been learnt').center(columns))
        return ['learnt']

    while (1):
        #ch = input('\'m\' to make a memo,\'q\' to quit, other keys to continue')
        print(colored("m,p,q,s,enter".center(columns),'white','on_grey'))
        ch = getch.getch()
        if (ch == "p"):
            say(word['word'])
        elif (ch == "m"):
            memo = input('Input Memo:')
            return ['memo',count_down,memo]
        elif (ch == "q"):
            return ["quit",count_down]
        elif (ch == "s"):
            try:
                search_str = input("Input search str, and mode('f', 's','e' or 'm'): ")
                search_str, mode = search_str.split(',')
                print("Search for ",search_str," with mode ", mode)
                word_list = get_similar(search_str, word_db, mode)
                for word in word_list:
                    # print(word)
                    print(word['word'], word['explanation'])
            except Exception as e:
                print("Wrong arguments")
                continue
        else:
            return ["continue",count_down]

def reciting(word_db, learning_word_count, learning_cycle):

    def more_word():
        print(colored('Wow! A new set of words! Let\'s continue!','blue').center(columns))
        while (len(word_db['learning']) < learning_word_count):
            if len(word_db['tolearn']) >= 0:
                index = randint(0,len(word_db['tolearn'])-1)
                item = word_db['tolearn'].pop(index)
                item['cycle'] = learning_cycle
                word_db['learning'].append(item)

    try:
        for key in word_db.keys():
            print(key+' word count:', len(word_db[key]))

        columns = shutil.get_terminal_size().columns
        rows = shutil.get_terminal_size().lines

        # move word from tolearn to learning

        start_time = time.time()
        while (True):
            if (len(word_db['learning']) <= 0):
                pickle.dump(word_db,open(pkl_path,'wb'))
                os.system('cls' if os.name == 'nt' else 'clear')
                print("This round costs %s seconds" %str(time.time() - start_time))
                print("Learnt Count:",len(word_db[
                    'learnt']))
                print("To learn count:",len(word_db['tolearn']))
                input("Continue?")
                more_word()
                start_time = time.time()
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
            for i in range(0, int(rows/2 -3)):
                print()

            rtn = recite_word(word, word_db)

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
    except Exception as e:
        print("Something is wrong. Save learning status in "+pkl_path)
        pickle.dump(word_db,open(pkl_path,'wb'))
        return e

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

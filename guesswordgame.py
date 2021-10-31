# class project - 27.10.2021
# guess game
import random
import time

def welcome_to_game():
    print('***************** welcome to guess the word game! *****************\ncorrect guess - 5 points!\nevery mistake drops 1 point!\nif guess is right, bonus == 100 points! ;)')
    time.sleep(3)
    print('READY')
    time.sleep(1)
    print('SET')
    time.sleep(1)
    print('GO!')
    time.sleep(1)

def lists_of_words(x = random.randint(0,9)):
    words = [['always', 'be', 'yourself'], ['keep', 'it', 'cool'], ['just', 'do', 'it'],
             ['yes', 'we', 'can'], ['go', 'for', 'it'], ['i', 'love', 'python'], ['we', 'are', 'champions'],
             ['one', 'two', 'three'], ['keep', 'it', 'simple'], ['keep', 'calm', 'tea'], ]
    return words[x]

def timer():
    return time.time()

def game(words):
    score = 0
    letter = ""
    ans = " ".join(words)
    for j in range(3):
        letter = letter+('_'*len(words[j]))+' '
    while True:
        print(letter)
        print(f'your score is: {score}')
        guess = input('guess a letter!: ')
        if guess == " " or len(guess) > 1: continue
        elif guess.isalpha() and guess in ans:
            print('right guess!')
            score += 5
            letter = list(letter)
            for k in range(len(ans)):
                if ans[k] == guess: letter[k] = guess
                else: pass
            letter = "".join(letter).rstrip()
            if letter == ans: break
        else:
            print('wrong!')
            score -= 1
            if score < 0: score = 0
    return score, time.time()

def final_score(totaltime, score, answer):
    print(f'game over! the words is: "{" ".join(answer)}". you have guessed in {int(totaltime)} seconds')
    if totaltime < 30: print(f'*************************************************\n************** final score is: {score + 100} **************\n*************************************************')
    else: print(f'*************************************************\n************** final score is: {score} **************\n*************************************************')

def main():
    welcome_to_game()
    s_time = time.time()
    answer = lists_of_words()
    score, end_time = game(answer)
    final_score(end_time - s_time, score, answer)

main()
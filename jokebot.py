import time
import csv
import sys
import os
import requests

class Jokebot:

    def __init__(self, file = None):
        if file == None:
            self.joke_list = self.use_reddit()
        else:
            self.joke_list = self.read_csv(file)

        self.run_jokebot()

    #tells joke when given prompt and punchline
    def tell_joke(self, prompt, punchline):
            print(prompt)
            time.sleep(2)
            print(punchline)
    #reads user input
    def read_input(self):
        user_input = input()
        if user_input == "next":
            return True
        elif user_input == "quit":
            return False
        else:
            print('Please type either "next" or "quit"!')
            return self.read_input()

    #reads csv file and creates joke_list
    def read_csv(self,csv_file):
        joke_list = []
        with open(os.path.dirname(os.path.abspath(__file__)) + "/" + csv_file) as f:
            reader = csv.reader(f)
            for line in reader:
                joke_list.append(line)
        return joke_list

    #makes jokebot tell jokes
    def run_jokebot(self):
        joke_spitter = iter(self.joke_list)
        print("hello, I'm jokebot!")
        print("Type 'next' to hear a joke :-)")
        while self.read_input():
            try:
                joke = next(joke_spitter)
                self.tell_joke(joke[0], joke[1])
            except:
                print("sorry! out of jokes")

    #filters and stores reddit jokes in joke_list
    def use_reddit(self):
        r = requests.get("https://www.reddit.com/r/dadjokes.json", headers = {'User-agent': 'your bot 0.1'})
        data = r.json()
        jokes = []
        for joke in data['data']['children']:
            prompt = joke['data']['title']
            punchline = joke['data']['selftext']
            if not joke['data']['over_18'] and self.valid_question(joke['data']['title']):
                jokes.append([prompt, punchline])
        return jokes

    #use_reddit helper function - returns whether a prompt is valid or not
    def valid_question(self, prompt):
        lower = prompt.lower()
        return lower.startswith("what") or lower.startswith("how") or lower.startswith("why")

if __name__ == "__main__":
    
    inputs = sys.argv

    if len(inputs) == 1:
        Jokebot()
        
    elif len(inputs) == 2:
        Jokebot(inputs[1])
    
    else:
        print('invalid input. Please input a valid jokes file.')
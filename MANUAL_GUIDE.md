### Features:

- Basic Queries
- IIT Mandi Freshers' Queries
- Programming Queries
- Weather
- Audio MODE
- Replying to specific messages(see [image](https://i.stack.imgur.com/EewCe.png))
- Random choice(Roll a dice or coin toss)
- Link to related page for detailed answer(along with the bot's normal answer)


### Database:
- similar questions are in one class

- each question can have multiple patterns

- class is identified using patterns


### Model:
- Using Gensim library

- calculating minimum err for each class

- calculating unknown words

- minimizing error for each class

- finding the correct class

- finding correct question by question matching



### How to Run:

- Install dependencies via

`pip3 install -r requirements.txt`

- Install FFMPEG

`sudo apt install ffmpeg`

- Download the file [here](https://drive.google.com/file/d/1UosU4oEUXa-Yc2VZX3nTV6NNCH1BgxUw/view?usp=sharing)(~331 MB)

- To run,

`python3 main.py`


### References:

[1] https://github.com/stanfordnlp/GloVe

[2] https://core.telegram.org/bots/api

[3] https://www.codementor.io/@karandeepbatra/part-1-how-to-create-a-telegram-bot-in-python-in-under-10-minutes-19yfdv4wrq

[4] https://www.codementor.io/@karandeepbatra/part-2-deploying-telegram-bot-for-free-on-heroku-19ygdi7754

[5] https://chatbotslife.com/full-tutorial-on-how-to-create-and-deploy-a-telegram-bot-using-python-69c6781a8c8f

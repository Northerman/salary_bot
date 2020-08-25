from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

# Creating ChatBot Instance
chatbot = ChatBot('northerman')
trainer_corpus = ChatterBotCorpusTrainer(chatbot)
trainer_corpus.train('chatterbot.corpus.english')


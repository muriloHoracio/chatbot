import sys
import io
import numpy as np
import random
import string
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import psycopg2
import psycopg2.extras
import warnings
warnings.filterwarnings('ignore')

if len(sys.argv) != 3:
    print("Por favor insira o nome do usuário postgresql que tenha acesso ao banco chatbot e a senha como argumentos do programa\nO banco de dados pode ser restaurado através do arquivo chatbot_db.sql\n\nExemplo: python3 chatbot.py admin admin\n")
    exit(-1)
else:
    USER = sys.argv[1]
    PASSWORD = sys.argv[2]

conn = psycopg2.connect("dbname=chatbot host=localhost user="+USER+" password="+PASSWORD)
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cursor.execute("SELECT * FROM chatbot_knowledge_base")

#loading knowledge base from db
knowledge_base = dict()
new_rules = dict()
for e in cursor.fetchall():
	knowledge_base[e[1]] = e[2]
cursor.close()

GREETINGS_INPUT = ("olá", "oi", "eaí",)
GREETINGS_RESPONSES = ["Olá, Tudo bem?", "Oi", "Eaí!"]
GOOD_BYE = ["tchau","até mais","até logo"]
THANKS = ["obrigado", "muito obrigado", "agradeço"]
NEGATIVE_FEEDBACK = ["não", "não sei", "também não sei"]
POSITIVE_FEEDBACK = ["sim", "claro", "com certeza", "positivo", "prontamente", "ok"]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

stemmer = nltk.stem.RSLPStemmer()

def stem_tokens(tokens):
    return [stemmer.stem(token) for token in tokens]

def stem_normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

def greetings(entry):
    for word in entry.split():
        if word.lower() in GREETINGS_INPUT:
            return random.choice(GREETINGS_RESPONSES)

def get_distance_to_dict(sentence, collection):
    if type(collection) is type(dict()): 
        sent_tokens = [sent for sent in collection.keys()]
    elif type(collection) is type(list()):
        sent_tokens = collection
    sent_tokens.append(sentence.lower().translate(remove_punct_dict))

    sim_vec = TfidfVectorizer(tokenizer=stem_normalize, stop_words=nltk.corpus.stopwords.words('portuguese'))
    tfidf = sim_vec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]

    return sent_tokens, idx, req_tfidf


def response(user_entry):
    question = user_entry
    tokens, index, dist = get_distance_to_dict(user_entry, knowledge_base)
    if(dist<0.2):
        print("Sistema: Me desculpe! Não sei a resposta para esta pergunta... Você poderia informar uma resposta adequada?")
        user_entry = input("Cliente: ")
        feedback_tokens, feedback_idx, feedback_dist = get_distance_to_dict(user_entry, POSITIVE_FEEDBACK)
        if feedback_dist > 0.40:
            user_entry = input("Resposta: ")
            knowledge_base[question] = user_entry
            new_rules[question] = user_entry
            print("Sistema: Não sabia disso! Obrigado por me ensinar!")
            return
        print("Sistema: Que pena... Em que mais posso te ajudar?")
        return
    else:
        print("Sistema: "+knowledge_base[tokens[index]])
        print("Sistema: Você ficou satisfeito com essa resposta?")
        user_entry = input("Cliente: ")
        feedback_tokens, feedback_idx, feedback_dist = get_distance_to_dict(user_entry, POSITIVE_FEEDBACK)
        if feedback_dist > 0.40:
            print("Sistema: Ótimo! Em que mais posso te ajudar?")
            return
        else:
            print("Você poderia me ensinar uma resposta adequada para esta pergunta?")
            user_entry = input("Cliente: ")
            feedback_tokens, feedback_idx, feedback_dist = get_distance_to_dict(user_entry, POSITIVE_FEEDBACK)
            if feedback_dist > 0.40:
                user_entry = input("Resposta: ")
                knowledge_base[question] = user_entry
                new_rules[question] = user_entry
                print("Sistema: Não sabia disso! Obrigado por me ensinar!")
                return
            else:
                print("Sistema: Que pena... Em que mais posso te ajudar?")
                return

flag=True
print("Sistema: Olá! Com o que posso te ajudar?")
while(flag):
    user_entry = input("Cliente: ").lower()

    if(user_entry not in GOOD_BYE):
        if(user_entry in THANKS):
            flag=False
            print("Sistema: Não há de quê!")
        else:
            is_greeting = greetings(user_entry)
            if(is_greeting):
                print("Sistema: "+is_greeting)
            else:
                response(user_entry)
    else:
        flag=False
        print("Bot: Tchau, até mais! Se cuide!")

try:
    cursor = conn.cursor()
    sql = 'INSERT INTO chatbot_knowledge_base(question, answer) VALUES %s'
    data = [(new_entry, new_rules[new_entry]) for new_entry in new_rules]
    psycopg2.extras.execute_values(cursor, sql, data, template=None)
    conn.commit()
    cursor.close()
except (Exception, psycopg2.DatabaseError) as e:
    print(e)
finally:
    if conn is not None:
        conn.close()

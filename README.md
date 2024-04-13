# Verb lemmatizer for brazilian portuguese language

This program aims to give the infinitive form of a verb in a very fast and effective way on portuguese-BR texts.

## Quantitative information about the dataset

- Total number of verbs: **9,233**
- Number of regular verbs: **8,941**
- Number of irregular verbs: **292**
- Total number of verbal inflections: **3,419,728**

## Installation

This package is installed using the command "*pip install*"
```bash
pip install pt-br-verbs-lemmatizer
```
For more information about this package, see it on: [Pypi](https://pypi.org/project/pt-br-verbs-lemmatizer/)

## Usage Examples
This package was designed to be integrated with other NLP tools, in order to say if a word is or is not a verb we highly recommend you to use the spaCy lib model trained on portuguese corpus.

### Simple usage

```python
from pt_br_verbs_lemmatizer import lemmatize

verb = 'apresentava'

verb_lemma = lemmatize(verb)

print(verb_lemma)
```

Output:

```python
'apresentar'
```

### Execution time

```python
from pt_br_verbs_lemmatizer import lemmatize
import time

verb = 'apresentá-lo-ia'

t1 = time.time()

verb_lemma = lemmatize(verb)

time.sleep(0.1)

t2 = time.time()

duration = round((t2-t1-0.1),8)

print(verb_lemma)
print(f'Duration: {duration} seconds')
```

Output:

```python
'apresentar'
'Duration: 0.00047889 seconds'
```

## How it was built
- First of all we downloaded the [Base TeP 2.0 database](http://www.nilc.icmc.usp.br/tep2/), which gave us X number of verbs after filtering it. 
- After that we went to the list of most popular verbs used on portuguese present on https://www.conjugacao.com.br/verbos-populares/ and web scraped the 5000 verbs there.
- We compare to the list we had from the Base TeP 2.0, adding the ones who doesn't match.
- Then we start web scraping the inflections of all the verbs we got, also using the [conjugacao website](https://www.conjugacao.com.br).
- Some additional steps were taken during the scraping process, we add a bunch of inflections endins to be prepared for almost every cenario (except the wrong writening).
- Some examples of that is the female form of -lo, -o, -no, etc... which are -la, -a, -na, etc...
- Finally we start to build our dictionary architecture to store all that verbs and that could search into it very quickly. Then we just fill it, which is available at the folder "dataset".

_Observation: It is possible to find some wrong inflection verbs inside our dataset, we try out many ways to be highly prepared, but, as we don't have a portuguese grammar teacher on board, we may have committed some mistakes. But, just to be clear, we have more than just the common inflection verbs. If you notice any wrong word or some trouble during the execution of this package, please contact us!_

## Tests against the giant **[spaCy](https://spacy.io/)** - **[lemmatizer](https://spacy.io/api/lemmatizer)** - **[portuguese trained model](https://spacy.io/models/pt)**:
Now we are going to see some tests related to the results spaCy has in his lemmatization and the execution time to find that lemmatized verb, comparing to our program.

<details>
  <summary>Installing and importing spaCy process  <i>(click to expand)</i></summary>
  <br><br>
  
  ```bash
  pip install -U spacy
  pip install -U spacy-lookups-data
  python -m spacy download pt_core_news_lg
  
  import spacy
  nlp = spacy.load('pt_core_news_lg',enable=["tok2vec","lemmatizer","morphologizer"])
  ```
</details>

```python
from pt_br_verbs_lemmatizer import lemmatize

texto = '''Hoje vou jogar bola e espero que você esteja saindo com seus amigos também.
Gostaria de abrir a janela, será que você vê o céu? Quero apresentá-la para meus pais.
Eu tinha duas casas, agora só consigo ter uma. Eu apresentá-la-ia para vocês ontem!
Olhando para ele que observava ela.'''

doc = nlp(texto)

for token in doc:

if token.pos_ == 'VERB':
    print('Verb identified:',token.orth_)
    t1 = time.time()
    verb_lemma_spacy = token.lemma_
    time.sleep(0.1)
    t2 = time.time()

    duration_spacy = round((t2-t1-0.1),8)

    print('spaCy:',verb_lemma_spacy,duration_spacy,'seconds.')

    t1 = time.time()
    verb_lemma_mine = lemmatize(token.orth_)
    time.sleep(0.1)
    t2 = time.time()

    duration_mine = round((t2-t1-0.1),8)
    
    print('Mine:',verb_lemma_mine,duration_mine,'seconds.')

    print('-'*40)
```
<details>
  <summary>Full Output  <i>(click to expand)</i></summary>
  <br><br>
  
  ```python
  '''Verb identified: jogar
    spaCy: jogar 0.00021591 seconds.
    Mine: jogar 0.00191703 seconds.
    ----------------------------------------
    Verb identified: espero
    spaCy: esperar 0.00014153 seconds.
    Mine: esperar 0.00021949 seconds.
    ----------------------------------------
    Verb identified: saindo
    spaCy: sair 0.00013509 seconds.
    Mine: sair 0.0001792 seconds.
    ----------------------------------------
    Verb identified: Gostaria
    spaCy: Gostaria 0.00014081 seconds.
    Mine: gostar 0.00018969 seconds.
    ----------------------------------------
    Verb identified: abrir
    spaCy: abrir 0.0001389 seconds.
    Mine: abrir 0.00023022 seconds.
    ----------------------------------------
    Verb identified: será
    spaCy: ser 0.00020018 seconds.
    Mine: ser 0.00017014 seconds.
    ----------------------------------------
    Verb identified: vê
    spaCy: ver 6.261e-05 seconds.
    Mine: ver 0.00018539 seconds.
    ----------------------------------------
    Verb identified: Quero
    spaCy: querer 0.00096145 seconds.
    Mine: querer 0.0001966 seconds.
    ----------------------------------------
    Verb identified: apresentá-la
    spaCy: apresentá-la 0.00013962 seconds.
    Mine: apresentar 0.00027146 seconds.
    ----------------------------------------
    Verb identified: tinha
    spaCy: ter 0.00013342 seconds.
    Mine: ter 0.00016847 seconds.
    ----------------------------------------
    Verb identified: consigo
    spaCy: consigo 0.00016179 seconds.
    Mine: conseguir 0.00019159 seconds.
    ----------------------------------------
    Verb identified: ter
    spaCy: ter 0.00014439 seconds.
    Mine: ter 0.00023308 seconds.
    ----------------------------------------
    Verb identified: apresentá-la-ia
    spaCy: apresentá-la-ia 5.569e-05 seconds.
    Mine: apresentar 0.00023594 seconds.
    ----------------------------------------
    Verb identified: Olhando
    spaCy: Olhando 0.00017633 seconds.
    Mine: olhar 0.00023808 seconds.
    ----------------------------------------
    Verb identified: observava
    spaCy: observar 0.00013556 seconds.
    Mine: observar 0.00020494 seconds.
    ----------------------------------------'''
  ```
</details>

So, as we can see, although spaCy has better searching times (but we are very close to it), many times it mistakes the lemmatized verbs. To be honest, for my personal tests, almost every time a verb has hyphen "-" spaCy starts to make some confusion. 

I want to make it clear: spaCy is one of, if not the, best NLP library available at the moment. What I tried to do was improve the replacements of the inflected verb for the infinitive verb. So, if you want to lemmatize your verbs with much more accuracy I suggest you mix the spaCy and **pt-br-verbs-lemmatizer** to get the bests results on your portuguese-BR texts!

### Tokenizing using spaCy's lemmatizer

```python
texto = '''Tem-se que ter muito cuidado com isso. Tu recomendarias o que? 
Ele apresentava-se como queria. Foi bom tê-lo por perto!
Tu fosse no show ontem? Eu estava olhando e apreciava-a muito.
Esperava-se que ele chegaria mais cedo.'''

doc = nlp(texto)

tokenization = []

print('Verbs:')

t1 = time.time()

for token in doc:
token_text = token.orth_
if not (token.is_punct or token.is_space):
    if token.pos_ == 'VERB':
    print(token_text)
    token_text = token.lemma_
    tokenization.append(token_text.lower())

t2 = time.time()

print('\n')
print(tokenization)
print(f'\nTime: {t2-t1}')
```

Output:

```python
'''Verbs:
  Tem-se
  ter
  Tu
  apresentava-se
  queria
  tê-lo
  olhando
  apreciava-a
  Esperava-se
  chegaria'''


  ['tem-se', 'que', 'ter', 'muito', 'cuidado', 'com', 'isso', 'tu', 
  'recomendarias', 'o', 'que', 'ele', 'apresentar se', 'como', 'querer', 
  'foi', 'bom', 'ter ele', 'por', 'perto', 'tu', 'fosse', 'no', 'show', 
  'ontem', 'eu', 'estava', 'olhar', 'e', 'apreciava-r', 'muito', 'esperava-se', 
  'que', 'ele', 'chegar', 'mais', 'cedo']

  'Time: 0.0021452903747558594'
```

### Tokenizing using our lemmatizer

```python
texto = '''Tem-se que ter muito cuidado com isso. Tu recomendarias o que? 
Ele apresentava-se como queria. Foi bom tê-lo por perto!
Tu fosse no show ontem? Eu estava olhando e apreciava-a muito.
Esperava-se que ele chegaria mais cedo.'''

doc = nlp(texto)

tokenization = []

print('Verbs:')

t1 = time.time()

for token in doc:
token_text = token.orth_
if not (token.is_punct or token.is_space):
    if token.pos_ == 'VERB':
    print(token_text)
    token_text = lemmatize(token_text)
    tokenization.append(token_text.lower())

t2 = time.time()

print('\n')
print(tokenization)
print(f'\nTime: {t2-t1}')

```

Output:

```python
'''Verbs:
  Tem-se
  ter
  Tu
  apresentava-se
  queria
  tê-lo
  olhando
  apreciava-a
  Esperava-se
  chegaria'''


  ['ter', 'que', 'ter', 'muito', 'cuidado', 'com', 'isso', 'tu', 
  'recomendarias', 'o', 'que', 'ele', 'apresentar', 'como', 'querer', 
  'foi', 'bom', 'ter', 'por', 'perto', 'tu', 'fosse', 'no', 'show', 
  'ontem', 'eu', 'estava', 'olhar', 'e', 'apreciar', 'muito', 'esperar', 
  'que', 'ele', 'chegar', 'mais', 'cedo']

  'Time: 0.0023202896118164062'
```

_The time is not suppose to be so exact for these cases. For more exact statistic we may try it out much more times and make a mean, for example._

### Some verbs weren't found, but we would lemmatize then properly:

```python
print(lemmatize('recomendarias'))
print(lemmatize('tê-lo'))
print(lemmatize('fosse'))
print(lemmatize('estava'))
print(lemmatize('apreciava-a'))
```

Output:

```python
'''recomendar
    ter
    ir
    estar
    apreciar'''
```

## Authors

- [@IgorCaetano](https://github.com/IgorCaetano)

## Used by

- This project is used in the text pre-processing stage in the **[WOKE](https://github.com/iaehistoriaUFSC/Repositorio_UFSC)** project of the Grupo de Estudos e Pesquisa em IA e História ("Study and Research Group on AI and History") at UFSC ("Federal University of Santa Catarina").

# Special credits to:
- **[Base TeP 2.0 database](http://www.nilc.icmc.usp.br/tep2/)**
 
- **[conjucagao.com.br website](https://www.conjugacao.com.br/)**

# References

DIAS-DA-SILVA, B.C.; MORAES, H.R.; OLIVEIRA, M.F.; HASEGAWA, R.; AMORIM, D.A.; PASCHOALINO, C.; NASCIMENTO, A.C. (2000). Construção de um thesaurus eletrônico para o português do Brasil. PROCESSAMENTO COMPUTACIONAL DO PORTUGUÊS ESCRITO E FALADO (PROPOR), Vol. 4, pp. 1-10.
 
DIAS-DA-SILVA, B.C.; MORAES, H.R. (2003). A construção de um thesaurus eletrônico para o português do Brasil. ALFA, Vol. 47, N. 2, pp. 101-115.  
MAZIERO, E.G.; PARDO, T.A.S.; DI FELIPPO, A.; DIAS-DA-SILVA, B.C. (2008). A Base de Dados Lexical e a Interface Web do TeP 2.0 - Thesaurus Eletrônico para o Português do Brasil. VI WORKSHOP EM TECNOLOGIA DA INFORMAÇÃO E DA LINGUAGEM HUMANA (TIL), pp. 390-392.  
OLIVEIRA H.G.; Santos D.; Gomes P. (2008). Extracção de relações semânticas entre palavras a partir de um dicionário: primeira avaliação. ENVIADO PARA APRECIAÇÃO A LINGUAMÁTICA 3 (2010).  
BARROS, C. D. Antonímia nos adjetivos descritivos do português do Brasil: uma proposta de análise e representação. 2010. 89 f. Dissertação (Mestrado em Linguística) – Universidade Federal de São Carlos, São Carlos, 2010.
 
VERBOS. In: CONJUGAÇÃO. 7Graus, c2024. Disponível em: https://www.conjugacao.com.br/verbos-populares/. Acesso em: 11 abril 2024.

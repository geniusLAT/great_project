print("ai - ok")

from transformers import pipeline


example_prompt='''Ты гид по городу. Напиши полный адрес и название заведения.  Турист спрашивает:Где находится стоматология?
    '''
example_context='''

   
Президиум УрО РАН,  Первомайская улица  91
 Институт математики и механики УрО РАН,  улица Софьи Ковалевской  16
 Институт машиноведения УрО РАН,  Комсомольская улица  34
 Институт физики металлов УрО РАН,  улица Софьи Ковалевской  18
 Институт иммунологии и физиологии,  Первомайская улица  106
 Институт высокотемпературной электрохимии УрО РАН,  Академическая улица  20
 Уральский государственный юридический университет,  Комсомольская улица  23
 Уральский государственный юридический университет,  Комсомольская улица  21
 Общежитие №1 УЭМЗ,  Студенческая улица  24
 Средняя школа,  Студенческая улица  26
 Начальная школа,  Студенческая улица  26
 ТЦ Современник,  улица Блюхера  32
 Экспериментальная База,  улица Блюхера  28
 Стоматологическая поликлиника N12,  улица Данилы Зверева  9А
 Жилконтора паспортный стол,  улица Блюхера  49Б
 Общежитие УралГАХА,  Садовая улица  22
 Блиц,  улица Сулимова  27
 ТК Парус,  улица Сулимова  26
 ЦК «Урал»,  Студенческая улица  3
 СК «Урал»,  Комвузовская улица  9
 Магнит,  Боровая улица  22
 Общежитие УрГСХА,  Июльская улица  16
 Общежитие УрГСХА,  Июльская улица  16
 Общежитие УрГСХА,  Июльская улица  20
 Галерея 11,  Студенческая улица  11
 ЖК \Даниловский\,  улица Данилы Зверева  17А
 ГИБДД Кировского района,  улица Раевского  9
 Специальное управление Федеральной Противопожарной Службы № 49 МЧС России ГУ,  улица Раевского  11
 Клиника УНИИТО,  Студенческая улица  12
 Невьянский машиностроительный завод,  переулок Автоматики  8
 Подземный гараж,  Советская улица  52А
 Baku Plaza,  улица Сулимова  21
 Гимназия №35,  Уральская улица  79
 ЖК \Даниловский-2\,  улица Данилы Зверева  11
 ЖК \Культура\,  Советская улица  45'''

def request_AI(request, places):
    prompt='Ты гид по городу. Напиши полный адрес и название заведения. Турист спрашивает:'+request
    context=places
    result=''

    try:
        result=process(prompt,context)
    except:
        return "Ошибка."

    return result

def process(prompt,context):
    qa_model = pipeline("question-answering", "timpal0l/mdeberta-v3-base-squad2")
    question = prompt#"Where do I live?"
    context = context#"My name is Tim and I live in Sweden."
    answer=qa_model(question = question, context = context)
    print(answer)
    print(answer['answer'])
    return answer['answer']

#process(example_prompt,example_context)
'''
#

import requests
import pydantic

from datetime import datetime, date, time


# URL для запроса к Yandex GPT
YGPT_URL: str = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'


# Модели данных для запросов
class YGPTCompletionOptionsReq(pydantic.BaseModel):
    stream: bool
    temperature: float
    maxTokens: int

class YGPTMessageReq(pydantic.BaseModel):
    role: str
    text: str

class YGPTRequest(pydantic.BaseModel):
    modelUri: str
    completionOptions: YGPTCompletionOptionsReq
    messages: list[YGPTMessageReq]
    
# Модели данных для ответов
class YGPTMessageRes(pydantic.BaseModel):
    role: str 
    text: str

class YGPTAlternativeRes(pydantic.BaseModel):
    message: YGPTMessageRes
    status: str
    
class YGPTUsageRes(pydantic.BaseModel):
    completionTokens: str
    inputTextTokens: str
    totalTokens: str
    
class YGPTResultRes(pydantic.BaseModel):
    alternatives: list[YGPTAlternativeRes]
    modelVersion: str 
    usage: YGPTUsageRes
    
class YGPTResponse(pydantic.BaseModel):
    result: YGPTResultRes
    
    
# Определение контекста для истории сообщений
history = list()
    

# Метод отправки запросов к модели
def ygpt_send_question(question: str) -> str:

    if not question:
        return ""
    
    comp_options = YGPTCompletionOptionsReq(
        stream=False,
        temperature=0,
        maxTokens=1000
    )

    # Тут надо указать каталог пользователя
    # И еще тут указывается тип модели
    # Подробнее - https://cloud.yandex.ru/docs/yandexgpt/concepts/models
    ygpt_req = YGPTRequest(
        modelUri='gpt://<каталог>/yandexgpt-lite',
        completionOptions=comp_options,
        messages=history
    )
        
    # Если запускается в первый раз, то добавить определение модели
    if not len(history):
        # Создание системного сообщения для модели
        # Тут настраивается промт для самоопределения модели
        msg_system = YGPTMessageReq(
            role='system',
            text='Ты - справочник по <тема>.'
        )
        list.append(history, msg_system)
        ygpt_req.messages.append(msg_system)

    # Добавляется вопрос пользователя
    msg_user = YGPTMessageReq(
        role='user',
        text=question
    )
    list.append(history, msg_user)
    ygpt_req.messages.append(msg_user)
    
    # Тут указать API ключ
    headers = {'Authorization': 'Api-Key AQVNwbGOjHNJs9qHSXcXfQhyub6NXcRSxUxcTmsn'}

    DUMP=ygpt_req.model_dump()

    print(DUMP)

    response = requests.post(YGPT_URL, 
                             headers=headers,
                             json=DUMP)

    print(response.text)
    
    ygpt_res = YGPTResponse.model_validate_json(response.text)
    
    # Ничего не вернула
    if len(ygpt_res.result.alternatives) == 0:
        return "" 
    
    # Добавление ответа в историю
    msg_assistant = YGPTMessageReq(
        role='assistant',
        text=ygpt_res.result.alternatives[0].message.text
    )
    list.append(history, msg_assistant)    
    
    return ygpt_res.result.alternatives[0].message.text




# Можно копировать этот код или вызвать какое то количество раз
# Тогда будет подобие диалога
#question = input("Введите вопрос: ")
question ='Кто изобрёл велосипед?'
print(f'-> Вопрос для Яндекс.GPT: {question}')
print(f'-> Ответ Яндекс.GPT: \n{ygpt_send_question(question)}', end='\n\n')
'''
print("ai - ok")



def request_AI(request, places):
    prompt='Ты гид по городу. Турист спрашивает:'+request+'''
    

    Используй в своём ответе следующие данные:
    '''+places

    result=''

    try:
        result=process(prompt)
    except:
        return "Ошибка."

    return result

def process(prompt):
    return prompt
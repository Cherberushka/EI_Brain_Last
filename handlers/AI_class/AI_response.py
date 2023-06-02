import openai


# Обработка ответа GPT AI_class
async def ai_response(data, text):
    # await message.answer_chat_action("typing")
    history = []
    if len(data) > 1:
        for index in range(0, len(data)):
            if data[index].get('question') is None:
                data[index]['question'] = text
                d = {"role": "user", "content": data[index]['question']}
                history.append(d)
            else:
                d = [#{"role": "system",
                      #"content": "Вы - психолог, к которому пришел пациент, вы должны дать ему подробный ответ, что можно сделать в случае его проблемы"},
                     {"role": "user",
                      "content": "Ответь в режиме психолога, но не советуй обратиться к специалисту, а разберись сам, на какой психологический аспект личности мне стоит обратить внимание, когда я задаюсь следующим вопросом:" +
                                 data[index]['question']},
                     {"role": "assistant", "content": data[index].get('answer')}]
                history += d
    else:
        data[0]['question'] = text
        # d = {"role": "user",
        #      "content": "Перейди в режим психолога и сформулируй вопрос для психологической консультации из следующего, но не советуй посетить специалиста, а попробуй разобраться сам: " +
        #                 data[0].get(
        #                     'question') + " Твой вопрос должен начинаться с 'Правильно ли я понимаю', а дальше твои рассуждения, в каком психологическом аспекте необходимо помочь пользователю"}
        d = {"role": "user",
             "content": "Ответь в режиме психолога, но не советуй обратиться к специалисту, а разберись сам, на какой психологический аспект личности мне стоит обратить внимание, когда я задаюсь следующим вопросом: " +
                        data[0].get(
                            'question')}
        history.append(d)
    print(history)
    request = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=history,
        max_tokens=1500,
        temperature=1,
    )
    resp_ai = request['choices'][0]['message']['content']
    return resp_ai
from openai import OpenAI

def requestGptAPI(text):
    print("requestGptAPI is called")
    mygptkey = "mygptkey"

    client = OpenAI(
        api_key=mygptkey,
    )

    my_msg = [
        {
            "role" : "user",
            "content" : "techCrunch사이트의 글을 제공할거야. 해당 글에 대한 블로그 리뷰글을 한글로 써줘",
        },
        {
            "role": "user",
            "content": "본문의 글을 단순히 번역하지 말고, 한글로 사람의 견해가 들어간 것처럼 써줘",
        },
        {
            "role": "user",
            "content": "리뷰글 답변의 가장 첫 문장은 리뷰글의 한글로 제목을 줘. 그리고 제목은 항상 마침표로 끝맺음 되게 해줘."
        }
    ]

    for t in text:
        my_msg.append(
            {
                "role":"user",
                "content":t

            }
        )
    #model="gpt-3.5-turbo"
    #model="gpt-4"
    #gpt 한테 메시지를 보내는 함수

    chat_completion = client.chat.completions.create(
        messages= my_msg,
        model="gpt-3.5-turbo"
    )
    #gpt api를 요청했을 때 사용된 토큰
    prompt_token = chat_completion.usage.prompt_tokens
    #요청을 보내서 반환을 받은 답변큰 사용된 토
    completion_token = chat_completion.usage.completion_tokens


    print("prompt token : ", prompt_token)
    print("completion token : ", completion_token)

    gpt3_5turbo_input_price = 0.15
    gpt3_5turbo_output_price = 0.6

    input_cost = (prompt_token/1000000) * gpt3_5turbo_input_price
    output_cost = (completion_token/1000000) * gpt3_5turbo_output_price

    total_cost = input_cost + output_cost

    print(f"gpt3.5 usage cost : ${total_cost: .6f}" )


    return chat_completion.choices[0].message.content
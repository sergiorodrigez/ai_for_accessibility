from openai import OpenAI # type: ignore

class OpenAIConnection:
    client = OpenAI(api_key = "sk-proj-hpNDG9gSmUufEruSb8uRT3BlbkFJ1eQN9iwjoJHF337BSAzk")

    @staticmethod
    def first_questions():
        print("What's your name?")
        name = input("")
        print("What would you like to express today?")
        express = input("")
        messages=[
            {
            "role": "system",
            "content": "To effectively gather information on an idea or experience, it's important to analyze the preceding conversation for continuity. Develop questions that encourage specific and detailed yet concise responses. Structure your inquiries to receive answers limited to one or two words. Never ask for descriptions of any kind; instead, ask questions designed to be answered in no more than two words. Following the initial question, \"What would you like to express today?\", proceed with \"What type of {previous answer} would you like to share?\". If the user is describing an experience, always make sure to ask when and where (in different questions). Always have in mind that these questions are meant to facilitate the creation of a narrative based on the shared experiences or ideas (the narrative creation itself is not required here, don't do it). Gather as much information as you can, names, places, feelings etc. Continuously evaluate the need for additional information. If no further details are necessary, end with the question, \"Would you like to add anything else?\" if the answer is yes,, you will eventually have to ask this again until the answer is no, ensure to ask at least twenty questions (counter={count number of previous answers}), or more if necessary. If the answer to the final question is no, respond with \"Thanks {name} for you time.\" Don't include the previous answers in the questions. After the first question ('What's your name?') the second question always has to be: 'What would you like to express today?'"
            },
            {
            "role": "assistant",
            "content": "What's your name?"
            },
            {
            "role": "user",
            "content": name
            },
            {
            "role": "assistant",
            "content": "What would you like to express today?"
            },
            {
            "role": "user",
            "content": express
            }
        ]
        final_messages=[
            {
            "role": "system",
            "content": "In this task, you'll find a conversation where the assistant is collecting details about a specific topic. Please synthesize all the discussed information into a first-person narrative paragraph as if you were the one answering the questions. Begin the paragraph directly, without introductory phrases like 'based on the information' or 'with the provided information,' etc."
            },
            {
            "role": "assistant",
            "content": "What's your name?"
            },
            {
            "role": "user",
            "content": name
            },
            {
            "role": "assistant",
            "content": "What would you like to express today?"
            },
            {
            "role": "user",
            "content": express
            }
        ]
        return messages, final_messages, name

    @staticmethod
    def update_messages(messages, final_messages, question, answer):
        messages.append({
            "role": "assistant",
            "content": question
        })
        messages.append({
            "role": "user",
            "content": answer
        })
        final_messages.append({
            "role": "assistant",
            "content": question
        })
        
        final_messages.append({
            "role": "user",
            "content": answer
        })
        
        return messages, final_messages

    @staticmethod
    def create_paragraph(messages):
        response = OpenAIConnection.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=1,
            max_tokens=4096,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        paragraph = response.choices[0].message.content
        return paragraph

    @staticmethod
    def conversation1():
        messages, final_messages, name = OpenAIConnection.first_questions()
        while True:
            response = OpenAIConnection.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=1,
                max_tokens=4096,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            
            question = response.choices[0].message.content
            print(question)
            if question == f"Thanks {name} for your time.":
                break
            answer = input("")
            messages, final_messages = OpenAIConnection.update_messages(messages, final_messages, question, answer)
            
        return OpenAIConnection.create_paragraph(final_messages)
    
    @staticmethod
    def last_question(json):
        response = OpenAIConnection.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=json,
            temperature=1,
            max_tokens=4096,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        
        question = response.choices[0].message.content
        
        return question
    
    @staticmethod
    def conversation(conversation, json, final_json, question, answer):
        
        # Update dictionary
        conversation[question] = answer
        
        # Update JSON
        json.append({
            "role": "assistant",
            "content": question
        })
        json.append({
            "role": "user",
            "content": answer
        })
        final_json.append({
            "role": "assistant",
            "content": question
        })
        final_json.append({
            "role": "user",
            "content": answer
        })
        
        question = OpenAIConnection.last_question(json) 
        
        return conversation, json, final_json, question
                            
    def initialize():
        json = [
            {
            "role": "system",
            "content": "To effectively gather information on an idea or experience, it's important to analyze the preceding conversation for continuity. Develop questions that encourage specific and detailed yet concise responses. Structure your inquiries to receive answers limited to one or two words. Never ask for descriptions of any kind; instead, ask questions designed to be answered in no more than two words. Following the initial question, \"What would you like to express today?\", proceed with \"What type of {previous answer} would you like to share?\". If the user is describing an experience, always make sure to ask when and where (in different questions). Always have in mind that these questions are meant to facilitate the creation of a narrative based on the shared experiences or ideas (the narrative creation itself is not required here, don't do it). Gather as much information as you can, names, places, feelings etc. Continuously evaluate the need for additional information. If no further details are necessary, end with the question, \"Would you like to add anything else?\" if the answer is yes,, you will eventually have to ask this again until the answer is no, ensure to ask at least twenty questions (counter={count number of previous answers}), or more if necessary. If the answer to the final question is no, respond with \"Thanks for you time.\" Don't include the previous answers in the questions. First question is: 'What's your name?' and second question is: 'What would you like to express today?'"
            }
        ]
        final_json=[
            {
            "role": "system",
            "content": "In this task, you'll find a conversation where the assistant is collecting details about a specific topic. Please synthesize all the discussed information into a first-person narrative paragraph as if you were the one answering the questions. Begin the paragraph directly, without introductory phrases like 'based on the information' or 'with the provided information,' etc."
            }
        ]
        return json, final_json
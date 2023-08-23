import openai
from colorama import Fore, Style


# set constants
MODEL = "gpt-3.5-turbo" # language model to be used
MAX_TOKENS = 100 # max output tokens
TEMPERATURE = 1.3 # set temperature
MAX_HISTORY = 7 # use odd number. max messages to pass to the chatbot for context
SYS_PROMPT = "Chat succinctly with but retain a detailed mental model of the user."


class Utility:
    @staticmethod
    def run_function(func, message, *args, **kwargs):
        print(f"{Style.RESET_ALL}=> {message}... ", end="")
        try:
            result = func(*args, **kwargs)
            str_result = f"{Style.RESET_ALL}{Fore.LIGHTGREEN_EX}OK{Style.RESET_ALL} {Style.DIM}{str(result)}{Style.RESET_ALL}"
            print(str_result)
            return result
        except Exception as e:
            str_result = f"{Style.RESET_ALL}{Fore.LIGHTRED_EX}FAIL{Style.RESET_ALL}\n{Style.DIM}==> {str(e)}\n==> Stack trace follows{Style.RESET_ALL}"
            print(str_result)
            return result


class Chatbot:
    # initialise env
    def __init__(self):
        self.messages = [{"role": "system", "content": SYS_PROMPT}]
        self.counter_tokens = 0
        self.conversation = Conversation(self)


    # function to update history with user input
    def update_payload(self, role, text):
        self.messages.append({"role": role, "content": text})
        return self.messages


    # function to update token count
    def update_token_count(self, tokens):
        self.counter_tokens += tokens
        return self.counter_tokens


    # function to prune history
    def rotate_chatlog(self, MAX_HISTORY, len_messages):
        if len_messages >= MAX_HISTORY:
            self.messages.pop(1) # keep the system instructions at index 0
            self.messages.pop(1) # and remove the first user and assistant entries
        return f"{len_messages}/{MAX_HISTORY}"


    def run(self):
        while True:
            self.conversation.run()


class Conversation:
    def __init__(self, chatbot):
        self.chatbot = chatbot


    # function to get user input
    def get_user_input(self):
        user_prompt = input(f"{Fore.BLUE}")
        return user_prompt


    # function to generate chat completion
    def get_bot_reply(self, messages):
        response = openai.ChatCompletion.create(
            model=MODEL, max_tokens=MAX_TOKENS, temperature=TEMPERATURE, messages=messages
        )
        reply = response.choices[0].message.content
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens
        print(f"{Fore.LIGHTCYAN_EX}\n==> {reply}{Style.RESET_ALL}")
        return {"reply": reply, "total_tokens": total_tokens, "prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens}


    def run(self):
        while True:
            user_input = utility.run_function(self.get_user_input, "type your query")
            utility.run_function(chatbot.update_payload, "updating payload [user]", "user", user_input)
            bot_reply = utility.run_function(self.get_bot_reply, "rendering LLM response", self.chatbot.messages)
            utility.run_function(chatbot.update_payload, "updating payload [bot]", "assistant", bot_reply["reply"])
            counter_tokens = utility.run_function(self.chatbot.update_token_count, "updating token counter", bot_reply["total_tokens"])
            utility.run_function(self.chatbot.rotate_chatlog, "updating history", MAX_HISTORY, len(self.chatbot.messages))


# Enter main loop
if __name__ == "__main__":
    utility = Utility()
    chatbot = Chatbot()
    chatbot.run()
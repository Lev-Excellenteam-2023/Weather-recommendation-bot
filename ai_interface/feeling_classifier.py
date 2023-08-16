from ai_interface.openai_client import OpenAiClient


class FeelingClassifier(OpenAiClient):
    MODEL = "gpt-3.5-turbo"
    MAX_TOKENS = 200

    def __init__(self, api_key):
        super().__init__(api_key, self.MAX_TOKENS)

    @classmethod
    def _set_prompt(cls, input_data: str) -> str:
        return f"""
            Given a free text of a person describing how he experiences the weather.
            Given the text, categorize its feeling into one of the following categories:
            "very hot","hot","Pleasant","cold","Very cold". (answer only with the category 
            without additional words)
            example: 
            example_input: Yesterday I was really wet with sweat
            example_output: "very hot"

            input: {input_data}.
            output: 
            """



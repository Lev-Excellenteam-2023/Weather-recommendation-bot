from ai_interface.openai_client import OpenAiClient
from shared.consts import FeelingCategories


class FeelingClassifier(OpenAiClient):
    MODEL = "gpt-3.5-turbo"
    MAX_TOKENS = 200
    INPUT_INDEX = 0

    def __init__(self, api_key):
        super().__init__(api_key, self.MAX_TOKENS)

    def _set_prompt(self, input_data: tuple) -> str:
        return f"""
        Given a free text of a person describing how he experiences the weather.
        Given the text, categorize its feeling into one of the following categories:
        "{FeelingCategories.VERY_HOT}","{FeelingCategories.HOT}","{FeelingCategories.PLEASANT}",
        "{FeelingCategories.COLD}","{FeelingCategories.VERY_COLD}". 
        (answer only with the category 
        without additional words)
        example: 
        example_input: Yesterday I was really wet with sweat
        example_output: very hot

        input: {input_data[self.INPUT_INDEX]}.
        output: 
        """

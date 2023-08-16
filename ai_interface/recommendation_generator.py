from ai_interface.openai_client import OpenAiClient


class RecommendationGenerator(OpenAiClient):
    MODEL = "gpt-3.5-turbo"
    MAX_TOKENS = 350
    HISTORY_INDEX = 0
    FORCAST_INDEX = 1

    def __init__(self, api_key):
        super().__init__(api_key, self.MAX_TOKENS)

    def _set_prompt(self, input_data: tuple) -> str:
        ordered_input = f"History: {input_data[0]}. Forecast{input_data[1]}"
        return f"""
        You should act as an advisor on how to behave given the weather conditions and 
        weather history. Considering the history of a certain person 
        (details about the weather conditions in previous days and how the person 
        experienced this weather), and details about the expected weather, 
        give him a recommendation in 5-6 sentences on how to conduct himself in order to make him as comfortable as 
        possible (for example, what to wear, whether to go outside, whether to stay in air conditioning, etc.).
        The answer should be in the first person and it should start like this: 
        "based on you and the forecast, the recommendation for you is..."
        input: {ordered_input}
        output: 
        """

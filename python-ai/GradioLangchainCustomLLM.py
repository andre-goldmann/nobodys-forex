from typing import Any, Dict, Iterator, List, Mapping, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from langchain_core.outputs import GenerationChunk
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from gradio_client import Client
class GradioClientChat(LLM):
    """
    Custom LLM class based on the Gradio API call.
    """

    chatbot: Any = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Instantiating the ChatBot class
        # add here you hf_token, in case as shown here below
        #yourHFtoken = "hf_xxxxxxxxxxxxxxxxx" #here your HF token
        #self.chatbot =("ysharma/Chat_with_Meta_llama3_8b", hf_token=yourHFtoken)
        self.chatbot = Client("ysharma/Chat_with_Meta_llama3_8b")

    @property
    def _llm_type(self) -> str:
        return "Gradio API client Meta_llama3_8b"

    def _call(
            self,
            prompt: str,
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            chatbot=None,
            request: float = 0.95,
            param: float = 512,
    ) -> str:
        """
        Make an API call to the Gradio API client Meta_llama3_8b using the specified prompt and return the response.
        """
        if chatbot is None:
            chatbot = self.chatbot

        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")

        # Return the response from the API
        result = chatbot.predict(   #.submit for streaming effect / .predict for normal output
            message=prompt,
            request=request,
            param_3=param,
            api_name="/chat"
        )
        return str(result)

    def _stream(
            self,
            prompt: str,
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            chatbot=None,
            request: float = 0.95,
            param: float = 512,
            **kwargs: Any,
    ) -> Iterator[GenerationChunk]:
        """Stream the LLM on the given prompt.

        This method should be overridden by subclasses that support streaming.

        If not implemented, the default behavior of calls to stream will be to
        fallback to the non-streaming version of the model and return
        the output as a single chunk.

        Args:
            prompt: The prompt to generate from.
            stop: Stop words to use when generating. Model output is cut off at the
                first occurrence of any of these substrings.
            run_manager: Callback manager for the run.
            **kwargs: Arbitrary additional keyword arguments. These are usually passed
                to the model provider API call.

        Returns:
            An iterator of GenerationChunks.
        """
        if chatbot is None:
            chatbot = self.chatbot

        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")

        # Return the response from the API
        for char in chatbot.submit(   #.submit for streaming effect / .predict for normal output
                message=prompt,
                request=request,
                param_3=param,
                api_name="/chat"
        ):
            chunk = GenerationChunk(text=char)
            if run_manager:
                run_manager.on_llm_new_token(chunk.text, chunk=chunk)

            yield chunk

if __name__ == "__main__":
    #https://github.com/fabiomatricardi/GradioLangchainCustomLLM?source=post_page-----08cae7d29714--------------------------------
    llm = GradioClientChat()

    # INference with no parameters
    #result = llm.invoke("what is artificial Intelligence?")  #[10:]   to remove the assitant from the output
    #print(result)

    # inference with temperature and ma_lenght
    #result = llm.invoke("what are the differences between artificial Intelligence and machine learning?", request = 0.45, param = 600)[10:]  # to remove the assitant from the output
    #print(result)

    #
    final = ''
    for token in llm.stream("what is the scientific method?",request = 0.25, param = 600):
        if final == '':
            final=token
            print(token, end="", flush=True)
        else:
            try:
                print(token.replace(final,''), end="", flush=True)
                final = token
            except:
                pass
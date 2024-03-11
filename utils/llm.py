from langchain.chains import LLMChain, RetrievalQA, ConversationalRetrievalChain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT, QA_PROMPT
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chains.question_answering import load_qa_chain
from langchain.retrievers import SelfQueryRetriever, ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_community.llms.llamacpp import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.outputs import LLMResult
class ChainStreamHandler(StreamingStdOutCallbackHandler):
    def __init__(self):
        self.tokens = []
        self.str = ''
        # 记得结束后这里置true
        self.finish = False

    def on_llm_new_token(self, token: str, **kwargs):
        print(token)
        self.str +=token
        self.tokens.append(token)

    def on_llm_end(self, response: LLMResult, **kwargs: any) -> None:
        self.finish = 1

    def on_llm_error(self, error: Exception, **kwargs: any) -> None:
        print(str(error))
        self.tokens.append(str(error))

    def generate_tokens(self):
        while not self.finish or self.tokens:
            if self.tokens:
                data = self.tokens.pop(0)
                yield data
            else:
                pass
def load_llm():
    # callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    # return LlamaCpp(model_path=MODEL_PATH['llm_model'][LLM_MODELS], callback_manager=callback_manager,
    #                 verbose=True, n_ctx=2048,temperature=0)
    from langchain_community.llms.ollama import Ollama
    from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler

    llm = Ollama(base_url="http://localhost:11434",
                     model="qwen:7b",
                     callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
                 )

    return llm

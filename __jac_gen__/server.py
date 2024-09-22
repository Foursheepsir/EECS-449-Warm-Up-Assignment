from __future__ import annotations
from jaclang import jac_import as __jac_import__
import typing as _jac_typ
from jaclang.plugin.feature import JacFeature as _Jac
from jaclang.plugin.builtin import *
from dataclasses import dataclass as __jac_dataclass__
if _jac_typ.TYPE_CHECKING:
    from mtllm.llms import Ollama
else:
    Ollama, = __jac_import__(target='mtllm.llms', base_path=__file__, lng='py', absorb=False, mdl_alias=None, items={'Ollama': None})
llm1 = Ollama(model_name='llama3.1')
llm2 = Ollama(model_name='gemma2')
if _jac_typ.TYPE_CHECKING:
    from rag import RagEngine
else:
    RagEngine, = __jac_import__(target='rag', base_path=__file__, lng='jac', absorb=False, mdl_alias=None, items={'RagEngine': None})
rag_engine: RagEngine = RagEngine()

@_Jac.make_node(on_entry=[], on_exit=[])
@__jac_dataclass__(eq=False)
class Session(_Jac.Node):
    id: str
    chat_history: list[dict]
    status: int = _Jac.has_instance_default(gen_func=lambda: 1)

    def llm_chat(self, message: str, chat_history: list[dict], agent_role: str, context: list) -> str:
        return _Jac.with_llm(file_loc=__file__, model=llm2, model_params={}, scope='server(Module).Session(node).llm_chat(Ability)', incl_info=[], excl_info=[], inputs=[('current message', str, 'message', message), ('chat history', list[dict], 'chat_history', chat_history), ('role of the agent responding', str, 'agent_role', agent_role), ('retrieved context from documents', list, 'context', context)], outputs=('response', 'str'), action='Respond to message using chat_history as context and agent_role as the goal of the agent', _globals=globals(), _locals=locals())

@_Jac.make_node(on_entry=[], on_exit=[])
@__jac_dataclass__(eq=False)
class Session_2(_Jac.Node):
    id: str
    chat_history: list[dict]
    status: int = _Jac.has_instance_default(gen_func=lambda: 1)

    def llm_chat(self, message: str, chat_history: list[dict], agent_role: str, context: list) -> str:
        return _Jac.with_llm(file_loc=__file__, model=llm2, model_params={}, scope='server(Module).Session_2(node).llm_chat(Ability)', incl_info=[], excl_info=[], inputs=[('current message', str, 'message', message), ('chat history', list[dict], 'chat_history', chat_history), ('role of the agent responding', str, 'agent_role', agent_role), ('retrieved context from documents', list, 'context', context)], outputs=('response', 'str'), action='Respond to message using chat_history as context and agent_role as the goal of the agent', _globals=globals(), _locals=locals())

@_Jac.make_walker(on_entry=[_Jac.DSFunc('init_session', _Jac.RootType), _Jac.DSFunc('chat', Session)], on_exit=[])
@__jac_dataclass__(eq=False)
class interact(_Jac.Walker):
    message: str
    session_id: str

    def init_session(self, _jac_here_: _Jac.RootType) -> None:
        if _Jac.visit_node(self, (lambda x: [i for i in x if i.id == self.session_id])((lambda x: [i for i in x if isinstance(i, Session)])(_Jac.edge_ref(_jac_here_, target_obj=None, dir=_Jac.EdgeDir.OUT, filter_func=None, edges_only=False)))):
            pass
        else:
            session_node = _Jac.connect(left=_jac_here_, right=Session(id=self.session_id, chat_history=[], status=1), edge_spec=_Jac.build_edge(is_undirected=False, conn_type=None, conn_assign=None))
            print('Session Node Created')
            if _Jac.visit_node(self, session_node):
                pass

    def chat(self, _jac_here_: Session) -> None:
        _jac_here_.chat_history.append({'role': 'user', 'content': self.message})
        data = rag_engine.get_from_chroma(query=self.message)
        response = _jac_here_.llm_chat(message=self.message, chat_history=_jac_here_.chat_history, agent_role='You are a conversation agent designed to help users with their queries based on the documents provided. Please answer the queries according to what you retrieved from the documents.', context=data)
        _jac_here_.chat_history.append({'role': 'assistant', 'content': response})
        _Jac.report({'response': response})
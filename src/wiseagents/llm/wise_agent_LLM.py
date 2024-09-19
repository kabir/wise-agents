from abc import abstractmethod
from typing import Iterable

import yaml
from openai.types.chat import ChatCompletionMessageParam, ChatCompletion, ChatCompletionToolParam
from wiseagents.yaml import ValidatingYAMLObject,WiseAgentsLoader


class WiseAgentLLM(ValidatingYAMLObject):
    """Abstract class to define the interface for a WiseAgentLLM."""
    yaml_tag = u'!WiseAgentLLM'
    yaml_loader = WiseAgentsLoader
    def __init__(self, system_message, model_name):
        '''Initialize the agent.

        Args:
            system_message (str): the system message
            model_name (str): the model name
        '''
        super().__init__()
        self._system_message = system_message
        self._model_name = model_name
    
    def __repr__(self):
        '''Return a string representation of the agent.'''
        return f"{self.__class__.__name__}(system_message={self.system_message}, model_name={self.model_name})"    
    
    @property  
    def system_message(self):
        '''Get the system message.'''
        return self._system_message

    @property
    def model_name(self):
        '''Get the model name.'''
        return self._model_name     

    @abstractmethod
    def process_single_prompt(self, prompt):
        '''Process a single prompt. This method should be implemented by subclasses.
        The single prompt is processed and the result is returned, all the context and state is maintained locally in the method

        Args:
            prompt (str): the prompt to process'''
        
        ...
    
    @abstractmethod
    def process_chat_completion(self, 
                                messages: Iterable[ChatCompletionMessageParam], 
                                tools: Iterable[ChatCompletionToolParam]) -> ChatCompletion:
        '''Process a chat completion. This method should be implemented by subclasses.
        The context and state is passed in input and returned as part of the output.
        Deal with the messages and tools is responsibility of the caller.

        Args:
            messages (Iterable[ChatCompletionMessageParam]): the messages to process
            tools (Iterable[ChatCompletionToolParam]): the tools to use
        
        Returns:
                ChatCompletion: the chat completion result'''
        ...
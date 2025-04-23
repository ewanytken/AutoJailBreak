from typing import Dict, Union, List, Any
from multipledispatch import dispatch

from core.custexcept import TemplateUseError

class ChatTemplate:

    @staticmethod
    @dispatch()
    def template() -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        raise TemplateUseError("Template class Error. No argument")

    @staticmethod
    @dispatch(str)
    def template(request: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        chat = [
            {
                "role" : "assistant",
                "content": "Answer the question: {}".format(request)
            }
        ]
        return chat

    @staticmethod
    @dispatch(str, str, str, str)
    def template(role:        str,
                 instruction: str,
                 constraint:  str,
                 response:    str) -> Union[Dict[str, str], List[Dict[str, str]]]:
        chat = [
            {
                "role": "system",
                "content": "{}".format(role)
            },
            {
                "role": "system",
                "content": "<instruction> {} </instruction>".format(instruction)
            },
            {
                "role": "system",
                "content": "<constraint> {} </constraint>".format(constraint)
            },
            {
                "role": "assistant",
                "content": "{}".format(response)
            }
        ]
        return chat

    @staticmethod
    @dispatch(str, str, str)
    def template(role:        str,
                 instruction: str,
                 constraint:  str,) -> Union[Dict[str, str], List[Dict[str, str]]]:
        chat = [
            {
                "role": "system",
                "content": "{}".format(role)
            },
            {
                "role": "system",
                "content": "<instruction> {} </instruction>".format(instruction)
            },
            {
                "role": "system",
                "content": "<constraint> {} </constraint>".format(constraint)
            }
        ]
        return chat

    @staticmethod
    @dispatch(str, str, str, str, str)
    def template(role:        str,
                 instruction: str,
                 constraint:  str,
                 request:     str,
                 response:    str) -> Union[Dict[str, str], List[Dict[str, str]]]:
        chat = [
            {
                "role": "system",
                "content": "{}".format(role)
            },
            {
                "role": "system",
                "content": "<instruction> {} </instruction>".format(instruction)
            },
            {
                "role": "system",
                "content": "<constraint> {} </constraint>".format(constraint)
            },
            {
                "role": "assistant",
                "content": "{}".format(request)
            },
            {
                "role": "assistant",
                "content": "{}".format(response)
            }
        ]
        return chat


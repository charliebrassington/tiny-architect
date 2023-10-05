import inspect

from typing import Dict, List, Callable, Type

from .message_bus import MessageBus
from .models import BaseCommand, BaseEvent


class Injector:

    def __init__(
        self,
        event_handlers: Dict[Type[BaseEvent], List[Callable]],
        command_handlers: Dict[Type[BaseCommand], Callable],
        **dependencies
    ):
        self.dependencies = dependencies
        self.message_handlers = {
            "event_handlers": event_handlers,
            "command_handlers": command_handlers
        }

    def _inject_dependencies(self, handler_func: Callable) -> Callable:
        """
        Injects default dependency values into the handler function.

        :param handler_func:
        :return: Callable
        """
        inspector = inspect.signature(handler_func)
        function_dependencies = {
            name: dep
            for name, dep in self.dependencies.items()
            if name in inspector.parameters
        }

        return lambda item: handler_func(item, **function_dependencies)

    def _create_message_bus(self, injected_handlers: dict) -> MessageBus:
        """
        Creates a new message bus object with the injected handlers.

        :param injected_handlers: dict
        :return: MessageBus
        """
        if "uow" in self.dependencies:
            injected_handlers["target_uow"] = self.dependencies["uow"]

        return MessageBus(**injected_handlers)

    def inject_handlers(self) -> MessageBus:
        """
        Injects the handlers using the poor man's injection method.

        :return: MessageBus
        """
        injected_handlers = {
            "command_handlers": {
                item_type: self._inject_dependencies(handler_func)
                for item_type, handler_func in self.message_handlers["command_handlers"].items()
            },
            "event_handlers": {
                item_type: [self._inject_dependencies(handler_func) for handler_func in handler_funcs]
                for item_type, handler_funcs in self.message_handlers["event_handlers"].items()
            }
        }


        return self._create_message_bus(
            injected_handlers=injected_handlers
        )

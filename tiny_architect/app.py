import logging

from dataclasses import dataclass
from typing import (
    Any,
    Dict,
    List,
    Callable,
    Type,
    Union
)


from .models import *
from .message_bus import MessageBus
from .injector import Injector
from .utils import logger


class TinyArchitect:

    def __init__(self, logging_enabled=False):
        self._logger = logger.create_logger(__name__)
        if not logging_enabled:
            self._logger.setLevel(logging.INFO)

        self._message_bus = MessageBus(command_handlers={}, event_handlers={})
        self._dependencies = {}

    def _update_message_bus(self):
        """
        Injects the message busses handlers and applications dependencies into a new message bus.
        Runs when new items are added to the message bus.

        :return: None
        """
        self._logger.debug("Injecting and updating message bus handlers and dependencies")
        dependency_injector = Injector(
            command_handlers=self._message_bus.command_handlers,
            event_handlers=self._message_bus.event_handlers,
            **self._dependencies
        )

        self._message_bus = dependency_injector.inject_handlers()

    def add_command_handler(self, command: Type[BaseCommand], handler_func: Callable) -> None:
        """
        Adds a command along with the handler func to this command.

        :param command: Any
        :param handler_func: Callable
        :return: None
        """
        self._logger.debug(f"Adding command: {command.__name__} and handler: {handler_func.__name__}")

        self._message_bus.command_handlers[command] = handler_func
        self._update_message_bus()

    def add_event_handlers(self, event: Type[BaseEvent], handler_funcs: List[Callable]):
        """
        Adds an event along with the handler funcs are added as values.

        :param event:
        :param handler_funcs:
        :return: None
        """
        handler_names = ", ".join([func.__name__ for func in handler_funcs])
        self._logger.debug(f"Adding event: {event.__name__} and handlers: {handler_names}")

        self._message_bus.event_handlers[event] = handler_funcs
        self._update_message_bus()

    def add_service(self, service: Union[Type[BaseService], BaseService], name: str) -> None:
        """
        Adds the uow to the message bus uow list.

        :param service: BaseService
        :param name: str
        :return: None
        """
        self._logger.debug(f"Adding service with the name: {name}")

        self._dependencies[name] = service
        self._update_message_bus()

    def handle_command(self, cmd: BaseCommand) -> Any:
        """
        Handles the command runs the handler and returns the handler value.

        :param cmd: BaseCommand
        :return: Any
        """
        self._logger.debug(f"Handling command {cmd}")
        if isinstance(cmd, BaseCommand):
            return self._message_bus.handle_item(item=cmd)

        raise ValueError("command must inherit off a BaseClass")

    def handle_event(self, event: BaseEvent) -> Any:
        """
        Handles the event runs the handler and returns the handler value.

        :param event: BaseEvent
        :return: Any
        """
        self._logger.debug(f"Handling event {event}")
        if isinstance(event, BaseEvent):
            return self._message_bus.handle_item(item=event)

        raise ValueError("event must inherit off a BaseEvent")

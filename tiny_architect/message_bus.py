from dataclasses import dataclass
from typing import (
    Any,
    Type,
    Dict,
    List,
    Callable,
    Union
)

from .models import *


class MessageBus:

    def __init__(
        self,
        command_handlers: Dict[Type[BaseCommand], Callable],
        event_handlers: Dict[Type[BaseEvent], List[Callable]],
        target_uow: Union[BaseUnitOfWork, None] = None,
    ):
        self.uow = target_uow
        self.command_handlers = command_handlers
        self.event_handlers = event_handlers

    def _run_command_handler(self, cmd: BaseCommand) -> Any:
        """
        Finds the handler paired to the command passed in then runs and returns the handlers result

        :param cmd:
        :return: Any
        """

        return self.command_handlers[type(cmd)](cmd)

    def _run_event_handler(self, event: BaseEvent) -> List[Any]:
        """
        Finds the handlers paired to the event then returns all the handlers and returns the result values.

        :param event:
        :return: List[Any]
        """
        return [handler(event) for handler in self.event_handlers[type(event)]]

    def handle_item(self, item: Union[BaseCommand, BaseEvent]):
        """
        Handles an item running the correct function depending on the items type.

        :param item:
        :return: Any
        """
        if isinstance(item, BaseEvent):
            return self._run_event_handler(event=item)

        elif isinstance(item, BaseCommand):
            return self._run_command_handler(cmd=item)

        raise ValueError("item doesn't inherit off a BaseCommand or EventCommand")

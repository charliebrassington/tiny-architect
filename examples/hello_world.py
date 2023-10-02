from dataclasses import dataclass

import tiny_architect


@dataclass
class SendMessageCommand(tiny_architect.BaseCommand):
    message: str


def send_message_handler(
    command: SendMessageCommand
):
    print(f"Handler has recieved a new command, here's the message {command.message}")


hello_world_application = tiny_architect.TinyArchitect()

hello_world_application.add_command_handler(command=SendMessageCommand, handler_func=send_message_handler)
hello_world_application.handle_command(SendMessageCommand(message="Hello World"))

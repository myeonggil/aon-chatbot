# slack message trigger
# telemetry apply
# something API? I don't know well...
# Go for DevOps.ref
from abc import ABCMeta, abstractmethod
from enum import StrEnum
from dataclasses import dataclass
from functools import partialmethod
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.socket_mode.builtin import SocketModeClient
from slack_sdk import WebClient


class Ops(metaclass=ABCMeta):
    @abstractmethod
    def listen_traces():
        pass

    @abstractmethod
    def show_trace():
        pass

    @abstractmethod
    def change_sampling():
        pass

    @abstractmethod
    def deployed_version():
        pass

    @abstractmethod
    def alerts():
        pass


app = App()
@app.event()

class AppMention(StrEnum):
    MESSAGE: str = "message"
    REACTION_ADDED: str = "reaction_added"
    REACTION_REMOVED: str = "reaction_removed"
    MEMBER_JOINED_CHANNEL: str = "member_joined_channel"
    MEMBER_LEFT_CHANNEL: str = "member_left_channel"
    APP_MENTION: str = "app_mention"
    USER_CHANGE: str = "user_change"
    CHANNEL_CREATED: str = "channel_created"
    CHANNEL_DELETED: str = "channel_deleted"
    FILE_SHARED: str = "file_shared"


@dataclass
class Register:
    r: partialmethod
    h: partialmethod

@dataclass
class Message:
    user: str
    app_mention: AppMention
    text: str

@dataclass
class Bot:
    api: WebClient
    client: SocketModeClient
    default_handler: partialmethod
    reg: list[Register]
    ctx: any = None
    cancel: any = None

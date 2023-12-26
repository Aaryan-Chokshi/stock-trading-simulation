from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DbID(_message.Message):
    __slots__ = ["dbid"]
    DBID_FIELD_NUMBER: _ClassVar[int]
    dbid: str
    def __init__(self, dbid: _Optional[str] = ...) -> None: ...

class NotingTransaction(_message.Message):
    __slots__ = ["dbid", "symbol", "qty", "price"]
    DBID_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    QTY_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    dbid: str
    symbol: str
    qty: int
    price: float
    def __init__(self, dbid: _Optional[str] = ..., symbol: _Optional[str] = ..., qty: _Optional[int] = ..., price: _Optional[float] = ...) -> None: ...

class ShareQuery(_message.Message):
    __slots__ = ["dbid", "symbol"]
    DBID_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    dbid: str
    symbol: str
    def __init__(self, dbid: _Optional[str] = ..., symbol: _Optional[str] = ...) -> None: ...

class ShareQtyResponse(_message.Message):
    __slots__ = ["qty"]
    QTY_FIELD_NUMBER: _ClassVar[int]
    qty: int
    def __init__(self, qty: _Optional[int] = ...) -> None: ...

class FundResponse(_message.Message):
    __slots__ = ["fund"]
    FUND_FIELD_NUMBER: _ClassVar[int]
    fund: float
    def __init__(self, fund: _Optional[float] = ...) -> None: ...

class Message(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

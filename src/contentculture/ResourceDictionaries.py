from typing import TypedDict

class Media(TypedDict):
    Id=int
    List_id=int
    Title=str
    Medium=str
    External_id=str
    Rating=int
    Genre=str
    Commentary=str

class List1(TypedDict):
    Id=int
    User_id=int
    Name=str
    Description=str
    Medias=list[Media]

class Lists(TypedDict):
    lists=list[List1]

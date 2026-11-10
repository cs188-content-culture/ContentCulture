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

class Lists(TypedDict):
    Id=int
    Medias=list[Media]
    User_id=int
    Decription=str
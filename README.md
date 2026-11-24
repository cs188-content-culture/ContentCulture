Content Culture

a website designed to allow users to create their own lists of favorite medias, and view others. They may also leave reviews of media to serve as recommendations for others.

Endpoints:
    Media:
        id: int
        title: string
        medium: string
        genre: string
        external_id: string
        rating: int
        genre: string
        commentary: string

    List:
        id: int
        user_id: int
        name: string
        description: string
        medias: list[Media]

    Lists:
        list[List]
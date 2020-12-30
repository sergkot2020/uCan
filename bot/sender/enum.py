class MessageTypeEnum:
    """ Type outgoing messages """
    TEXT = 1
    PHOTO = 2
    VIDEO = 3
    URL = 4
    DOC = 5
    AUDIO = 6
    MEDIA_GROUP = 7

    values = {
        TEXT: 'text',
        PHOTO: 'photo',
        VIDEO: 'video',
        URL: 'url',
        DOC: 'document',
        AUDIO: 'audio',
        MEDIA_GROUP: 'media_group'
    }

    LINK_TYPES = [
        PHOTO, VIDEO, DOC, AUDIO
    ]

# User role
ADMIN = 0
STAFF = 1
USER = 2
ROLES = {
    ADMIN: 'admin',
    STAFF: 'staff',
    USER: 'пользователь',
}

# user status
INACTIVE = 0
ACTIVE = 1
STATUS = {
    INACTIVE: 'не в сети',
    ACTIVE: 'в сети',
}

# user sex
MAN = 0
WOMEN = 1
OTHER = 2
SEX = {
    MAN: 'мужчина',
    WOMEN: 'женщина',
    OTHER: '-',
}

# modality
METABOLIC = 0
GYMNASTIC = 1
EXTERNAL_OBJECT = 2
MOBILITY = 3
MODALITY = {
    METABOLIC: 'метаболика',
    GYMNASTIC: 'гимнастика',
    EXTERNAL_OBJECT: 'внешние объекты',
    MOBILITY: 'подвижность'
}

# wod confirm
BOOL = 0
REPS = 1
TIME = 2
TIEBRAEK = 3
WODCONFIRM = {
    BOOL: 'выполнено',
    REPS: 'повторения',
    TIME: 'время',
    TIEBRAEK: 'смешанно'
}

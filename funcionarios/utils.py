def is_administrador(user):

    return user.groups.filter(
        name='Administrador'
    ).exists()


def is_rh(user):

    return user.groups.filter(
        name='RH'
    ).exists()


def is_gestor(user):

    return user.groups.filter(
        name='Gestor'
    ).exists()
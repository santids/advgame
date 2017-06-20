


def act(artefact,loc,world,hero):
    """Do whatever de artefact does"""
    tipo = artefact[0]
    activate = artefact[1] == "on"
    if tipo == "door":
        if activate:
            world.map[loc] = 0
        else:
            world.map[loc] = 1

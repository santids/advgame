
import utils.vect2d as vect


def act(artefact,loc,world,hero):
    """Do whatever de artefact does"""
    tipo = artefact[0]
    activate = artefact[1] == "on"
    if tipo == "door":
        if activate:
            world.map[loc] = 0
        else:
            world.map[loc] = 1
    elif tipo == "lava-maker":
        if activate:
            for l in vect.around(loc):
                world.map[l] = 5 
        else:
            for l in vect.around(loc):
                world.map[l] = 0
    elif tipo == "explosive-crate":
        if activate:
            world.map[loc] = 0
            del world.artefacts[loc]



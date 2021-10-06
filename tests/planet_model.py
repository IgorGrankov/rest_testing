from attr import attrs, attrib


@attrs
class Planet:
    name = attrib(type=str)
    diameter = attrib(type=str)
    rotation_period = attrib(type=str)
    orbital_period = attrib(type=str)
    gravity = attrib(type=str)
    population = attrib(type=str)
    climate = attrib(type=str)
    terrain = attrib(type=str)
    surface_water = attrib(type=str)
    residents = attrib(type=list)
    films = attrib(type=list)
    url = attrib(type=str)
    created = attrib(type=str)
    edited = attrib(type=str)


@attrs
class Planets:
    results = attrib(converter=lambda items: [Planet(**item) for item in items])
    count = attrib(type=int)
    next = attrib(type=int)
    previous = attrib(type=int)


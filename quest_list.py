import enum


class Maps(enum.Enum):
    DAM_BATTLEGROUNDS = "Dam Battlegrounds"
    BURIED_CITY = "Buried City"
    SPACEPORT = "Spaceport"
    STELLA_MONTIS = "Stella Montis"
    BLUE_GATE = "Blue Gate"
    RIVEN_TIDES = "Riven Tides"


FIRST_QUESTS = ["picking up the pieces", "a first foothold"]


quest_list = {
    "picking up the pieces": {
        "maps": [Maps.DAM_BATTLEGROUNDS],
        "new_quests": ["clearer skies", "trash into treasure"],
    },
    "clearer skies": {
        "maps": [Maps.DAM_BATTLEGROUNDS],
        "new_quests": ["off the radar"],
    },
    "trash into treasure": {
        "maps": [Maps.DAM_BATTLEGROUNDS],
        "new_quests": ["off the radar"],
    },
    "off the radar": {
        "maps": [Maps.DAM_BATTLEGROUNDS],
        "new_quests": ["a bad feeling", "battening down", "shoring up defenses"],
    },
    "a bad feeling": {
        "maps": [Maps.DAM_BATTLEGROUNDS],
        "new_quests": ["the right tool", "hatch repairs", "safe passage", "in my image"],
    },
    "the right tool": {
        "maps": [Maps.DAM_BATTLEGROUNDS, Maps.BURIED_CITY, Maps.SPACEPORT, Maps.STELLA_MONTIS, Maps.BLUE_GATE, Maps.RIVEN_TIDES],
        "new_quests": ["a better use"],
    },
    "hatch repairs": {
        "maps": [Maps.DAM_BATTLEGROUNDS, Maps.BURIED_CITY, Maps.SPACEPORT, Maps.STELLA_MONTIS, Maps.BLUE_GATE, Maps.RIVEN_TIDES],
        "new_quests": ["down to earth"],
    },
    "safe passage": {
        "maps": [Maps.DAM_BATTLEGROUNDS, Maps.BURIED_CITY, Maps.SPACEPORT, Maps.STELLA_MONTIS, Maps.BLUE_GATE, Maps.RIVEN_TIDES],
        "new_quests": ["what goes around", "collision course"],
    },
    "in my image": {
        "maps": [Maps.STELLA_MONTIS],
        "new_quests": ["cold storage"],
    },
    "a better use": {
        "maps": [Maps.DAM_BATTLEGROUNDS, Maps.BURIED_CITY, Maps.SPACEPORT, Maps.BLUE_GATE, Maps.RIVEN_TIDES],
        "new_quests": ["greasing her palms (part 1)", "greasing her palms (part 2)", "greasing her palms (part 3)"],
    },
    "down to earth": {
        "maps": [Maps.DAM_BATTLEGROUNDS, Maps.BURIED_CITY, Maps.SPACEPORT, Maps.BLUE_GATE, Maps.RIVEN_TIDES],
        "new_quests": ["the trifecta"],
    },
    "what goes around": {
        "maps": [Maps.DAM_BATTLEGROUNDS, Maps.BURIED_CITY, Maps.SPACEPORT, Maps.STELLA_MONTIS, Maps.BLUE_GATE, Maps.RIVEN_TIDES],
        "new_quests": ["sparks fly"],
    },
    "cold storage": {
        "maps": [Maps.STELLA_MONTIS],
        "new_quests": ["snap and salvage"],
    },
    "snap and salvage": {
        "maps": [Maps.STELLA_MONTIS],
        "new_quests": ["with a view"],
    },
    "with a view": {
        "maps": [Maps.STELLA_MONTIS],
        "new_quests": ["movie night", "stable housing"],
    },
    "movie night": {
        "maps": [Maps.STELLA_MONTIS],
        "new_quests": [],
    },
    "stable housing": {
        "maps": [Maps.STELLA_MONTIS],
        "new_quests": [],
    },
    "sparks fly": {
        "maps": [Maps.DAM_BATTLEGROUNDS, Maps.BURIED_CITY, Maps.SPACEPORT, Maps.BLUE_GATE, Maps.RIVEN_TIDES],
        "new_quests": ["out of the shadows", "the league (part 1)", "the league (part 2)"],
    },
    "the league (part 1)": {
        "maps": [Maps.DAM_BATTLEGROUNDS],
        "new_quests": ["test case"],
    },
    "the league (part 2)": {
        "maps": [Maps.BURIED_CITY],
        "new_quests": ["test case"],
    },
    "the trifecta": {
        "maps": [Maps.DAM_BATTLEGROUNDS, Maps.BURIED_CITY, Maps.SPACEPORT, Maps.BLUE_GATE, Maps.RIVEN_TIDES],
        "new_quests": ["dormant barons", "dust on the wires"],
    },
    "greasing her palms (part 1)": {
        "maps": [Maps.DAM_BATTLEGROUNDS],
        "new_quests": ["doctor's orders", "dormant barons"],
    },
    "greasing her palms (part 2)": {
        "maps": [Maps.SPACEPORT],
        "new_quests": ["doctor's orders", "dormant barons"],
    },
    "greasing her palms (part 3)": {
        "maps": [Maps.BURIED_CITY],
        "new_quests": ["doctor's orders", "dormant barons"],
    },
    "doctor's orders": {
        "maps": [Maps.DAM_BATTLEGROUNDS, Maps.BURIED_CITY, Maps.STELLA_MONTIS, Maps.RIVEN_TIDES],
        "new_quests": ["medical merchandise (part 1)", "medical merchandise (part 2)", "medical merchandise (part 3)"],
        "prerequisites": ["greasing her palms (part 1)", "greasing her palms (part 2)", "greasing her palms (part 3)"],
    },
    "medical merchandise (part 1)": {
        "maps": [Maps.SPACEPORT],
        "new_quests": ["a reveal in ruins"],
    },
    "medical merchandise (part 2)": {
        "maps": [Maps.BURIED_CITY],
        "new_quests": ["a reveal in ruins"],
    },
    "medical merchandise (part 3)": {
        "maps": [Maps.DAM_BATTLEGROUNDS],
        "new_quests": ["a reveal in ruins"],
    },
    "a reveal in ruins": {
        "maps": [Maps.BURIED_CITY],
        "new_quests": ["a lay of the land"],
        "prerequisites": ["medical merchandise (part 1)", "medical merchandise (part 2)", "medical merchandise (part 3)"],
    },
    "a lay of the land": {
        "maps": [Maps.SPACEPORT],
        "new_quests": ["eyes in the sky (part 1)", "eyes in the sky (part 2)", "eyes in the sky (part 3)"],
    },
    "eyes in the sky (part 1)": {
        "maps": [Maps.DAM_BATTLEGROUNDS],
        "new_quests": ["after rain comes", "a balanced harvest", "back on top (part 1)", "back on top (part 2)", "back on top (part 3)", "back on top (part 4)"],
    },
    "eyes in the sky (part 2)": {
        "maps": [Maps.SPACEPORT],
        "new_quests": ["after rain comes", "a balanced harvest", "back on top (part 1)", "back on top (part 2)", "back on top (part 3)", "back on top (part 4)"],
    },
    "eyes in the sky (part 3)": {
        "maps": [Maps.BURIED_CITY],
        "new_quests": ["after rain comes", "a balanced harvest", "back on top (part 1)", "back on top (part 2)", "back on top (part 3)", "back on top (part 4)"],
    },
    "after rain comes": {
        "maps": [Maps.BURIED_CITY],
        "new_quests": ["water troubles"],
        "prerequisites": ["eyes in the sky (part 1)", "eyes in the sky (part 2)", "eyes in the sky (part 3)"],
    },
    "a balanced harvest": {
        "maps": [Maps.DAM_BATTLEGROUNDS],
        "new_quests": ["untended garden"],
        "prerequisites": ["eyes in the sky (part 1)", "eyes in the sky (part 2)", "eyes in the sky (part 3)"],
    },
    "untended garden": {
        "maps": [Maps.DAM_BATTLEGROUNDS],
        "new_quests": ["the root of the matter"],
    },
    "the root of the matter": {
        "maps": [Maps.BURIED_CITY],
        "new_quests": ["water troubles"],
    },
    "water troubles": {
        "maps": [Maps.DAM_BATTLEGROUNDS],
        "new_quests": ["source of the contamination", "into the fray"],
        "prerequisites": ["after rain comes", "the root of the matter"],
    },
    "source of the contamination": {
        "maps": [Maps.DAM_BATTLEGROUNDS],
        "new_quests": ["switching the supply"],
    },
    "switching the supply": {
        "maps": [Maps.SPACEPORT],
        "new_quests": ["a warm place to rest"],
    },
    "a warm place to rest": {
        "maps": [Maps.BURIED_CITY],
        "new_quests": ["prescriptions of the past"],
    },
    "prescriptions of the past": {
        "maps": [Maps.SPACEPORT],
        "new_quests": ["power out"],
    },
    "power out": {
        "maps": [Maps.SPACEPORT],
        "new_quests": ["flickering threat"],
    },
    "flickering threat": {
        "maps": [Maps.DAM_BATTLEGROUNDS],
        "new_quests": ["bees!"],
    },
    "bees!": {
        "maps": [Maps.BLUE_GATE],
        "new_quests": ["espresso"],
    },
    "espresso": {
        "maps": [Maps.DAM_BATTLEGROUNDS, Maps.BURIED_CITY],
        "new_quests": ["life of a pharmacist"],
    },
    "life of a pharmacist": {
        "maps": [Maps.BURIED_CITY],
        "new_quests": ["a toxic trail", "digging up dirt"],
    },
    "a toxic trail": {
        "maps": [Maps.DAM_BATTLEGROUNDS],
        "new_quests": ["the stench of corruption"],
    },
    "the stench of corruption": {
        "maps": [Maps.SPACEPORT],
        "new_quests": [],
    },
    "digging up dirt": {
        "maps": [Maps.BURIED_CITY],
        "new_quests": ["turnabout", "building a library"],
    },
    "turnabout": {
        "maps": [Maps.SPACEPORT],
        "new_quests": [],
    },
    "building a library": {
        "maps": [Maps.BURIED_CITY],
        "new_quests": ["a new type of plant"],
    },
    "a new type of plant": {
        "maps": [Maps.DAM_BATTLEGROUNDS],
        "new_quests": ["armored transports", "the clean dream (part 1)"],
    },
    "a first foothold": {
        "maps": [Maps.BLUE_GATE],
        "new_quests": ["reduced to rubble"],
    },
    "reduced to rubble": {
        "maps": [Maps.BLUE_GATE],
        "new_quests": ["with a trace"],
    },
    "with a trace": {
        "maps": [Maps.BLUE_GATE],
        "new_quests": ["armored transports", "the clean dream (part 1)"],
    },
    "armored transports": {
        "maps": [Maps.BLUE_GATE],
        "new_quests": [],
        "prerequisites": ["a new type of plant", "with a trace"],
    },
    "the clean dream (part 1)": {
        "maps": [Maps.SPACEPORT],
        "new_quests": ["the clean dream (part 2)"],
        "prerequisites": ["a new type of plant", "with a trace"],
    },
    "the clean dream (part 2)": {
        "maps": [Maps.BLUE_GATE],
        "new_quests": ["a prime specimen", "keeping an eye out", "outstanding balance"],
    },
    "a prime specimen": {
        "maps": [Maps.BLUE_GATE],
        "new_quests": [],
    },
    "keeping an eye out": {
        "maps": [Maps.BLUE_GATE],
        "new_quests": [],
    },
    "dormant barons": {
        "maps": [Maps.DAM_BATTLEGROUNDS, Maps.SPACEPORT, Maps.BLUE_GATE],
        "new_quests": ["mixed signals", "what we left behind (part 1)", "what we left behind (part 2)", "what we left behind (part 3)", "clamoring for attention"],
        "prerequisites": ["the trifecta", "greasing her palms (part 1)", "greasing her palms (part 2)", "greasing her palms (part 3)"],
    },
    "mixed signals": {
        "maps": [Maps.DAM_BATTLEGROUNDS, Maps.BURIED_CITY, Maps.SPACEPORT, Maps.BLUE_GATE],
        "new_quests": [],
    },
    "what we left behind (part 1)": {
        "maps": [Maps.BURIED_CITY],
        "new_quests": ["broken monument"],
    },
    "what we left behind (part 2)": {
        "maps": [Maps.DAM_BATTLEGROUNDS],
        "new_quests": ["broken monument"],
    },
    "what we left behind (part 3)": {
        "maps": [Maps.SPACEPORT],
        "new_quests": ["broken monument"],
    },
    "broken monument": {
        "maps": [Maps.DAM_BATTLEGROUNDS],
        "new_quests": ["marked for death", "straight record"],
        "prerequisites": ["what we left behind (part 1)", "what we left behind (part 2)", "what we left behind (part 3)"],
    },
    "marked for death": {
        "maps": [Maps.BURIED_CITY],
        "new_quests": ["market correction"],
    },
    "market correction": {
        "maps": [Maps.BURIED_CITY],
        "new_quests": ["eyes on the prize"],
    },
    "eyes on the prize": {
        "maps": [Maps.BURIED_CITY],
        "new_quests": ["industrial espionage"],
    },
    "industrial espionage": {
        "maps": [Maps.BURIED_CITY],
        "new_quests": ["unexpected initiative"],
    },
    "straight record": {
        "maps": [Maps.DAM_BATTLEGROUNDS],
        "new_quests": ["keeping the memory"],
    },
    "keeping the memory": {
        "maps": [Maps.DAM_BATTLEGROUNDS],
        "new_quests": ["echoes of victory ridge"],
    },
    "echoes of victory ridge": {
        "maps": [Maps.DAM_BATTLEGROUNDS],
        "new_quests": ["unexpected initiative"],
    },
    "unexpected initiative": {
        "maps": [Maps.BURIED_CITY],
        "new_quests": ["a symbol of unification"],
        "prerequisites": ["industrial espionage", "echoes of victory ridge"],
    },
    "a symbol of unification": {
        "maps": [Maps.DAM_BATTLEGROUNDS],
        "new_quests": ["celeste's journals", "out of the shadows", "the major's footlocker"],
    },
    "out of the shadows": {
        "maps": [Maps.DAM_BATTLEGROUNDS, Maps.BURIED_CITY, Maps.SPACEPORT, Maps.BLUE_GATE, Maps.RIVEN_TIDES],
        "new_quests": [],
        "prerequisites": ["sparks fly", "a symbol of unification"],
    },
    "celeste's journals": {
        "maps": [Maps.DAM_BATTLEGROUNDS],
        "new_quests": ["back on top (part 1)", "back on top (part 2)", "back on top (part 3)", "back on top (part 4)"],
    },
    "the major's footlocker": {
        "maps": [Maps.DAM_BATTLEGROUNDS],
        "new_quests": ["back on top (part 1)", "back on top (part 2)", "back on top (part 3)", "back on top (part 4)"],
    },
    "back on top (part 1)": {
        "maps": [Maps.DAM_BATTLEGROUNDS],
        "new_quests": ["our presence up there"],
        "prerequisites": ["eyes in the sky (part 1)", "eyes in the sky (part 2)", "eyes in the sky (part 3)", "celeste's journals", "the major's footlocker"],
    },
    "back on top (part 2)": {
        "maps": [Maps.BLUE_GATE],
        "new_quests": ["our presence up there"],
        "prerequisites": ["eyes in the sky (part 1)", "eyes in the sky (part 2)", "eyes in the sky (part 3)", "celeste's journals", "the major's footlocker"],
    },
    "back on top (part 3)": {
        "maps": [Maps.SPACEPORT],
        "new_quests": ["our presence up there"],
        "prerequisites": ["eyes in the sky (part 1)", "eyes in the sky (part 2)", "eyes in the sky (part 3)", "celeste's journals", "the major's footlocker"],
    },
    "back on top (part 4)": {
        "maps": [Maps.BURIED_CITY],
        "new_quests": ["our presence up there"],
        "prerequisites": ["eyes in the sky (part 1)", "eyes in the sky (part 2)", "eyes in the sky (part 3)", "celeste's journals", "the major's footlocker"],
    },
    "our presence up there": {
        "maps": [Maps.DAM_BATTLEGROUNDS],
        "new_quests": ["lost in transmission"],
        "prerequisites": ["back on top (part 1)", "back on top (part 2)", "back on top (part 3)", "back on top (part 4)"],
    },
    "lost in transmission": {
        "maps": [Maps.SPACEPORT],
        "new_quests": ["communication hideout"],
    },
    "communication hideout": {
        "maps": [Maps.BURIED_CITY],
        "new_quests": ["into the fray"],
    },
    "into the fray": {
        "maps": [Maps.DAM_BATTLEGROUNDS, Maps.BURIED_CITY, Maps.SPACEPORT, Maps.BLUE_GATE, Maps.RIVEN_TIDES],
        "new_quests": ["paving the way (part 1)", "combat recon"],
        "prerequisites": ["water troubles", "communication hideout"],
    },
    "combat recon": {
        "maps": [Maps.BURIED_CITY],
        "new_quests": ["bombing run"],
    },
    "bombing run": {
        "maps": [Maps.DAM_BATTLEGROUNDS, Maps.BURIED_CITY, Maps.SPACEPORT, Maps.BLUE_GATE, Maps.RIVEN_TIDES],
        "new_quests": [],
    },
    "paving the way (part 1)": {
        "maps": [Maps.DAM_BATTLEGROUNDS, Maps.SPACEPORT],
        "new_quests": ["paving the way (part 2)"],
    },
    "paving the way (part 2)": {
        "maps": [Maps.BURIED_CITY],
        "new_quests": ["deciphering the data"],
    },
    "deciphering the data": {
        "maps": [Maps.SPACEPORT],
        "new_quests": ["groundbreaking"],
    },
    "groundbreaking": {
        "maps": [Maps.BLUE_GATE],
        "new_quests": ["a dead end", "worth your salt"],
    },
    "a dead end": {
        "maps": [Maps.BLUE_GATE],
        "new_quests": ["a rising tide (part 1)", "fragmented logs"],
    },
    "a rising tide (part 1)": {
        "maps": [Maps.BURIED_CITY],
        "new_quests": ["a rising tide (part 2)"],
    },
    "a rising tide (part 2)": {
        "maps": [Maps.DAM_BATTLEGROUNDS],
        "new_quests": [],
    },
    "worth your salt": {
        "maps": [Maps.SPACEPORT],
        "new_quests": ["on deaf ears"],
    },
    "on deaf ears": {
        "maps": [Maps.STELLA_MONTIS],
        "new_quests": ["on the map"],
    },
    "on the map": {
        "maps": [Maps.SPACEPORT],
        "new_quests": [],
    },
    "dust on the wires": {
        "maps": [Maps.SPACEPORT],
        "new_quests": ["waking the grid", "fragmented logs"],
    },
    "fragmented logs": {
        "maps": [Maps.STELLA_MONTIS],
        "new_quests": ["furtive meetings"],
        "prerequisites": ["dust on the wires", "a dead end"],
    },
    "furtive meetings": {
        "maps": [Maps.STELLA_MONTIS],
        "new_quests": ["last entry"],
    },
    "last entry": {
        "maps": [Maps.STELLA_MONTIS],
        "new_quests": ["line in the sand"],
    },
    "outstanding balance": {
        "maps": [Maps.BLUE_GATE],
        "new_quests": ["settled in full"],
    },
    "clamoring for attention": {
        "maps": [Maps.BLUE_GATE],
        "new_quests": [],
    },
    "waking the grid": {
        "maps": [Maps.SPACEPORT],
        "new_quests": [],
    },
    "settled in full": {
        "maps": [Maps.DAM_BATTLEGROUNDS, Maps.BURIED_CITY, Maps.SPACEPORT, Maps.STELLA_MONTIS, Maps.BLUE_GATE, Maps.RIVEN_TIDES],
        "new_quests": [],
    },
    "test case": {
        "maps": [Maps.DAM_BATTLEGROUNDS, Maps.BURIED_CITY, Maps.SPACEPORT, Maps.STELLA_MONTIS, Maps.BLUE_GATE, Maps.RIVEN_TIDES],
        "new_quests": [],
        "prerequisites": ["the league (part 1)", "the league (part 2)"],
    },
    "line in the sand": {
        "maps": [Maps.BURIED_CITY],
        "new_quests": ["safe harbor"],
    },
    "safe harbor": {
        "maps": [Maps.RIVEN_TIDES],
        "new_quests": ["a wrench in the works"],
    },
    "a wrench in the works": {
        "maps": [Maps.SPACEPORT],
        "new_quests": [],
    },
    "battening down": {
        "maps": [Maps.RIVEN_TIDES],
        "new_quests": [],
    },
    "shoring up defenses": {
        "maps": [Maps.RIVEN_TIDES],
        "new_quests": [],
    },
    "collision course": {
        "maps": [Maps.DAM_BATTLEGROUNDS, Maps.BURIED_CITY, Maps.SPACEPORT, Maps.STELLA_MONTIS, Maps.BLUE_GATE, Maps.RIVEN_TIDES, Maps.RIVEN_TIDES],
        "new_quests": [],
    },
}

"""Battle Pass quest data for Arc Raiders."""

from quest_list import Maps

FIRST_QUESTS = ["picking up the pieces"]

quest_list = {
    "the major's footlocker": {
        "maps": [Maps.DAM_BATTLEGROUNDS],
        "new_quests": [],
    },
    "a symbol of unification": {
        "maps": [Maps.DAM_BATTLEGROUNDS],
        "new_quests": ["the major's footlocker"],
    },
    "unexpected initiative": {
        "maps": [Maps.BURIED_CITY],
        "new_quests": ["a symbol of unification"],
        "prerequisites": ["industrial espionage", "echoes of victory ridge"],
    },
    "dormant barons": {
        "maps": [Maps.DAM_BATTLEGROUNDS, Maps.SPACEPORT, Maps.BLUE_GATE],
        "new_quests": ["what we left behind (part 1)", "what we left behind (part 2)", "what we left behind (part 3)"],
        "prerequisites": ["the trifecta", "greasing her palms (part 1)", "greasing her palms (part 2)", "greasing her palms (part 3)"],
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
    "the trifecta": {
        "maps": [Maps.DAM_BATTLEGROUNDS, Maps.BURIED_CITY, Maps.SPACEPORT, Maps.BLUE_GATE],
        "new_quests": ["dormant barons"],
    },
    "hatch repairs": {
        "maps": [Maps.DAM_BATTLEGROUNDS, Maps.BURIED_CITY, Maps.SPACEPORT, Maps.STELLA_MONTIS, Maps.BLUE_GATE],
        "new_quests": ["down to earth"],
    },
    "down to earth": {
        "maps": [Maps.DAM_BATTLEGROUNDS, Maps.BURIED_CITY, Maps.SPACEPORT, Maps.BLUE_GATE],
        "new_quests": ["the trifecta"],
    },
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
        "new_quests": ["a bad feeling"],
    },
    "a bad feeling": {
        "maps": [Maps.DAM_BATTLEGROUNDS],
        "new_quests": ["the right tool", "hatch repairs"],
    },
    "greasing her palms (part 1)": {
        "maps": [Maps.DAM_BATTLEGROUNDS],
        "new_quests": ["dormant barons"],
    },
    "greasing her palms (part 2)": {
        "maps": [Maps.SPACEPORT],
        "new_quests": ["dormant barons"],
    },
    "greasing her palms (part 3)": {
        "maps": [Maps.BURIED_CITY],
        "new_quests": ["dormant barons"],
    },
    "the right tool": {
        "maps": [Maps.DAM_BATTLEGROUNDS, Maps.BURIED_CITY, Maps.SPACEPORT, Maps.STELLA_MONTIS, Maps.BLUE_GATE],
        "new_quests": ["a better use"],
    },
    "a better use": {
        "maps": [Maps.DAM_BATTLEGROUNDS, Maps.BURIED_CITY, Maps.SPACEPORT, Maps.BLUE_GATE],
        "new_quests": ["greasing her palms (part 1)", "greasing her palms (part 2)", "greasing her palms (part 3)"],
    },
}

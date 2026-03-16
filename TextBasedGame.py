#Zahra Harris
# Night of the Pumpkin King — Text Adventure (restart + start-over map)
SHOW_MAP_EVERY_TURN = True   # you can set False to show only on moves or when typing 'map'

START_ROOM = "Farm Gate"
VILLAIN_ROOM = "Pumpkin Throne"

REQUIRED_ITEMS = {
    "Serrated Saw", "Candle", "Matches",
    "Stencil Sheet", "Paring Knife", "Scoop",
}

ABBR = {  # short labels for the mini-map
    "Farm Gate": "FG",
    "Tool Shed": "TS",
    "Orchard Edge": "OE",
    "Corn Maze": "CM",
    "Pumpkin Patch": "PP",
    "Chapel Ruins": "CR",
    "Hay Barn": "HB",
    "Pumpkin Throne": "PT",
}

def make_rooms():
    """Return a FRESH copy of the world so items reset each new game."""
    return {
        "Farm Gate":      {"N": "Corn Maze",      "S": None,        "E": "Tool Shed",      "W": None,           "item": None},
        "Tool Shed":      {"N": "Pumpkin Patch",  "S": None,        "E": "Orchard Edge",   "W": "Farm Gate",    "item": "Serrated Saw"},
        "Orchard Edge":   {"N": "Chapel Ruins",   "S": None,        "E": None,             "W": "Tool Shed",    "item": "Candle"},
        "Corn Maze":      {"N": "Hay Barn",       "S": "Farm Gate", "E": "Pumpkin Patch",  "W": None,           "item": "Matches"},
        "Pumpkin Patch":  {"N": "Pumpkin Throne", "S": "Tool Shed", "E": "Chapel Ruins",   "W": "Corn Maze",    "item": "Stencil Sheet"},
        "Chapel Ruins":   {"N": None,             "S": "Orchard Edge","E": None,           "W": "Pumpkin Patch","item": "Paring Knife"},
        "Hay Barn":       {"N": None,             "S": "Corn Maze", "E": "Pumpkin Throne", "W": None,           "item": "Scoop"},
        "Pumpkin Throne": {"N": None,             "S": "Pumpkin Patch","E": None,          "W": "Hay Barn",     "item": None},
    }

def normalize_direction(d):
    d = d.strip().lower()
    mapping = {"n":"N","north":"N","s":"S","south":"S","e":"E","east":"E","w":"W","west":"W"}
    return mapping.get(d)

def normalize_item(s):
    return " ".join(s.strip().lower().split())

def list_exits(rooms, room):
    dirs = []
    for key, label in [("N","North"),("S","South"),("E","East"),("W","West")]:
        if rooms[room][key]:
            dirs.append(label)
    return ", ".join(dirs) if dirs else "None"

def parse_command(raw):
    text = raw.strip()
    if not text:
        return None, None
    parts = text.split(maxsplit=1)
    verb = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else ""
    if verb in {"n","s","e","w"}:
        return "go", verb
    return verb, arg

def render_map(rooms, current_room):
    def item_display(room_name):
        it = rooms[room_name]["item"]
        return it if it else "—"

    def cell(room_name):
        if room_name is None:
            return [" " * 21, " " * 21, " " * 21]
        ab = ABBR[room_name]
        title = f"[* {ab:^15} *]" if room_name == current_room else f"[  {ab:^15}  ]"
        full = room_name
        full = (full[:19] + "…") if len(full) > 21 else full
        it = item_display(room_name)
        line3 = f"Item: {it}" if it != "—" else "No item"
        line3 = (line3[:19] + "…") if len(line3) > 21 else line3
        return [title, f"{full:^21}", f"{line3:^21}"]

    layout = [
        ["Hay Barn", "Pumpkin Throne", None],           # top row
        ["Corn Maze", "Pumpkin Patch", "Chapel Ruins"], # middle row
        ["Farm Gate", "Tool Shed", "Orchard Edge"],     # bottom row
    ]

    print("\nMAP")
    print("-" * 70)
    for row in layout:
        lines = [[], [], []]
        for r in row:
            c = cell(r) if r is not None else [" " * 21, " " * 21, " " * 21]
            for i in range(3):
                lines[i].append(c[i])
        for i in range(3):
            print(("   ").join(lines[i]))
        print()
    print("-" * 70)
    print("Legend: [* XX *] = your current room; Items show if present.\n")

def one_game():
    """Run a single game; returns when player wins/loses/quits."""
    rooms = make_rooms()          # fresh world each run
    current = START_ROOM
    inventory = set()

    print("\nWelcome to Night of the Pumpkin King!")
    print("Collect all six tools, then enter the Pumpkin Throne.")
    print("Commands: 'go <north|south|east|west>' or 'get <item>'.")
    print("Extras: 'inventory', 'look', 'map', 'help', 'quit'.\n")

    # show the START map immediately so “reboot” is visual
    render_map(rooms, current)

    while True:
        print("-" * 50)
        print(f"Location: {current}")
        item_here = rooms[current]["item"]
        print("Visible item:", item_here if item_here else "None")
        print("Exits:", list_exits(rooms, current))
        print("Inventory:", ", ".join(sorted(inventory)) if inventory else "Empty")
        if SHOW_MAP_EVERY_TURN:
            render_map(rooms, current)

        raw = input("Enter command: ")
        verb, arg = parse_command(raw)

        if verb in {None, ""}:
            print("Please enter a command.")
            continue

        if verb == "quit":
            print("Goodbye!")
            # show current map snapshot before exiting one run
            render_map(rooms, current)
            return

        if verb == "help":
            print("Use 'go north/south/east/west' to move. Use 'get <item>' to pick up.")
            print("Win by holding all 6 tools and entering the Pumpkin Throne.")
            print("Use 'map' to reprint the map anytime.")
            continue

        if verb in {"look", "map"}:
            render_map(rooms, current)
            continue

        if verb == "inventory":
            print("You are carrying:", ", ".join(sorted(inventory)) if inventory else "nothing.")
            continue

        if verb == "go":
            dir_key = normalize_direction(arg)
            if not dir_key:
                print("Invalid direction. Use north, south, east, or west.")
                continue
            next_room = rooms[current][dir_key]
            if not next_room:
                print("You can't go that way.")
                continue
            current = next_room

            if current == VILLAIN_ROOM:
                if inventory.issuperset(REQUIRED_ITEMS):
                    print("\nYou step into the Pumpkin Throne, light the candle,")
                    print("trace the stencil, and carve the sigil. The King withers. YOU WIN!")
                else:
                    print("\nThe Pumpkin King rises from the throne. You came unprepared...")
                    print("The harvest claims you. GAME OVER.")
                render_map(rooms, current)  # final snapshot of the end state
                return

            print(f"You move to {current}.")
            if not SHOW_MAP_EVERY_TURN:
                render_map(rooms, current)
            continue

        if verb == "get":
            if not arg:
                print("Get what? (Example: get candle)")
                continue
            if item_here is None:
                print("There is nothing to pick up here.")
                continue
            if normalize_item(arg) != normalize_item(item_here):
                print(f"'{arg}' isn't here. You can pick up: {item_here}.")
                continue
            inventory.add(item_here)
            rooms[current]["item"] = None
            print(f"You picked up the {item_here}.")
            if inventory.issuperset(REQUIRED_ITEMS):
                print("You have all six tools! Find the Pumpkin Throne to finish this.")
            continue

        print("Invalid command. Try 'go <direction>' or 'get <item>'.")

def main():
    while True:
        one_game()  # plays a single run and returns on win/lose/quit
        again = input("\nPlay again from the start? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break
        # loop continues; next iteration calls one_game() which:
        # - builds a fresh world (items reset),
        # - shows the START map immediately

if __name__ == "__main__":
    main()
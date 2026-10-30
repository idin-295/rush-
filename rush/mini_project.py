
import os
import time

player_inventory = set()

game_state = {
    "iggy_awake": False,
    "iggy_moved": False,
    "iggy_key_collected": False,
    "joseph_suitcase_unlocked": False,
}


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPress Enter to continue...")


def get_choice(prompt, minimum, maximum):
    try:
        choice = int(input(prompt))
        if minimum <= choice <= maximum:
            return choice
        print("Invalid choice.")
    except ValueError:
        print("Please enter a number.")
    return None



kakyoin_room = {
    "description": (
        "You enter Kakyoin's tidy bedroom. "
        "A school uniform hangs beside the window."
    ),
    "objects": {
        1: ("School uniform", "The uniform is neatly folded."),
        2: ("Red painting", "A strange red painting hangs above the desk."),
        3: ("Desk", "There are pens, papers, and a notebook."),
        4: ("Bed", "The bed is neatly made."),
    }
}

avdol_room = {
    "description": (
        "You enter Avdol's room. The air smells faintly of incense. "
        "Strange decorations and books fill the shelves."
    ),
    "objects": {
        1: ("Bookshelf", "Books about ancient Egyptian history fill the shelves."),
        2: ("Incense burner", "A thin trail of smoke rises from the burner."),
        3: ("Desk", "A map of Egypt lies open on the desk."),
        4: ("Bed", "A dark red blanket covers the bed."),
    }
}

joseph_room = {
    "description": (
        "You enter Joseph Joestar's messy bedroom. "
        "Old furniture fills the room, and something rattles "
        "inside a leather suitcase."
    ),
    "objects": {
        1: ("Bed", "The blanket is messy. Someone slept here recently."),
        2: ("Wardrobe", "You find old coats and a photograph."),
        3: ("Desk", "There is an old map and a mysterious note."),
        4: ("Leather suitcase", "The suitcase is locked."),
        5: ("Pocket watch", "An old watch stopped at 3:15."),
    }
}

iggy_room = {
    "description": (
        "You enter Iggy's room. It smells like coffee and old furniture. "
        "Model airplanes cover the table. A small dog is sleeping "
        "on the bed, surrounded by scattered wrappers."
    ),
    "objects": {
        1: ("Model airplanes", "Several model airplanes sit on the table."),
        2: ("Brown fedora", "An old brown fedora hangs on the wall."),
        3: ("Storage box", "A dusty storage box sits in the corner."),
        4: ("Iggy", "A small dog is sleeping. He looks grumpy."),
        5: ("Bed", "The bed is messy, with something underneath it."),
    }
}

jojo_room = {
    "description": (
        "You enter a quiet, dark bedroom. A long black coat hangs "
        "beside the door. A white cap rests on the desk."
    ),
    "objects": {
        1: ("White cap", "A white cap with a golden emblem."),
        2: ("Black coat", "A heavy black coat hangs beside the door."),
        3: ("Desk", "Notes about strange humanoid figures lie on the desk."),
        4: ("Drawer", "Inside is an old photograph and a train ticket."),
        5: ("Pocket notebook", "A notebook filled with mysterious symbols."),
    }
}


npcs = {
    "old_man": {
        "name": "Old Man",
        "role": "Dorm Owner",
        "dialogue": (
            "Oh! Hello there, young man. Are you the new tenant?\n"
            "Could you do an old man a favor?\n"
            "I've forgotten where I put something important.\n"
            "It's my old pocket watch. I think I left it somewhere "
            "in this dorm.\n"
            "Could you look around and find it for me?\n"
            "Oh, my memory isn't what it used to be..."
        ),
        "quest": {
            "name": "The Missing Pocket Watch",
            "target_item": "pocket_watch",
            "completed": False
        }
    }
}



def talk_to_old_man():
    npc = npcs["old_man"]
    quest = npc["quest"]

    clear_screen()
    print(f"====== {npc['name']} ======\n")

    if quest["completed"]:
        print("Old Man: Ah, hello again, young man!")
        print("Old Man: Thank you for finding my pocket watch.")
        print("Old Man: Now... what was I doing again?")

    elif quest["target_item"] in player_inventory:
        print("Old Man: Wait a minute...")
        print("Old Man: Is that my pocket watch?!")
        print("Old Man: You found it! Thank you so much!")
        print("Old Man: I thought I had lost it forever!")

        quest["completed"] = True
        player_inventory.remove(quest["target_item"])

        print("\n*** QUEST COMPLETED ***")
        print(quest["name"])

    else:
        print(npc["dialogue"])

    pause()



def explore_room(room, room_name, collectible_choices=None):
    if collectible_choices is None:
        collectible_choices = set()

    while True:
        clear_screen()
        print(f"====== {room_name.upper()} ======\n")
        print(room["description"])
        print("\nWhat do you want to inspect?")

        for number, (name, description) in room["objects"].items():
            print(f"{number}. {name}")

        exit_choice = max(room["objects"]) + 1
        print(f"{exit_choice}. Return to main hall")

        choice = get_choice(
            f"\nChoose 1-{exit_choice}: ", 1, exit_choice
        )

        if choice is None:
            pause()
            continue

        if choice == exit_choice:
            break

        name, description = room["objects"][choice]
        print(f"\nYou inspect the {name}.")
        print(description)

        if room is joseph_room and choice == 4:
            if game_state["joseph_suitcase_unlocked"]:
                print("\nThe suitcase is already unlocked.")
                print("Inside, you find some old photographs.")

            elif "rusty_key" in player_inventory:
                answer = input(
                    "\nUse the rusty key to unlock it? (y/n): "
                ).strip().lower()

                if answer == "y":
                    player_inventory.remove("rusty_key")
                    game_state["joseph_suitcase_unlocked"] = True

                    print("\nThe key fits!")
                    print("You unlock the suitcase.")
                    print("Inside are old photographs and a letter.")

            else:
                print("You need a key to open the suitcase.")

        elif room is joseph_room and choice == 5:
            item_id = "pocket_watch"

            if npcs["old_man"]["quest"]["completed"]:
                print("You have already returned this watch.")

            elif item_id in player_inventory:
                print("You already have the pocket watch.")

            else:
                answer = input(
                    "\nPick up the pocket watch? (yes/no): "
                ).strip().lower()

                if answer == "yes":
                    player_inventory.add(item_id)
                    print("You picked up the pocket watch!")

        elif room is jojo_room and choice == 5:
            item_id = "jojo_notebook"

            if item_id in player_inventory:
                print("You already have the notebook.")
            else:
                answer = input("\nPick up the notebook? (yes/no): ").strip().lower()
                if answer == "yes":
                    player_inventory.add(item_id)
                    print("You picked up the notebook!")

        input("\nPress Enter to continue...")


def room_of_iggy():
    while True:
        clear_screen()

        print("====== IGGY'S ROOM ======\n")
        print(iggy_room["description"])

        print("\nWhat do you want to do?")
        print("1. Inspect model airplanes")
        print("2. Inspect the brown fedora")
        print("3. Search the storage box")
        print("4. Interact with Iggy")
        print("5. Inspect the bed")
        print("6. Return to main hall")

        choice = get_choice("\nChoose 1-6: ", 1, 6)

        if choice is None:
            pause()
            continue

        # Find hidden coffee-flavored gum
        if choice == 1:
            print("\nYou inspect the model airplanes.")

            if "coffee_gum" in player_inventory:
                print("You already found everything here.")
            else:
                print(
                    "Behind one of the model airplanes, "
                    "you discover a packet of coffee-flavored gum!"
                )

                answer = input("Pick up the gum? (y/n): ").strip().lower()

                if answer == "y":
                    player_inventory.add("coffee_gum")
                    print("You picked up the coffee-flavored gum.")

        elif choice == 2:
            print("\nYou inspect the brown fedora.")
            print("It is dusty and smells faintly of dog fur.")
            print("You decide not to wear it.")

        elif choice == 3:
            print("\nYou search the storage box.")

            if not game_state["iggy_moved"]:
                print(
                    "Iggy is sleeping nearby. You don't want "
                    "to make too much noise."
                )
                print("Perhaps you should distract him first.")

            elif game_state["iggy_key_collected"]:
                print("The box is empty except for dust and spider webs.")

            else:
                print("You find some old newspapers and broken toys.")
                print("There is nothing useful inside.")

        # Feed Iggy and make him move away from the bed
        elif choice == 4:
            print("\nYou approach Iggy.")

            if game_state["iggy_moved"]:
                print("Iggy is busy chewing gum and ignoring you.")

            elif "coffee_gum" in player_inventory:
                print("Iggy wakes up and stares at the gum.")
                answer = input(
                    "Give Iggy the coffee-flavored gum? (y/n): "
                ).strip().lower()

                if answer == "y":
                    player_inventory.remove("coffee_gum")
                    game_state["iggy_awake"] = True
                    game_state["iggy_moved"] = True

                    print("\nIggy snatches the gum from your hand!")
                    print(
                        "He jumps off the bed and runs toward "
                        "the corner to chew it."
                    )
                    print("Something rusty is now visible under the bed.")

                else:
                    print("You keep the gum for now.")

            else:
                print("Iggy growls at you.")
                print('"Grrr... Woof!"')
                print("He refuses to move. Maybe he wants a treat.")

        # Reveal and collect the rusty key
        elif choice == 5:
            print("\nYou inspect the bed.")

            if not game_state["iggy_moved"]:
                print("Iggy is occupying the bed.")
                print("You cannot search underneath while he is there.")

            elif game_state["iggy_key_collected"]:
                print("You have already taken everything useful from here.")

            elif "rusty_key" in player_inventory:
                print("You already have the rusty key.")

            else:
                print(
                    "Under the bed, you find an old rusty key "
                    "covered in dust."
                )

                answer = input("Pick up the rusty key? (y/n): ").strip().lower()

                if answer == "y":
                    player_inventory.add("rusty_key")
                    game_state["iggy_key_collected"] = True
                    print("\nYou picked up the rusty key!")
                    print("It might unlock something in the dorm.")

        elif choice == 6:
            print("You leave Iggy's room.")
            time.sleep(1)
            break

        pause()


def room_of_kakyoin():
    explore_room(kakyoin_room, "Kakyoin's Room")


def room_of_Muhammed_Avdul():
    explore_room(avdol_room, "Muhammad Avdol's Room")


def room_of_joseph():
    explore_room(
        joseph_room,
        "Joseph's Room",
        collectible_choices={5}
    )


def room_of_jostar():
    explore_room(iggy_room, "Iggy's Room")


def room_of_jojo():
    explore_room(
        jojo_room,
        "JoJo's Room",
        collectible_choices={5}
    )

def show_inventory():
    clear_screen()
    print("====== INVENTORY ======\n")

    if not player_inventory:
        print("Your inventory is empty.")
    else:
        for item in sorted(player_inventory):
            print(f"- {item.replace('_', ' ').title()}")

    pause()

def main():
    while True:
        clear_screen()

        print("========= MAIN HALL =========")
        print("1. Kakyoin's Room")
        print("2. Muhammad Avdol's Room")
        print("3. Joseph's Room")
        print("4. Iggy's Room")
        print("5. JoJo's Room")
        print("6. Talk to Old Man")
        print("7. Check Inventory")
        print("8. Exit the building")

        choice = get_choice("\nChoose 1-8: ", 1, 8)

        if choice is None:
            pause()
            continue

        match choice:
            case 1:
                room_of_kakyoin()
            case 2:
                room_of_Muhammed_Avdul()
            case 3:
                room_of_joseph()
            case 4:
                room_of_iggy()
            case 5:
                room_of_jojo()
            case 6:
                talk_to_old_man()
            case 7:
                show_inventory()
            case 8:
                print("\nYou leave the building. Goodbye!")
                break

if __name__ == "__main__":
    clear_screen()

    print("========================================")
    print("       THE ABANDONED DORMITORY")
    print("========================================\n")

    print("An old man sits beside the entrance.")
    print("He looks confused as you approach him.\n")

    time.sleep(1)

    print("Old Man:")
    print(npcs["old_man"]["dialogue"])

    pause()
    main()

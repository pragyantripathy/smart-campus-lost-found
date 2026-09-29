# Smart Campus Lost & Found Matching System
# Simple version: lost items are matched with found items using a score out of 100.

from datetime import datetime

# Common words that should not count as a "match"
STOP_WORDS = ["a", "an", "the", "and", "with", "in", "on", "at", "of",
              "near", "found", "lost", "is", "was", "for", "to"]


class Item:
    def __init__(self, item_id, name, category, color, location,
                 description, date_reported, owner_name):
        self.item_id = item_id
        self.name = name
        self.category = category
        self.color = color
        self.location = location
        self.description = description
        self.date_reported = date_reported
        self.owner_name = owner_name
        self.status = "active"   # becomes "returned" once handed back


lost_items = []
found_items = []


# ---------- Helper functions ----------

def clean(text):
    """Lowercase the text and remove extra spaces."""
    return " ".join(text.lower().split())


def get_keywords(text):
    """Return the important words of a text (stop words removed)."""
    words = clean(text).split()
    keywords = set()
    for word in words:
        if word not in STOP_WORDS:
            keywords.add(word)
    return keywords


def is_valid_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def find_item(items, item_id):
    """Search a list for an item with the given ID."""
    for item in items:
        if item.item_id == item_id:
            return item
    return None


def id_exists(item_id):
    return find_item(lost_items, item_id) is not None or \
           find_item(found_items, item_id) is not None


# ---------- Matching logic ----------

def calculate_score(lost, found):
    """Score out of 100:
       category 25 + color 20 + location 20 + keywords 25 + date 10"""
    score = 0

    # Category
    if clean(lost.category) == clean(found.category):
        score += 25

    # Color
    if clean(lost.color) == clean(found.color):
        score += 20

    # Location (partial match allowed: "library" matches "library study hall")
    lost_place = clean(lost.location)
    found_place = clean(found.location)
    if lost_place in found_place or found_place in lost_place:
        score += 20

    # Keywords from name + description (5 points per common word, max 25)
    lost_words = get_keywords(lost.name + " " + lost.description)
    found_words = get_keywords(found.name + " " + found.description)
    common = lost_words & found_words
    score += min(len(common) * 5, 25)

    # Date (dates are already checked when the item is added)
    lost_date = datetime.strptime(lost.date_reported, "%Y-%m-%d")
    found_date = datetime.strptime(found.date_reported, "%Y-%m-%d")
    days_apart = abs((found_date - lost_date).days)
    if days_apart <= 2:
        score += 10
    elif days_apart <= 7:
        score += 5

    return score


def find_matches(lost):
    """Return a list of (score, found_item), best match first."""
    results = []
    for found in found_items:
        if found.status != "active":
            continue   # skip items already returned
        results.append((calculate_score(lost, found), found))
    results.sort(key=lambda pair: pair[0], reverse=True)
    return results


# ---------- Input / output ----------

def collect_item():
    """Ask the user for item details and return an Item."""
    while True:
        item_id = input("Enter item ID: ").strip()
        if item_id == "":
            print("ID cannot be empty.")
        elif id_exists(item_id):
            print("This ID is already used. Try another one.")
        else:
            break

    name = input("Enter item name: ")
    category = input("Enter item category: ")
    color = input("Enter item color: ")
    location = input("Enter location: ")
    description = input("Enter item description: ")

    while True:
        date_reported = input("Enter date (YYYY-MM-DD): ").strip()
        if is_valid_date(date_reported):
            break
        print("Invalid date. Please use the format YYYY-MM-DD.")

    owner_name = input("Enter owner/contact name: ")

    return Item(item_id, name, category, color, location,
                description, date_reported, owner_name)


def show_matches():
    item_id = input("Enter lost item ID to find matches: ").strip()
    lost = find_item(lost_items, item_id)

    if lost is None:
        print("Lost item not found.")
        return

    matches = find_matches(lost)
    if len(matches) == 0:
        print("No found items available.")
        return

    print("\nTop possible matches:")
    number = 1
    for score, found in matches[:5]:
        print(f"{number}. [{found.item_id}] {found.name} ({found.category}) - Match: {score}%")
        print(f"   Location: {found.location} | Color: {found.color} | Date: {found.date_reported}")
        print(f"   Description: {found.description}")
        number += 1


def mark_returned():
    item_id = input("Enter found item ID that was returned: ").strip()
    found = find_item(found_items, item_id)

    if found is None:
        print("Found item not found.")
    else:
        found.status = "returned"
        print("Item marked as returned. It will not appear in matches anymore.")


def add_sample_data():
    lost_items.append(Item("L-101", "Black Wallet", "wallet", "black", "library",
                           "Black leather wallet with academic ID and cash",
                           "2026-09-15", "Aisha"))
    found_items.append(Item("F-202", "Black Leather Wallet", "wallet", "black", "library",
                            "Found near the library study hall; leather wallet",
                            "2026-09-16", "Campus Desk"))
    lost_items.append(Item("L-102", "Notebook", "notebook", "red", "engineering block",
                           "Red spiral notebook with mathematics notes",
                           "2026-09-17", "Rahul"))
    found_items.append(Item("F-203", "Notebook", "notebook", "red", "engineering block",
                            "Red notebook found in classroom 204",
                            "2026-09-18", "Campus Desk"))


def print_menu():
    print("\nSMART CAMPUS LOST & FOUND MATCHING SYSTEM")
    print("1. Add Lost Item")
    print("2. Add Found Item")
    print("3. Find Matches")
    print("4. Mark Found Item as Returned")
    print("5. Exit")


def main():
    add_sample_data()

    while True:
        print_menu()
        option = input("Choose an option: ").strip()

        if option == "1":
            lost_items.append(collect_item())
            print("Lost item added successfully.")
        elif option == "2":
            found_items.append(collect_item())
            print("Found item added successfully.")
        elif option == "3":
            show_matches()
        elif option == "4":
            mark_returned()
        elif option == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


main()

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any


@dataclass
class Item:
    item_id: str
    name: str
    category: str
    color: str
    location: str
    description: str
    date_reported: str
    owner_name: str = ""
    status: str = "active"


class LostFoundSystem:
    def __init__(self):
        self.lost_items: List[Item] = []
        self.found_items: List[Item] = []

    def normalize_text(self, text: str) -> str:
        return " ".join(text.lower().split())

    def compute_match_score(self, lost_item: Item, found_item: Item) -> float:
        score = 0.0

        if lost_item.category.lower() == found_item.category.lower():
            score += 25
        else:
            score += 5

        if lost_item.color.lower() == found_item.color.lower():
            score += 20

        if lost_item.location.lower() == found_item.location.lower():
            score += 20

        lost_keywords = set(self.normalize_text(lost_item.name + " " + lost_item.description).split())
        found_keywords = set(self.normalize_text(found_item.name + " " + found_item.description).split())
        common_keywords = lost_keywords & found_keywords
        score += min(len(common_keywords) * 10, 25)

        try:
            lost_date = datetime.strptime(lost_item.date_reported, "%Y-%m-%d")
            found_date = datetime.strptime(found_item.date_reported, "%Y-%m-%d")
            days_apart = abs((found_date - lost_date).days)
            if days_apart <= 2:
                score += 10
            elif days_apart <= 7:
                score += 5
        except ValueError:
            pass

        if self.normalize_text(lost_item.description) in self.normalize_text(found_item.description):
            score += 10

        return round(score, 2)

    def add_lost_item(self, item: Item):
        self.lost_items.append(item)

    def add_found_item(self, item: Item):
        self.found_items.append(item)

    def find_matches(self, lost_item: Item) -> List[Dict[str, Any]]:
        matches = []
        for found_item in self.found_items:
            score = self.compute_match_score(lost_item, found_item)
            matches.append({"found_item": found_item, "score": score})
        matches.sort(key=lambda m: m["score"], reverse=True)
        return matches


def create_sample_data():
    system = LostFoundSystem()

    lost1 = Item(item_id="L-101",name="Black Wallet",category="wallet",color="black",location="library",description="Black leather wallet with academic ID and cash",date_reported="2026-09-15",owner_name="Aisha")
    found1 = Item(item_id="F-202",name="Black Leather Wallet",category="wallet",color="black",location="library",description="Found near the library study hall; leather wallet",date_reported="2026-09-16",owner_name="Campus Desk")

    lost2 = Item(item_id="L-102", name="Notebook", category="notebook", color="red", location="engineering block", description="Red spiral notebook with mathematics notes", date_reported="2026-09-17", owner_name="Rahul")
    found2 = Item(item_id="F-203",name="Notebook",category="notebook",color="red",location="engineering block",description="Red notebook found in classroom 204",date_reported="2026-09-18",owner_name="Campus Desk",)
    system.add_lost_item(lost1)
    system.add_found_item(found1)
    system.add_lost_item(lost2)
    system.add_found_item(found2)
    return system


def print_menu():
    print("\nSMART CAMPUS LOST & FOUND MATCHING SYSTEM")
    print("1. Add Lost Item")
    print("2. Add Found Item")
    print("3. Find Matches")
    print("4. Exit")


def collect_item():
    item_id = input("Enter item ID: ")
    name = input("Enter item name: ")
    category = input("Enter item category: ")
    color = input("Enter item color: ")
    location = input("Enter lost/found location: ")
    description = input("Enter item description: ")
    date_reported = input("Enter date (YYYY-MM-DD): ")
    owner_name = input("Enter owner/contact name: ")

    return Item(item_id=item_id,name=name,category=category,color=color,location=location,description=description,date_reported=date_reported,owner_name=owner_name,status="active",)


def main():
    system = create_sample_data()

    while True:
        print_menu()
        option = input("Choose an option: ")

        if option == "1":
            item = collect_item()
            system.add_lost_item(item)
            print("Lost item added successfully.")

        elif option == "2":
            item = collect_item()
            system.add_found_item(item)
            print("Found item added successfully.")

        elif option == "3":
            item_id = input("Enter lost item ID to find matches: ")
            lost_item = None
            for item in system.lost_items:
                if item.item_id == item_id:
                    lost_item = item
                    break

            if lost_item is None:
                print("Lost item not found.")
                continue

            matches = system.find_matches(lost_item)
            print("\nRanked possible matches:")
            if not matches:
                print("No matches found.")
                continue

            for index, match in enumerate(matches[:5], start=1):
                found_item = match["found_item"]
                print(f"{index}. {found_item.name} ({found_item.category}) - Score: {match['score']}%")
                print(f"   Location: {found_item.location} | Color: {found_item.color} | Date: {found_item.date_reported}")
                print(f"   Description: {found_item.description}")

        elif option == "4":
            print("Exiting the system. Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()

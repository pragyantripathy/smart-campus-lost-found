# Smart Campus Lost & Found Matching System

A smart campus solution to help students and campus staff report lost items and receive intelligent suggestions for matching found items using item characteristics, keywords, and time proximity.

## Project Title
Smart Campus Lost & Found Matching System

## Overview
The system is designed to reduce the time and effort required to recover lost belongings on campus. Students can report lost items while staff can register found items, and the system intelligently compares both using attributes such as item name, category, color, location, description, and date reported. The result is a ranked list of likely matches, helping users recover items quickly and efficiently.

## Problem Statement
On many campuses, lost items are reported separately without a structured way to connect them with found items. This often leads to delays, confusion, and a lower chance of retrieving personal belongings. There is a growing need for a digital and intelligent lost-and-found system that can assist students and campus administrators.

## Scope of the Project
This project focuses on building a simple but practical prototype for a campus lost and found system. It is intended to support item reporting, item matching, and quick identification of possible matches. The solution is scalable and can be extended into a larger web or mobile application in the future.

## Target Users
- Students
- Campus security staff
- Lost and found desk administrators
- Faculty and administrative office staff

## High-Level Features
- Report lost items
- Report found items
- Store item metadata such as name, category, color, and location
- Match lost items with found items using similarity scoring
- Suggest the most likely matches based on keyword overlap and item attributes
- Simplify the recovery process for both students and staff

## Technologies / Tools Used
- Python 3
- Standard Python libraries
- Object-oriented programming
- CLI-based user interaction

## Steps to Install & Run the Project
1. Clone the repository
   ```bash
   git clone https://github.com/pragyantripathy/smart-campus-lost-found.git
   cd smart-campus-lost-found
   ```
2. Ensure Python 3 is installed on your machine.
3. Run the project using:
   ```bash
   python source_code.py
   ```

## Instructions for Testing
1. Run the program.
2. Add one or more lost items.
3. Add one or more found items.
4. Search for possible matches using the lost item ID.
5. Review the ranked matches displayed by the system.
6. Confirm that the highest-scoring item is the most relevant match.

## Example Output
```text
SMART CAMPUS LOST & FOUND MATCHING SYSTEM
1. Add Lost Item
2. Add Found Item
3. Find Matches
4. Exit
```

The system will display a ranked list of likely matches with their scores and attributes.

## Project Status
This is a working prototype demonstrating smart matching logic for campus lost and found item recovery.

## Future Enhancements
- Add database support
- Create a web interface
- Add image-based item recognition
- Use a more advanced ML-based matching model
- Integrate with student ID or campus authentication systems

## Screenshots
Screenshots can be added later to show the CLI workflow and sample match results.

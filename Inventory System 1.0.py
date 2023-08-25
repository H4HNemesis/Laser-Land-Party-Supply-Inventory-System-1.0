#Laser Land Party Supply Inventory System V1.0!
#Programmed by Noah Kim
#Last updated 8/24/2023
import sys
sys.path.append("../../")
from appJar import gui
import json

#Uncommment the inventory file of your choice:
data_file = "inventory.json" #used for the official version
#data_file = "inventory_test.json" #used for the demo version

def read_inventory():
    with open(data_file, "r") as file:
        return json.load(file)
def write_inventory(data):
    with open(data_file, "w") as file:
        json.dump(data, file, indent=4)
inventory = read_inventory()

def on_cancel():
    app.stop()

def on_submit_party(button):
    if button == "Submit Party":
        theme = app.getOptionBox("Theme")
        participants = int(app.getEntry("Participants"))
        parents = int(app.getEntry("Parents"))
        lemonades = int(app.getEntry("Lemonades"))
        if theme == "Neon":
            inventory['neon']['plate'] -= participants
            inventory['neon']['cake plate'] -= participants
            inventory['neon']['cup'] -= participants
            inventory['neon']['fork'] -= participants
            inventory['neon']['spoon'] -= participants
            inventory["basic"]["cake plate"] -= parents
            inventory["basic"]["fork"] -= parents
            inventory["both"]["lemonade"] -= lemonades
            inventory["both"]["table_covers"] -= 3
        elif theme == "General":
            inventory["basic"]["plates"] -= participants
            inventory["basic"]["cake plate"] -= participants + parents
            inventory["basic"]["cup"] -= participants
            inventory["basic"]["fork"] -= participants
            inventory["basic"]["spoon"] -= participants
            inventory["both"]["lemonade"] -= lemonades
            inventory["both"]["table_covers"] -= 3
    else:
        pass
    check()

def on_submit_supplies(button):
    if button == "Submit Supplies":
        bathroom = app.getOptionBox("Bathroom")
        toilet_paper = int(app.getEntry("bathroom", "Toilet Paper"))
        paper_towels = int(app.getEntry("bathroom", "Paper towels"))
        if bathroom == "Men":
            inventory['bathroom']['toilet paper'] -= toilet_paper
            inventory['bathroom']['paper towels'] -= paper_towels
            check()
        elif bathroom == "Women":
            inventory['bathroom']['toilet paper'] -= toilet_paper
            inventory['bathroom']['paper towels'] -= paper_towels
            check()
    else:
        check()


def on_restock(button):
    if button == "Add To Inventory":
        neon_boxes = int(app.getEntry("Restock Neon Supplies (in boxes, 36 sets per box)"))
        neon_cakeplates = int(app.getEntry("Restock Neon Cake Plates (individually counted)"))
        basic_plates = int(app.getEntry("Restock Basic Plates"))
        basic_cakeplates = int(app.getEntry("Restock Basic Cake Plates"))
        basic_cups = int(app.getEntry("Restock Basic Cups"))
        basic_forks = int(app.getEntry("Restock Basic Forks"))
        basic_spoons = int(app.getEntry("Restock Basic Spoons"))
        table_cover_rolls = int(app.getEntry("Restock Table Cover Rolls"))
        lemonades = int(app.getEntry("Restock Lemonade"))
        toilet_paper = int(app.getEntry("Restock Toilet Papers"))
        paper_towels = int(app.getEntry("Restock Paper Towels"))
        
        inventory['neon']['plate'] += (32 * neon_boxes)
        inventory['neon']['cake plate'] += neon_cakeplates
        inventory['neon']['cup'] += (32 * neon_boxes)
        inventory['neon']['fork'] += (32 * neon_boxes)
        inventory['neon']['spoon'] += (32 * neon_boxes)
        
        inventory['basic']['plate'] += basic_plates
        inventory['basic']['cake plate'] += basic_cakeplates
        inventory['basic']['cup'] += basic_cups
        inventory['basic']['fork'] += basic_forks
        inventory['basic']['spoon'] += basic_spoons
        
        inventory['both']['lemonade'] += lemonades
        inventory['both']['table covers'] += (30 * table_covers_rolls)
        
        inventory['bathroom']['toilet paper'] += toilet_paper
        inventory['bathroom']['paper towels'] += paper_towels
        write_inventory(inventory)
        app.infoBox("Restock", "Supplies have been added to inventory.")
        display_inventory()
        check()
    else:
        check()

def check():
    selected_theme = app.getOptionBox("Theme").lower()
    theme_inventory = inventory[selected_theme]
    
    low_supplies = []

    if selected_theme == "both":
        if theme_inventory['lemonade'] < 6:
            low_supplies.append("Lemonade for Both theme")
        if theme_inventory['table cover'] < 2:
            low_supplies.append("Table Covers for Both theme")
    elif selected_theme == "bathroom":
        if theme_inventory['paper towels'] < 5:
            low_supplies.append("Paper Towels for Bathroom theme")
        if theme_inventory['toilet paper'] < 5:
            low_supplies.append("Toilet Paper for Bathroom theme")
    else:
        for item, quantity in theme_inventory.items():
            if quantity < 24:
                low_supplies.append(f"{item.capitalize()} for {selected_theme.capitalize()} theme")

    if low_supplies:
        app.setFont(12)
        alert_message = "Please ask Greg to order more of the following supplies:\n"
        alert_message += "\n".join(low_supplies)
        app.infoBox("Low Supplies Alert", alert_message)
        #message_Greg()
    else:
        participants = int(app.getEntry("Participants")) if app.getEntry("Participants") else 0
        parents = int(app.getEntry("Parents")) if app.getEntry("Parents") else 0
        if any(theme_inventory[item] < participants for item in theme_inventory) or theme_inventory['cake plate'] < parents or theme_inventory['fork'] < parents:
            app.errorBox("Error", "Report uses more supplies than available!")
        else:
            app.infoBox("Report Successful", "Stock is good.")


def display_inventory():
    inventory_text = ""
    for item, quantity in inventory.items():
        inventory_text += f"{item}: {quantity}\n"
    
    app.setTextArea("inventory_display", inventory_text)

#def message_Greg(): This feature is still in development
    
app = gui()
app.setBg("orange")

app.startTabbedFrame("Laser Land Inventory System V0.9 (Test version)")

# Main Menu
app.startTab("Main Menu")
app.addLabel("l1", "Welcome to the Laser Land Supply Inventory System!")
app.addLabel("12", "Use this program to report the number of supplies used in a party AFTER the party is complete.")
app.addLabel("13", "If it tells you to message Greg... Please please please please please message Greg!")
app.stopTab()

# Report a Party
app.startTab("Report a Party")
app.addLabel("l4", "Report a Party")
theme = app.addLabelOptionBox("Theme", ["Neon", "General"], 1, 0)
participants = app.addLabelEntry("Participants", 2, 0)
parents = app.addLabelEntry("Parents", 3, 0)
lemonades = app.addLabelEntry("Lemonades", 4, 0)
app.addButtons(["Submit Party", "Cancel Party"], on_submit_party, colspan=2)
app.stopTab()

# Bathroom/Cleaning supplies
app.startTab("Bathroom/Cleaning supplies")
app.addLabel("l5", "Bathroom/Cleaning supplies")
app.addLabelOptionBox("Bathroom", ["Men", "Women"], 5, 0)
toilet_paper = app.addLabelEntry("Toilet Paper", 6, 0)
paper_towels = app.addLabelEntry("Paper towels", 7, 0)
app.addButtons(["Submit Supplies", "Cancel Supplies"], on_submit_supplies, colspan=2)
app.stopTab()

# View inventory
app.startTab("Inventory")
app.addLabel("16", "Current Inventory:")
app.addTextArea("inventory_display")
display_inventory()
app.addButton("Refresh", display_inventory)
app.stopTab()

# Restock Supplies
app.startTab("Restock Supplies")
app.addLabel("l7", "Restock Supplies")
neon_boxes_added = app.addLabelEntry("Restock Neon Supplies (in boxes, 36 sets per box)", 8, 0)
neon_cakeplates_added = app.addLabelEntry("Restock Neon Cake Plates (individually counted)", 9, 0)
plates = app.addLabelEntry("Restock Basic Plates", 10, 0)
cakeplates = app.addLabelEntry("Restock Basic Cake Plates", 11, 0)
cups = app.addLabelEntry("Restock Basic Cups", 12, 0)
forks = app.addLabelEntry("Restock Basic Forks", 13, 0)
spoons = app.addLabelEntry("Restock Basic Spoons", 14, 0)
lemonades_added = app.addLabelEntry("RestockLemonade", 15, 0)
table_covers = app.addLabelEntry("RestockTableCovers", 16, 0)
pt_added = app.addLabelEntry("Restock Paper Towels", 17, 0)
tp_added = app.addLabelEntry("Restock Toilet PaperS", 18, 0)
app.addButtons(["Add To Inventory", "Cancel Restock"], on_restock, colspan=2)
app.stopTab()

#Message Greg
app.startTab("Message Greg")
app.addLabel("18", "In the future, this program will send a Telegram message to Greg, when supplies are low.")
app.addLabel("19", "This feature is still in development... check back soon!")
app.stopTab()
             
app.stopTabbedFrame()
app.go()

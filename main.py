import json
from datetime import datetime as dt

with open('files.json') as f:
    files = json.load(f)
file_ids = []
for file in files:
    file_ids.append(file["file_id"])

def select_action():
    print("__Actions__\n1 : Select Contact\n2 : Add Contact")
    choice = input("Enter your choice (Enter 'e' to exit) : ")
    return choice

def add_contact():
    print("____ADD CONTACT____")
    with open('contacts.json') as f:
        contacts = json.load(f)
    new_contact = {"contact_id":contacts[-1]["contact_id"]+1, "contact_name":"", "contact_number":"", "files_shared": []}
    new_contact["contact_name"] = input("Enter Contact Name : ")
    new_contact["contact_number"] = input("Enter Contact Number : ")
    contacts.append(new_contact)
    with open('contacts.json','w') as f:
        json.dump(contacts, f, indent=4)
    print("Contact added successfully.")

def select_contact():
    contact_ids = []
    print("____CONTACTS____")
    with open('contacts.json') as f:
        contacts = json.load(f)
    for contact in contacts:
        contact_ids.append(contact["contact_id"])
        print(contact["contact_id"], ":", contact["contact_name"])
    choice = input("Select a contact (Enter 'b' to go back) : ")
    return choice, contact_ids

def select_file(contact_id):
    with open('contacts.json') as f:
        contacts = json.load(f)
    recent_files = []
    for contact in contacts:
        if contact["contact_id"]==contact_id:
            recent_files = contact["files_shared"]
    print("____RECENT FILES____")
    for file in recent_files:
        print(file["file_id"], ":", file["file_name"], "\t", dt.fromtimestamp(file["recent_share"]), "\t", file["share_count"])
    print("____ALL FILES____")
    for file in files:
        print(file["file_id"], ":", file["file_name"])
    choice = input("Select file to send (Enter 'b' to go back) : ")
    return choice

def send_file(file_id, contact_id):
    file_name = ''
    for file in files:
        if file_id==file["file_id"]:
            file_name = file["file_name"]
    with open('contacts.json') as f:
        contacts = json.load(f)
    for contact in contacts:
        if contact_id==contact["contact_id"]:
            for file in contact["files_shared"]:
                if file["file_id"]==file_id:
                    file["share_count"] += 1
                    file["recent_share"] = int(dt.now().timestamp())
                    break
            else:
                contact["files_shared"].append({"file_id":file_id, "file_name":file_name, "share_count":1, "recent_share": int(dt.now().timestamp())})
            with open('contacts.json', 'w') as f:
                json.dump(contacts, f, indent=4)
            print("File sent successfully")
            break


if __name__ == "__main__":
    while True:
        choice = select_action()
        if choice not in ["1", "2", "e"]:
            print("Invalid Choice")

        elif choice=="1":
            while True:
                selected_contact, contact_ids = select_contact()
                if selected_contact!='b' and selected_contact not in map(str, contact_ids):
                    print("Invalid Choice")
                    continue
                elif selected_contact=='b':
                    break
                else:
                    while True:
                        selected_file = select_file(int(selected_contact))
                        if selected_file!='b' and selected_file not in map(str, file_ids):
                            print("invalid Choice")
                            continue
                        elif selected_file=='b':
                            break
                        else:
                            send_file(int(selected_file), int(selected_contact))
                            break

        elif choice=="2":
            add_contact()

        else:
            quit()

        
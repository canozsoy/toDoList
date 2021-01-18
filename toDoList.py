import difflib
import json


def initialStart(usrList, data):
    print("Welcome, this is a 'To do List Application!. This is the First Time Execution of the Application!\nPress Ctrl + c to Abort")
    updatedData = newUser(usrList, data)
    return updatedData


def newUser(usrList, data):
    regSwitch = input("Would you like to register? (y/n)?\n")
    if regSwitch == "y":
        usrName = input("Please enter your username:\n")
        if " " in usrName:
            usrName = usrName.replace(" ", "")
            print("Your username changed to " + usrName)
        while usrName in usrList:
            usrName = input("Username exists, please select another username!\n")
        print("Welcome, " + usrName + "!\nYour list is empty!")
        todoList = ""
        updatedList = decisioner(todoList)
        data['users'].append({
            'username': usrName,
            'list': updatedList
        })
        print(data)
    elif regSwitch == "n":
        print("As you wish!\n")
    else:
        print("Incorrect Input Type!")
    return data


def existingUser(usrList, data):
    usrName = input("Please enter your username:\n")
    usrName, newSwitch = checkIfExist(usrName, usrList)
    if newSwitch == 1:
        data = newUser(usrList, data)
    else:
        index = usrList.index(usrName)
        todoList = data['users'][index]["list"]
        if not todoList:
            print("Your list is empty!")
        else:
            print("Your list is as follows:\n\n" + todoList)
        updatedList = decisioner(todoList)
        data['users'][index]["list"] = updatedList
    return data


def addElement(todoList):
    addItem = input("What would you like to add?\n")
    ltodoList = todoList.splitlines()
    ltodoList.append(addItem)
    return ltodoList


def delElement(todoList):
    remItem = input("Which element would you like to remove?\n")
    ltodoList = todoList.splitlines()
    if remItem in ltodoList:
        ltodoList.remove(remItem)
    else:
        index = int(input("Item not found, please enter number of item.\n"))
        listLength = ltodoList.__len__()
        if (index-1) < listLength and index >= 0:
            ltodoList.pop(index - 1)
        else:
            print("Invalid Input Type!")
    return ltodoList


def decisioner(todoList):
    actSwitch = input("\nWhat would you like to do next? (a): Add, (d): Delete, (e): End \n")
    if actSwitch == "a":
        updList = addElement(todoList)
        formUpdList = "\n".join(updList)
        print("Your list is as follows:\n\n" + formUpdList)
        updatedList = decisioner(formUpdList)
    elif actSwitch == "d":
        if not todoList:
            print("Your list is empty, you can not delete anything!")
            updatedList = decisioner(todoList)
        else:
            updList = delElement(todoList)
            formUpdList = "\n".join(updList)
            print("Your list is as follows:\n\n" + formUpdList)
            updatedList = decisioner(formUpdList)
    elif actSwitch == 'e':
        updatedList = todoList
    else:
        print('Incorrect Input!')
        updatedList = decisioner(todoList)
    return updatedList


def checkIfExist(usrName, usrList):
    if usrName in usrList:
        print("Welcome, " + usrName + "!")
        newSwitch = 0
    else:
        closItem = difflib.get_close_matches(usrName, usrList)
        if not closItem:
            print("You are not registered! \n")
            newSwitch = 1
        else:
            newSwitch = 0
            closSwitch = input("Did you mean " + "".join(closItem) + "? (y/n)\n")
            if closSwitch == "y":
                usrName = "".join(closItem)
                print("Welcome, " + usrName + "!")
            elif closSwitch == "n":
                usrName = input("Please enter your username:\n")
                usrName = checkIfExist(usrName, usrList)
            else:
                print("Incorrect Input Type!")
                usrName = checkIfExist(usrName, usrList)
    return usrName, newSwitch


def main():
    usrFileName = "userData.json"
    with open(usrFileName) as json_file:
        data = json.load(json_file)

    #print(data)    # to control json file
    usrList = []

    for i in data['users']:
        usrList.append(i['username'])
    #print(usrList)  # to control user list

    if not usrList:
        updatedData = initialStart(usrList, data)
    else:
        print("Welcome, this is a 'To do List Application'!, to Abort the Program Press Ctrl + c")
        exSwitch = input("Are you an existing user? (y/n)\n")
        if exSwitch == "y":
            updatedData = existingUser(usrList, data)
        elif exSwitch == "n":
            updatedData = newUser(usrList, data)
        else:
            print("Incorrect Input Type!")
            updatedData = data

    with open(usrFileName, 'w') as outfile:
        json.dump(updatedData, outfile, indent=4)


if __name__ == '__main__':
    infLoop = 1
    while infLoop == 1:
        main()


import tkinter as tk
import turtle as tu

TRUE_WINDOW = tk.Tk()
container = tk.Frame(master = TRUE_WINDOW)
canvas = tk.Canvas(master = container, width=750)
scrollbar = tk.Scrollbar(master = TRUE_WINDOW, orient = "vertical", command = canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill="y")
window = tk.Frame(master = canvas)
container.pack()
canvas.pack()
window.pack()

window.bind("<Configure>", lambda e : canvas.configure(scrollregion = canvas.bbox("all")))
canvas.create_window((0,0), window=window, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)


class IOHandler:

    allDict = {}
    
    @staticmethod
    def getDictionaries():
        read = open("Inventory.txt")
        c = read.readline()
        cName = ""
        while (c != ""):
            # print("Current: '" + c + "'\nCurrent.lstrip(): '" + c.lstrip() + "'")
            if (len(c) > len(c.lstrip())):
                data = c.strip().split(":")
                if (len(data) <= 2):
                    IOHandler.allDict[cName][data[0].strip()] = int(data[1].strip())
                elif (len(data) == 3):
                    IOHandler.allDict[cName][data[0].strip()] = int(data[1].strip())
                    if ("BINS" in IOHandler.allDict[cName].keys()):
                        if (data[2].strip() in IOHandler.allDict[cName]["BINS"].keys()):
                            IOHandler.allDict[cName]["BINS"][data[2].strip()].append(data[0].strip())
                        else:
                            IOHandler.allDict[cName]["BINS"][data[2].strip()] = [data[0].strip()]
                    else:
                        # print("Dict made!")
                        IOHandler.allDict[cName]["BINS"] = {data[2].strip():[data[0].strip()]}
            else:
                cName = c.strip()
                IOHandler.allDict[cName] = {}

            c = read.readline()
        read.close()

        # for cName in IOHandler.allDict:
        #     print("'" + cName + "'")

        return IOHandler.allDict
    
    @staticmethod
    def writeDictionary():
        output = ""
        for cName in IOHandler.allDict:
            output += cName + "\n"
            for item in IOHandler.allDict[cName]:
                if (item != "BINS"):
                    output += "\t" + item + ":" + str(IOHandler.allDict[cName][item]) + ":"
                    for loc in IOHandler.allDict[cName]["BINS"]:
                        if item in IOHandler.allDict[cName]["BINS"][loc]:
                            output += str(loc)
                            # print(str(loc))
                            break
                    output += "\n"
        write = open("Inventory.txt", "w")
        write.write(output.rstrip())
        write.close()

    # overwrites the Inventory.txt file with saved change data regarding a single camp
    @staticmethod
    def overwrite(campName:str, campDict:dict):
        try:
            IOHandler.allDict[campName] = campDict
            IOHandler.writeDictionary()
        except:
            print("No such camp name '" + campName + "' in static dictionary IOHandler.allDict")

    # @staticmethod
    # def overwrite(locChanged:str, )
        

class AddCampDisplay:
    def __init__(self, mainContext):
        self.mainContext = mainContext
        self.frame = tk.Frame(master= window)
        self.label = tk.Label(master = self.frame, text="Enter the camp name in the box bellow:")
        self.entry = tk.Entry(master = self.frame)
        self.button = tk.Button(master = self.frame, text = "Add Camp", command = lambda : self.checkData())
        self.label.pack(side = tk.TOP)
        self.entry.pack(side = tk.TOP)
        self.button.pack(side = tk.TOP)
        self.frame.pack()
        self.firstUse = True

    def checkData(self):
        if (self.entry.get() != ""):
            self.openCamp()
        elif (self.firstUse):
            self.errorFrame = tk.Label(master = self.frame, text = "Camp name cannot be empty!")
            self.errorFrame.pack(side=tk.TOP)
            self.frame.pack()
            self.firstUse = False

    def openCamp(self):
        self.frame.pack_forget()
        MainDisplay.openCamp(self.mainContext, self.entry.get().strip())

class MainDisplay:
    def __init__(self):
        self.buildWindow()

    def buildWindow(self):
        self.mainFrame = tk.Frame(master = window)
        # Create a list of buttons that lead to camp specific inventories
        self.allCamps = IOHandler.getDictionaries()
        index = 0
        for i in self.allCamps:
            if i != "GENERAL":
                temp = tk.Button(master = self.mainFrame, text = i, width = 50, command=lambda name = str(i): self.openCamp(name))
                temp.grid(row = index, column = 1)
                index += 1

        newCampButton = tk.Button(master = self.mainFrame, text="Add New Camp", bg="peach puff", fg="saddle brown", width = 50, command = lambda:self.addNewCamp())
        newCampButton.grid(row = index, column = 1)

        # Create a list of unique bin buttons
        self.bins = []
        for i in self.allCamps:
            for j in self.allCamps[i]["BINS"]:
                if j not in self.bins:
                    self.bins.append(j)

        index = 0
        for i in self.bins:
            temp = tk.Button(master = self.mainFrame, text = i, width = 20, command = lambda name=str(i): self.openLoc(name))
            temp.grid(row = index, column = 0)
            index += 1

        newLocButton = tk.Button(master = self.mainFrame, text="Add New Location", bg="peach puff", fg="saddle brown", width = 20, command = lambda:print("Add new location!!!"))
        newLocButton.grid(row = index, column = 0)

        self.mainFrame.pack(side=tk.RIGHT) 
        
    def addNewCamp(self):
        self.closeContext()
        nextContext = AddCampDisplay(self)

    def openLoc(self, _locID):
        self.closeContext()
        nextContext = LocDisplay(_locID,self.allCamps,self)

    def openCamp(self, _campName):
        self.closeContext()
        try:
            # for when existing camps need opening
            newView = CampDisplay(_campName, self.allCamps[_campName], self)
        except:
            # Occurs when adding a new camp
            IOHandler.allDict[_campName] = {"BINS":{}}
            self.allCamps = IOHandler.allDict
            CampDisplay(_campName, self.allCamps[_campName], self)

    def closeContext(self):
        self.mainFrame.pack_forget()

    def getFileData(self):
        allCamps = {}
        read = open("./Inventory.txt", "r")
        campName = ""
        current = read.readline()
        while (current != ""):
            # print("current: " + current)

            if (len(current) == len(current.lstrip())):
                campName = current.rstrip("\n")
                # print(str([campName]))
                allCamps[campName] = {}
            else:
                data = current.lstrip().split(":")
                data[1] = data[1].strip()
                # print("\tdata: " + str(data))
                allCamps[campName][data[0]] = int(data[1].strip())

            current = read.readline()
        read.close()

        return allCamps
    
    def closeApplication(self):
        IOHandler.writeDictionary()
        TRUE_WINDOW.destroy()
        
        # output = ""
        # for i in self.allCamps:
        #     output += i + "\n"
        #     for j in self.allCamps[i]:
        #         output += "\t" + j + ":" + str(self.allCamps[i][j]) + "\n"
        # write = open("Inventory.txt", "w")
        # write.write(output.rstrip())
        # write.close()
        # window.destroy()
        
class LocDisplay:
    def __init__(self, _locID:str, _allDict:dict, _returnContext:MainDisplay):
        self.locID = _locID
        self.allDict = _allDict
        self.returnContext = _returnContext
        self.entries = []
        self.counts = []
        self.cNames = {}
        self.buildWindow()

    def buildWindow(self):
        self.topFrame = tk.Frame(master = window, bg = "black")
        
        self.locIDLabel = tk.Label(master = self.topFrame, text = self.locID, bg = "gray15", fg = "gray80", width = 25)
        self.returnButton = tk.Button(master = self.topFrame, text = "<", command = lambda : self.exitDisplay())

        self.returnButton.pack(side=tk.LEFT)
        self.locIDLabel.pack(side=tk.LEFT)

        # Show each item for the class, and its location
        self.mainFrame = tk.Frame(master = window)
            # Info labels
        tk.Label(master = self.mainFrame, text = "ITEM", bg = "gray30", fg = "white", width = 25).grid(row = 0, column = 0)
        tk.Label(master = self.mainFrame, text = "COUNT", bg = "gray20", fg = "white", width = 25).grid(row = 0, column = 1)
        tk.Label(master = self.mainFrame, text = "CAMP", bg = "gray30", fg = "white", width = 25).grid(row = 0, column = 2)

        index = 1
        for cName in self.allDict:
            for _locID in self.allDict[cName]["BINS"]:
                if _locID == self.locID:
                    for item in self.allDict[cName]["BINS"][self.locID]:
                        _bg = "gray90" if index%2==0 else "gray75"
                        _fg = "gray15"
                        label = tk.Label(master = self.mainFrame, text = item, fg = _fg, bg = _bg, width = 25, pady = 5)
                        entry = tk.Entry(master = self.mainFrame, width = 25)
                        locLabel = tk.Label(master = self.mainFrame, text = cName, fg = _fg, bg = _bg, width = 25, pady = 5)
                        # Delete entry button
                        delButton = tk.Button(master = self.mainFrame, text = "X", bg = "salmon", fg="firebrick4", command = lambda _i = str(item), _cName = str(cName) : self.removeItem(_i, _cName), pady = 2)
                        delButton.grid(row = index, column = 3)
                        entry.insert(0, str(self.allDict[cName][item]))
                        self.counts.append(int(self.allDict[cName][item]))
                        
                        try:
                            self.cNames[cName].append((item,index-1))
                        except:
                            self.cNames[cName] = [(item,index-1)]

                        label.grid(row = index, column = 0)
                        entry.bind("<FocusOut>", lambda event, _ind = index-2 : self.assessAndRecolor(_ind))
                        entry.grid(row = index, column = 1)
                        self.entries.append(entry)
                        locLabel.grid(row = index, column = 2)
                        index += 1

        # new Item region
        self.newItem_ITEM = tk.Entry(master = self.mainFrame)
        self.newItem_COUNT = tk.Entry(master = self.mainFrame)
        self.newItem_CAMP = tk.Entry(master = self.mainFrame)
        self.newItem_CONFIRM = tk.Button(master = self.mainFrame, text = "Add", command = lambda : self.addItem()) # Add new thing here

        self.newItem_ITEM.grid(row = index, column = 0)
        self.newItem_COUNT.grid(row = index, column = 1)
        self.newItem_CAMP.grid(row = index, column = 2)
        self.newItem_CONFIRM.grid(row = index, column = 3)

        window.bind("<Control-s>", lambda event : self.saveChanges())

        # location operations
        

        # all UI built, pack it
        self.topFrame.pack(side = tk.TOP)
        self.mainFrame.pack(side = tk.TOP)

    def addItem(self):
        if self.newItem_ITEM.get() != "" and self.newItem_COUNT.get() != "" and self.newItem_CAMP != "":
            try:
                item = self.newItem_ITEM.get()
                count = int(self.newItem_COUNT.get())
                cName = self.newItem_CAMP = self.newItem_CAMP.get()
                IOHandler.allDict[cName][item] = count
                try:
                    IOHandler.allDict[cName]["BINS"][self.locID].append(item)
                except:
                    # camp has first item from current location
                    IOHandler.allDict[cName]["BINS"][self.locID] = [item]

                IOHandler.writeDictionary()

                self.forgetPacks()
                self.buildWindow()

            except:
                # Error in parsing
                pass

    def removeItem(self, item, cName):
        # print(cName + " " + item)
        # remove item from camp
        IOHandler.allDict[cName].pop(item)
        # remove item from bins of camp
        if (self.locID in IOHandler.allDict[cName]["BINS"]):
            for _itemCheck in IOHandler.allDict[cName]["BINS"][self.locID]:
                if _itemCheck == item:
                    IOHandler.allDict[cName]["BINS"][self.locID].remove(item)
                    if len(list(IOHandler.allDict[cName]["BINS"][self.locID])) == 0:
                        IOHandler.allDict[cName]["BINS"].pop(self.locID)
        # save changes
        IOHandler.writeDictionary()
        # rebuild window to account for now removed item        
        self.forgetPacks()
        self.buildWindow()

    def assessAndRecolor(self, index):
        if self.counts[index-1] != int(self.entries[index-1].get()):
            self.entries[index-1].config(bg = "peach puff")
        
    def saveChanges(self):
        for i in range(len(self.counts)):
            if self.counts[i] != int(self.entries[i].get()):
                self.counts[i] = int(self.entries[i].get())
                self.entries[i].config(bg = "DarkOliveGreen1")
        
        # Dirrectly change every camp associated with the altered location
        for cName in self.cNames:
            for pair in self.cNames[cName]:
                print(str(pair))
                IOHandler.allDict[cName][pair[0]] = int(self.entries[pair[1]].get())
            IOHandler.overwrite(cName, IOHandler.allDict[cName])
    
    def forgetPacks(self):
        self.topFrame.pack_forget()
        self.mainFrame.pack_forget()

    def exitDisplay(self):
        # Back end checks
        # Remove location from existence if it's empty
        empty = True
        for cName in IOHandler.allDict:
            if self.locID in IOHandler.allDict[cName]["BINS"]:
                empty = False
                break
        if empty:
            for cName in IOHandler.allDict:
                if self.locID in IOHandler.allDict[cName]["BINS"]:
                    IOHandler.allDict[cName]["BINS"].pop(self.locID)
        # Front end
        self.topFrame.pack_forget()
        self.mainFrame.pack_forget()
        window.unbind_all("<Control-s>")
        self.returnContext.buildWindow()

class CampDisplay:
    def __init__(self, _campName:str, _campDict:dict, _returnContext:MainDisplay):
        self.campName = _campName
        self.campDict = _campDict
        self.returnContext = _returnContext
        self.counts = []
        self.entries = []
        self.countChanges = {}
        self.buildWindow()
        
    def buildWindow(self):
        # top section
        self.topFrame = tk.Frame(master = window, bg="gray20", width = window.winfo_width())

        self.returnButton = tk.Button(master = self.topFrame, text = "<", command=lambda : self.exitDisplay())
        self.campNameLabel = tk.Label(master = self.topFrame, text = self.campName, fg = "gray80", bg="gray20", width = 50)
        
        self.returnButton.pack(side = tk.LEFT)
        self.campNameLabel.pack(side = tk.LEFT)

        self.topFrame.pack(side = tk.TOP)

        # display camp specific items
        self.mainFrame = tk.Frame(master = window)

        tk.Label(master = self.mainFrame, text = "ITEM", bg = "gray30", fg = "white", width = 25).grid(row = 0, column = 0)
        tk.Label(master = self.mainFrame, text = "COUNT", bg = "gray20", fg = "white", width = 25).grid(row = 0, column = 1)
        tk.Label(master = self.mainFrame, text = "LOCATION", bg = "gray30", fg = "white", width = 25).grid(row = 0, column = 2)

        index = 1
        # print(str(self.campDict))
        for item in IOHandler.allDict[self.campName]:
            # print(item)
            if (item != "BINS"):
                _bg = "gray90" if index%2==0 else "gray75"
                _fg = "gray15"
                label = tk.Label(master = self.mainFrame, fg = _fg, bg = _bg, text = item, width = 25, pady = 5)
                entry = tk.Entry(master = self.mainFrame, width = 25)
                loc = ""
                for i in IOHandler.allDict[self.campName]["BINS"]:
                    if item in IOHandler.allDict[self.campName]["BINS"][i]:
                        loc = i
                        break
                locLabel = tk.Label(master = self.mainFrame, width = 25, fg = _fg, bg = _bg, text = loc, pady = 5)
                entry.insert(0, str(IOHandler.allDict[self.campName][item]))
                # print("index: " + str(index))
                tempIndex = index
                entry.bind("<FocusOut>", lambda event, _index = int(tempIndex), _color = "peach puff" : self.changeEditedEntryColor(_index, _color))
                self.entries.append(entry)
                self.counts.append(int(IOHandler.allDict[self.campName][item]))

                #remove button
                tk.Button(master = self.mainFrame, text = "X", bg = "salmon", fg="firebrick4", command = lambda _item = str(item), _locID = str(loc) : self.removeItem(_item, _locID)).grid(row = index, column = 3)

                label.grid(row = index, column = 0)
                entry.grid(row = index, column = 1)
                locLabel.grid(row = index, column = 2)
                index += 1

        self.newItem_ITEM = tk.Entry(master = self.mainFrame)
        self.newItem_COUNT = tk.Entry(master = self.mainFrame)
        self.newItem_LOC = tk.Entry(master = self.mainFrame)
        self.newItem_CONFIRM = tk.Button(master = self.mainFrame, text = "Add", command = lambda : self.addItem())

        self.newItem_ITEM.grid(row = index, column = 0)
        self.newItem_COUNT.grid(row = index, column = 1)
        self.newItem_LOC.grid(row = index, column = 2)
        self.newItem_CONFIRM.grid(row = index, column = 3)

        self.mainFrame.pack(side = tk.TOP)
        window.bind("<Control-s>", lambda event : self.saveChanges())

    def removeItem(self, item, locID):
        IOHandler.allDict[self.campName].pop(item)
        IOHandler.allDict[self.campName]["BINS"][locID].remove(item)
        if len(IOHandler.allDict[self.campName]["BINS"][locID]) == 0:
            IOHandler.allDict[self.campName]["BINS"].pop(locID)
        IOHandler.writeDictionary()
        self.packForget()
        self.buildWindow()

    def addItem(self):
        if self.newItem_ITEM.get() != "" and self.newItem_COUNT != "" and self.newItem_LOC.get() != "":
            try:
                item = self.newItem_ITEM.get()
                count = int(self.newItem_COUNT.get())
                locID = self.newItem_LOC.get()
                IOHandler.allDict[self.campName][item] = count
                try:
                    IOHandler.allDict[self.campName]["BINS"][locID].append(item)
                except:
                    # No such list to append, create it
                    IOHandler.allDict[self.campName]["BINS"][locID] = [item]

                IOHandler.writeDictionary()
                self.packForget()
                self.buildWindow()
            except:
                # parsing error
                pass

    # To make update the frame; they have to be unpacked
    def packForget(self):
        self.topFrame.pack_forget()
        self.mainFrame.pack_forget()

    def checkEntryForChange(self, index):
        if (self.entries[index].get() != str(self.counts[index]) and index not in self.countChanges):
            return True
        elif (index in self.countChanges):
            return True if int(self.countChanges[index]) != int(self.entries[index].get()) else False
        return False
            
    def changeEditedEntryColor(self, index:int, color):
        # print(index, color)
        if (self.checkEntryForChange(index - 1)):
            self.entries[index - 1].config(bg = color)
        elif (index-1 in self.countChanges):
            self.entries[index - 1].config(bg = "DarkOliveGreen1")
        else:
            self.entries[index - 1].config(bg = "white")

    def saveChanges(self):
        index = 0
        for entry in self.entries:
            # print(entry.get(), str(self.counts[index]))
            if (str(entry.get()) != str(self.counts[index])):
                entry.config(bg="DarkOliveGreen1")
                self.countChanges[index] = int(entry.get())
                self.counts[index] = int(entry.get())

                IOHandler.allDict[self.campName][list(IOHandler.allDict[self.campName].keys())[index]] = entry.get()

            index += 1
        IOHandler.overwrite(self.campName, IOHandler.allDict[self.campName])

    def exitDisplay(self):
        # Back end checks
        if len(list(IOHandler.allDict[self.campName].keys())) == 0:
            IOHandler.allDict.pop(self.campName)
        # Front end
        self.topFrame.pack_forget()
        self.mainFrame.pack_forget()
        window.unbind_all("<Control-s>")
        self.returnContext.buildWindow()


# test = tk.Label(text="test", bg="chartreuse2")
# test.pack()

start = MainDisplay()
TRUE_WINDOW.protocol("WM_DELETE_WINDOW", lambda : start.closeApplication())
TRUE_WINDOW.title("Lavner Site Inventory v0.0.1")

window.mainloop()
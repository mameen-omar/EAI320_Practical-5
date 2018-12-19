#Mohamed Ameen Omar
#u16055323
#EAI PRACTICAL ASSIGNMENT 5
#2018
import csv
import math
import copy

class Stack:
     def __init__(self):
         self.list = []
     def isEmpty(self):
         if(self.list == []):
             return True
         return False
     def push(self, item):
         self.list.append(item)
     def pop(self):
         return self.list.pop()
     def peek(self):
         return self.list[len(self.items)-1]
     def size(self):
         return len(self.list)

class Node:
    def __init__(self, category = None, parent = None, child = []):
        self.category = category #category
        self.value = None #only assigned if it is a split node
        self.parent = parent #parent of the node
        self.children = child
        self.subset = None # for the subset for which this node represnts   
        self.isCategoryNode = False #if it is a category or a option
        self.isDecisionNode = False #if it is a decision
    def isLeaf(self):
        if(self.child is None):
            return True
        return False
    
class ID3:
    def __init__(self):
        self.root = None
        self.fileName = ""
        self.mainData = None #each index is a dictonary for the data given
        self.numAttributes = 0
        self.categories = ""
        self.default = None #boolean for the default files
        self.defaultFilename = "restaurant(1).csv"
        self.defaultCategories = ["Alt", "Bar", "Fri", "Hun", "Pat", "Price", "Rain", "Res", "Type", "Est", "WillWait"]
        self.testedDecisions = []
        self.numNodes = 0
        self.numAttNodes = 0
        self.numDecNodes = 0
        self.numCatNodes = 0
        self.runID3()
        
    #dummy fucntion to do admin work for the program and make it run
    def runID3(self):
        anotherFile = input("Would you like to build a decision tree for the data in restaurant(1).csv? (Please input Y or N)\n")        
        while(anotherFile.upper() != "Y" and anotherFile.upper() != "N"):
            string = "You entered"
            string = string + " "
            string= string + anotherFile
            string = string + (" which is invalid, please input \"Y\" or \"N\"\n")            
            anotherFile = input(string)
        print("Building Tree...")
        if(anotherFile.upper() == "Y"):
            self.default = True
            self.buildDefaultTree()
        else:
            self.default = False
            self.buildOtherTree()
        self.countNodes()
        print("Tree has been built")
        print()
        print("The Tree has:")
        print(self.numNodes, end = " ")
        print("Nodes.")
        print(self.numCatNodes, end = " ")
        print("Category Nodes.")
        print(self.numAttNodes, end = " ")
        print("Attribute Value Nodes.")
        print(self.numDecNodes, end = " ")
        print("Decision Nodes.")
        test = (input("Would you like to input a test case?\n")).upper()
        while(test.upper() != "Y" and test.upper() != "N"):
            string = "You entered"
            string = string + " "
            string= string + test
            string = string + (" which is invalid, please input \"Y\" or \"N\"\n")            
            test = input(string)
        if(test.upper() == "N"):
            print("The program has ended.")
            return
        print("Please enter the name of the file for which you would like to know the outcome.")
        print("Please include the file extension (.csv) as well")
        testFile = input("Test file Name: ")
        testList = self.readTestFile(testFile)
        print("Testing attributes in file: ", testFile, end = "")
        print(" with the sample data")        
        print("Retrieving Decision....")
        self.testFunc(testList)
        again = input("Would you like to test another file?\n")        
        while(again.upper() != "Y" and again.upper() != "N"):
            string = "You entered"
            string = string + " "
            string= string + again
            string = string + (" which is invalid, please input \"Y\" or \"N\"\n")            
            again = input(string)
        while(again.upper() == "Y"):
            print("Please enter the name of the file for which you would like to know the outcome.")
            print("Please include the file extension (.csv) as well")
            testFile = input("Test file Name: ")
            testList = self.readTestFile(testFile)
            print("Testing attributes in file: ", testFile, end = "")
            print(" with the sample data")        
            print("Retrieving Decision....")
            self.testFunc(testList)
            again = input("Would you like to test another file?\n")            
            while(again.upper() != "Y" and again.upper() != "N"):
                string = "You entered"
                string = string + " "
                string= string + again
                string = string + (" which is invalid, please input \"Y\" or \"N\"\n")            
                again = input(string)            
        if(again.upper() == "N"):
            print("A reminder, the decisions for the input test cases were: ")
            count = 1
            for x in self.testedDecisions:
                print("Decision ", count, end = " ")
                print("was:", x)
                count = count + 1
            print("The program has ended")
            return
    
    #takes in a list of dicnonaries and returns the dicisions
    def testFunc(self,testList):
        tempDict = testList[0]
        myNode = self.root
        decision = False
        while(decision == False):
            if(myNode.isDecisionNode == True):
                decision = True
                print()
                print("At a decision Node")
                print("Congratulations we have found a decision")
                print("Based off of the sample data, the final decision for this test case is predicted to be: ", myNode.value)
                self.testedDecisions.append(myNode.value)
            elif(myNode.isCategoryNode == True):
                print()
                print("At a Category Node.")
                print("The category being compared is: ", myNode.category)
                for child in myNode.children:
                    if(tempDict[myNode.category] == child.value):
                        myNode = child
            else:
                print()
                print("At an attribute value Node.")
                print("Attribute is :", myNode.value)
                myNode = myNode.children[0]
    #builds the tree for the defualt given csv in the prac spec     
    def buildDefaultTree(self):
        self.fileName = self.defaultFilename
        self.categories = self.defaultCategories
        self.numAttributes = len(self.categories)
        self.readFile(self.fileName, self.categories)
        self.build()
   
    #builds a tree that isnt for the default csv
    def buildOtherTree(self):
        self.categories = []
        print("Please note, the data needs to be in a csv file with the target value or final decision being the last value in every row.")
        name = input("Please input the name of the file name to be used to build the tree.\n")
        self.fileName = name
        numAttributes = input("How many attributes does the data consist of?\n")
        y = 1
        while(y <= int(numAttributes)):
            string = "Please enter attribute number " + str(y) + "\n"
            att = input(string)
            y = y+1
            self.categories.append(att)
        for x in self.categories:
            print(x)
        self.readFile(self.fileName, self.categories)
        self.build()
    
    #reads a test file
    def readTestFile(self,fileName):
        temp = []
        csvfile = open(fileName)
        cat = copy.deepcopy(self.categories)
        del cat[-1]
        temp = list(csv.DictReader(csvfile, cat)) #make the DictReader iterator a list        
        for decision in temp:
            for k,v in decision.items():
                decision[k] = v.replace(" ", "")   
        return temp
        
    #helper to read the file and sort out main data
    def readFile(self, fileName, categories):
        csvfile = open(fileName)
        self.mainData = list(csv.DictReader(csvfile, categories)) #make the DictReader iterator a list        
        for decision in self.mainData:
            for k,v in decision.items():
                decision[k] = v.replace(" ", "")                
     
    # returns the entropy value for a category within a given data subset
    #name is the name of the catgory who's entropy we are getting
    #"data" is the dicntonary list which we are using to get the entropy
    def getEntropy(self,name,data):
        if(data is None):
            return 1
        variableNames = self.getVariableValues(data,name)#for the category we are testing        
        decisions = [] #different decisions that can result    
        for x in data:
            new = True
            if(decisions == []):
                decisions.append(x[self.categories[self.numAttributes-1]])
            else:
                for y in decisions:
                    if(y == x[self.categories[self.numAttributes-1]]):
                        new = False
                if(new == True):
                    decisions.append(x[self.categories[self.numAttributes-1]])
        # now we have the decision names and the different variable names
        totalOcc = len(data)        
        entropy = 0.0
        tempEnt = 0.0
        for attribute in variableNames:
            tempEnt = 0.0
            attOcc = self.getAttributeOccurrences(attribute,name,data)
            for decision in decisions:
                temp = 0.0
                tempDecOcc = self.getAttDecOccurrences(attribute,name,decision,data)
                if(tempDecOcc == 0):
                    temp = 0
                else:
                    temp = (tempDecOcc/attOcc) * math.log2(tempDecOcc/attOcc)
                tempEnt = tempEnt + temp   
           # print((attOcc)/totalOcc)
            tempEnt = ((-1 * attOcc)/totalOcc)*tempEnt
            entropy = entropy + tempEnt
        return entropy
    #returns the amount of times a attribute value= attribute, is found within a category = category  
    #within the data dictionary list
    def getAttributeOccurrences(self, attribute,category,data):
        occ = 0
        for x in data:
            if(x[category] == attribute):
                occ = occ +1
        return occ
    #returns number of occurences of an attribute in a catrgory for a specific decision
    #within the "data" dictonary list
    def getAttDecOccurrences(self,attribute,category,decision,data):
        occ = 0.0        
        for x in self.mainData:
            if(x[category] == attribute):
                if(x[self.categories[self.numAttributes -1]] == decision):
                    occ = occ+1
        return occ
    #takes in a data subset, which is a list of dictonaries, sees if it is pure
    #by checking that the decision for all is the same
    def isPure(self,data):
        if(len(data) == 1):
            return True
        decisionIndex = self.categories[self.numAttributes-1]
        decisionKey = data[0][decisionIndex]   
        for decision in data:
            if(decision[decisionIndex] != decisionKey):
                return False        
        return True
    #returns the name of the category which has the lowest entropy
    #data is a list of dictionaries for which each dictionary attributes(keys) still need to be split
    def getLowestEntropy(self,data):
        temp = data[0]
        returnKey = ""
        entropy = -1.0
        keys = []
        for k in temp:
            if(k != self.categories[self.numAttributes-1]):
                keys.append(k)
        for key in keys:
            temp = self.getEntropy(key,data)
            if(entropy == -1.0):
                entropy = temp
                returnKey = key
            elif(entropy > temp):
                entropy = temp
                returnKey = key
        return returnKey
    #builds the tree recursively
    def build(self, node = None):
        if(self.root is None):
            temp = Node()
            temp.isDecisionNode = False
            temp.isCategoryNode = True
            temp.parent = None
            temp.subset = copy.deepcopy(self.mainData)
            splitCat = self.getLowestEntropy(temp.subset)
            temp.category = splitCat
            childVals = self.getVariableValues(temp.subset,splitCat)
            self.root = temp
            for child in childVals:
                tempChild = None
                tempChild = Node()
                tempChild.category = self.root.category
                tempChild.isCategoryNode = False
                tempChild.isDecisionNode = False
                tempChild.value = child
                tempChild.children = []
                tempChild.parent = self.root
                tempSub = copy.deepcopy(self.root.subset)
                tempSub = self.removeRowFromList(tempSub,temp.category,tempChild.value)
                tempSub = self.removeKeyFromDicList(tempSub,tempChild.category)                
                tempChild.subset = tempSub
                self.root.children.append(tempChild)  
            for child in self.root.children:
                if(child.isDecisionNode != True):
                    self.build(child)  
        else:
            if(self.isPure(node.subset) == True):
                temp = Node()
                temp.parent = node
                temp.category = node.category
                temp.isDecisionNode = True
                temp.isCategoryNode = False
                temp.subset = copy.deepcopy(node.subset)
                temp.value = self.getDecision(temp.subset)
                node.children.append(temp)
                temp.children = []
                return
            else:               
                #node is our parent
                #temp is our new category node
                temp = Node()
                temp.isCategoryNode = True
                temp.isDecisionNode = False
                temp.subset = copy.deepcopy(node.subset)
                temp.children = []
                temp.parent = node        
                node.children.append(temp)
                temp.category = self.getLowestEntropy(temp.subset)            
                catValues = self.getVariableValues(temp.subset,temp.category)
                #temp is sorted now get children for temp
                for val in catValues:
                    child = Node()
                    child.value = val
                    child.category = temp.category
                    child.isCategoryNode = False
                    child.isDecisionNode = False
                    child.children = []
                    child.parent = temp
                    child.subset = self.removeRowFromList(copy.deepcopy(temp.subset), child.category,val)
                    child.subset = self.removeKeyFromDicList(copy.deepcopy(child.subset), child.category)
                    temp.children.append(child)
                for child in temp.children:
                    self.build(child)
    #returns a list of all variable names or different attrbiute names
    #within a given data set = data and a catergory = category
    def getVariableValues(self,data,category):
        vals = []
        for row in data:
            if(vals == []):
                vals.append(row[category])
            else:
                new = True
                for x in vals:
                    if(x == row[category]):
                        new = False                    
                if(new == True):
                    vals.append(row[category])
        return vals
    #returns the decision
    def getDecision(self,data):
        if(self.isPure(data) == False):
            return None        
        return data[0][self.categories[self.numAttributes -1]]
    #removes a key from a dictionary list
    def removeKeyFromDicList(self,data,key):
        for row in data:
            del row[key]            
        return data
    #removes all rows from a data subset that is not for this category value
    #data = list of dictonaries, splitCategory = the category for which we are checking a value
    #val = the value within the category for which we only want the rows
    def removeRowFromList(self,data,splitCategory,val):
        remove = True
        while(remove == True):
            remove = False
            for row in data:
                if(row[splitCategory] != val):
                    data.remove(row)
                    remove = True
        return data
    #counts nodes and types of nodes
    def countNodes(self):
        if(self.root == None):
            return 0
        count = 0
        temp = Stack()
        temp.push(self.root)
        while(temp.isEmpty() == False):
            node = temp.pop()
            count = count +1 
            if(node.isCategoryNode == True):
                self.numCatNodes += 1
            elif(node.isDecisionNode == True):
                self.numDecNodes += 1
            else:
                self.numAttNodes +=1
            for child in node.children:
                temp.push(child)
        self.numNodes = count
        return count  
test = ID3()
print()
print("The initial entropy values for the given data set:")

for cat in range (0,len(test.categories)-1):
    print("The Entropy for ", end = "")
    print(test.categories[cat], end = " ")
    print("is ", end = "")
    print(test.getEntropy(test.categories[cat],test.mainData))
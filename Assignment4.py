import matplotlib.pyplot as plt
import numpy as np
import itertools
import math
from prettytable import PrettyTable
import csv



# Implement Ito, Saito Nishizekis Share Assignment
# 	Given an r participants and m + 1 threshold
# 	Compute who gets what shares
def Ito_Share_Assignment(r, m, printBool):
    #Creating Array of participants
    #Pariticpants are labeled by index 0 -> r-1
    #Since arange is [)
    participants = np.arange(0, r, 1)
    numShares = nCr(r, m)
    shareAssignment = dict()
    for participant in participants:
        assignedShares = []
        B = itertools.combinations(participants, m)
        for index, combination in enumerate(B):
            if participant not in combination:
                assignedShares.append(index)
        shareAssignment[participant] = assignedShares

    if printBool:
        table = PrettyTable()
        table.field_names = ["Participant", "Shares"]
        keys = shareAssignment.keys()
        for key in keys:
            table.add_row([key, shareAssignment[key]])
        print table
    return shareAssignment

    expNumSharesParticipant = nCr(r-1, m)
    expNumParticipantsShare = r - m

    return shareAssignment


def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)

# Implement Gridsharing
# 	Given a l,b,c
# 	    Choose an appropriate r
# 		Compute min number of servers
# 		Compute number of shares
# 		Compute who gets which shares
# 		Display on grid
def Gridsharing(l, b, c):
    r = Choose_Num_Rows(l, b, c)
    numServers = Compute_Min_N(l, b, c, r)
    shareAssignment = Compute_Sharers(l, b, r)
    Display_Stats(l, b, c, r)
    Display_Gridshare(shareAssignment, numServers/r)

def GridsharingSave(l, b, c, filename):
    r = Choose_Num_Rows(l, b, c)
    numServers = Compute_Min_N(l, b, c, r)
    shareAssignment = Compute_Sharers(l, b, r)
    Display_Stats(l, b, c, r)
    Export_CSV(shareAssignment,numServers/r, filename)

# Utilizing r for smallest number of servers required
# r = 4b + l + c + 1
# Lower bound = l + b + 1
# Upper bound = 4b + l + c + 1
def Choose_Num_Rows(l, b, c):
    upperBound = 4*b + l + c + 1
    lowerBound = l + b + 1
    print "Rows for GridSharing"
    print "Lower Bound: " + str(lowerBound)
    print "Upper Bound: " + str(upperBound)
    rows = input("Choose a number of rows between the bounds (inclusive): ")
    if (int(rows) <= upperBound) and (int(rows) >= lowerBound):
        return int(rows)
    else:
        print "Error in row input"
        exit(1)


# is the minimum number of servers required for a given l, b, c, and r. This is given by the smallest N satisfying Inequality 3, with N being a multiple of r.
def Compute_Min_N(l, b, c, r):
    minN = ((3*b + c + 1) / (1 - ((float(l)+b)/r)))
    remainder = minN % r
    if remainder != 0:
        return int(minN + (r - remainder))
    else:
        return int(minN)

# The total number of shares generated per secret. For the proposed framework, #Shares = r choose (l+b)
def Compute_Num_Shares(l, b, r):
    return nCr(r, l+b)

def Compute_Sharers(l, b, r):
    shareAssignment = Ito_Share_Assignment(r, l + b, 0)
    return shareAssignment

def Display_Gridshare(shareAssignment, numServersPerRow):
    table = PrettyTable()
    field_names = []
    field_names.append("Secret Sharing Row")
    for col in range(numServersPerRow):
        field_names.append("Replication Col" + str(col))
    table.field_names = field_names
    keys = shareAssignment.keys()
    for key in keys:
        row = []
        row.append(key)
        for col in range(numServersPerRow):
            row.append(shareAssignment[key])
        table.add_row(row)
    print table

def Display_Stats(l, b, c, r):
    minN = Compute_Min_N(l, b, c, r)
    numShares = Compute_Num_Shares(l, b, r)
    print "---Stats---\n"
    print "Leaky Servers: " + str(l)
    print "Byzantine Servers: " + str(b)
    print "Crash Servers: " + str(c)
    print "Rows: " + str(r)
    print "MinN: " + str(minN)
    print "Num of Shares per secret: " + str(numShares) + "\n"
    print "-----------\n"

def Export_CSV(shareAssignment,numServersPerRow,filename):
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        string = "Secret Sharing Row"
        for col in range(numServersPerRow):
            string = string + "; Replication Col" + str(col);
        writer.writerow([string]);
        keys = shareAssignment.keys()
        for key in keys:
            row = []
            row.append(key)
            for col in range(numServersPerRow):
                row.append(shareAssignment[key])
            writer.writerow(row)


# Given a specific set of l,b,c, for r [[5, 10]]
# 	Compute the min N for servers
# 	Compute # opf shares
# 	Compute Storage Blowup
# 	Plot all 3 as a function of r

# is defined as the ratio of the
# storage space taken at each server to the size of the data encoded. For the proposed framework, the storage blowup fac-tor is (r-1) choose (l+b). Since we use the XOR secret sharing scheme, the size of a share is the same as the size of the secret.
def Compute_Storage_Blowup(l, b, r):
    return nCr(r-1, l+b)

def Plot_Min_N(l, b, c, rows):
    minNList = []
    for r in rows:
        minN = Compute_Min_N(l, b, c, r)
        minNList.append(minN)
    plt.plot(rows, minNList)
    plt.title('Min. Number of servers satisfying l,b,c,r')
    #min(N): is the minimum number of servers required for a given l, b, c, and r. This is given by the smallest N satisfying Inequality 3, with N being a multiple of r.
    plt.ylabel('Smallest number of servers (Multiple of r)')
    plt.xlabel('Rows')
    plt.grid(True)

def Plot_Num_Shares(l, b, rows):
    numSharesList = []
    for r in rows:
        numShares = Compute_Num_Shares(l, b, r)
        numSharesList.append(numShares)
    plt.plot(rows, numSharesList)
    plt.title('Shares per secret')
    ##Shares: The total number of shares generated per secret. For the proposed framework, #Shares = r choose (l + b)
    plt.ylabel('Shares')
    plt.xlabel('Rows')
    plt.grid(True)

def Plot_Storage_Blowup(l, b, rows):
    storageBlowupList = []
    for r in rows:
        numShares = Compute_Storage_Blowup(l, b, r)
        storageBlowupList.append(numShares)
    plt.plot(rows, storageBlowupList)
    plt.title('Storage Blowup (storage per server:total data)')
    #For the proposed framework, the storage blowup fac-tor is (r-1) choose (l+b). Since we use the XOR secret sharing scheme, size of share is the same as the size of the secret
    plt.ylabel('Storage per server : Encoded data size')
    plt.xlabel('Rows')
    plt.grid(True)

def Plot_All(l, b, c, rows):
    #PLoting is index rows first then columns
    #Index 1, Top Left Graph
    plt.subplot(2,2,1)
    Plot_Min_N(l, b, c, rows)
    #Index 2 Top Right Graph
    plt.subplot(2,2,2)
    Plot_Num_Shares(l, b, rows)
    #Index 3 Bottom Left Graph
    plt.subplot(2,2,3)
    Plot_Storage_Blowup(l, b, rows)

    plt.show()


def driverPart1():
    print "------ Ito Sharing ------"
    print "Enter the following parameters: "
    print "r participants"
    print "m where m + 1 is the threshold"
    r = input("Input r the number of participants: ")
    m = input("Input m where m + 1 is the threshold: ")
    Ito_Share_Assignment(int(r), int(m), 1)
    raw_input("Select enter to return to the main menu.")

def driverPart2():
    print "------ GridSharing ------"
    print "Options:"
    print "\t1. Compute shares"
    print "\t2. Store Shares in File"
    print "\t3. Plot characteristics"
    print "\t4. Exit"
    choice = input("Choice: ")
    if (int(choice) == 1):
        driverPart2Shares()
    elif (int(choice) == 2):
        driverPart2Save()
    elif (int(choice) == 3):
        driverPart2Plot()
    elif (int(choice) == 4):
        exit(0)
    else:
        print "Error in choice input"
        exit(1)

def driverPart2Shares():
    print "------ GridSharing Compute Shares ------"
    print "Give an l, b, c, r to simulate GridSharing"
    l = input("Leaky Servers (l) =  ")
    b = input("Byzantine Servers (b) = ")
    c = input("Crash Servers (c) = ")
    Gridsharing(int(l), int(b), int(c))
    raw_input("Select enter to return to the main menu.")

def driverPart2Save():
    print "------ GridSharing Compute Shares ------"
    print "Give an l, b, c, r to simulate GridSharing"
    l = input("Leaky Servers (l) =  ")
    b = input("Byzantine Servers (b) = ")
    c = input("Crash Servers (c) = ")
    filename = raw_input("Provide a .csv file to store the resulting data: ")
    GridsharingSave(int(l), int(b), int(c), filename)
    raw_input("Select enter to return to the main menu.")

def driverPart2Plot():
    print "------ GridSharing Plot Characteristics ------"
    print "Plots:"
    print "\tMinN: Minimum number of servers required"
    print "\tNumber of shares required"
    print "\tStorage blowup"
    print "Provide a set of l,b,c and a range of rows to plot"
    l = input("Leaky Servers (l) =  ")
    b = input("Byzantine Servers (b) = ")
    c = input("Crash Servers (c) = ")
    print "Enter a range of rows to plot against (e.x. 5,10)"
    print "The range will be limited by the bounds on r for GridSharing"
    start, stop = input("Enter a range: ")
    rows = np.arange(start, stop + 1, 1)
    Plot_All(int(l), int(b), int(c), rows)
    raw_input("Select enter to return to the main menu.")

if __name__ == '__main__':
    while(1):
        print "------ Main Menu ------"
        print "Select functionality by entering the number of the function"
        print "1. Assignment Part 1: Ito Sharing"
        print "2. Assignment Part 2: Grid Sharing"
        print "3. Exit"
        choice = input("Choice: ")
        if (int(choice) == 1):
            driverPart1()
        elif (int(choice) == 2):
            driverPart2()
        elif (int(choice) == 3):
            exit(0)
        else:
            print "Error in choice input"
            exit(1)

from requirements import *

""" *************************************************************
    Class for adding lines of code
************************************************************* """
class fileChange:
    def __init__(self, old="old_code.src", new="new_code.src"):
        self.oldfilename = old
        self.newfilename = new
    
    ''' Code to read in lines of KRL code removing the \n '''
    def oldCodeRead(self):
        output = []
        fp = open(self.oldfilename, "r")
        lines = fp.readlines()
        fp.close()

        for line in lines:
            output.append(line.replace('\n', ""))

        return output
    
    """ Reads in an array of commands to be input """
    def newCode(self, cmd):
        fp = open(self.newfilename, "a")
        for line in cmd:
            fp.write(line + "\n")
        fp.close()
        return

""" ***********************************************
    Function to take line of code and return dict
    with details of the KRL code ************** """
def krl2dict(krl_code):
    output = {}
    
    # Get the first LIN or ARC or PTP command
    krl_code = krl_code.split("{")
    output["cmd"] = krl_code[0]

    # Now remove unnecessary spaces and commas
    krl_code = krl_code[1]
    krl_code = krl_code.replace(", ", ",")
    krl_code = krl_code.replace("}", "")
    krl_code = krl_code.split(",")

    # Assign remaining values to dict
    for pos in krl_code:
        axis, value = pos.split()
        output[axis] = eval(value)

    return output


    """ ************************************************
    Function to read KRL code from a file and return
    a pandas dataframe with the axis commands broken
    down for every line ************************ """
def dictnum2dictls(dictitself):
    for key in dictitself.keys():
        dictitself[key] = [dictitself[key]]
    
    return dictitself
def dataFraming(fileChangeInstance):
    code = fileChangeInstance.oldCodeRead() # Returns code line by line
    count = 0
    output = []

    for line in code:
        if count == 0:
            output = pd.DataFrame(dictnum2dictls(krl2dict(line)))
            count = 1
            continue
        else:
            newDF = pd.DataFrame((dictnum2dictls(krl2dict(line))))
            output = pd.concat([output, newDF], ignore_index=True)
            
    return output

""" ***********************************************
    Function to analyze effort used by every axis
    of the robot code
*********************************************** """
def extEffort(dataFrame):

    for column in dataFrame.columns.tolist():
        if column == "cmd":
            continue
        else:
            series = dataFrame[column].sub(dataFrame[column].shift())
            series = series.rename(column + "_work")
            dataFrame = pd.concat([dataFrame, series], axis=1)
    
    return dataFrame

""" ***********************************************
    Function to graph out the position that the 
    each axis will be
    ******************************************* """
def plotter(dataFrame, column_name='E1', all_col=False):
    if not (column_name or all_col):
        return
    
    plt.figure()
    plt.xlabel("CMD Number")
    plt.ylabel("AXES")
    x = dataFrame.index.tolist()

    line_ls = []
    legend_names = []
    if all_col:
        for column in dataFrame.columns.tolist():
            line_ls.append(plt.plot(x, dataFrame[column].tolist(), label=column))
            legend_names.append(column)
    
    else:
        y = dataFrame[column_name].tolist()
        plt.plot(x, y)
    
    plt.legend()
    plt.show()

    return

def preprocessor(filename):
    fp = open(filename, "r")
    lines = fp.readlines()
    fp.close()

    output = []

    for line in lines:
        if line[0:2] != "LIN":
            continue
        else:
            output.append(line)
    
    fp = open("good.src", "w")

    for line in output:
        fp.write(output)
    fp.close()

    return
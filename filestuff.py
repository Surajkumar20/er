from requirements import *

""" *************************************************************
    Class for adding lines of code
************************************************************* """
class codeObject:
    def __init__(self, old="old_code.src", new="new_code.src"):
        self.oldfilename = old
        self.newfilename = new
        self.fullCode_strls = self.oldCodeRead() # As a string
        #print(self.fullCode_strls)
        self.code_strls = self.preprocess(self.fullCode_strls)
        self.oldcodeDF = self.dataFraming(self.code_strls)
        self.oldCodeAxEf = [] # This variable will be updated once we call the external axis effort graph

    """ This code will save lines that start with LIN, ARC, or PTP into a list of strings """
    def preprocess(self, code):
        output = []

        for line in code:
            #print(line[0:(2+1)])
            match (line[0: (2 + 1)]):
                case "LIN":
                    output.append(line)
                    continue            
                case "ARC":
                    output.append(line)
                    continue
                case "PTP":
                    output.append(line)
                    continue
                case _:
                    continue

        return output

    ''' Code to read in lines of KRL code removing the \n as a list of strings'''
    def oldCodeRead(self):
        output = []
        fp = open(self.oldfilename, "r")
        lines = fp.readlines()
        fp.close()

        for line in lines:
            output.append(line.replace('\n', ""))

        return output

    """ Writes new code from a complete DF into a file """
    def codeWrite(self, codeDF):
        fp = open(self.newfilename, "w")

        for index, row in codeDF.iterrows():
            fp.write("{} {{X {}, Y {}, Z {}, A {}, B {}, C {}, E1 {}}} {}\n".format(codeDF.at[index, "cmd"], codeDF.at[index, "X"], codeDF.at[index, "Y"], codeDF.at[index, "Z"], codeDF.at[index, "A"], codeDF.at[index, "B"], codeDF.at[index, "C"], codeDF.at[index, "E1"], "C_DIS" if codeDF.at[index, "C_DIS"] else ""))

        fp.close()
        return

    """ Accepts code as a list of strings and returns a pandas dataframe """
    def dataFraming(self, code):
        """ ************************************************
        Function to read KRL code from a file and return
        a pandas dataframe with the axis commands broken
        down for every line ************************ """
        def dictnum2dictls(dictitself):
            for key in dictitself.keys():
                dictitself[key] = [dictitself[key]]

            return dictitself

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
                if len(pos.split()) == 3:
                    axis, value, cdis = pos.split()
                    output[axis] = eval(value)
                    output[cdis] = True
                elif len(pos.split()) == 2:
                    axis, value = pos.split()
                    output[axis] = eval(value)
                    output["C_DIS"] = False

            return output

         # Returns code line by line
        count = 0 # This code is because the first line does not have a datastructure to join into. So we need to make it the matriach
        output = []

        for line in code:
            if count == 0:
                if (line[0: (2+1)] == "LIN") or (line[0: (2+1)] == "PTP") or (line[0: (2+1)] == "ARC"):
                    misc_dict = {"MISC":[line]}
                    output = pd.DataFrame(misc_dict)
                else:
                    output = pd.DataFrame(dictnum2dictls(krl2dict(line)))
                    count = 1
                continue
            else:
                if (line[0: (2+1)] == "LIN") or (line[0: (2+1)] == "PTP") or (line[0: (2+1)] == "ARC"):
                    misc_dict = {"MISC":[line]}
                    output = pd.DataFrame(misc_dict)
                else:
                    newDF = pd.DataFrame((dictnum2dictls(krl2dict(line))))
                    output = pd.concat([output, newDF], ignore_index=True)
                continue
                
        if "E1" not in output:
            output["E1"] = 0
        
        return output.fillna(0)
    
    """ ***********************************************
    Function to analyze effort used by every axis
    of the robot code
    *********************************************** """
    def AxEffort(self, dataFrame):
        for column in dataFrame.columns.tolist():
            if column == "cmd" or column == "C_DIS":
                continue
            else:
                series = dataFrame[column].sub(dataFrame[column].shift())
                series = series.rename(column + "_work")
                dataFrame = pd.concat([dataFrame, series], axis=1)

        self.oldCodeAxEf = dataFrame
        return dataFrame

    """ ***********************************************
        This function will check if the external axis
        is used at all. Returns boolean variable """
    def extAxUse(self):
        try:
            # Check if the table has been initialized in the class. It is possible that the user did not bother calculating the effort table yet
            emptytable = (self.oldCodeAxEf["E1_work"] != 0).sum() - 1
        except:
            print("Effort Table was not calculated for this code.  Currently calculating!")
            eft = self.oldCodeAxEf(self.codeDF)
        finally:
            # If the code does no work
            if ((self.oldCodeAxEf["E1_work"] != 0).sum()-1) <= 0:
                return False
            else:
                return True
        
    """ ***********************************************
        Same function as extAxUse, but taking in a list
        of axes so that we can do it for multiple axes """
    def AxUse(self, ax_ls):
        output = []
        for ax in ax_ls:
            try:
                emptyTable = (self.oldCodeAxEf[ax] != 0).sum() - 1
            except:
                print("Effort Table was not calculated for this code. Currently calculating!")
                eft = self.oldCodeAxEf(self.oldcodeDF)
            finally:
                # If the code does no work
                if ((self.oldCodeAxEf[ax] != 0).sum()-1) <= 0:
                    output.append(False)
                else:
                    output.append(True)        
        return output

    """ ***********************************************
        Function to graph out the position that the 
        each axis will be in
        ******************************************* """
    def plotter(self, dataFrame, column_name='E1', all_col=False):
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
    
    """ ***********************************************
        Quick loader. Reading in line by line       """
    def quickDF(self):
        return
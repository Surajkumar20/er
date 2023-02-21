import filestuff as fs
import framework as fw
import numpy as np

if __name__ == "__main__":

    code = fs.codeObject("old_code.src")
    print(code.oldcodeDF)
    #print(code.oldcodeDF.at[3, "E1"])
    #code.codeWrite(code.oldcodeDF)
    """ This code is to see if any particuar axis was used
    print(code.AxEffort(code.oldcodeDF))
    if (code.AxUse(["C"])):
        print("We used the C ax for code")
    else:
        print("C axis was not hurt today") """

    '''inertial = fw.frame()
    table = fw.frame(inertial, )'''
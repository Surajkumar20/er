import filestuff as fs
import framework as fw

if __name__ == "__main__":

    codex = fs.codeObject(old="s1001_1.src")
    value = codex.oldcodeDF
    print(value)
    print(value.loc[10:50,'CMD':'E1'])

    '''print(codex.parse_string(str1))
    print(codex.parse_string(str2))
    print(codex.parse_string(str3))
    print(codex.parse_string(str4))'''


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
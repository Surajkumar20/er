import storage as st

if __name__ == "__main__":

    code = st.codeObject("codenoe1.txt")
    print(code.moveCodeDF)
    print(code.AxEffort(code.moveCodeDF))
    if (code.extAxUse()):
        print("We used the external axis in this code")
    else:
        print("No external axis was hurt here today")
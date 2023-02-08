import storage as st

if __name__ == "__main__":

    fileObject = st.fileChange("old_code.src")
    pdf = st.dataFraming(fileObject)
    print(pdf)

    st.plotter(pdf, all_col=True)

    st.preprocessor("DIGITALWRITE_s3DP_end_effector_1.src")

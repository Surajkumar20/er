import re 

code = "LIN {X -130.000,Y -129.250,Z 0.200,A -135.000,B 0.000,C 180.000, E1 0.01} C_DIS"

result = [float(i) for i in re.findall(r'-?\d+\.\d+', code)]
print(result)
import os
global_folder = os.getcwd()
folder_location = os.path.join(global_folder, "")
folder_location = os.path.join(folder_location, "scripts/scripts_for_model_generation")
file_location = os.path.join(folder_location, "model_db.txt")

with open(file_location, "r") as f:
    view_file = f.readlines()


model_fields = []
for line in view_file:
    line = line.strip()
    n = len(line)
    if(n==0):
        continue
    parameter_name = line.split()[0]
    if("pk" in line):
        s = "{} = models.AutoField(primary_key=True, editable=False)".format(parameter_name)
        model_fields.append(s)
        continue

    if("ref" in line):
        # ForeignField
        check_1 = False
        ind1 = n
        check_2 = False
        ind2 = n
        for i in range(n):
            if(line[i]==">"):
                check_1 = True
                ind1 = i
            if(line[i]=="." and i>ind1):
                check_2 = True
                ind2 = i
            if(check_1 and check_2):
                break
        if(check_1 and check_2):
            s = line[ind1+1:ind2].strip()
            if(s[-2:]=="es" and (s[-3:-2] in ["s", "x", "z"] or s[-4:-2] in ["sh", "ch"])):
                s = s[:-2]
            elif(s[-1]=="s"):
                s = s[:-1]
        s = s.split("_")
        s = [x[0].upper()+x[1:] for x in s if (len(x)!=0)]
        s = "".join(s)
        foreign_field = s
        temp = "{} = models.ForeignKey({}, on_delete=models.CASCADE)".format(parameter_name, foreign_field)
        model_fields.append(temp)
        continue

    dp = {
        "int": "models.IntegerField()",
        "datetime": "models.DateTimeField()",
        "varchar": "models.CharField(max_length=100)",
        "phonenumber": "models.CharField(max_length=100)",
        "boolean": "models.BooleanField(default=False)",
        "textfield": "models.TextField(max_length=500)",
        "text": "models.TextField(max_length=500)",
        "decimal": "models.DecimalField(max_digits=25, decimal_places=10)",
        "percentage": "models.DecimalField(max_digits=25, decimal_places=10)",
        "email": "models.EmailField(max_length=100)",
    }
    temp = line.split()[1]
    parameter_field = ""
    for i in temp:
        if(i.isalpha()):
            parameter_field += i
        else:
            break
    s = "{} = {}".format(parameter_name, dp.get(parameter_field, None))
    model_fields.append(s)

# Dumping the result into a file
ans = "\n".join(model_fields)
import_file = open(os.path.join(folder_location, "models.txt"), "w")
n = import_file.write(ans)
import_file.close()
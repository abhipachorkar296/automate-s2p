import os
global_folder = os.getcwd()
app_name = "event"
folder_location = os.path.join(global_folder, app_name+"/views")

def get_classes_from_view(view_file_name):
    file_location = os.path.join(folder_location, view_file_name)
    with open(file_location, "r") as f:
        view_file = f.readlines()

    class_names = []
    # Filtering the class names
    for i in view_file:
        if("class" in i):
            # class func(APIView):
            i = i.strip()
            class_names.append(i[6:-10])

    # Formatting the class name with import 
    view_name = app_name+".views." + view_file_name[:-3]
    for i in range(len(class_names)):
        word = class_names[i]
        s = "from {} import {}".format(view_name, word)
        class_names[i] = s
    return class_names


all_views = ["event_view.py", "bid.py", "award.py"]
class_names = []
for view_file in all_views:
    temp_class_names = get_classes_from_view(view_file)
    class_names.extend(temp_class_names)

# Dumping the result into a file
ans = "\n".join(class_names)
import_file = open(os.path.join(folder_location, "__init__.py"), "w")
n = import_file.write(ans)
import_file.close()
import os

def getVITONDirectory(root_path, viton_path, dirs):
    results = []
    for dir in dirs:
        result = os.path.join(root_path, viton_path, dir)
        if os.path.exists(result):
            results.append(result)
        else:
            print(f"WARNING! : '{result}' in working list does_not exist!")
    return results

def readPairsFile(root_path, viton_path, file):
    cloth_results = []
    image_results = []
    file_path = os.path.join(root_path, viton_path, file)
    
    if (os.path.exists(file_path)):
        with open(file_path, 'r') as file:
            for i, line in enumerate(file):
                values = line.split()
                if len(values) == 2:
                    image_results.append(values[0])
                    cloth_results.append(values[1])
                else:
                    print(f"WARNING! : Mismatched image pair in line {i+1}")

        if len(image_results)>0 and len(cloth_results)>0:
            if len(image_results)==len(cloth_results):        
                print(f"Extracted {len(image_results)} pairs from '{file_path}'")            
            else:    
                print(f"ERROR! : Mismatched image pair counts {len(image_results)} != {len(cloth_results)}")
        else:
            print(f"ERROR! : Did not find any image pairs in '{file_path}'")
    else:
        print(f"ERROR! : File '{file_path}' does not exist!")

    return cloth_results, image_results

#Set the path to the VITON data
viton_dir = "data/viton"

#Sub-directories to check within the viton directory
dir_list = ["data/cloth", 
            "data/image", 
            "data/cloth-mask", 
            "data/image_body_parse", 
            "data/image_densepose_parse",
            "data/image_parse_with_hands",
            "data/image-parse"]

test_dir_list = ["data/cloth", 
                 "data/image"]

pairs_file = "viton_test_pairs_old.txt"
#pairs_file = "viton_test_pairs.txt"
#pairs_file = "viton_train_pairs.txt"

root_dir = os.getcwd()

print(f"Current working directory: {root_dir}")
print(f"VITON data directories   : {viton_dir}")
print(f"Directories to check     : {test_dir_list}")

working_dir_list = getVITONDirectory(root_dir, viton_dir, dir_list)
testing_dir_list = getVITONDirectory(root_dir, viton_dir, test_dir_list)

file_lists   = []
for dir in testing_dir_list:
    file_list = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    file_list = sorted(file_list)
    file_lists.append(file_list)    
    print(f"{len(file_lists[-1])} files found in {dir}")

lengths_equal = all(len(lst) == len(file_lists[0]) for lst in file_lists)
if not lengths_equal:
    print("WARNING! : The number of files in each test list are not equal!")

cloth_files, image_files = readPairsFile(root_dir, viton_dir, pairs_file)

line_no = 0
cloth_errors = image_errors = 0
error_list = []
for cloth_file, image_file in zip(cloth_files, image_files):
    OK = True
    line_no = line_no + 1
    cloth_file_path = os.path.join(testing_dir_list[0], cloth_file)
    image_file_path = os.path.join(testing_dir_list[1], image_file)
    #print(f"Line {line_no} : {cloth_file_path} {image_file_path}")

    if not os.path.exists(cloth_file_path):
        cloth_errors = cloth_errors + 1
        #print(f"  > Line: {line_no} : CLOTH PATH! Error_no: {cloth_errors}")
        OK = False

    if not os.path.exists(image_file_path):
        image_errors = image_errors + 1
        #print(f"  > Line: {line_no} : IMAGE PATH! Error_no: {image_errors}")
        OK = False

    if not OK:
        error_list.append(f"ERROR! Line: {line_no}, Image: {image_file}, Cloth: {cloth_file}")

if image_errors>0 or cloth_errors>0:
    print(f"WARNING! : There were {image_errors} missing image file(s) and {cloth_errors} missing cloth file(s)!")
else:
    print("All image-cloth pairs checked out OK!")

for i, error in enumerate (error_list):
    print(f"{i} : {error}")

if len(error_list)==0:

    print("------------------------------------------------------")
    train_prop = 0.8
    train_count = round(len(cloth_files) * 0.8)

    new_image_train_files = image_files[:train_count]
    new_image_test_files = image_files[train_count+1:]

    new_train_pairs_file = "new_train_pairs_file.txt"
    new_test_pairs_file = "new_test_pairs_file.txt"

    new_train_file_path = os.path.join(root_dir, viton_dir, new_train_pairs_file)
    new_test_file_path  = os.path.join(root_dir, viton_dir, new_test_pairs_file)

    print("NEW TRAINING PAIRS_FILE:")
    with open(new_train_file_path, 'w') as file:
        for i, image_file in enumerate(new_image_train_files):
            cloth_file = image_file.replace('_0','_1')        
            out_string = f"{image_file} {cloth_file}"
            file.write(out_string + '\n')
            #print(f"{i} : {image_file} : {cloth_file}")
    print("-------------------")

    print("NEW TESTING PAIRS FILE:")
    with open(new_test_file_path, 'w') as file:
        for i, image_file in enumerate(new_image_test_files):
            cloth_file = image_file.replace('_0','_1')      
            out_string = f"{image_file} {cloth_file}"
            file.write(out_string + '\n')
            #print(f"{i} : {image_file} : {cloth_file}")
    print("-------------------")

    


    
    







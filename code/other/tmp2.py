'''
@author Shijing
@author Davis
@create date 2020-12-07 01:26:56
'''
import re
import os
import sys
from shutil import copyfileobj
import glob
import subprocess

# ========================
# SQL Script part
# ========================
def output_file(sqlCommand:str, dirPath='%s/output'%(os.getcwd())): 
    outPutCommand = "insert overwrite local directory '%s' row format delimited fields terminated by ',' %s;\n" % (dirPath,sqlCommand)
    return outPutCommand


def create_script(outputScriptName: str):
    f = open("%s/%s.sql"%(os.getcwd(),outputScriptName), "w")
    f.write("USE RecursiveDB;\n")
    f.close()
    return "%s.sql" % outputScriptName


def load_data(outputTableName: str, dirPath='{path}/output/000000_0'.format(path=os.getcwd())):
    loadDataCommand = "load data local inpath '{path}' into table {tableName};\n".format(path=dirPath,tableName=outputTableName)
    return loadDataCommand


def create_table(firstTableName: str, secondTableName: str):
    createTableCommand = "drop table if exists {secondTableName};\ncreate table {secondTableName} like {firstTableName};\n".format(secondTableName=secondTableName, firstTableName=firstTableName)
    return createTableCommand


# =======================
# file handling part
# =======================

def create_directory(currDirPath=os.getcwd(), dirName="finalOutput"):
    try:
        os.makedirs('%s/%s' % (currDirPath,dirName),exist_ok=True)
    except OSError as e:
        print(e.errno)
        print(e)


def concat_files(fileDir='{cwd}/finalOutput'.format(cwd=os.getcwd()), outputName="concat"):
    fileNames = glob.glob("%s/*.txt"%fileDir)
    with open("%s/%s.txt" % (fileDir,outputName), "wb") as outfile:
        for f in fileNames:
            with open(f, "rb") as infile:
                outfile.write(infile.read())


def copy_file(fileName: int, currDirPath='%s'%os.getcwd()):
    with open('%s/finalOutput/%s.txt'%(currDirPath,fileName), 'wb') as output, open('%s/output/000000_0'%currDirPath, 'rb') as input:
        copyfileobj(input, output)


def add_empty_line(fileName: str, currDirPath='%s'%os.getcwd()):
    f = open('%s/finalOutput/%s.txt'%(currDirPath,fileName),'a')
    f.write("\n")
    f.close()

def remove_empty_line(fileName: str, currDirPath='%s'%os.getcwd()):
    with open('%s/finalOutput/%s.txt'%(currDirPath,fileName), 'r') as f:
        data = f.read()
        with open('%s/finalOutput/%s.txt'%(currDirPath,fileName), 'w') as w:
            w.write(data[:-1])


if __name__ == "__main__":
    
    inputCommand = "with recursive ancestor as (select * from people \
where Name = \"Hannah\" union all select people.* from people \
inner join ancestor on ancestor.father = people.ID or ancestor.mother = people.ID) \
select * from ancestor;"

    # inputCommand = "with recursive ancestor as (select * from people where Name = \"Hannah\" union all select people.* from people inner join ancestor on ancestor.father = people.ID or ancestor.mother = people.ID) select * from ancestor;"


    # inputCommand = sys.argv[1]

    baseCaseName = re.search(r"\"([a-zA-Z0-9]+)\"",inputCommand,re.IGNORECASE).group(1)
    firstTableName = re.search(r"from\s([a-zA-Z]+)\s",inputCommand,re.IGNORECASE).group(1)
    baseColumnName = re.search(r"where\s(\w+)",inputCommand, re.IGNORECASE).group(1)
    secondTableName = re.search(r"recursive\s(\w+)\s",inputCommand,re.IGNORECASE).group(1)
    baseCaseCommand = re.search(r"\((select\s[*a-zA-Z0-9_].*\s[a-zA-Z=\"0-9].*)\sunion",inputCommand,re.IGNORECASE).group(1)
    recursionCommand1 = re.search(r"all\s+([a-zA-Z0-9_].*)on",inputCommand,re.IGNORECASE).group(1)
    recursionCommand2 = re.search(r"\son\s([a-zA-Z0-9_].*)\)",inputCommand,re.IGNORECASE).group(1)
    recursionCommand = recursionCommand1 + "where " + recursionCommand2
    finalCommand = re.search(r"\)\s([a-zA-Z0-9*_;].*);",inputCommand,re.IGNORECASE).group(1)
    dirPath = os.getcwd()

    count = 0
    if "recursive" in inputCommand:
        create_directory()
        f = open(create_script(secondTableName),"a")
        f.write(output_file(baseCaseCommand))
        f.close()
      
        # # =========================================
        # # TODO: run the script to generate 000000_0
        # # =========================================
        r = subprocess.run('hive -f ancestor.sql', shell=True)
        # copy the file to directory "finalOutput"
        copy_file(str(count))
        # just in case it does not have an empty new line at the end
        # add_empty_line(str(count))
        # while the output file is not empty
        while os.path.getsize("%s/output/000000_0"%os.getcwd()) != 0:
            # create an output directory
            create_directory()
            count += 1
        
            f = open(create_script(secondTableName),"a")
            # create a new table based on the temp table name given from sql command
            f.write(create_table(firstTableName,secondTableName))
            # load data to the new table
            f.write(load_data(secondTableName))
            # output the new result 
            f.write(output_file(recursionCommand))
            f.close()
      
            # ++++++++++++++++++++++++++++++++++++++++++++
            # TODO: run the file command to get 000000_0 
            # ++++++++++++++++++++++++++++++++++++++++++++
            r = subprocess.run('hive -f ancestor.sql', shell=True)

            # copy the file to directory "finalOutput"
            copy_file(str(count))
            # just in case it does not have an empty new line at the end
            # add_empty_line(str(count))
            # temporary terminate it after three runs 
            # if count == 3:
            #     open('%s/output/000000_0'%os.getcwd(), 'w').close()
        try:
            # merge all files into one file
            concat_files()
            f = open(create_script(secondTableName),"a")
            # create a new table based on the temp table name given from sql command
            f.write(create_table(firstTableName,secondTableName))
            # load data to the new table
            f.write(load_data(secondTableName,'%s/finalOutput/concat.txt' % os.getcwd()))
            # output the new result
            f.write(output_file(finalCommand))
            f.close()

            # ++++++++++++++++++++++++++++++++++++++++++++
            # TODO: run the file command to get 000000_0 
            # ++++++++++++++++++++++++++++++++++++++++++++
            r = subprocess.run('hive -f ancestor.sql', shell=True)

                # copy the file to directory "finalOutput"
            copy_file("result")
            #     # just in case it does not have an empty new line at the end
            #     add_empty_line("result")
        except Exception as e:
            print("nothing to contatenate!!")


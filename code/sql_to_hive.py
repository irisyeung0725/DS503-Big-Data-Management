import re
import os
import sys
from shutil import copyfileobj
import glob
import hive_executor

# ========================
# SQL Script part
# ========================
def output_file(sqlCommand: str, baseDir=os.getcwd(), subDir='.tmp/output'):
    outPutCommand = 'insert overwrite local directory \'{bd}/{sd}\' row format delimited fields terminated by \',\' {sql};\n'.format(sql=sqlCommand, bd=baseDir, sd=subDir)
    return outPutCommand


def create_script(scriptName='tmp_script', baseDir=os.getcwd(), subDir='.tmp', database="RecursiveDB"):
    f = open('{bd}/{sd}/{scriptName}.sql'.format(bd=baseDir, sd=subDir, scriptName=scriptName), 'w')
    f.write('USE {db};\n'.format(db=database))
    f.close()
    return '{bd}/{sd}/{scriptName}.sql'.format(bd=baseDir, sd=subDir, scriptName=scriptName)


def load_data(outputTableName: str, fileName="000000_0", baseDir=os.getcwd(), subDir='.tmp/output'):
    loadDataCommand = 'load data local inpath \'{bd}/{sd}/{fn}\' into table {tableName};\n'.format(bd=baseDir, sd=subDir, fn=fileName, tableName=outputTableName)
    return loadDataCommand


def create_like_table(firstTableName: str, secondTableName: str):
    createTableCommand = 'drop table if exists {secondTableName};\ncreate table {secondTableName} like {firstTableName};\n'.format(secondTableName=secondTableName, firstTableName=firstTableName)
    return createTableCommand


# =======================
# file handling part
# =======================

def create_directory(baseDir=os.getcwd(), subDir='.tmp/finalOutput'):
    try:
        os.makedirs('{bd}/{sd}'.format(bd=baseDir, sd=subDir), exist_ok=True)
    except OSError as e:
        print(e.errno)
        print(e)


def concat_files(fileName='concat', baseDir=os.getcwd(), subDir='.tmp/finalOutput'):
    fileNames = glob.glob('{bd}/{sd}/*.txt'.format(bd=baseDir, sd=subDir))

    with open('{bd}/{sd}/{fn}.txt'.format(bd=baseDir, sd=subDir, fn=fileName), 'wb') as outfile:
        for f in fileNames:
            with open(f, 'rb') as infile:
                outfile.write(infile.read())


def copy_file(fileName: int, baseDir=os.getcwd(), subDir1='.tmp/output', subDir2='.tmp/finalOutput'):
    with open('{bd}/{sd}/{fn}.txt'.format(bd=baseDir, sd=subDir2, fn=fileName), 'wb') as output, open('{bd}/{sd}/{fn}'.format(bd=baseDir, sd=subDir1, fn='000000_0'), 'rb') as input:
        copyfileobj(input, output)


def add_empty_line(fileName: str, baseDir=os.getcwd(), subDir='.tmp/finalOutput'):
    f = open('{bd}/{sd}/{fn}.txt'.format(bd=baseDir, sd=subDir, fn=fileName), 'a')
    f.write('\n')
    f.close()

def remove_empty_line(fileName: str, baseDir=os.getcwd(), subDir='.tmp/finalOutput'):
    with open('{bd}/{sd}/{fn}.txt'.format(bd=baseDir, sd=subDir, fn=fileName), 'r') as f:
        data = f.read()
        with open('{bd}/{sd}/{fn}.txt'.format(bd=baseDir, sd=subDir, fn=fileName), 'w') as w:
            w.write(data[:-1])


def convert_and_run(inputCommand, database="recursivedb"):
    print(inputCommand)

    # inputCommand = 'with recursive ancestor as (select * from people where Name = \"Hannah\" union all select people.* from people inner join ancestor on ancestor.father = people.ID or ancestor.mother = people.ID) select * from ancestor;'


    # inputCommand = sys.argv[1]

    # inputCommand = inputCommand.lower()
    baseCaseName = re.search(r'(["a-zA-Z0-9]+)\sunion',inputCommand,re.IGNORECASE).group(1)
    firstTableName = re.search(r'from\s([a-zA-Z]+)\s',inputCommand,re.IGNORECASE).group(1)
    baseColumnName = re.search(r'where\s(\w+)',inputCommand, re.IGNORECASE).group(1)
    secondTableName = re.search(r'recursive\s(\w+)\s',inputCommand,re.IGNORECASE).group(1)
    baseCaseCommand = re.search(r'\((select\s[*a-zA-Z0-9_].*\s[a-zA-Z=\"0-9].*)\sunion',inputCommand,re.IGNORECASE).group(1)
    recursionCommand1 = re.search(r'all\s+([a-zA-Z0-9_].*)on',inputCommand,re.IGNORECASE).group(1)
    recursionCommand2 = re.search(r'\son\s([a-zA-Z0-9_].*)\)',inputCommand,re.IGNORECASE).group(1)
    recursionCommand = recursionCommand1 + 'where ' + recursionCommand2
    finalCommand = re.search(r"\)\s([a-zA-Z0-9*_;].*);",inputCommand,re.IGNORECASE).group(1)
    dirPath = os.getcwd()

    TMP_SQL_FILENAME = 'ancestor'

    count = 0
    if 'recursive' in inputCommand:
        create_directory()
        f = open(create_script(scriptName=TMP_SQL_FILENAME, database=database),'a')
        f.write(output_file(sqlCommand=baseCaseCommand))
        f.close()
        
        r =  hive_executor.from_file(TMP_SQL_FILENAME)

        # copy the file to directory 'finalOutput'
        copy_file(str(count))
        # just in case it does not have an empty new line at the end
        # add_empty_line(str(count))
        # while the output file is not empty
        while os.path.getsize('%s/.tmp/output/000000_0'%os.getcwd()) != 0:

            # create an output directory
            create_directory()
            count += 1

            print("Loopin!", count)
        
            f = open(create_script(scriptName=TMP_SQL_FILENAME),'a')
            # create a new table based on the temp table name given from sql command
            f.write(create_like_table(firstTableName,secondTableName))
            # load data to the new table
            f.write(load_data(secondTableName))
            # output the new result 
            f.write(output_file(sqlCommand=recursionCommand))
            f.close()

            r =  hive_executor.from_file(TMP_SQL_FILENAME)

            # copy the file to directory 'finalOutput'
            copy_file(str(count))
            # just in case it does not have an empty new line at the end
            # add_empty_line(str(count))
            # temporary terminate it after three runs 
            # if count == 3:
            #     open('%s/output/000000_0'%os.getcwd(), 'w').close()
        try:
            # merge all files into one file
            concat_files()
            f = open(create_script(scriptName=TMP_SQL_FILENAME),'a')
            # create a new table based on the temp table name given from sql command
            f.write(create_like_table(firstTableName,secondTableName))
            # load data to the new table
            f.write(load_data(secondTableName, fileName='concat.txt', subDir='.tmp/finalOutput'))
            # output the new result
            f.write(output_file(finalCommand))
            f.close()

            # ++++++++++++++++++++++++++++++++++++++++++++
            # TODO: run the file command to get 000000_0 
            # ++++++++++++++++++++++++++++++++++++++++++++
            r =  hive_executor.from_file(TMP_SQL_FILENAME)

                # copy the file to directory 'finalOutput'
            copy_file('result')
            #     # just in case it does not have an empty new line at the end
            #     add_empty_line('result')
        except Exception as e:
            print('nothing to contatenate!!')


if __name__=="__main__":
        
    test = 'with recursive ancester as (select * from people \
where Name = \"Hannah\" union all select people.* from people \
inner join ancester on ancester.father = people.ID or ancester.mother = people.ID) \
select * from ancester;"'

    convert_and_run(test)
# Implementing Recursive Queries on Hive+Hadoop

## Dependencies
- [Java](https://www.java.com/en/)
- [Python3](https://www.python.org/downloads/)
- [Apache Hadoop](https://hadoop.apache.org/)
- [Apache Hive](https://hive.apache.org/)
- Python development and [PyQt](https://riverbankcomputing.com/software/pyqt/intro) packages (dependent on OS) 

> Recommended: follow these instructions for setup
https://www.edureka.co/community/1828/installing-hive-hadoop-in-vm

## Test Environment
Tested on `Ubuntu 20.04` with Hadoop installed in single cluster mode and Hive installed on top.

## Setup
If not already in code directory:
```
cd code/
```

Then run:
```
pip install -r requirements.txt
```

Now you can run the system:
```
python3 main.py
```
## Background 
Recursive queries (or also called Transitive Closure Queries) are a class of queries that first build an initial answer  state  (say  R),  and  then  use  this  answer  state  to  execute  more  queries.  The  results  from  each execution  get  augmented  to  the  answer  state.  The  execution  continues  until  no  more  records  are augmented to the answer state.  Here is an example of how a recursive query looks like.
![recursive](https://user-images.githubusercontent.com/45746834/132790248-9f3f5bc7-9120-45ec-915f-4bcbf159ef94.png)

This project is to 
- Build a good understanding on the class of recursive queries and how they work
- Implement a high-level interface for end-users to enter and submit a recursive query.
- The interface should parse the query, and decide on the sequence of queries it will generate. And then submit these queries  (one at a time) to the Hive engine. 
- Hive does not see the recursive queryitself; it just sees one isolated query at a time. The higher-level interface is controlling the execution of the entire recursive query.

## Implementation
The solution was implemented to support command line queries and a graphical user interface. The interface is what will be detailed in this section as it is an example implementation of howto leverage the functionality. The interface was completed with `PyQt5` following a Model-View-Controller design paradigm. The controller section depicts the interaction with the Hivequery tool. The interface is able to accept both recursive and non-recursive commands enteredinto the multi-line text box. The user may then click `Execute!` to process the commands. Therecursive results will be saved in `a.tmp/directory`, however, this can be easily modified.

The user interface of the application
![execute](https://user-images.githubusercontent.com/45746834/132789930-b45a0e8a-c149-4b79-aee2-6a4bd3a7e57d.png)

The application is processing user-input recursive query written in `SQL`
![processing](https://user-images.githubusercontent.com/45746834/132789922-b2406aad-2301-4645-a540-c912a7b3b838.png)

## Final Report
To view the final report for this project, please navigate to [this page](https://github.com/irisyeung0725/DS503-Big-Data-Management/blob/master/report.pdf)

## Contributers
Shijing Yang syang6@wpi.edu | Davis Catherman dscatherman@wpi.edu

create database if not exists recursiveDB;

USE recursiveDB;

-- drop table if exist
Drop table if exists people;

-- create table
create table people (ID int, Name string, father int, mother int) row format delimited fields terminated by ',';

-- Insert Data into the table
load data local inpath '/home/davis/DS503FinalProject/other/catherman_tree.txt' into table people;

-- -- output txt file
-- insert overwrite local directory '/home/davis/DS503FinalProject/output' row format delimited fields terminated by ',' select *, 0 as level from people where Name = 'Hannah';
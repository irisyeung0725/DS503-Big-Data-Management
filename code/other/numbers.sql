
USE recursiveDB;

-- drop table if exist
Drop table if exists numbers;

-- create table
create table numbers (num int) row format delimited fields terminated by ',';

-- Insert Data into the table
load data local inpath '/home/davis/DS503FinalProject/numbers.txt' into table numbers;
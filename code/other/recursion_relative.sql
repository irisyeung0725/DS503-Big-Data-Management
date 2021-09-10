-- create dababase
CREATE database if not exists recursionDB;

-- use database
USE recursionDB;

-- drop table if exist
Drop table if exists folks;

-- create table
create table folks (ID int, Name string, father int, mother int) row format delimited fields terminated by ',';

-- see the table columns
describe folks;

-- Insert Data into the table
load data local inpath '/home/davis/DS503FinalProject/folks_data.txt' into table folks;

-- fetch the records from the table
select * from folks where Name = 'Alex';

-- output txt file
insert overwrite local directory '/home/davis/DS503FinalProject/output' row format delimited fields terminated by ',' select * from folks where Name = 'Alex';



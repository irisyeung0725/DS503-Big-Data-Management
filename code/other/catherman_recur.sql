USE recursionDB;

drop table if exists ancestor;

-- create a table that shares exact schema with the one alrealy exists
create table ancestor like people;

-- load data to a new table 
load data local inpath '/home/davis/DS503FinalProject/output/000000_0' into table ancestor;

-- output txt file
insert overwrite local directory '/home/davis/DS503FinalProject/output' row format delimited fields terminated by ',' select people.* from people inner join ancestor where (people.ID = ancestor.mother or people.ID = ancestor.father);




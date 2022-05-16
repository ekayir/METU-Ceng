insert into publication (pub_key, title, year) 
(
	select   p.pub_key , f2.field_value  as title,  CAST (f1.field_value AS INTEGER)  as year from pub p 
	left join field f1 on p.pub_key = f1.pub_key and f1.field_name ='year' 
	left join field f2 on p.pub_key = f2.pub_key and f2.field_name ='title'
);

insert into author ("name") 
(
	select distinct f.field_value  from field f where f.field_name ='author'
);


insert into article 
(
	select pu.pub_id ,f1.field_value as journal,f2.field_value as month,
		   f3.field_value as volume,f4.field_value as number from pub p
	left join field f1 on p.pub_key = f1.pub_key and f1.field_name ='journal' 
	left join field f2 on p.pub_key = f2.pub_key and f2.field_name ='month'
	left join field f3 on p.pub_key = f3.pub_key and f3.field_name ='volume'
	left join field f4 on p.pub_key = f4.pub_key and f4.field_name ='number'
		 join publication pu on p.pub_key = pu.pub_key 
	where p.pub_key =  pu.pub_key and p.pub_type ='article'
);


insert into book 
(
	select pu.pub_id ,f1.field_value as publisher, max(f2.field_value) as isbn from pub p
	left join field f1 on p.pub_key = f1.pub_key and f1.field_name ='publisher' 
	left join field f2 on p.pub_key = f2.pub_key and f2.field_name ='isbn'
		 join publication pu on p.pub_key = pu.pub_key 
	where p.pub_key =  pu.pub_key and p.pub_type ='book' 
group by  pu.pub_id , f1.field_value
);



insert into incollection 
(
	select pu.pub_id, f1.field_value as booktitle,f2.field_value  as publisher,max(f3.field_value) as isbn
	from pub p
	left join field f1 on p.pub_key = f1.pub_key and f1.field_name ='booktitle' 
	left join field f2 on p.pub_key = f2.pub_key and f2.field_name ='publisher'
	left join field f3 on p.pub_key = f3.pub_key and f3.field_name ='isbn'
		 join publication pu on p.pub_key = pu.pub_key 
	where p.pub_key =  pu.pub_key and p.pub_type ='incollection' 
group by  pu.pub_id, f1.field_value ,f2.field_value 
);


insert into inproceedings 
(
	select pu.pub_id, f1.field_value as booktitle,f2.field_value  as editor
	from pub p
	left join field f1 on p.pub_key = f1.pub_key and f1.field_name ='booktitle' 
	left join field f2 on p.pub_key = f2.pub_key and f2.field_name ='editor'
		 join publication pu on p.pub_key = pu.pub_key 
	where p.pub_key =  pu.pub_key and p.pub_type ='inproceedings' 
);



insert into authored 
(
	select    a.author_id , pu.pub_id from  publication pu, field f , author a
	where  pu.pub_key = f.pub_key 
	and f.field_name ='author'
	and a."name" = f.field_value
	group by a.author_id , pu.pub_id
);

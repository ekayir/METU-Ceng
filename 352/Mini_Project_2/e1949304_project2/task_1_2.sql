select f.field_name from pub p , field f 
where p.pub_key = f.pub_key 
group by f.field_name 
having count(distinct pub_type) = (select count(distinct p.pub_type) from pub p )
order by 1;



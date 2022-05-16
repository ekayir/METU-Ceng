select aa."name" , hh.collab_count from (
select * from (
select count(distinct a2.author_id )collab_count,a1.author_id from authored a1,authored a2 
where a1.pub_id = a2.pub_id and a2.author_id <>a1.author_id 
group by a1.author_id)tt)hh, author aa
where aa.author_id = hh.author_id
order by 2 desc,1
limit 1000

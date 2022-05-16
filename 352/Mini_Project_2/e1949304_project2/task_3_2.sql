select a3."name" as author_name ,count(a.journal ) as pub_count from "publication" p , article a , authored a2 , author a3 
where p.pub_id = a.pub_id and a.journal  like '%IEEE%' and a2.pub_id = p.pub_id 
and a2.author_id =a3.author_id 
group by a3."name" 
order by 2 desc, 1
limit 50

--8sn
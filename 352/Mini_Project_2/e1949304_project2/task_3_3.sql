select a3."name" as name, count(a.journal ) as pub_count from "publication" p 
, article a , 
authored a2 ,
author a3  
where a3.author_id not in (select a2.author_id from article a , authored a2 
where a.journal= 'IEEE Wireless Commun. Letters' and a.pub_id = a2.pub_id) and
p.pub_id = a.pub_id 
and a.journal='IEEE Trans. Wireless Communications' and a2.pub_id = p.pub_id 
and a2.author_id =a3.author_id  
group by a3."name" 
having count(*)>=10
order by 2 desc, 1
select a2."name" as author_name, aa.sayi as pub_count from (
select  count(distinct p.pub_key)as sayi, a.author_id from "publication" p , authored a  
where p.pub_id = a.pub_id  
group by a.author_id) aa, author a2
where aa.sayi>=150 and aa.sayi<200 and a2.author_id =aa.author_id
order by 2,1

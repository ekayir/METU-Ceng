select tt.decade, sum(tt.sayi)as total from 
(select '"'||cast(ye.year as varchar)|| '-'||cast(ye.year+10 as varchar)||'"' as decade,say.sayi
from (select distinct year as year from "publication" p where  "year" >= 1940)ye,
(
select count(1)as sayi, p."year" from "publication" p 
where  p."year" >=1940
group by p."year" )say
where say.year between ye.year and ye.year+9
)tt
group by tt.decade
order by 1

--1sn
select zz.year, a.name, zz.sayi as count from (
select year, max(sayi)sayi from (
select p."year", a.author_id,count(1)sayi from "publication" p , authored a 
where p.pub_id = a.pub_id and p."year" between 1940 and 1990
group by p."year", a.author_id  ) aa
group by year)zz,(
select p."year", a.author_id,count(1)sayi from "publication" p , authored a 
where p.pub_id = a.pub_id and p."year" between 1940 and 1990
group by p."year", a.author_id  ) tab,author a 
where tab.year = zz.year and tab.sayi = zz.sayi
and a.author_id = tab.author_id
order by 1,2
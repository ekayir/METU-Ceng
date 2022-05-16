select
	aa.plane_tail_number,
	aa.year,
	sum(aa.countFlight) * 1.0 / count(aa.monthDay)daily_avg
from
	(
	select
		fr.plane_tail_number ,
		cast (fr."month" as varchar) || '/' || cast (fr."day" as varchar)monthDay ,
		count(*)as countFlight,
		fr."year"
	from
		flight_reports fr
	where
		fr.is_cancelled = 0
	group by
		fr."year" ,
		fr.plane_tail_number,
		cast (fr."month" as varchar) || '/' || cast (fr."day" as varchar))AA
group by
	aa.plane_tail_number,
	aa.year
having
	sum(aa.countFlight) * 1.0 / count(aa.monthDay)>5
order by
	1 ,
	2
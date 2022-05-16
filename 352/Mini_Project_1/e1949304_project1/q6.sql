select
	aa.weekday_id,
	(
	select
		w2.weekday_name
	from
		weekdays w2
	where
		w2.weekday_id = aa.weekday_id)as weekday_name,
	aa.avg_delay
from
	(
	select
		fr.weekday_id ,
		avg(fr.arrival_delay + fr.departure_delay )avg_delay
	from
		flight_reports fr
	where
		fr.origin_city_name = 'San Francisco, CA'
		and fr.dest_city_name = 'Boston, MA'
	group by
		fr.weekday_id) AA
where
	AA.avg_delay = (
	select
		min(AA.avg_delay)
	from
		(
		select
			fr.weekday_id ,
			avg(fr.arrival_delay + fr.departure_delay )avg_delay
		from
			flight_reports fr
		where
			fr.origin_city_name = 'San Francisco, CA'
			and fr.dest_city_name = 'Boston, MA'
		group by
			fr.weekday_id) AA)
select
	bosAir.year,
	bosAir.airline_code,
	sum(case when fr.dest_city_name = 'Boston, MA' then 1 else 0 end) boston_flight_count,
	(sum(case when fr.dest_city_name = 'Boston, MA' then 1 else 0 end) * 100.0 / count(1))boston_flight_percentage
from
	(
	select
		distinct fr.airline_code ,
		fr."year"
	from
		flight_reports fr
	where
		fr.is_cancelled = 0
		and fr.dest_city_name = 'Boston, MA' )bosAir,
	flight_reports fr
where
	bosAir.airline_code = fr.airline_code
	and fr.is_cancelled = 0
	and bosAir.year = fr."year"
group by
	bosAir.year,
	bosAir.airline_code
having
	(sum(case when fr.dest_city_name = 'Boston, MA' then 1 else 0 end) * 100.0 / count(1)) > 1
	order by 1,2
/****** Script for SelectTopNRows command from SSMS  ******/
select
	air.airline_name,
	air.airline_code,
	avg(ff.departure_delay)as avg_delay
from
	airline_codes air,
	flight_reports ff
where
	air.airline_code = ff.airline_code
	and ff.is_cancelled = 0
	and ff.year = 2018
group by
	air.airline_name,
	air.airline_code
order by
	3,
	1
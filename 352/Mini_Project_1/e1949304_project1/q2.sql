/****** Script for SelectTopNRows command from SSMS  ******/
select
	port.airport_code,
	port.airport_desc,
	count(1) as cancel_count
from
	airport_codes port,
	flight_reports ff
where
	port.airport_code = ff.origin_airport_code
	and ff.cancellation_reason = 'D'
group by
	port.airport_code,
	port.airport_desc
order by
	3 desc,
	1 asc
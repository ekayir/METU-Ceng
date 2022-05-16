select * from 
(select
	aa.airline_name,
	sum(aa.monday_flights)as monday_flights,
	sum(aa.sunday_flights)as sunday_flights
from
	(
	select
		ac.airline_name,
		count(1)as monday_flights,
		0 as sunday_flights
	from
		airline_codes ac
	right outer join flight_reports fr on
		fr.airline_code = ac.airline_code
	where
		fr.is_cancelled = 0
		and "day" = 1
	group by
		ac.airline_name
union all
	select
		ac.airline_name,
		0 ,
		count(1) as sunday_flights
	from
		flight_reports fr ,
		airline_codes ac
	where
		fr.airline_code = ac.airline_code
		and fr.is_cancelled = 0
		and "day" = 6
	group by
		ac.airline_name
union
	select
		ac2.airline_name ,
		0 ,
		0
	from
		airline_codes ac2 )AA
group by
	airline_name
)zz
order by 1

select
	AA.*
from
	(
	select
		ac.airline_name,
		fr."year" ,
		count(1) as total_num_flights ,
		sum(is_cancelled) as cancelled_flights
	from
		flight_reports fr ,
		airline_codes ac
	where
		fr.airline_code = ac.airline_code
	group by
		fr."year" ,
		ac.airline_name
	having
		count(1)/ count(distinct "month" + day)>2000 )AA ,
	(
	select
		bb.airline_name
	from
		(
		select
			ac.airline_name
		from
			flight_reports fr ,
			airline_codes ac
		where
			fr.airline_code = ac.airline_code
		group by
			fr."year" ,
			ac.airline_name
		having
			count(1)/ count(distinct "month" + day)>2000) BB
	group by
		BB.airline_name
	having
		count(1) = 4 )CC
where
	AA.airline_name = CC.airline_name
order by
	airline_name
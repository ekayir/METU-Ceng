select
	*
from
	(
	select
		aa.airport_desc
	from
		(
		select
			ac.airport_desc ,
			count(1) as outgoing
		from
			flight_reports fr ,
			airport_codes ac
		where
			fr.is_cancelled = 0
			and ac.airport_code = fr.origin_airport_code
		group by
			ac.airport_desc
	union
		select
			ac.airport_desc ,
			count(1) as outgoing
		from
			flight_reports fr ,
			airport_codes ac
		where
			fr.is_cancelled = 0
			and ac.airport_code = fr.dest_airport_code
		group by
			ac.airport_desc )AA
	group by
		aa.airport_desc
	order by
		sum(outgoing) desc
	limit 5)ZZ
order by
	1
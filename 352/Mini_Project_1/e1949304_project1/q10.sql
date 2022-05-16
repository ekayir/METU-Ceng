select
	ac.airline_name ,
	count(1) as flight_count
from
	(
	select
		fr.airline_code ,
		fr.plane_tail_number
	from
		flight_reports fr
	where
		fr.dest_wac_id = 74
except
	select
		fr1.airline_code ,
		fr1.plane_tail_number
	from
		flight_reports fr1
	where
		fr1.dest_wac_id <> 74)AA ,
	flight_reports fr,
	airline_codes ac
where
	fr.plane_tail_number = aa.plane_tail_number
	and fr.airline_code = aa.airline_code
	and ac.airline_code = fr.airline_code
group by
	ac.airline_name
order by
	ac.airline_name
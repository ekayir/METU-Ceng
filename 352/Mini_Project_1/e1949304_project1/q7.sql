select
	ac.airline_name ,
	sum(fr.is_cancelled) * 100 / count(1) as percentage
from
	flight_reports fr, airline_codes ac  
where
	fr.origin_city_name = 'Boston, MA' and ac.airline_code = fr.airline_code 
group by
	ac.airline_name 
having
	sum(fr.is_cancelled) * 100 / count(1) > 10
	order by 2 desc
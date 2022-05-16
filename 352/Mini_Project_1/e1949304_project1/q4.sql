select
	AC.airline_name
from
	airline_codes ac ,
	flight_reports fr
where
	ac.airline_code = fr.airline_code
	and fr.is_cancelled = 0
	and (fr."year" = 2018
	or fr."year" = 2019)
	and (fr.dest_city_name = 'Boston, MA'
	or fr.dest_city_name = 'New York, NY'
	or fr.dest_city_name = 'Portland, ME'
	or fr.dest_city_name = 'Washington, DC'
	or fr.dest_city_name = 'Philadelphia, PA')
group by
	AC.airline_code ,
	AC.airline_name
having
	count(distinct FR.dest_city_name)= 5
except
select
	AC.airline_name
from
	airline_codes ac ,
	flight_reports fr
where
	ac.airline_code = fr.airline_code
	and fr.is_cancelled = 0
	and (fr."year" = 2016
	or fr."year" = 2017)
	and (fr.dest_city_name = 'Boston, MA'
	or fr.dest_city_name = 'New York, NY'
	or fr.dest_city_name = 'Portland, ME'
	or fr.dest_city_name = 'Washington, DC'
	or fr.dest_city_name = 'Philadelphia, PA')
group by
	AC.airline_code ,
	AC.airline_name
having
	count(distinct FR.dest_city_name)= 5
order by
	1
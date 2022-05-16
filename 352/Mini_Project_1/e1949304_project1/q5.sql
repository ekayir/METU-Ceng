select
	case
		when length( cast (fr2."day" as varchar)) = 1 then '0' || cast (fr2."day" as varchar)
		else cast (fr2."day" as varchar) end || '/' ||
		case
			when length( cast (fr2."month" as varchar)) = 1 then '0' || cast (fr2."month" as varchar)
			else cast (fr2."month" as varchar) end || '/' || cast (fr2."year" as varchar) as flight_date,
			fr2.plane_tail_number ,
			tab.arrival_time as flight1_arrival_time,
			fr2.departure_time as flight2_departure_time,
			tab.origin_city_name,
			fr2.origin_city_name as stop_city_name,
			fr2.dest_city_name ,
			tab.flight_time + tab.taxi_out_time + fr2.taxi_in_time + fr2.flight_time as total_time,
			tab.flight_distance + fr2.flight_distance as total_distance
		from
			flight_reports fr2,
			(
			select
				*
			from
				flight_reports fr
			where
				fr.is_cancelled = 0
				and fr.origin_city_name = 'Seattle, WA'
				and fr.dest_city_name <> 'Boston, MA')tab
		where
			fr2.plane_tail_number = tab.plane_tail_number
			and fr2.origin_airport_code = tab.dest_airport_code
			and fr2.origin_city_name = tab.dest_city_name
			and fr2.dest_city_name = 'Boston, MA'
			and fr2.is_cancelled = 0
			and tab."day" = fr2."day"
			and fr2."year" = tab.year
			and fr2."month" = tab.month
			and tab.arrival_time < fr2.departure_time
		order by
			total_time,
			total_distance ,
			plane_tail_number ,
			stop_city_name
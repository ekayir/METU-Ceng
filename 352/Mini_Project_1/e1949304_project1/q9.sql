select
	fr.plane_tail_number,
	avg(fr.flight_distance / fr.flight_time) as avg_speed
from
	flight_reports fr
where
	fr."month" = 1
	and fr."year" = 2016
	and fr.weekday_id > 5
	and fr.weekday_id < 8
	and fr.is_cancelled = 0
	and not exists (
	select
		1
	from
		flight_reports fr2
	where
		fr2."month" = 1
		and fr2."year" = 2016
		and fr2.weekday_id < 6
		and fr2.is_cancelled = 0
		and fr2.plane_tail_number = fr.plane_tail_number )
group by
	fr.plane_tail_number
order by
	avg_speed desc
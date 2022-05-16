select
	AA.year,
	AA.weekday_name,
	(
	select
		cr.reason_desc
	from
		cancellation_reasons cr
	where
		cr.reason_code = AA.cancellation_reason) as reason,
	AA.count1 as number_of_cancellations
from
	(
	select
		"year",
		w.weekday_name ,
		fr.cancellation_reason ,
		count(1) as count1,
		w.weekday_id
	from
		flight_reports fr ,
		weekdays w
	where
		fr.is_cancelled = 1
		and w.weekday_id = fr.weekday_id
	group by
		"year" ,
		fr.cancellation_reason ,
		w.weekday_name,
		w.weekday_id ) AA,
	(
	select
		max(CC.count1)as count1,
		CC.year,
		CC.weekday_name,CC.weekday_id
	from
		(
		select
			"year",
			w.weekday_name ,
			fr.cancellation_reason ,
			count(1) as count1,
			w.weekday_id
		from
			flight_reports fr ,
			weekdays w
		where
			fr.is_cancelled = 1
			and w.weekday_id = fr.weekday_id
		group by
			"year" ,
			fr.cancellation_reason ,
			w.weekday_name,w.weekday_id )CC
	group by
		CC.year,
		CC.weekday_name,
		cc.weekday_id ) BB
where
	BB.year = AA.year
	and BB.weekday_name = AA.weekday_name
	and AA.count1 = BB.count1
order by
	year,aa.weekday_id
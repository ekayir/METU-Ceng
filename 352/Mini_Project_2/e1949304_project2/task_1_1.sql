select
	p.pub_type as publication_type,
	count(1) as total_number_of_publication
from
	pub p
group by
	p.pub_type
order by
	2 desc;
	

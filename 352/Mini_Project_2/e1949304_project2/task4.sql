CREATE TABLE public.activeauthors (
	"name" text PRIMARY KEY
);

insert into activeauthors(
select distinct a."name" from author a , "publication" p, authored a2 
where a2.author_id = a.author_id  and a2.pub_id  = p.pub_id 
and p."year" between 2018 and 2020
);


CREATE OR REPLACE FUNCTION public.trig_func()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$ 
begin IF 
      ( 
      SELECT Count(1) 
      FROM   "publication" p 
      WHERE  p.pub_id = new.pub_id 
      AND    p."year" BETWEEN 2018 AND    2020) = 1 
  AND 
  ( 
         SELECT Count(1) 
         FROM   author a 
         WHERE  a.author_id = new.author_id 
         AND    NOT EXISTS 
                ( 
                       SELECT 1 
                       FROM   activeauthors a2 
                       WHERE  a2."name" = a."name" )) = 1 then 
  INSERT INTO activeauthors 
              ( 
                     SELECT a."name" 
                     FROM   author a 
                     WHERE  a.author_id = new.author_id 
              );end IF;RETURN new;END;$function$
;




create trigger trig after
insert
    on
    public.authored for each row execute function trig_func();

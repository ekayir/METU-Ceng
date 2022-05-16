CREATE INDEX field_field_name_pub_key_idx ON public.field (field_name,pub_key);


cluster field using field_field_name_pub_key_idx;


CREATE INDEX pub_pub_key_index ON public.pub (pub_key);



cluster pub using pub_pub_key_index;
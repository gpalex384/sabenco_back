CREATE DEFINER=`ejemplo`@`localhost` TRIGGER publish_aft_trg
BEFORE UPDATE
ON eventdraft FOR EACH row
BEGIN
	if (
		old.published != new.published 
		and new.published = 1
		and (select event_id from eventdraft where id = new.id) is null 
	) then 
		insert into event (title, detail, createdby, updatedby) values (new.title, new.detail, new.createdby, new.updatedby);
		set new.event_id = (select id from event where title = new.title and detail = new.detail order by created desc limit 1);
	elseif (
		old.published != new.published 
		and new.published = 1
		and (select event_id from eventdraft where id = new.id) is not null 
	) then 
		update event set title = new.title, detail = new.detail, updated = current_timestamp, updatedby = new.createdby
		where id = new.event_id;
	end if;
end$
CREATE DEFINER=`ejemplo`@`localhost` TRIGGER category_bef_trg
BEFORE INSERT
ON event FOR EACH row
set new.category_id = (select id from category where name = 'myself')
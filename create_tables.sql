create table if not exists orders_status (
	order_id uuid primary key,
    creation_date timestamp default now(),
    order_status varchar(30) not null
);

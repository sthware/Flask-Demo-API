drop table if exists games;
drop table if exists categories;
create table games (
    id serial primary key,
    name varchar(256) not null,
    description varchar(2048),
    pub_date timestamptz not null default now()
);

create table categories (
    id serial primary key,
    name varchar(64) not null,
    nickname varchar(32),
    description varchar(256)
);

create table games_categories (
    game_id integer references games(id),
    category_id integer references categories(id),
    category_priority smallint,
    primary key(game_id, category_id)
);

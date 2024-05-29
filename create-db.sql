create table if not exists bills
(
    biennium           varchar(255)                                              not null,
    bill_id            varchar(255)                                              not null,
    bill_number        smallint unsigned                                         null,
    substitute_version tinyint unsigned                                          null,
    engrossed_version  tinyint unsigned                                          null,
    original_agency    varchar(255)                                              null,
    active             boolean                                                   null,
    fiscal_notes       set('State', 'Local')                                     null,
    appropriations     boolean                                                   null,
    requested_by       set('Governor', 'BudgetCommittee', 'Department', 'Other') null,
    short_description  varchar(255)                                              null,
    request            varchar(255)                                              null,
    introduced_date    timestamp                                                 null,
    sponsor_id         mediumint unsigned                                        null,
    long_description   varchar(255)                                              null,
    legal_title        varchar(255)                                              null,
    companion_bill     varchar(255)                                              null,
    last_updated       timestamp default CURRENT_TIMESTAMP                       not null,
    primary key (biennium, bill_id)
);

create table if not exists status
(
    biennium                 varchar(255)                        not null,
    bill_id                  varchar(255)                        not null,
    history_line             varchar(255)                        null,
    action_date              timestamp                           not null,
    amended_by_opposite_body boolean                             null,
    vetoed                   set('true', 'partial', 'false')     null,
    amendments_exist         boolean                             null,
    status                   varchar(255)                        null,
    last_updated             timestamp default CURRENT_TIMESTAMP not null,
    primary key (biennium, bill_id, action_date),
    foreign key (biennium, bill_id) references bills(biennium, bill_id)
);

create table if not exists sponsors
(
    biennium     varchar(255)                        not null,
    id           mediumint unsigned                  not null,
    long_name    varchar(255)                        null,
    agency       varchar(255)                        null,
    acronym      varchar(255)                        null,
    party        varchar(255)                        null,
    district     varchar(255)                        null,
    phone        varchar(255)                        null,
    email        varchar(255)                        null,
    first_name   varchar(255)                        null,
    last_name    varchar(255)                        null,
    last_updated timestamp default CURRENT_TIMESTAMP not null,
    primary key (biennium, id)
);

create table if not exists lists
(
    id     uuid default uuid() not null
        primary key,
    color  tinyint             null,
    author int(11)             not null,
    name   varchar(255)        not null,
    foreign key (author) references auth_user (id)
        on delete cascade
);

create table if not exists marks
(
    list uuid             not null,
    biennium varchar(255) not null,
    bill_id  varchar(255) not null,
    foreign key (biennium, bill_id) references bills(biennium, bill_id)
        on delete cascade,
    foreign key (list) references lists(id)
        on delete cascade
);

create table if not exists notes
(
    id            uuid default uuid()                   not null
        primary key,
    content       text                                  null,
    author        int(11)                               not null,
    creation_time timestamp default current_timestamp() not null,
    edit_time     timestamp default current_timestamp() not null on update current_timestamp(),
    biennium      varchar(255)                          not null,
    bill_id       varchar(255)                          not null,
    foreign key (author) references auth_user (id)
        on delete cascade,
    foreign key (biennium, bill_id) references bills(biennium, bill_id)
        on delete cascade
);

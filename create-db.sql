create table if not exists bills
(
    biennium           varchar(255)                                              not null,
    bill_id            varchar(255)                                              not null,
    bill_number        smallint unsigned                                         not null,
    substitute_version tinyint unsigned                                          not null,
    engrossed_version  tinyint unsigned                                          not null,
    original_agency    varchar(255)                                              not null,
    active             boolean                                                   not null,
    companion_bill     varchar(255)                                              null,
    fiscal_notes       set('State', 'Local')                                     null,
    requested_by       set('Governor', 'BudgetCommittee', 'Department', 'Other') null,
    first_accessed     timestamp default CURRENT_TIMESTAMP                       not null,
    last_accessed      timestamp default CURRENT_TIMESTAMP                       not null,
    last_updated       timestamp default CURRENT_TIMESTAMP                       not null,
    appropriations     boolean                                                   not null,
    short_description  varchar(255)                                              not null,
    request            varchar(255)                                              not null,
    introduced_date    timestamp                                                 not null,
    sponsor            varchar(255)                                              not null,
    sponsor_id         smallint unsigned                                         not null,
    long_description   varchar(255)                                              not null,
    legal_title        varchar(255)                                              not null,
    primary key (biennium, bill_id)
);

create table if not exists status
(
    biennium                 varchar(255)                        not null,
    bill_id                  varchar(255)                        not null,
    history_line             varchar(255)                        not null,
    action_date              timestamp                           not null,
    retrieved                timestamp default CURRENT_TIMESTAMP not null,
    amended_by_opposite_body boolean                             not null,
    vetoed                   set('true', 'partial', 'false')     not null,
    amendments_exist         boolean                             not null,
    status                   varchar(255)                        not null,
    foreign key (biennium, bill_id) references bills(biennium, bill_id)
);

create table if not exists sponsors
(
    biennium   varchar(255) not null,
    party      varchar(255) not null,
    district   varchar(255) not null,
    phone      varchar(255) not null,
    email      varchar(255) not null,
    first_name varchar(255) not null,
    last_name  varchar(255) not null,
    primary key (biennium, email),
    index (biennium, last_name)
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
    foreign key (biennium, bill_id) references bills(biennium, bill_id),
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
);

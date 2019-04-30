create table if not exists `user` (
  `id`      INT UNSIGNED                 AUTO_INCREMENT,
  `name`    VARCHAR(128),
  `count`   VARCHAR(256)        NOT NULL
  COMMENT '登录账户',
  `email`   VARCHAR(128),
  `user_id` BIGINT(20) unsigned NOT NULL DEFAULT '0'
  COMMENT '用户id',
  primary key (`id`),
  unique (`user_id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci
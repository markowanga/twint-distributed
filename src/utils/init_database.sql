CREATE DATABASE twint_distributed_tasks;
USE twint_distributed_tasks;


CREATE TABLE ScrapSession
(
    scrap_session_id   VARCHAR(50)  NOT NULL PRIMARY KEY,
    scrap_session_name VARCHAR(512) NOT NULL
);


CREATE TABLE UserTweetScrapTasks
(
    task_id          VARCHAR(50)  NOT NULL PRIMARY KEY,
    username         VARCHAR(200) NOT NULL,
    since            DATETIME     NOT NULL,
    until            DATETIME     NOT NULL,
    created          DATETIME     NOT NULL,
    finished         DATETIME,
    scrap_session_id VARCHAR(50)  NOT NULL,
    queue_name       VARCHAR(512) NOT NULL,
    CONSTRAINT UserTweetScrapTasks_fk_scrap_session_id
        FOREIGN KEY (scrap_session_id) REFERENCES ScrapSession (scrap_session_id)
);

CREATE TABLE UserTweetScrapSubTasks
(
    sub_task_id VARCHAR(50) NOT NULL PRIMARY KEY,
    task_id     VARCHAR(50) NOT NULL,
    since       DATETIME    NOT NULL,
    until       DATETIME    NOT NULL,
    created     DATETIME    NOT NULL,
    finished    DATETIME,
    CONSTRAINT UserTweetScrapSubTasks_fk_task_id
        FOREIGN KEY (task_id) REFERENCES UserTweetScrapTasks (task_id)
);

CREATE TABLE UserDetailsScrapTasks
(
    task_id          VARCHAR(50)  NOT NULL PRIMARY KEY,
    username         VARCHAR(200) NOT NULL,
    created          DATETIME     NOT NULL,
    finished         DATETIME,
    scrap_session_id VARCHAR(50)  NOT NULL,
    queue_name       VARCHAR(512) NOT NULL,
    CONSTRAINT UserDetailsScrapTasks_fk_scrap_session_id
        FOREIGN KEY (scrap_session_id) REFERENCES ScrapSession (scrap_session_id)
);

CREATE TABLE UserFollowersScrapTasks
(
    task_id          VARCHAR(50)  NOT NULL PRIMARY KEY,
    username         VARCHAR(200) NOT NULL,
    created          DATETIME     NOT NULL,
    finished         DATETIME,
    scrap_session_id VARCHAR(50)  NOT NULL,
    queue_name       VARCHAR(512) NOT NULL,
    CONSTRAINT UserFollowersScrapTasks_fk_scrap_session_id
        FOREIGN KEY (scrap_session_id) REFERENCES ScrapSession (scrap_session_id)
);

CREATE TABLE UserFollowingScrapTasks
(
    task_id          VARCHAR(50)  NOT NULL PRIMARY KEY,
    username         VARCHAR(200) NOT NULL,
    created          DATETIME     NOT NULL,
    finished         DATETIME,
    scrap_session_id VARCHAR(50)  NOT NULL,
    queue_name       VARCHAR(512) NOT NULL,
    CONSTRAINT UserFollowingScrapTasks_fk_scrap_session_id
        FOREIGN KEY (scrap_session_id) REFERENCES ScrapSession (scrap_session_id)
);

CREATE TABLE UserFavoritesScrapTasks
(
    task_id          VARCHAR(50)  NOT NULL PRIMARY KEY,
    username         VARCHAR(200) NOT NULL,
    created          DATETIME     NOT NULL,
    finished         DATETIME,
    scrap_session_id VARCHAR(50)  NOT NULL,
    queue_name       VARCHAR(512) NOT NULL,
    CONSTRAINT UserFavoritesScrapTasks_fk_scrap_session_id
        FOREIGN KEY (scrap_session_id) REFERENCES ScrapSession (scrap_session_id)
);

CREATE TABLE SearchTweetScrapTasks
(
    task_id          VARCHAR(50)  NOT NULL PRIMARY KEY,
    phrase           VARCHAR(200) NOT NULL,
    since            DATETIME     NOT NULL,
    until            DATETIME     NOT NULL,
    language         VARCHAR(10),
    created          DATETIME     NOT NULL,
    finished         DATETIME,
    scrap_session_id VARCHAR(50)  NOT NULL,
    queue_name       VARCHAR(512) NOT NULL,
    CONSTRAINT SearchTweetScrapTasks_fk_scrap_session_id
        FOREIGN KEY (scrap_session_id) REFERENCES ScrapSession (scrap_session_id)
);

CREATE TABLE SearchTweetScrapSubTasks
(
    sub_task_id VARCHAR(50) NOT NULL PRIMARY KEY,
    task_id     VARCHAR(50) NOT NULL,
    since       DATETIME    NOT NULL,
    until       DATETIME    NOT NULL,
    created     DATETIME    NOT NULL,
    finished    DATETIME,
    CONSTRAINT SearchTweetScrapSubTasks_fk_task_id
        FOREIGN KEY (task_id) REFERENCES SearchTweetScrapTasks (task_id)
);

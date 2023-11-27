-- Database: musicbox

-- DROP DATABASE IF EXISTS musicbox;

CREATE DATABASE musicbox
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;


DROP TABLE IF EXISTS public.answers;
DROP TABLE IF EXISTS public.players;
DROP TABLE IF EXISTS public.games;



CREATE TABLE IF NOT EXISTS public.games
(
    id numeric NOT NULL,
    session_date date NOT NULL,
    CONSTRAINT games_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.games
    OWNER to postgres;


CREATE TABLE IF NOT EXISTS public.players
(
    id numeric NOT NULL,
    username text COLLATE pg_catalog."default" NOT NULL,
    game numeric NOT NULL,
    CONSTRAINT prim PRIMARY KEY (id),
    CONSTRAINT players_game_fkey FOREIGN KEY (game)
        REFERENCES public.games (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.players
    OWNER to postgres;


CREATE TABLE IF NOT EXISTS public.answers
(
    id numeric NOT NULL,
    answer text COLLATE pg_catalog."default" NOT NULL,
    round numeric NOT NULL DEFAULT 0,
    score numeric NOT NULL DEFAULT 0,
    player numeric NOT NULL,
    CONSTRAINT answers_pkey PRIMARY KEY (id),
    CONSTRAINT answers_player_fkey FOREIGN KEY (player)
        REFERENCES public.players (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.answers
    OWNER to postgres;
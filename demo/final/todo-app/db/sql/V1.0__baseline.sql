CREATE TABLE IF NOT EXISTS public."Todo"
(
    "Id" integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    "Title" character varying(500) COLLATE pg_catalog."default" NOT NULL,
    "Completed" boolean NOT NULL DEFAULT 'false',
    "DueDate" date,
    CONSTRAINT "Todo_pkey" PRIMARY KEY ("Id")
)
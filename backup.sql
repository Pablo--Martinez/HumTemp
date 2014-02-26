--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

DROP TABLE control;
DROP TABLE registro;
DROP TABLE sesion;

--
-- Name: control; Type: TABLE; Schema: public; Owner: pi; Tablespace: 
--

CREATE TABLE control (
    "ID" integer NOT NULL,
    "ID_SESION" integer,
    "ESTADO" integer
);


ALTER TABLE public.control OWNER TO pi;

--
-- Name: control_ID_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

CREATE SEQUENCE "control_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."control_ID_seq" OWNER TO pi;

--
-- Name: control_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi
--

ALTER SEQUENCE "control_ID_seq" OWNED BY control."ID";


--
-- Name: registro; Type: TABLE; Schema: public; Owner: pi; Tablespace: 
--

CREATE TABLE registro (
    "ID" integer NOT NULL,
    "ID_SESION" integer,
    "TIPO" character(1),
    "SENSOR" integer,
    "TEMP" double precision,
    "HUM" double precision,
    "FECHA" timestamp without time zone
);


ALTER TABLE public.registro OWNER TO pi;

--
-- Name: registro_ID_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

CREATE SEQUENCE "registro_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."registro_ID_seq" OWNER TO pi;

--
-- Name: registro_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi
--

ALTER SEQUENCE "registro_ID_seq" OWNED BY registro."ID";


--
-- Name: sesion; Type: TABLE; Schema: public; Owner: pi; Tablespace: 
--

CREATE TABLE sesion (
    "ID" integer NOT NULL,
    "NOMBRE" character varying(50),
    "CICLO" integer,
    "CONT" integer,
    "GPIO" integer[],
    "ONEWIRE" integer,
    "INICIO" timestamp without time zone,
    "FIN" timestamp without time zone
);


ALTER TABLE public.sesion OWNER TO pi;

--
-- Name: sesion_ID_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

CREATE SEQUENCE "sesion_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."sesion_ID_seq" OWNER TO pi;

--
-- Name: sesion_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi
--

ALTER SEQUENCE "sesion_ID_seq" OWNED BY sesion."ID";


--
-- Name: ID; Type: DEFAULT; Schema: public; Owner: pi
--

ALTER TABLE ONLY control ALTER COLUMN "ID" SET DEFAULT nextval('"control_ID_seq"'::regclass);


--
-- Name: ID; Type: DEFAULT; Schema: public; Owner: pi
--

ALTER TABLE ONLY registro ALTER COLUMN "ID" SET DEFAULT nextval('"registro_ID_seq"'::regclass);


--
-- Name: ID; Type: DEFAULT; Schema: public; Owner: pi
--

ALTER TABLE ONLY sesion ALTER COLUMN "ID" SET DEFAULT nextval('"sesion_ID_seq"'::regclass);


--
-- Data for Name: control; Type: TABLE DATA; Schema: public; Owner: pi
--

COPY control ("ID", "ID_SESION", "ESTADO") FROM stdin;
1	\N	0
\.


--
-- Name: control_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: pi
--

SELECT pg_catalog.setval('"control_ID_seq"', 2, true);


--
-- Data for Name: registro; Type: TABLE DATA; Schema: public; Owner: pi
--

COPY registro ("ID", "ID_SESION", "TIPO", "SENSOR", "TEMP", "HUM", "FECHA") FROM stdin;
\.


--
-- Name: registro_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: pi
--

SELECT pg_catalog.setval('"registro_ID_seq"', 1, false);


--
-- Data for Name: sesion; Type: TABLE DATA; Schema: public; Owner: pi
--

COPY sesion ("ID", "NOMBRE", "CICLO", "CONT", "GPIO", "ONEWIRE", "INICIO", "FIN") FROM stdin;
\.


--
-- Name: sesion_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: pi
--

SELECT pg_catalog.setval('"sesion_ID_seq"', 1, true);


--
-- Name: control_pkey; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY control
    ADD CONSTRAINT control_pkey PRIMARY KEY ("ID");


--
-- Name: registro_pkey; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY registro
    ADD CONSTRAINT registro_pkey PRIMARY KEY ("ID");


--
-- Name: sesion_pkey; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY sesion
    ADD CONSTRAINT sesion_pkey PRIMARY KEY ("ID");


--
-- Name: control_ID_SESION_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY control
    ADD CONSTRAINT "control_ID_SESION_fkey" FOREIGN KEY ("ID_SESION") REFERENCES sesion("ID");


--
-- Name: registro_ID_SESION_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY registro
    ADD CONSTRAINT "registro_ID_SESION_fkey" FOREIGN KEY ("ID_SESION") REFERENCES sesion("ID");


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- Name: control; Type: ACL; Schema: public; Owner: pi
--

REVOKE ALL ON TABLE control FROM PUBLIC;
REVOKE ALL ON TABLE control FROM pi;
GRANT ALL ON TABLE control TO pi;
GRANT ALL ON TABLE control TO root;


--
-- Name: registro; Type: ACL; Schema: public; Owner: pi
--

REVOKE ALL ON TABLE registro FROM PUBLIC;
REVOKE ALL ON TABLE registro FROM pi;
GRANT ALL ON TABLE registro TO pi;
GRANT ALL ON TABLE registro TO root;


--
-- Name: sesion; Type: ACL; Schema: public; Owner: pi
--

REVOKE ALL ON TABLE sesion FROM PUBLIC;
REVOKE ALL ON TABLE sesion FROM pi;
GRANT ALL ON TABLE sesion TO pi;
GRANT ALL ON TABLE sesion TO root;


--
-- PostgreSQL database dump complete
--


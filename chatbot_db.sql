--
-- PostgreSQL database dump
--

-- Dumped from database version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: chatbot_knowledge_base; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.chatbot_knowledge_base (
    id integer NOT NULL,
    question text NOT NULL,
    answer text NOT NULL
);


--
-- Name: chatbot_knowledge_base_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.chatbot_knowledge_base_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: chatbot_knowledge_base_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.chatbot_knowledge_base_id_seq OWNED BY public.chatbot_knowledge_base.id;


--
-- Name: chatbot_knowledge_base id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chatbot_knowledge_base ALTER COLUMN id SET DEFAULT nextval('public.chatbot_knowledge_base_id_seq'::regclass);


--
-- Data for Name: chatbot_knowledge_base; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.chatbot_knowledge_base (id, question, answer) FROM stdin;
1	olá, como você está?	eu estou bem! obrigado por perguntar!
2	tudo bem com você?	está tudo bem sim, e com você?
3	tudo bem, e com você?	eu estou ótimo! obrigado por perguntar!
4	gostaria de alugar um imóvel?	para alugar um imóvel, preciso que informe o seu nome completo e o número do seu cpf
5	como faço para sair?	para sair, digite tchau! :)
\.


--
-- Name: chatbot_knowledge_base_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.chatbot_knowledge_base_id_seq', 5, true);


--
-- Name: chatbot_knowledge_base chatbot_knowledge_base_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chatbot_knowledge_base
    ADD CONSTRAINT chatbot_knowledge_base_pkey PRIMARY KEY (id);


--
-- Name: chatbot_knowledge_base chatbot_knowledge_base_question_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chatbot_knowledge_base
    ADD CONSTRAINT chatbot_knowledge_base_question_key UNIQUE (question);


--
-- PostgreSQL database dump complete
--


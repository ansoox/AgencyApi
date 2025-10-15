--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.2

-- Started on 2025-10-15 22:33:01

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 6 (class 2615 OID 16473)
-- Name: agency; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA agency;


ALTER SCHEMA agency OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 229 (class 1259 OID 16755)
-- Name: artist; Type: TABLE; Schema: agency; Owner: postgres
--

CREATE TABLE agency.artist (
    id integer NOT NULL,
    full_name character varying(255) NOT NULL,
    genre character varying(100) NOT NULL,
    organizer_id integer,
    phone_number character varying(20),
    work_experience integer,
    CONSTRAINT artist_work_experience_check CHECK ((work_experience >= 0))
);


ALTER TABLE agency.artist OWNER TO postgres;

--
-- TOC entry 4916 (class 0 OID 0)
-- Dependencies: 229
-- Name: TABLE artist; Type: COMMENT; Schema: agency; Owner: postgres
--

COMMENT ON TABLE agency.artist IS 'Table with artist information';


--
-- TOC entry 228 (class 1259 OID 16754)
-- Name: artist_id_seq; Type: SEQUENCE; Schema: agency; Owner: postgres
--

CREATE SEQUENCE agency.artist_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE agency.artist_id_seq OWNER TO postgres;

--
-- TOC entry 4917 (class 0 OID 0)
-- Dependencies: 228
-- Name: artist_id_seq; Type: SEQUENCE OWNED BY; Schema: agency; Owner: postgres
--

ALTER SEQUENCE agency.artist_id_seq OWNED BY agency.artist.id;


--
-- TOC entry 232 (class 1259 OID 16774)
-- Name: artist_performance; Type: TABLE; Schema: agency; Owner: postgres
--

CREATE TABLE agency.artist_performance (
    artist_id integer NOT NULL,
    performance_id integer NOT NULL
);


ALTER TABLE agency.artist_performance OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16696)
-- Name: client; Type: TABLE; Schema: agency; Owner: postgres
--

CREATE TABLE agency.client (
    id integer NOT NULL,
    full_name character varying(255) NOT NULL,
    phone character varying(20) NOT NULL,
    email character varying(100) NOT NULL,
    age integer,
    organizer_id integer,
    CONSTRAINT client_age_check CHECK ((age >= 0))
);


ALTER TABLE agency.client OWNER TO postgres;

--
-- TOC entry 4918 (class 0 OID 0)
-- Dependencies: 221
-- Name: TABLE client; Type: COMMENT; Schema: agency; Owner: postgres
--

COMMENT ON TABLE agency.client IS 'Table with client data';


--
-- TOC entry 220 (class 1259 OID 16695)
-- Name: client_id_seq; Type: SEQUENCE; Schema: agency; Owner: postgres
--

CREATE SEQUENCE agency.client_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE agency.client_id_seq OWNER TO postgres;

--
-- TOC entry 4919 (class 0 OID 0)
-- Dependencies: 220
-- Name: client_id_seq; Type: SEQUENCE OWNED BY; Schema: agency; Owner: postgres
--

ALTER SEQUENCE agency.client_id_seq OWNED BY agency.client.id;


--
-- TOC entry 225 (class 1259 OID 16723)
-- Name: concert_program; Type: TABLE; Schema: agency; Owner: postgres
--

CREATE TABLE agency.concert_program (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    date date NOT NULL,
    venue_id integer,
    duration integer NOT NULL,
    address character varying(100),
    number_of_performances integer NOT NULL,
    "time" character varying(20)
);


ALTER TABLE agency.concert_program OWNER TO postgres;

--
-- TOC entry 4920 (class 0 OID 0)
-- Dependencies: 225
-- Name: TABLE concert_program; Type: COMMENT; Schema: agency; Owner: postgres
--

COMMENT ON TABLE agency.concert_program IS 'Table with concert program data';


--
-- TOC entry 224 (class 1259 OID 16722)
-- Name: concert_program_id_seq; Type: SEQUENCE; Schema: agency; Owner: postgres
--

CREATE SEQUENCE agency.concert_program_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE agency.concert_program_id_seq OWNER TO postgres;

--
-- TOC entry 4921 (class 0 OID 0)
-- Dependencies: 224
-- Name: concert_program_id_seq; Type: SEQUENCE OWNED BY; Schema: agency; Owner: postgres
--

ALTER SEQUENCE agency.concert_program_id_seq OWNED BY agency.concert_program.id;


--
-- TOC entry 219 (class 1259 OID 16686)
-- Name: organizer; Type: TABLE; Schema: agency; Owner: postgres
--

CREATE TABLE agency.organizer (
    id integer NOT NULL,
    full_name character varying(255) NOT NULL,
    phone character varying(20) NOT NULL,
    "position" character varying(100) NOT NULL,
    work_experience integer,
    CONSTRAINT organizer_work_experience_check CHECK ((work_experience >= 0))
);


ALTER TABLE agency.organizer OWNER TO postgres;

--
-- TOC entry 4922 (class 0 OID 0)
-- Dependencies: 219
-- Name: TABLE organizer; Type: COMMENT; Schema: agency; Owner: postgres
--

COMMENT ON TABLE agency.organizer IS 'Table with organizer data';


--
-- TOC entry 234 (class 1259 OID 16804)
-- Name: organizer_concert_program; Type: TABLE; Schema: agency; Owner: postgres
--

CREATE TABLE agency.organizer_concert_program (
    organizer_id integer NOT NULL,
    concert_program_id integer NOT NULL
);


ALTER TABLE agency.organizer_concert_program OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 16685)
-- Name: organizer_id_seq; Type: SEQUENCE; Schema: agency; Owner: postgres
--

CREATE SEQUENCE agency.organizer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE agency.organizer_id_seq OWNER TO postgres;

--
-- TOC entry 4923 (class 0 OID 0)
-- Dependencies: 218
-- Name: organizer_id_seq; Type: SEQUENCE OWNED BY; Schema: agency; Owner: postgres
--

ALTER SEQUENCE agency.organizer_id_seq OWNED BY agency.organizer.id;


--
-- TOC entry 231 (class 1259 OID 16767)
-- Name: performance; Type: TABLE; Schema: agency; Owner: postgres
--

CREATE TABLE agency.performance (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    duration integer,
    genre character varying(100) NOT NULL,
    number_of_artists integer NOT NULL,
    CONSTRAINT performance_duration_check CHECK ((duration > 0))
);


ALTER TABLE agency.performance OWNER TO postgres;

--
-- TOC entry 4924 (class 0 OID 0)
-- Dependencies: 231
-- Name: TABLE performance; Type: COMMENT; Schema: agency; Owner: postgres
--

COMMENT ON TABLE agency.performance IS 'Table with concert performances';


--
-- TOC entry 233 (class 1259 OID 16789)
-- Name: performance_concert_program; Type: TABLE; Schema: agency; Owner: postgres
--

CREATE TABLE agency.performance_concert_program (
    performance_id integer NOT NULL,
    concert_program_id integer NOT NULL
);


ALTER TABLE agency.performance_concert_program OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 16766)
-- Name: performance_id_seq; Type: SEQUENCE; Schema: agency; Owner: postgres
--

CREATE SEQUENCE agency.performance_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE agency.performance_id_seq OWNER TO postgres;

--
-- TOC entry 4925 (class 0 OID 0)
-- Dependencies: 230
-- Name: performance_id_seq; Type: SEQUENCE OWNED BY; Schema: agency; Owner: postgres
--

ALTER SEQUENCE agency.performance_id_seq OWNED BY agency.performance.id;


--
-- TOC entry 237 (class 1259 OID 16876)
-- Name: test; Type: TABLE; Schema: agency; Owner: postgres
--

CREATE TABLE agency.test (
    id integer NOT NULL,
    a integer,
    b text
);


ALTER TABLE agency.test OWNER TO postgres;

--
-- TOC entry 236 (class 1259 OID 16875)
-- Name: test_id_seq; Type: SEQUENCE; Schema: agency; Owner: postgres
--

CREATE SEQUENCE agency.test_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE agency.test_id_seq OWNER TO postgres;

--
-- TOC entry 4926 (class 0 OID 0)
-- Dependencies: 236
-- Name: test_id_seq; Type: SEQUENCE OWNED BY; Schema: agency; Owner: postgres
--

ALTER SEQUENCE agency.test_id_seq OWNED BY agency.test.id;


--
-- TOC entry 227 (class 1259 OID 16735)
-- Name: ticket; Type: TABLE; Schema: agency; Owner: postgres
--

CREATE TABLE agency.ticket (
    id integer NOT NULL,
    ticket_number character varying(50) NOT NULL,
    price integer NOT NULL,
    client_id integer,
    concert_program_id integer,
    place character varying(50),
    address character varying(100),
    date date NOT NULL,
    "time" character varying(20),
    CONSTRAINT ticket_price_check CHECK ((price >= 0))
);


ALTER TABLE agency.ticket OWNER TO postgres;

--
-- TOC entry 4927 (class 0 OID 0)
-- Dependencies: 227
-- Name: TABLE ticket; Type: COMMENT; Schema: agency; Owner: postgres
--

COMMENT ON TABLE agency.ticket IS 'Table with concert tickets';


--
-- TOC entry 226 (class 1259 OID 16734)
-- Name: ticket_id_seq; Type: SEQUENCE; Schema: agency; Owner: postgres
--

CREATE SEQUENCE agency.ticket_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE agency.ticket_id_seq OWNER TO postgres;

--
-- TOC entry 4928 (class 0 OID 0)
-- Dependencies: 226
-- Name: ticket_id_seq; Type: SEQUENCE OWNED BY; Schema: agency; Owner: postgres
--

ALTER SEQUENCE agency.ticket_id_seq OWNED BY agency.ticket.id;


--
-- TOC entry 223 (class 1259 OID 16713)
-- Name: venue; Type: TABLE; Schema: agency; Owner: postgres
--

CREATE TABLE agency.venue (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    address character varying(255) NOT NULL,
    capacity integer,
    type character varying(50) NOT NULL,
    CONSTRAINT venue_capacity_check CHECK ((capacity > 0))
);


ALTER TABLE agency.venue OWNER TO postgres;

--
-- TOC entry 4929 (class 0 OID 0)
-- Dependencies: 223
-- Name: TABLE venue; Type: COMMENT; Schema: agency; Owner: postgres
--

COMMENT ON TABLE agency.venue IS 'Table with venue information';


--
-- TOC entry 222 (class 1259 OID 16712)
-- Name: venue_id_seq; Type: SEQUENCE; Schema: agency; Owner: postgres
--

CREATE SEQUENCE agency.venue_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE agency.venue_id_seq OWNER TO postgres;

--
-- TOC entry 4930 (class 0 OID 0)
-- Dependencies: 222
-- Name: venue_id_seq; Type: SEQUENCE OWNED BY; Schema: agency; Owner: postgres
--

ALTER SEQUENCE agency.venue_id_seq OWNED BY agency.venue.id;


--
-- TOC entry 4697 (class 2604 OID 16758)
-- Name: artist id; Type: DEFAULT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.artist ALTER COLUMN id SET DEFAULT nextval('agency.artist_id_seq'::regclass);


--
-- TOC entry 4693 (class 2604 OID 16699)
-- Name: client id; Type: DEFAULT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.client ALTER COLUMN id SET DEFAULT nextval('agency.client_id_seq'::regclass);


--
-- TOC entry 4695 (class 2604 OID 16726)
-- Name: concert_program id; Type: DEFAULT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.concert_program ALTER COLUMN id SET DEFAULT nextval('agency.concert_program_id_seq'::regclass);


--
-- TOC entry 4692 (class 2604 OID 16689)
-- Name: organizer id; Type: DEFAULT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.organizer ALTER COLUMN id SET DEFAULT nextval('agency.organizer_id_seq'::regclass);


--
-- TOC entry 4698 (class 2604 OID 16770)
-- Name: performance id; Type: DEFAULT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.performance ALTER COLUMN id SET DEFAULT nextval('agency.performance_id_seq'::regclass);


--
-- TOC entry 4699 (class 2604 OID 16879)
-- Name: test id; Type: DEFAULT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.test ALTER COLUMN id SET DEFAULT nextval('agency.test_id_seq'::regclass);


--
-- TOC entry 4696 (class 2604 OID 16738)
-- Name: ticket id; Type: DEFAULT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.ticket ALTER COLUMN id SET DEFAULT nextval('agency.ticket_id_seq'::regclass);


--
-- TOC entry 4694 (class 2604 OID 16716)
-- Name: venue id; Type: DEFAULT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.venue ALTER COLUMN id SET DEFAULT nextval('agency.venue_id_seq'::regclass);


--
-- TOC entry 4903 (class 0 OID 16755)
-- Dependencies: 229
-- Data for Name: artist; Type: TABLE DATA; Schema: agency; Owner: postgres
--

COPY agency.artist (id, full_name, genre, organizer_id, phone_number, work_experience) FROM stdin;
2	Мария Смирнова	Поп	152	+375292345678	3
4	Елена Сидорова	Классика	154	+375294567890	10
5	Иван Петров	Хип-хоп	155	+375295678901	2
6	Ольга Васильева	Рок	156	+375296789012	8
7	Сергей Кузнецов	Поп	156	+375297890123	6
8	Анна Новикова	Джаз	156	+375298901234	4
9	Павел Федоров	Классика	159	+375299012345	9
10	Наталья Орлова	Хип-хоп	160	+375291123456	5
11	Роман Тихонов	Рок	160	+375292234567	3
12	Екатерина Зайцева	Поп	160	+375293345678	7
13	Владимир Белов	Джаз	160	+375294456789	10
14	Александра Ковалева	Классика	160	+375295567890	2
15	Григорий Павлов	Хип-хоп	165	+375296678901	8
16	Виктория Мельникова	Рок	166	+375297789012	6
17	Максим Фролов	Поп	167	+375298890123	4
18	Татьяна Степанова	Джаз	168	+375299901234	9
19	Олег Данилов	Классика	169	+375291012345	5
20	Светлана Игнатова	Хип-хоп	170	+375292123456	3
21	Евгений Гусев	Рок	171	+375293234567	7
22	Алина Соколова	Поп	172	+375294345678	10
23	Артур Романов	Джаз	173	+375295456789	2
24	Полина Анисимова	Классика	174	+375296567890	8
25	Николай Лебедев	Хип-хоп	175	+375297678901	6
26	Жанна Егорова	Рок	176	+375298789012	4
28	Валентина Петрова	Джаз	178	+375291901234	5
29	Денис Сорокин	Классика	179	+375292012345	3
3	Дмитрий Козлов	Джаз	153	+375293456789	7
27	Игорь Вас	Поп	177	+375299890123	9
1	Алексей Иванов Иванович	Рок	151	+375291234567	5
\.


--
-- TOC entry 4906 (class 0 OID 16774)
-- Dependencies: 232
-- Data for Name: artist_performance; Type: TABLE DATA; Schema: agency; Owner: postgres
--

COPY agency.artist_performance (artist_id, performance_id) FROM stdin;
1	1
2	1
3	3
4	3
5	15
6	15
7	14
8	14
9	6
10	6
11	8
12	8
13	4
14	5
25	3
16	2
17	3
14	4
25	6
14	13
21	13
22	11
23	11
24	9
25	13
26	10
27	10
28	8
29	12
\.


--
-- TOC entry 4895 (class 0 OID 16696)
-- Dependencies: 221
-- Data for Name: client; Type: TABLE DATA; Schema: agency; Owner: postgres
--

COPY agency.client (id, full_name, phone, email, age, organizer_id) FROM stdin;
164	Болашенко Владимир	+375297777007	voV4ik@example.com	28	152
165	Бекетова Мария	+375298880088	masha@example.com	25	153
166	Борисенко Кирилл	+375299009999	sokolov@example.com	35	154
167	Бригадир Анна	+375291010101	orlova@example.com	40	155
168	Вадецкий Артем	+375291111111	petrov@example.com	32	151
169	Горох Андрей	+375292222222	smirnova@example.com	27	152
170	Кузнецов Евгений	+375293333333	kuznetsov@example.com	29	153
171	Ерофеев Виктор	+375294444444	popova@example.com	31	154
172	Зинович Иван	+375295555555	ivanovZ@example.com	33	155
173	Кисель Даниил	+375296666666	lebedeva@example.com	26	161
174	Копылова Екатерина	+375297777777	kiselev@example.com	34	162
175	Котик Алексей	+375298888888	tikhonova@example.com	24	163
176	Мухин Константин	+375299999999	pavlov@example.com	37	164
177	Паршуто Максим	+375292020202	golubeva@example.com	39	165
178	Потейчук Олег	+375292100212	vinogradov@example.com	36	161
179	Радкевич Никита	+375252002222	gromova@example.com	23	162
180	Тапальский Станислав	+375252300333	fedorov@example.com	38	163
181	Цвирко Егор	+375252004444	vasilieva_k@example.com	29	164
182	Мацур Иван	+375252555500	zaytsev@example.com	30	165
183	Дроздов Алексей	+375292666006	melnikova@example.com	27	171
184	Гончаренко Даниил	+375252777777	sidorov@example.com	35	172
185	Грибовская Александра	+375252888888	zakharova@example.com	26	173
186	Дроздов Алексей	+375252999999	efimov@example.com	31	174
187	Каплич Валерия	+375253030303	sergeeva@example.com	28	175
188	Копейкина Виктория	+375253131313	mironov@example.com	32	171
189	Коркотко Алексей	+375253232323	kovaleva@example.com	40	172
190	Кочан Максим	+375293366333	belov@example.com	39	173
191	Лазакович Владислав	+375293464343	grigorieva@example.com	25	174
192	Шершнева Елена	+375293536453	korolev@example.com	34	175
163	Бабкова Анна	+375293030300	babkova@creeper.com	30	151
\.


--
-- TOC entry 4899 (class 0 OID 16723)
-- Dependencies: 225
-- Data for Name: concert_program; Type: TABLE DATA; Schema: agency; Owner: postgres
--

COPY agency.concert_program (id, title, date, venue_id, duration, address, number_of_performances, "time") FROM stdin;
61	Рок-фестиваль	2025-06-15	91	120	Орловская 80	30	18:00
62	Джазовый вечер	2025-07-20	92	100	Минск, пр-т Партизанский, 8	25	12:00
63	Классическая музыка	2025-08-10	93	180	Минск, ул. Гикало, 5	50	20:00
64	Электронное шоу	2025-09-05	94	120	Минск, пр-т Победителей, 111	30	18:00
65	Поп-концерт	2025-10-12	95	180	Минск, пр-т Победителей, 111	50	20:00
66	Народная музыка	2025-06-25	96	180	Минск, пр-т Победителей, 111	100	18:00
67	Рэп-баттл	2025-07-10	97	100	Минск, пл. Свободы, 23А	25	12:00
68	Акустический вечер	2025-08-15	98	120	Орловская 80	30	18:00
69	Симфонический оркестр	2025-09-22	99	100	Минск, ул. Октябрьская, 16	25	12:00
70	Музыкальный марафон	2025-10-30	100	180	Минск, ул. Гикало, 5	50	20:00
71	Трибьют-концерт The Beatles	2025-11-05	101	100	Минск, пр-т Партизанский, 8	25	12:00
72	Фестиваль электронной музыки	2025-12-15	102	120	Орловская 80	30	18:00
73	Фолк-фестиваль	2026-01-20	103	120	Минск, ул. Ташкентская, 19	30	18:00
74	Панк-рок вечер	2026-02-10	104	180	Минск, Октябрьская площадь, 1	50	20:00
75	Ретро-дискотека 80-х	2026-03-05	105	100	Минск, пр-т Партизанский, 8	25	12:00
76	Метал-концерт	2026-04-12	106	180	Минск, ул. Маскарадная, 10	50	20:00
77	Инди-вечер	2026-05-18	107	120	Орловская 80	30	18:00
78	Танцевальное шоу	2026-06-25	108	100	Минск, ул. Ташкентская, 19	25	12:00
79	Концерт камерной музыки	2026-07-30	109	120	Минск, Октябрьская площадь, 1	30	18:00
80	Авторская песня	2026-08-22	110	100	Минск, пр-т Партизанский, 8	25	12:00
81	Гитарный фестиваль	2026-09-10	111	180	Минск, ул. Гикало, 5	50	20:00
82	Органный концерт	2026-10-05	112	100	Минск, пр-т Партизанский, 8	25	12:00
83	Джаз на крыше	2026-11-12	113	100	Минск, пр-т Победителей, 111	25	12:00
84	Хип-хоп концерт	2026-12-20	114	180	Минск, ул. Гикало, 5	50	12:00
85	Фестиваль классической гитары	2027-01-14	115	120	Орловская 80	30	18:00
86	Новогодний музыкальный бал	2027-02-10	116	100	Минск, ул. Октябрьская, 16	25	12:00
87	Музыкальный фестиваль Минска	2027-03-18	117	120	Орловская 80	30	18:00
88	Альтернативный рок-фестиваль	2027-04-22	118	100	Минск, пр-т Партизанский, 8	25	12:00
89	Фестиваль бардовской песни	2027-05-30	119	180	Минск, Октябрьская площадь, 1	50	20:00
90	Гала-концерт вокалистов	2027-06-15	120	120	Минск, ул. Маскарадная, 10	30	18:00
\.


--
-- TOC entry 4893 (class 0 OID 16686)
-- Dependencies: 219
-- Data for Name: organizer; Type: TABLE DATA; Schema: agency; Owner: postgres
--

COPY agency.organizer (id, full_name, phone, "position", work_experience) FROM stdin;
151	Иван Иванов	+375290011111	Менеджер	5
152	Петр Петров	+375290022222	Директор	10
153	Сергей Сергеев	+375290033333	Продюсер	7
154	Анна Смирнова	+375290044444	Координатор	4
155	Мария Козлова	+375290055555	Менеджер	6
156	Дмитрий Иванов	+375290066666	Координатор	8
157	Олег Сидоров	+375290077777	Директор	12
158	Екатерина Лебедева	+375290088888	Продюсер	9
159	Артем Васильев	+375290099999	Менеджер	7
160	Татьяна Ковалева	+375291010101	Координатор	6
161	Игорь Тихонов	+375291111111	Директор	15
162	Марина Федорова	+375291212121	Менеджер	5
163	Александр Егоров	+375291313131	Продюсер	10
164	Надежда Соловьева	+375291414141	Координатор	3
165	Максим Беляев	+375291515151	Директор	11
166	Ольга Миронова	+375291616161	Менеджер	4
167	Василий Громов	+375291717171	Продюсер	9
168	Елена Павлова	+375291818181	Координатор	5
169	Григорий Сафронов	+375291919191	Директор	14
170	Юлия Зайцева	+375292020202	Менеджер	6
171	Роман Карпов	+375292121212	Продюсер	7
172	Антон Васнецов	+375292222222	Координатор	4
173	Ксения Орлова	+375292323232	Директор	13
174	Светлана Богданова	+375292424242	Менеджер	5
175	Владимир Алексеев	+375292525252	Продюсер	8
176	Анастасия Крылова	+375292626262	Координатор	6
177	Сергей Токарев	+375292727272	Директор	10
178	Лариса Белкина	+375292828282	Менеджер	7
179	Павел Рябов	+375292929292	Продюсер	9
180	Дарья Фомина	+375293030303	Координатор	4
\.


--
-- TOC entry 4908 (class 0 OID 16804)
-- Dependencies: 234
-- Data for Name: organizer_concert_program; Type: TABLE DATA; Schema: agency; Owner: postgres
--

COPY agency.organizer_concert_program (organizer_id, concert_program_id) FROM stdin;
151	61
152	61
153	63
154	63
155	61
156	61
157	69
158	61
159	69
160	66
161	68
162	70
163	64
164	65
165	63
166	63
167	63
166	74
174	76
179	76
178	76
177	72
179	75
172	79
170	72
171	82
172	83
173	82
174	84
179	88
\.


--
-- TOC entry 4905 (class 0 OID 16767)
-- Dependencies: 231
-- Data for Name: performance; Type: TABLE DATA; Schema: agency; Owner: postgres
--

COPY agency.performance (id, title, duration, genre, number_of_artists) FROM stdin;
1	Гала-концерт рок-звезд	120	Рок	5
2	Поп-хиты 2024	90	Поп	3
3	Джазовый вечер	110	Джаз	4
4	Классическая симфония	150	Классика	6
5	Хип-хоп батл	80	Хип-хоп	2
6	Лучшее из Рока	130	Рок	5
7	Ночь Поп-музыки	100	Поп	3
8	Джаз в большом городе	120	Джаз	4
9	Оркестр мечты	160	Классика	7
10	Фристайл Хип-хоп	75	Хип-хоп	2
11	Легенды Рока	140	Рок	5
12	Поп-звезды сегодня	95	Поп	3
13	Джазовый экспромт	105	Джаз	4
14	Великие композиторы	155	Классика	6
15	Битва хип-хоперов	85	Хип-хоп	2
16	Энергия рока	135	Рок	5
17	Поп-вечеринка	98	Поп	3
18	Вечер джазовой импровизации	115	Джаз	4
19	Классика на бис	145	Классика	6
20	Хип-хоп шоу	82	Хип-хоп	2
21	Рок-хиты всех времен	125	Рок	5
22	Поп-концерт года	92	Поп	3
23	Великий Джаз	118	Джаз	4
24	Классическая ночь	150	Классика	7
25	Хип-хоп экспресс	78	Хип-хоп	2
26	Рок-фестиваль	138	Рок	5
27	Поп-идолы	97	Поп	3
28	Джазовое вдохновение	113	Джаз	4
29	Шедевры классики	148	Классика	6
30	Хип-хоп на улицах	79	Хип-хоп	2
\.


--
-- TOC entry 4907 (class 0 OID 16789)
-- Dependencies: 233
-- Data for Name: performance_concert_program; Type: TABLE DATA; Schema: agency; Owner: postgres
--

COPY agency.performance_concert_program (performance_id, concert_program_id) FROM stdin;
1	61
2	61
3	63
4	63
5	61
6	61
7	61
8	61
9	66
10	66
11	68
12	68
13	64
14	65
15	73
1	73
2	73
3	74
4	76
5	76
6	72
7	82
8	82
9	82
10	82
11	82
12	83
13	82
14	84
15	88
\.


--
-- TOC entry 4910 (class 0 OID 16876)
-- Dependencies: 237
-- Data for Name: test; Type: TABLE DATA; Schema: agency; Owner: postgres
--

COPY agency.test (id, a, b) FROM stdin;
5	1	2
6	1	3
\.


--
-- TOC entry 4901 (class 0 OID 16735)
-- Dependencies: 227
-- Data for Name: ticket; Type: TABLE DATA; Schema: agency; Owner: postgres
--

COPY agency.ticket (id, ticket_number, price, client_id, concert_program_id, place, address, date, "time") FROM stdin;
1	T001	3000	163	61	1 ряд 12 место	Минск, пр-т Победителей, 111	2026-11-12	18:00
2	T002	5000	164	62	2 ряд 3 место	Минск, пр-т Победителей, 111	2026-11-12	12:00
3	T003	2500	165	63	4 ряд 4 место	Минск, пр-т Победителей, 111	2026-11-12	20:00
4	T004	4000	166	64	5 ряд 9 место	Минск, пр-т Победителей, 111	2026-11-12	23:00
5	T005	3000	167	65	3 ряд 6 место	Минск, пр-т Победителей, 111	2026-11-12	16:00
6	T006	5000	168	66	1 ряд 2 место	Минск, пр-т Победителей, 111	2026-11-12	17:00
8	T008	4000	170	68	1 ряд 5 место	Минск, ул. Октябрьская, 16	2027-02-10	12:00
9	T009	3000	171	69	7 ряд 15 место	Минск, ул. Октябрьская, 16	2027-02-10	20:00
10	T010	5000	172	70	17 ряд 13 место	Минск, ул. Октябрьская, 16	2027-02-10	23:00
11	T011	2500	173	71	12 ряд 3 место	Минск, ул. Октябрьская, 16	2027-02-10	16:00
12	T012	4000	174	72	1 ряд 15 место	Минск, ул. Маскарадная, 10	2027-06-15	17:00
13	T013	3000	175	73	4 ряд 4 место	Минск, ул. Маскарадная, 10	2027-06-15	18:00
14	T014	5000	176	74	7 ряд 5 место	Минск, ул. Маскарадная, 10	2027-06-15	12:00
15	T015	2500	177	75	8 ряд 18 место	Минск, ул. Маскарадная, 10	2027-06-15	20:00
16	T016	4000	178	76	9 ряд 2 место	Минск, ул. Маскарадная, 10	2027-06-15	23:00
18	T018	5000	180	78	4 ряд 10 место	Минск, ул. Гикало, 5	2026-12-20	17:00
19	T019	2500	181	79	2 ряд 6 место	Минск, ул. Гикало, 5	2026-12-20	18:00
20	T020	4000	182	80	12 ряд 7 место	Минск, ул. Гикало, 5	2026-12-20	12:00
21	T021	3000	183	81	11 ряд 8 место	Минск, ул. Гикало, 5	2026-12-20	20:00
22	T022	5000	184	82	17 ряд 14 место	Минск, ул. Ташкентская, 19	2026-06-25	23:00
23	T023	2500	185	83	1 ряд 9 место	Минск, ул. Ташкентская, 19	2026-06-25	16:00
24	T024	4000	186	84	3 ряд 14 место	Минск, ул. Ташкентская, 19	2026-06-25	17:00
25	T025	3000	187	85	8 ряд 4 место	Минск, ул. Ташкентская, 19	2026-06-25	18:00
26	T026	5000	188	86	1 ряд 4 место	Минск, пл. Парижской Коммуны, 1	2026-06-20	12:00
27	T027	2500	189	87	15 ряд 15 место	Минск, пл. Парижской Коммуны, 1	2026-06-20	20:00
28	T028	2500	190	88	6 ряд 6 место	Минск, пл. Парижской Коммуны, 1	2026-06-20	23:00
29	T029	4000	191	89	16 ряд 16 место	Минск, пр-т Независимости, 32	2026-05-12	16:00
30	T030	3500	192	90	9 ряд 19 место	Минск, пр-т Независимости, 32	2026-05-12	17:00
7	T007	2500	\N	67	2 ряд 23 место	Минск, ул. Октябрьская, 16	2027-02-10	18:00
17	T017	3000	\N	77	10 ряд 11 место	Минск, ул. Гикало, 5	2026-12-20	16:00
\.


--
-- TOC entry 4897 (class 0 OID 16713)
-- Dependencies: 223
-- Data for Name: venue; Type: TABLE DATA; Schema: agency; Owner: postgres
--

COPY agency.venue (id, name, address, capacity, type) FROM stdin;
91	Минск-Арена	Минск, пр-т Победителей, 111	15000	стадион
92	Чижовка-Арена	Минск, ул. Ташкентская, 19	9600	стадион
93	Дворец Республики	Минск, Октябрьская площадь, 1	2700	закрытая
94	Футбольный манеж	Минск, пр-т Победителей, 20/2	5000	закрытая
95	Дворец спорта	Минск, пр-т Победителей, 4	3500	закрытая
96	Prime Hall	Минск, пр-т Победителей, 65	2000	закрытая
97	РЦ «Мир»	Минск, ул. Якутская, 4	800	закрытая
98	КЗ «Минск»	Минск, ул. Октябрьская, 5	1200	закрытая
99	Event Space	Минск, ул. Куйбышева, 22	700	закрытая
100	Платформа	Минск, ул. Куйбышева, 45	600	закрытая
101	Корпус	Минск, ул. Масловского, 8	900	закрытая
102	ОК16	Минск, Октябрьская, 16	1500	закрытая
103	КЗ «Верхний город»	Минск, пл. Свободы, 23А	1000	открытая
104	Галерея Ў	Минск, пр-т Независимости, 37А	300	закрытая
105	HIDE	Минск, ул. Октябрьская, 16	500	закрытая
106	КЗ «Белгосфилармония»	Минск, пр-т Независимости, 50	600	закрытая
107	ДК Железнодорожников	Минск, ул. Чкалова, 7	1000	закрытая
108	Театр эстрады	Минск, ул. Маскарадная, 10	1200	закрытая
109	Клуб Re:Public	Минск, ул. Притыцкого, 62	1500	закрытая
110	Minsk Marriott Hotel	Минск, пр-т Победителей, 20	500	закрытая
111	КЗ «Белгосцирк»	Минск, пр-т Независимости, 32	1700	закрытая
112	Театр оперы и балета	Минск, пл. Парижской Коммуны, 1	1200	закрытая
113	Большой театр Беларуси	Минск, пл. Парижской Коммуны, 1	1500	закрытая
114	Дом Москвы	Минск, ул. Коммунистическая, 86	600	закрытая
115	Клуб Граффити	Минск, ул. Советская, 14	300	закрытая
116	Loft Cafe	Минск, ул. Гикало, 5	400	закрытая
117	ДК МТЗ	Минск, пр-т Партизанский, 8	900	закрытая
118	Парк Dreamland	Минск, Орловская, 80	5000	открытая
119	Ресторан «Васильки» (банкетный зал)	Минск, пр-т Независимости, 89	200	закрытая
120	ТЦ «Галерея» (ивент-зона)	Минск, пр-т Победителей, 9	350	закрытая
\.


--
-- TOC entry 4931 (class 0 OID 0)
-- Dependencies: 228
-- Name: artist_id_seq; Type: SEQUENCE SET; Schema: agency; Owner: postgres
--

SELECT pg_catalog.setval('agency.artist_id_seq', 33, true);


--
-- TOC entry 4932 (class 0 OID 0)
-- Dependencies: 220
-- Name: client_id_seq; Type: SEQUENCE SET; Schema: agency; Owner: postgres
--

SELECT pg_catalog.setval('agency.client_id_seq', 192, true);


--
-- TOC entry 4933 (class 0 OID 0)
-- Dependencies: 224
-- Name: concert_program_id_seq; Type: SEQUENCE SET; Schema: agency; Owner: postgres
--

SELECT pg_catalog.setval('agency.concert_program_id_seq', 90, true);


--
-- TOC entry 4934 (class 0 OID 0)
-- Dependencies: 218
-- Name: organizer_id_seq; Type: SEQUENCE SET; Schema: agency; Owner: postgres
--

SELECT pg_catalog.setval('agency.organizer_id_seq', 180, true);


--
-- TOC entry 4935 (class 0 OID 0)
-- Dependencies: 230
-- Name: performance_id_seq; Type: SEQUENCE SET; Schema: agency; Owner: postgres
--

SELECT pg_catalog.setval('agency.performance_id_seq', 30, true);


--
-- TOC entry 4936 (class 0 OID 0)
-- Dependencies: 236
-- Name: test_id_seq; Type: SEQUENCE SET; Schema: agency; Owner: postgres
--

SELECT pg_catalog.setval('agency.test_id_seq', 7, true);


--
-- TOC entry 4937 (class 0 OID 0)
-- Dependencies: 226
-- Name: ticket_id_seq; Type: SEQUENCE SET; Schema: agency; Owner: postgres
--

SELECT pg_catalog.setval('agency.ticket_id_seq', 30, true);


--
-- TOC entry 4938 (class 0 OID 0)
-- Dependencies: 222
-- Name: venue_id_seq; Type: SEQUENCE SET; Schema: agency; Owner: postgres
--

SELECT pg_catalog.setval('agency.venue_id_seq', 120, true);


--
-- TOC entry 4729 (class 2606 OID 16778)
-- Name: artist_performance artist_performance_pkey; Type: CONSTRAINT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.artist_performance
    ADD CONSTRAINT artist_performance_pkey PRIMARY KEY (artist_id, performance_id);


--
-- TOC entry 4725 (class 2606 OID 16760)
-- Name: artist artist_pkey; Type: CONSTRAINT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.artist
    ADD CONSTRAINT artist_pkey PRIMARY KEY (id);


--
-- TOC entry 4711 (class 2606 OID 16706)
-- Name: client client_email_key; Type: CONSTRAINT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.client
    ADD CONSTRAINT client_email_key UNIQUE (email);


--
-- TOC entry 4713 (class 2606 OID 16704)
-- Name: client client_phone_key; Type: CONSTRAINT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.client
    ADD CONSTRAINT client_phone_key UNIQUE (phone);


--
-- TOC entry 4715 (class 2606 OID 16702)
-- Name: client client_pkey; Type: CONSTRAINT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.client
    ADD CONSTRAINT client_pkey PRIMARY KEY (id);


--
-- TOC entry 4719 (class 2606 OID 16728)
-- Name: concert_program concert_program_pkey; Type: CONSTRAINT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.concert_program
    ADD CONSTRAINT concert_program_pkey PRIMARY KEY (id);


--
-- TOC entry 4733 (class 2606 OID 16808)
-- Name: organizer_concert_program organizer_concert_program_pkey; Type: CONSTRAINT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.organizer_concert_program
    ADD CONSTRAINT organizer_concert_program_pkey PRIMARY KEY (organizer_id, concert_program_id);


--
-- TOC entry 4707 (class 2606 OID 16694)
-- Name: organizer organizer_phone_key; Type: CONSTRAINT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.organizer
    ADD CONSTRAINT organizer_phone_key UNIQUE (phone);


--
-- TOC entry 4709 (class 2606 OID 16692)
-- Name: organizer organizer_pkey; Type: CONSTRAINT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.organizer
    ADD CONSTRAINT organizer_pkey PRIMARY KEY (id);


--
-- TOC entry 4731 (class 2606 OID 16793)
-- Name: performance_concert_program performance_concert_program_pkey; Type: CONSTRAINT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.performance_concert_program
    ADD CONSTRAINT performance_concert_program_pkey PRIMARY KEY (performance_id, concert_program_id);


--
-- TOC entry 4727 (class 2606 OID 16773)
-- Name: performance performance_pkey; Type: CONSTRAINT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.performance
    ADD CONSTRAINT performance_pkey PRIMARY KEY (id);


--
-- TOC entry 4735 (class 2606 OID 16883)
-- Name: test test_pkey; Type: CONSTRAINT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.test
    ADD CONSTRAINT test_pkey PRIMARY KEY (id);


--
-- TOC entry 4721 (class 2606 OID 16741)
-- Name: ticket ticket_pkey; Type: CONSTRAINT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.ticket
    ADD CONSTRAINT ticket_pkey PRIMARY KEY (id);


--
-- TOC entry 4723 (class 2606 OID 16743)
-- Name: ticket ticket_ticket_number_key; Type: CONSTRAINT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.ticket
    ADD CONSTRAINT ticket_ticket_number_key UNIQUE (ticket_number);


--
-- TOC entry 4717 (class 2606 OID 16721)
-- Name: venue venue_pkey; Type: CONSTRAINT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.venue
    ADD CONSTRAINT venue_pkey PRIMARY KEY (id);


--
-- TOC entry 4740 (class 2606 OID 16761)
-- Name: artist artist_organizer_id_fkey; Type: FK CONSTRAINT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.artist
    ADD CONSTRAINT artist_organizer_id_fkey FOREIGN KEY (organizer_id) REFERENCES agency.organizer(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4741 (class 2606 OID 16779)
-- Name: artist_performance artist_performance_artist_id_fkey; Type: FK CONSTRAINT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.artist_performance
    ADD CONSTRAINT artist_performance_artist_id_fkey FOREIGN KEY (artist_id) REFERENCES agency.artist(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4742 (class 2606 OID 16784)
-- Name: artist_performance artist_performance_performance_id_fkey; Type: FK CONSTRAINT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.artist_performance
    ADD CONSTRAINT artist_performance_performance_id_fkey FOREIGN KEY (performance_id) REFERENCES agency.performance(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4736 (class 2606 OID 16707)
-- Name: client client_organizer_id_fkey; Type: FK CONSTRAINT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.client
    ADD CONSTRAINT client_organizer_id_fkey FOREIGN KEY (organizer_id) REFERENCES agency.organizer(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4737 (class 2606 OID 16729)
-- Name: concert_program concert_program_venue_id_fkey; Type: FK CONSTRAINT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.concert_program
    ADD CONSTRAINT concert_program_venue_id_fkey FOREIGN KEY (venue_id) REFERENCES agency.venue(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4745 (class 2606 OID 16814)
-- Name: organizer_concert_program organizer_concert_program_concert_program_id_fkey; Type: FK CONSTRAINT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.organizer_concert_program
    ADD CONSTRAINT organizer_concert_program_concert_program_id_fkey FOREIGN KEY (concert_program_id) REFERENCES agency.concert_program(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4746 (class 2606 OID 16809)
-- Name: organizer_concert_program organizer_concert_program_organizer_id_fkey; Type: FK CONSTRAINT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.organizer_concert_program
    ADD CONSTRAINT organizer_concert_program_organizer_id_fkey FOREIGN KEY (organizer_id) REFERENCES agency.organizer(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4743 (class 2606 OID 16799)
-- Name: performance_concert_program performance_concert_program_concert_program_id_fkey; Type: FK CONSTRAINT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.performance_concert_program
    ADD CONSTRAINT performance_concert_program_concert_program_id_fkey FOREIGN KEY (concert_program_id) REFERENCES agency.concert_program(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4744 (class 2606 OID 16794)
-- Name: performance_concert_program performance_concert_program_performance_id_fkey; Type: FK CONSTRAINT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.performance_concert_program
    ADD CONSTRAINT performance_concert_program_performance_id_fkey FOREIGN KEY (performance_id) REFERENCES agency.performance(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4738 (class 2606 OID 16744)
-- Name: ticket ticket_client_id_fkey; Type: FK CONSTRAINT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.ticket
    ADD CONSTRAINT ticket_client_id_fkey FOREIGN KEY (client_id) REFERENCES agency.client(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- TOC entry 4739 (class 2606 OID 16749)
-- Name: ticket ticket_concert_program_id_fkey; Type: FK CONSTRAINT; Schema: agency; Owner: postgres
--

ALTER TABLE ONLY agency.ticket
    ADD CONSTRAINT ticket_concert_program_id_fkey FOREIGN KEY (concert_program_id) REFERENCES agency.concert_program(id) ON UPDATE CASCADE ON DELETE CASCADE;


-- Completed on 2025-10-15 22:33:01

--
-- PostgreSQL database dump complete
--


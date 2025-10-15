COPY agency.test (id, a, b) FROM stdin;
5	1	2
6	1	3
\.

SELECT setval('agency.test_id_seq', 7, true);

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

SELECT setval('agency.client_id_seq', 192, true);

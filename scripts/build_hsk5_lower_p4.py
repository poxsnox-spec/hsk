# -*- coding: utf-8 -*-
"""Уроки 25-27 (Unit 9 — 感受人生)."""
from build_hsk5_lower import _vocab, _t, save


def lesson25():
    vocab = [
        _vocab("返航", "fǎnháng", "v.", "возвращаться из плавания", "to be on the homeward voyage"),
        _vocab("恶劣", "èliè", "adj.", "суровый, скверный", "bad, vile"),
        _vocab("可怕", "kěpà", "adj.", "страшный, ужасный", "terrible, dreadful"),
        _vocab("风浪", "fēnglàng", "n.", "шторм, буря", "storm, stormy waves"),
        _vocab("慌张", "huāngzhāng", "adj.", "растерянный", "flurried, flustered"),
        _vocab("舱", "cāng", "n.", "каюта, трюм", "cabin"),
        _vocab("使劲（儿）", "shǐjìn(r)", "v.", "изо всех сил", "to exert oneself"),
        _vocab("朝", "cháo", "prep.", "в сторону, к", "towards"),
        _vocab("简直", "jiǎnzhí", "adv.", "просто, прямо", "simply, virtually"),
        _vocab("沉", "chén", "v.", "тонуть, опускаться", "to sink"),
        _vocab("严肃", "yánsù", "adj.", "серьёзный, строгий", "serious, solemn"),
        _vocab("猛烈", "měngliè", "adj.", "яростный, сильный", "strong, violent, fierce"),
        _vocab("狂", "kuáng", "adj.", "бешеный, необузданный", "wildly, unrestrainedly"),
        _vocab("威胁", "wēixié", "v.", "угрожать", "to threaten"),
        _vocab("平衡", "pínghéng", "adj.", "равновесный", "balanced"),
        _vocab("吨", "dūn", "m.", "тонна", "metric ton"),
        _vocab("钢铁", "gāngtiě", "n.", "сталь", "steel"),
        _vocab("根基", "gēnjī", "n.", "основа, фундамент", "basis, foundation"),
        _vocab("重量", "zhòngliàng", "n.", "вес", "weight"),
        _vocab("相似", "xiāngsì", "adj.", "похожий", "similar"),
        _vocab("风景", "fēngjǐng", "n.", "пейзаж", "scenery, view"),
        _vocab("窄", "zhǎi", "adj.", "узкий", "narrow"),
        _vocab("万丈", "wànzhàng", "num.-m.", "бездонный, огромной высоты", "lofty, bottomless"),
        _vocab("深渊", "shēnyuān", "n.", "пропасть, бездна", "abyss, bottomless pit"),
        _vocab("游览", "yóulǎn", "v.", "осматривать, посещать", "to visit, to tour"),
        _vocab("发抖", "fādǒu", "v.", "дрожать", "to tremble, to shiver"),
        _vocab("负重", "fùzhòng", "v.", "нести груз", "to bear a load or weight"),
        _vocab("摔倒", "shuāidǎo", "v.", "упасть", "to fall down, to tumble"),
        _vocab("妇女", "fùnǚ", "n.", "женщина", "woman"),
        _vocab("起", "qǐ", "m.", "счётное слово для случаев", "case, instance"),
        _vocab("丝毫", "sīháo", "adj.", "ни малейший", "slightest, at all"),
        _vocab("滚", "gǔn", "v.", "катиться", "to roll, to tumble"),
        _vocab("风险", "fēngxiǎn", "n.", "риск", "risk"),
        _vocab("谨慎", "jǐnshèn", "adj.", "осмотрительный", "cautious, prudent"),
        _vocab("效应", "xiàoyìng", "n.", "эффект", "effect"),
        _vocab("胸", "xiōng", "n.", "грудь", "chest, bosom"),
        _vocab("承受", "chéngshòu", "v.", "выдерживать, выносить", "to bear, to endure"),
        _vocab("和尚", "héshang", "n.", "буддийский монах", "Buddhist monk"),
        _vocab("钟", "zhōng", "n.", "колокол; часы", "bell"),
        _vocab("彻底", "chèdǐ", "adj.", "полный, окончательный", "thorough, complete"),
    ]

    grammar = [
        {
            "word": "朝", "pos": "v./prep.",
            "explanation": {"ru": "«朝» как глагол — «обращённый лицом к чему-то». Как предлог — «в сторону, по направлению к». В отличие от «向» не может быть послеслогом (complement).",
                            "en": "«朝» as a verb means 'facing'. As a preposition — 'towards'. Unlike «向», it cannot be used as a complement."},
            "formula": {"ru": "朝 + место/направление + глагол", "en": "朝 + place/direction + verb"},
            "examples": [
                {"zh": "我们学校的正门坐西朝东。", "ru": "Главные ворота нашей школы обращены на восток.", "en": "Our school's main gate faces east."},
                {"zh": "老船长命令水手们立刻打开货舱，使劲儿朝里面放水。", "ru": "Старый капитан приказал матросам немедленно открыть трюм и изо всех сил заливать туда воду.", "en": "The old captain ordered the sailors to open the hold and pour water in with all their might."},
                {"zh": "我仿佛看到胜利正朝我们走来。", "ru": "Мне казалось, сама победа идёт нам навстречу.", "en": "It seemed victory itself was walking towards us."},
            ],
            "exercises": [{"type": "fill_blank", "question": "请问，去国家图书馆__？", "answer": "朝哪个方向走"}],
        },
        {
            "word": "简直", "pos": "adv.",
            "explanation": {"ru": "«简直» — наречие, «прямо, буквально, просто». Выражает близость к полному сходству, но не полное сходство. С оттенком восклицания, подчёркивания.",
                            "en": "«简直» is an adverb meaning 'simply, literally, virtually'. Expresses near-complete similarity. Has an emphatic, exclamatory tone."},
            "examples": [
                {"zh": "听到刘方离婚的消息时，我简直不敢相信自己的耳朵。", "ru": "Услышав о разводе Лю Фана, я просто не поверил своим ушам.", "en": "Hearing that Liu Fang had divorced, I simply couldn't believe my ears."},
                {"zh": "这次张小姐变得格外客气、礼貌，与从前相比，简直像换了个人。", "ru": "На этот раз госпожа Чжан была особенно вежлива — по сравнению с прошлым она словно стала другим человеком.", "en": "This time Miss Zhang was especially polite — she seemed like a completely different person."},
                {"zh": "船长简直是疯了。", "ru": "Капитан буквально сошёл с ума.", "en": "The captain has simply gone mad."},
            ],
            "exercises": [{"type": "fill_blank", "question": "眼前的情景让在场的所有人都惊呆了，__。", "answer": "简直像做梦一样"}],
        },
    ]

    comparisons = [
        {
            "word_a": "严肃", "word_b": "严格",
            "common": {"ru": "Оба прилагательных могут описывать строгость.", "en": "Both adjectives can describe strictness."},
            "differences": [
                {"ru": "«严肃» — «серьёзный, строгий (в выражении лица, в тоне)».", "en": "«严肃» — 'serious, solemn (expression, tone)'."},
                {"ru": "«严格» — «строгий, требовательный (к требованиям, правилам)».", "en": "«严格» — 'strict, demanding (requirements, rules)'."},
            ],
        },
    ]

    expansion = {
        "topic": {"zh": "度量单位 (Единицы измерения)", "ru": "Единицы измерения", "en": "Units of measurement"},
        "words": [
            {"hanzi": "厘米", "pinyin": "límǐ", "meaning": {"zh": "", "ru": "сантиметр", "en": "centimetre"}},
            {"hanzi": "克", "pinyin": "kè", "meaning": {"zh": "", "ru": "грамм", "en": "gram"}},
            {"hanzi": "平方", "pinyin": "píngfāng", "meaning": {"zh": "", "ru": "квадратный (метр и т.п.)", "en": "square (metre, etc.)"}},
            {"hanzi": "吨", "pinyin": "dūn", "meaning": {"zh": "", "ru": "тонна", "en": "tonne"}},
            {"hanzi": "尺子", "pinyin": "chǐzi", "meaning": {"zh": "", "ru": "линейка", "en": "ruler"}},
            {"hanzi": "胶水", "pinyin": "jiāoshuǐ", "meaning": {"zh": "", "ru": "клей", "en": "glue"}},
            {"hanzi": "文具", "pinyin": "wénjù", "meaning": {"zh": "", "ru": "канцтовары", "en": "stationery"}},
        ],
    }

    workbook = {
        "listening": [
            {"type": "mc", "audio": "workbook_25_1.mp3",
             "prompt": {"zh": "关于老船长，下列哪项是正确的？", "ru": "Что верно о старом капитане?", "en": "Which is true of the old captain?"},
             "options": ["有些慌张", "非常冷静", "轻松愉快", "格外激动"], "answer": 1},
            {"type": "mc", "audio": "workbook_25_1.mp3",
             "prompt": {"zh": "会议怎么样了？", "ru": "Что случилось с собранием?", "en": "What about the meeting?"},
             "options": ["提前了", "推迟了", "取消了", "按时举行"], "answer": 1},
        ],
        "reading": [
            {"type": "cloze",
             "text_zh": "26岁的荷兰残疾姑娘莫妮克收到了最棒的圣诞礼物：从轮椅上站起来了。原来，莫妮克曾在一次15的交通事故中瘫痪，但坚强的莫妮克并没有放弃生活。",
             "blanks": [
                 {"position": 15, "answer": "可怕", "options": ["恐怕", "可怕", "害怕", "厉害"]},
             ]},
        ],
        "writing": [
            {"type": "make_sentence", "words": ["他的", "一个", "命运", "彻底改变了", "偶然的机会"], "answer": "一个偶然的机会彻底改变了他的命运。"},
            {"type": "make_sentence", "words": ["经历", "也有", "相似的", "与老人", "陈工程师"], "answer": "陈工程师也有与老人相似的经历。"},
            {"type": "make_sentence", "words": ["简直", "书房", "就是", "李老师的", "一个小图书馆"], "answer": "李老师的书房简直就是一个图书馆。"},
            {"type": "short_essay", "words": ["风险", "威胁", "慌张", "承受", "谨慎"], "min_length": 80},
        ],
    }

    return {
        "title": _t("给自己加满水", "Наполнить себя водой", "", "Adding up the load on yourself", ""),
        "audio_files": {"textbook_1": "textbook_25_1.mp3", "vocab": "vocab_25.mp3", "workbook_25_1": "workbook_25_1.mp3"},
        "warmup": {
            "question": _t("你听说过“有压力才会有动力”这句话吗？你是否同意这种观点？为什么？",
                           "Слышали ли вы выражение «есть давление — есть и стимул»? Согласны ли вы? Почему?",
                           "", "Have you heard 'pressure creates motivation'? Do you agree? Why?"),
            "answers": ["返航"],
        },
        "text_zh": "有一位经验丰富的老船长，一次返航中，天气恶劣，他们的船遇到了可怕的巨大风浪。正当水手们慌张得不知如何是好时，老船长命令水手们立刻打开货舱，使劲儿朝里面放水。\n“船长简直是疯了，这样做只会增加船的压力，船就会下沉得更快，这不是找死吗？”一个年轻的水手骂道。看着船长严肃的表情，水手们还是照做了。随着货舱里的水位越升越高，船一点一点地下沉，狂风巨浪依然猛烈，对船的威胁却减小了，船也渐渐取得了平衡。船长望着松了一口气的水手们说：“几万吨的钢铁巨轮很少有被打翻的，被打翻的常常是根基很轻的小船。船在有一定重量的时候是最安全的，在空的时候则是最危险的。”\n另一个相似的故事发生在某一名风景区，那里有一段被当地人称为“鬼谷”的最危险的路段，山路非常窄，两边是万丈深渊。每当导游们带队来这里游览时，一定要让游客们背点或者拿点什么东西。“这么危险的地方，我不拿东西两腿都发抖，再负重前行，那不是更容易摔倒吗？”一位妇女不解地问。导游小姐解释道：“这里以前发生过好几起意外，都是迷路的游客在丝毫没有感觉到压力的情况下，一不小心滚下去的。当地人每天都从这条路上背着东西来来往往，却从来没人出事。假如你感觉到了有风险，谨慎地负重前行，反而会更安全。”\n这就是“压力效应”。那些胸怀理想、肩上有责任感的人，才能承受住压力，从历史的风雨中走过“鬼谷”；而那些没有理想，没有一点压力，做一天和尚撞一天钟的人，就像一艘风暴中的空船，往往一场人生的狂风巨浪便会把他们彻底地打翻在地。",
        "text_translation": {
            "zh": "",
            "ru": "У одного опытного старого капитана во время возвращения из плавания погода была суровой, и корабль попал в страшный шторм. Когда матросы в панике не знали, что делать, старый капитан приказал немедленно открыть трюм и изо всех сил заливать туда воду.\n«Капитан просто сошёл с ума: это только увеличит нагрузку, корабль быстрее пойдёт ко дну — разве это не самоубийство?» — выругался молодой матрос. Но, увидев серьёзное лицо капитана, матросы всё же выполнили приказ. По мере того как уровень воды в трюме поднимался, корабль медленно оседал, но яростные волны и ураганный ветер уже не так угрожали ему — судно постепенно обрело равновесие. Глядя на вздохнувших с облегчением матросов, капитан сказал: «Многотонные стальные гиганты редко опрокидываются; опрокидываются обычно лёгкие, с малой осадкой суда. Корабль наиболее безопасен при определённом весе и наиболее опасен пустым».\nПохожая история произошла в одном живописном районе, где есть самый опасный участок, прозванный местными «ущельем духов»: горная тропа очень узкая, по обе стороны — бездонные пропасти. Когда экскурсоводы ведут туристов, они обязательно велят им что-нибудь нести или взять в руки. «В таком опасном месте у меня и без ноши ноги дрожат, а если ещё с грузом — разве не легче упасть?» — недоумевала одна женщина. Экскурсовод объяснила: «Здесь раньше случались происшествия — потерявшиеся туристы, не чувствуя никакого давления, неосторожно скатывались вниз. Местные жители каждый день ходят по этой тропе с грузом туда и обратно, но никто не пострадал. Если вы чувствуете риск и осторожно идёте с грузом, вам, наоборот, безопаснее».\nЭто и есть «эффект давления». Только те, у кого в груди мечта и на плечах чувство ответственности, способны выдержать давление и пройти сквозь бури истории «ущелье духов»; а те, у кого нет мечты, нет ни малейшего давления, кто живёт «день прошёл — и ладно», подобны пустому судну в шторме — и любая буря жизни полностью опрокинет их.",
            "tk": "", "en": "An experienced old captain was returning from a voyage when the weather turned bad and the ship met a terrible storm. Just as the sailors were panicking, unsure what to do, the old captain ordered them to open the cargo hold at once and pour water in with all their might.\n'The captain has gone mad — this will only add weight and sink us faster. Isn't this suicide?' cursed a young sailor. But seeing the captain's serious face, the sailors obeyed. As the water level in the hold rose, the ship slowly sank lower, but the howling wind and waves threatened it less and less — the vessel gradually regained balance. Looking at the relieved sailors, the captain said: 'Multi-ton steel giants are rarely capsized; it's usually light, shallow-keeled boats that overturn. A ship is safest with a certain weight and most dangerous when empty.'\nA similar story took place at a scenic spot where there is a most dangerous stretch called by locals 'Ghost Valley' — a very narrow mountain path flanked by bottomless abysses. Whenever guides lead tour groups here, they always make visitors carry or hold something. 'In such a dangerous place my legs tremble even without a load — with extra weight, wouldn't I fall more easily?' asked a puzzled woman. The guide explained: 'Several accidents happened here before — lost tourists, feeling no pressure at all, carelessly rolled down. Locals pass this path daily carrying loads back and forth, yet no one has ever had an accident. If you sense the risk and cautiously walk with a load, you'll actually be safer.'\nThis is the 'pressure effect.' Only those with ideals in their hearts and a sense of responsibility on their shoulders can withstand pressure and pass through the 'Ghost Valley' of history's storms; those without ideals and with no pressure at all — those who 'live as a monk for a day and toll the bell for a day' — are like empty ships in a storm; a single wild wave of life will overturn them completely.",
            "uz": "", "tg": "", "id": "", "tr": "",
        },
        "vocabulary": vocab, "grammar": grammar, "comparisons": comparisons, "expansion": expansion,
        "application": {
            "discussion": _t("如何面对压力：目前你遇到的最大的压力来自哪方面？压力给你带来了什么影响？有什么好处和坏处？你觉得压力过大时，有什么好的减轻压力的办法吗？",
                           "Как справляться со стрессом: откуда сейчас самый большой стресс? Какое влияние он оказывает? Плюсы и минусы? Как можно его снизить?",
                           "", "Facing pressure: what's your biggest current source of stress? What impact does it have? Pros and cons? How do you relieve excessive stress?"),
            "writing_prompt": {"zh": "请以“我喜欢/不喜欢压力”为题，谈谈你的看法。尽量用上本课所学的生词，字数不少于100字。",
                              "ru": "Напишите эссе на тему «Люблю / не люблю давление», используя слова урока, не менее 100 иероглифов.",
                              "en": "Write an essay titled 'I like / dislike pressure', using this lesson's vocabulary, at least 100 characters."},
        },
        "workbook": workbook,
    }


def lesson26():
    vocab = [
        _vocab("忙碌", "mánglù", "adj.", "занятой, хлопотливый", "busy, fully occupied"),
        _vocab("被动", "bèidòng", "adj.", "пассивный", "passive"),
        _vocab("奴隶", "núlì", "n.", "раб", "slave"),
        _vocab("虚伪", "xūwěi", "adj.", "лицемерный", "hypocritical"),
        _vocab("思想", "sīxiǎng", "n.", "мысль, идеология", "thought, thinking"),
        _vocab("反省", "fǎnxǐng", "v.", "самоанализ, задуматься", "to reflect on oneself, to self-examine"),
        _vocab("据说", "jùshuō", "v.", "говорят, что...", "it is said, reputedly"),
        _vocab("个性", "gèxìng", "n.", "индивидуальность", "individual character, personality"),
        _vocab("冒险", "màoxiǎn", "v.", "рисковать", "to venture, to have an adventure"),
        _vocab("丛林", "cónglín", "n.", "джунгли", "jungle, forest"),
        _vocab("文明", "wénmíng", "n.", "цивилизация", "civilization"),
        _vocab("纪录", "jìlù", "n./v.", "рекорд; документировать", "record; to record"),
        _vocab("雇", "gù", "v.", "нанимать", "to employ, to hire"),
        _vocab("来", "lái", "part.", "около, приблизительно (после числ.)", "used after round numbers to indicate approximation"),
        _vocab("批", "pī", "m.", "партия, группа", "group, batch"),
        _vocab("出色", "chūsè", "adj.", "выдающийся", "remarkable, outstanding"),
        _vocab("健步如飞", "jiànbù-rúfēi", "идиом", "идти как на крыльях", "to walk as if on wings"),
        _vocab("一连", "yìlián", "adv.", "подряд", "in a row, in succession"),
        _vocab("耽误", "dānwu", "v.", "задерживать, упустить", "to delay, to spoil through delay"),
        _vocab("至于", "zhìyú", "prep.", "что касается", "as for, as to"),
        _vocab("投资", "tóuzī", "v.", "инвестировать", "to invest, to fund"),
        _vocab("人物", "rénwù", "n.", "персона, фигура", "figure, personage"),
        _vocab("得罪", "dézuì", "v.", "обидеть, нажить врага", "to offend, to displease"),
        _vocab("总算", "zǒngsuàn", "adv.", "наконец-то", "at last, finally"),
        _vocab("搞", "gǎo", "v.", "делать, разбираться", "to produce a certain effect"),
        _vocab("习俗", "xísú", "n.", "обычай", "custom, convention"),
        _vocab("灵魂", "línghún", "n.", "душа, дух", "soul, spirit"),
        _vocab("疲劳", "píláo", "adj.", "усталый", "tired, fatigued"),
        _vocab("哲理", "zhélǐ", "n.", "философия, мудрость", "philosophy"),
        _vocab("提倡", "tíchàng", "v.", "пропагандировать, призывать", "to advocate, to encourage"),
        _vocab("步骤", "bùzhòu", "n.", "шаг, этап", "step, procedure"),
        _vocab("闭关", "bìguān", "v.", "уединяться", "to stay secluded"),
        _vocab("一律", "yílǜ", "adv.", "без исключения, одинаково", "all, without exception"),
        _vocab("寂寞", "jìmò", "adj.", "одинокий", "lonely"),
        _vocab("效率", "xiàolǜ", "n.", "эффективность", "efficiency"),
    ]

    grammar = [
        {
            "word": "来", "pos": "part.",
            "explanation": {"ru": "«来» как служебное слово после числительных «十, 百, 千» и счётных слов образует приблизительное число: «около, примерно». Также в конструкции «一来…，二来…» перечисляет причины.",
                            "en": "«来» after numerals like 十, 百, 千 forms approximation: 'about, roughly'. Also in the pattern '一来…，二来…' it lists reasons."},
            "examples": [
                {"zh": "他雇了20来个当地人为他带路和搬运行李。", "ru": "Он нанял около 20 местных жителей — проводить его и носить багаж.", "en": "He hired about 20 locals to guide him and carry luggage."},
                {"zh": "今天是大年三十，我们来看看大家，一来是给大家送水果，二来是看看大家过节还有什么难处。", "ru": "Сегодня канун Нового года — мы пришли к вам: во-первых, принесли фрукты, во-вторых, узнать, какие у вас трудности с праздником.", "en": "Today is New Year's Eve — we've come to see you: first, to bring fruit; second, to see what difficulties you have for the holiday."},
            ],
            "exercises": [{"type": "fill_blank", "question": "这所学校是小班上课，每个班__。", "answer": "有二十来个学生"}],
        },
        {
            "word": "至于", "pos": "v./prep.",
            "explanation": {"ru": "«至于» как глагол — «доходить до такой степени», чаще в риторических вопросах. Как предлог в конструкции «…，至于…» — «что касается…».",
                            "en": "«至于» as a verb means 'to reach such an extent', often in rhetorical questions. As a preposition in '..., 至于...' — 'as for...'."},
            "examples": [
                {"zh": "我只是和你开个玩笑，你至于生那么大的气吗？", "ru": "Я же просто пошутил, стоит ли так злиться?", "en": "I was just joking with you — is it worth getting so angry?"},
                {"zh": "我只知道他是六班的学生，至于住在哪儿，我就不清楚了。", "ru": "Я знаю только, что он из шестого класса, а где живёт — не в курсе.", "en": "I only know he's in class six; as for where he lives, I have no idea."},
                {"zh": "至于这部影片的投资人，可是一位大人物，他可不敢得罪。", "ru": "Что касается инвестора этого фильма — это важная персона, обижать его он не смел.", "en": "As for the film's investor — that's an important figure; he wouldn't dare offend him."},
            ],
            "exercises": [{"type": "fill_blank", "question": "我刚毕业，现在最重要的是找到工作，__。", "answer": "至于工资多少，先不考虑"}],
        },
        {
            "word": "总算", "pos": "adv.",
            "explanation": {"ru": "«总算» — наречие, «наконец-то, в конце концов». Обозначает, что желаемое осуществилось после долгого времени. Также может значить «более-менее, сойдёт».",
                            "en": "«总算» is an adverb meaning 'finally, at long last'. Indicates the desired outcome after a long time. Can also mean 'more or less acceptable'."},
            "examples": [
                {"zh": "经过沟通，大导演总算搞明白了。", "ru": "После объяснений режиссёр наконец понял, в чём дело.", "en": "After some communication, the great director finally understood."},
                {"zh": "总算把活儿干完了，可把我累坏了。", "ru": "Наконец-то работа сделана — я страшно устал.", "en": "The work is finally done — I'm exhausted."},
                {"zh": "虽然我对这家宾馆不太满意，但总算有个睡觉的地方了。", "ru": "Хотя отель мне не очень нравится, но хоть есть где поспать.", "en": "Though I'm not satisfied with this hotel, at least there's a place to sleep."},
            ],
            "exercises": [{"type": "fill_blank", "question": "整整一个星期没出门，我__。", "answer": "总算把这本书读完了"}],
        },
    ]

    comparisons = [
        {
            "word_a": "总算", "word_b": "终于",
            "common": {"ru": "Оба наречия обозначают, что после долгого времени произошло нечто. Часто взаимозаменяемы.",
                        "en": "Both adverbs mean something happened after a long time; often interchangeable."},
            "differences": [
                {"ru": "«总算» — обычно желаемый результат.", "en": "«总算» — usually a desired result."},
                {"ru": "«终于» — может быть и нежелательный результат.", "en": "«终于» — can also be an undesirable result."},
                {"ru": "«总算» также «более-менее, сойдёт».", "en": "«总算» also means 'more or less acceptable'."},
            ],
        },
    ]

    expansion = {
        "topic": {"zh": "社会关系/婚恋 (Общество и брак)", "ru": "Общество и брак", "en": "Social relations and marriage"},
        "words": [
            {"hanzi": "演讲", "pinyin": "yǎnjiǎng", "meaning": {"zh": "", "ru": "публичное выступление", "en": "speech"}},
            {"hanzi": "发言", "pinyin": "fāyán", "meaning": {"zh": "", "ru": "выступление", "en": "statement"}},
            {"hanzi": "宴会", "pinyin": "yànhuì", "meaning": {"zh": "", "ru": "банкет", "en": "banquet"}},
            {"hanzi": "嘉宾", "pinyin": "jiābīn", "meaning": {"zh": "", "ru": "почётный гость", "en": "guest of honour"}},
            {"hanzi": "证件", "pinyin": "zhèngjiàn", "meaning": {"zh": "", "ru": "документ, удостоверение", "en": "certificate, ID"}},
            {"hanzi": "名片", "pinyin": "míngpiàn", "meaning": {"zh": "", "ru": "визитная карточка", "en": "business card"}},
            {"hanzi": "嫁", "pinyin": "jià", "meaning": {"zh": "", "ru": "выйти замуж", "en": "to marry (of a woman)"}},
            {"hanzi": "娶", "pinyin": "qǔ", "meaning": {"zh": "", "ru": "жениться", "en": "to marry (a woman)"}},
            {"hanzi": "分手", "pinyin": "fēnshǒu", "meaning": {"zh": "", "ru": "расстаться", "en": "to break up"}},
            {"hanzi": "怀孕", "pinyin": "huáiyùn", "meaning": {"zh": "", "ru": "быть беременной", "en": "to be pregnant"}},
            {"hanzi": "吻", "pinyin": "wěn", "meaning": {"zh": "", "ru": "поцелуй", "en": "kiss"}},
        ],
    }

    workbook = {
        "listening": [
            {"type": "mc", "audio": "workbook_26_1.mp3",
             "prompt": {"zh": "男的在忙什么？", "ru": "Чем занят мужчина?", "en": "What is the man busy with?"},
             "options": ["去查找资料", "去超市购物", "去教室自习", "回宿舍休息"], "answer": 0},
            {"type": "mc", "audio": "workbook_26_1.mp3",
             "prompt": {"zh": "男的和女的是什么关系？", "ru": "Кем являются мужчина и женщина?", "en": "What is the relationship?"},
             "options": ["恋人", "同事", "朋友", "客户"], "answer": 2},
        ],
        "reading": [
            {"type": "cloze",
             "text_zh": "某人在沙漠中行进了大半天，口渴得直冒烟。在他快要走出沙漠时，遇到了一位推销员，劝他买一条领带。他说：“你行行好吧，我渴得连衬衣都想撕开了，15！”",
             "blanks": [
                 {"position": 15, "answer": "还买什么领带", "options": ["还买什么领带", "快帮我选一条", "能不能便宜一点儿", "何况我自己就有"]},
             ]},
        ],
        "writing": [
            {"type": "make_sentence", "words": ["无效", "一律", "答卷", "书写的", "用铅笔"], "answer": "用铅笔书写的答卷一律无效。"},
            {"type": "make_sentence", "words": ["把", "给我", "强加", "请不要", "你的思想"], "answer": "请不要把你的思想强加给我。"},
            {"type": "make_sentence", "words": ["搞到", "我们", "问题是", "他的签名", "怎样才能"], "answer": "问题是怎样才能搞到他的签名。"},
            {"type": "short_essay", "words": ["效率", "提倡", "步骤", "耽误", "出色"], "min_length": 80},
        ],
    }

    return {
        "title": _t("你属于哪一种“忙”", "К какому типу «занятых» вы относитесь?", "", "Which kind of 'busy' person are you", ""),
        "audio_files": {"textbook_1": "textbook_26_1.mp3", "vocab": "vocab_26.mp3", "workbook_26_1": "workbook_26_1.mp3"},
        "warmup": {
            "question": _t("你觉得这幅图片想告诉我们什么？说说你对这幅图片的理解。请试着找出本课跟“出行”有关的词语。",
                           "Что хочет сказать эта картинка? Попробуйте найти слова из словаря урока, связанные с путешествием.",
                           "", "What does this picture tell us? Find travel-related words in this lesson's vocabulary."),
            "answers": ["行李"],
        },
        "text_zh": "工作中的忙碌大概可以分为三种：第一种忙，忙得很被动，总是被事情追着、赶着，人几乎成了工作的奴隶；第二种忙，忙得很主动，忙而不乱，人是工作的主人；第三种忙，忙得有些虚伪，因为在他们的思想中，已经把忙与成功、闲与失败联系到一起，所以，这样的人总是想办法让自己忙。\n你属于哪种忙呢？\n我有一个体会：现实中，我们不一定知道正确的道路是什么，但时时反省、总结，却可以使我们不会在错误的道路上走得太远。\n据说，曾经有一位很有个性、极爱冒险的大导演到南美丛林拍有关古代印加文明的纪录片。他雇了20来个当地人为他带路和搬运行李。这批当地人个个都表现出色，尽管他们背着重重的行李，但他们的脚力过人，健步如飞。一连三天，他们都很顺利地实现了原定的计划。到了第四天，大导演一早醒来就催着大家上路。然而，当地人却拒绝行动。大导演非常着急，一来，耽误了时间，日程就得重新安排；二来，会因为费用增加而让投资人不高兴，至于这部影片的投资人，可是一位大人物，他可不敢得罪。经过沟通，大导演总算搞明白了，当地人自古就有一种习俗：在赶路时，用尽全力地向前冲，但每走上三天，便要休息一天。当大导演进一步询问原因时，当地人的回答令他受益终生。\n“那是为了让我们的灵魂，能够追得上我们赶了三天路的疲劳的身体。”\n多么富有哲理的话！在这个提倡和鼓励竞争的时代，我们常常只顾低头拉车，却少了抬头看路，少了思考、总结这一重要的步骤。\n从20世纪80年代起，比尔·盖茨每年都要进行两次为期一周的“闭关”。在这一周的时间里，他会把自己关在一所房子里，包括家人在内的任何人他都一律不见，使自己完全不受日常工作的打扰。盖茨的这种令人寂寞难耐的“闭关”不只是一种休息方式，更是一种高效率的工作方式。\n忙碌的人们，请多给自己一点思考的时间吧。",
        "text_translation": {
            "zh": "",
            "ru": "Занятость на работе можно условно разделить на три типа. Первый тип — пассивная занятость: дела гонят и подгоняют человека, он почти стал рабом работы. Второй — активная занятость: хлопотливо, но без суеты, человек — хозяин работы. Третий — несколько лицемерная занятость: в их сознании «занятость» уже связана с успехом, а «праздность» — с неудачей, поэтому такие люди всегда стараются быть занятыми.\nК какому типу относитесь вы?\nУ меня есть одно наблюдение: в реальности мы не всегда знаем, какой путь правильный, но постоянный самоанализ и подведение итогов не позволяют нам зайти слишком далеко по неверной дороге.\nГоворят, был однажды очень самобытный и большой любитель приключений кинорежиссёр, приехавший в южноамериканские джунгли снимать документальный фильм о древней цивилизации инков. Он нанял около 20 местных жителей — провожатыми и носильщиками. Местные все работали отлично: несмотря на тяжёлый груз, шли легко, будто на крыльях. Три дня подряд они успешно выполняли план. Но на четвёртый день режиссёр поднял всех спозаранку, чтобы выступить в путь. Местные же отказались идти. Режиссёр очень волновался: во-первых, потеря времени — придётся перекроить график; во-вторых, из-за роста расходов будет недоволен инвестор — а инвестором фильма был важный человек, обижать его он не смел. После переговоров режиссёр наконец понял: у местных с древних времён есть обычай — в пути изо всех сил рваться вперёд, но каждые три дня пути делать день отдыха. Когда режиссёр спросил причину, ответ местных запомнился ему на всю жизнь.\n«Это чтобы наши души успевали догнать наши измождённые трёхдневным переходом тела».\nКакие мудрые слова! В наш век, когда пропагандируется и поощряется конкуренция, мы часто лишь опускаем голову и тянем телегу, но редко поднимаем глаза, чтобы посмотреть на дорогу, — упуская размышление и подведение итогов, эти важные шаги.\nС 1980-х годов Билл Гейтс дважды в год устраивал недельное «затворничество»: запирался в доме, никого — включая семью — не принимал, полностью ограждая себя от повседневных дел. Такое «затворничество», мучительное от одиночества, для Гейтса было не только отдыхом, но и высокоэффективным способом работы.\nЗанятые люди, дайте себе побольше времени на размышления.",
            "tk": "", "en": "Being busy at work can be roughly divided into three types. The first — passive busyness: work chases and drives the person; he has almost become a slave of work. The second — active busyness: busy without confusion; the person is master of the work. The third — somewhat hypocritical busyness: in their minds, 'busy' is already linked to success and 'idle' to failure, so they always try to keep themselves busy.\nWhich type are you?\nI have an insight: in reality, we don't always know which road is right, but constant self-reflection and summarizing can keep us from going too far down the wrong one.\nIt is said there was once a very original, adventure-loving film director who went to the South American jungle to shoot a documentary on ancient Inca civilization. He hired about twenty locals as guides and porters. They all performed outstandingly — carrying heavy loads, they walked as if on wings. Three days in a row they successfully fulfilled the plan. On the fourth day, the director woke everyone early to set off. But the locals refused to go. The director grew anxious: first, losing time meant rescheduling; second, added costs would displease the investor — and the film's investor was an important figure he dared not offend. After some negotiation, the director finally understood: the locals had an ancient custom — on a journey they dash forward with all their might, but every three days of travel they must rest one day. When the director asked why, their answer benefited him for life.\n'That's so our souls can catch up with our bodies, weary from three days on the road.'\nWhat a philosophical saying! In this era that advocates and encourages competition, we often only look down at the cart we're pulling, rarely lifting our heads to see the road — neglecting reflection and summarization, those important steps.\nSince the 1980s, Bill Gates has taken a week-long 'seclusion' twice a year. During that week he shuts himself in a house, seeing no one — family included — completely free from daily work. Gates' lonely 'seclusion' is not just a form of rest but a highly efficient way to work.\nBusy people, give yourselves a little more time for thought.",
            "uz": "", "tg": "", "id": "", "tr": "",
        },
        "vocabulary": vocab, "grammar": grammar, "comparisons": comparisons, "expansion": expansion,
        "application": {
            "discussion": _t("学会思考：你是一个平时爱思考的人吗？当你遇到不顺利的情况时，你通常会怎么做？请以学习或工作中一次经历为例，说说思考对你有哪些帮助。思考和行动，哪个更重要？",
                           "Научиться думать: любите ли вы думать? Что вы обычно делаете в трудной ситуации? На примере учёбы или работы расскажите, чем вам помогает размышление. Что важнее — думать или действовать?",
                           "", "Learning to think: Are you someone who likes to think? What do you usually do when things go wrong? Give an example from work or study — how has reflection helped you? Which is more important, thinking or acting?"),
            "writing_prompt": {"zh": "请以“认真思考，轻松生活”为题，谈谈你是如何面对生活中遇到的各种困难的。尽量用上本课所学的生词，字数不少于100字。",
                              "ru": "Напишите эссе на тему «Думать вдумчиво — жить легко», используя слова урока, не менее 100 иероглифов.",
                              "en": "Write an essay titled 'Think carefully, live easily', using this lesson's vocabulary, at least 100 characters."},
        },
        "workbook": workbook,
    }


def lesson27():
    vocab = [
        _vocab("（象）棋", "(xiàng)qí", "n.", "шахматы (сянци)", "(Chinese) chess, board game"),
        _vocab("教练", "jiàoliàn", "n.", "тренер", "coach, instructor"),
        _vocab("答应", "dāying", "v.", "соглашаться, обещать", "to agree, to promise"),
        _vocab("损失", "sǔnshī", "v.", "терять, утрачивать", "to lose"),
        _vocab("睁", "zhēng", "v.", "открывать (глаза)", "to open one's eyes"),
        _vocab("眼睁睁", "yǎnzhēngzhēng", "adj.", "беспомощно (смотреть)", "looking on helplessly"),
        _vocab("将军", "jiāngjūn", "n./v.", "генерал; шах!", "general; to check"),
        _vocab("服气", "fúqì", "v.", "признать поражение", "to be convinced, to be won over"),
        _vocab("运气", "yùnqi", "n.", "удача", "luck, fortune"),
        _vocab("局", "jú", "m.", "партия (в игре)", "game, set"),
        _vocab("发挥", "fāhuī", "v.", "проявить, реализовать", "to bring into play"),
        _vocab("灰心", "huīxīn", "adj.", "падать духом", "discouraged"),
        _vocab("吸取", "xīqǔ", "v.", "извлекать, впитывать", "to absorb, to draw"),
        _vocab("教训", "jiàoxùn", "n.", "урок", "lesson, moral"),
        _vocab("未必", "wèibì", "adv.", "не обязательно", "may not, not necessarily"),
        _vocab("次要", "cìyào", "adj.", "второстепенный", "less important, secondary"),
        _vocab("因素", "yīnsù", "n.", "фактор", "factor"),
        _vocab("在于", "zàiyú", "v.", "заключаться в", "to lie in, to consist in"),
        _vocab("心态", "xīntài", "n.", "психологическое состояние", "psychology, mental attitude"),
        _vocab("珍惜", "zhēnxī", "v.", "дорожить", "to cherish, to treasure"),
        _vocab("否认", "fǒurèn", "v.", "отрицать", "to deny"),
        _vocab("观察", "guānchá", "v.", "наблюдать", "to observe, to watch"),
        _vocab("失去", "shīqù", "v.", "терять", "to lose"),
        _vocab("期间", "qījiān", "n.", "период, время", "time, period"),
        _vocab("把握", "bǎwò", "n.", "уверенность", "assurance, confidence"),
        _vocab("不假思索", "bùjiǎ-sīsuǒ", "идиом", "не задумываясь", "without thinking or hesitation"),
        _vocab("犯", "fàn", "v.", "совершать (ошибку)", "to commit (an error)"),
        _vocab("过于", "guòyú", "adv.", "слишком, чрезмерно", "too, excessively"),
        _vocab("原则", "yuánzé", "n.", "принцип", "principle, tenet"),
        _vocab("责备", "zébèi", "v.", "упрекать", "to blame, to reproach"),
        _vocab("必然", "bìrán", "adj.", "неизбежный", "inevitable, certain"),
        _vocab("事先", "shìxiān", "n.", "заранее", "beforehand, in advance"),
        _vocab("舍不得", "shěbude", "v.", "жалко, не хочется расставаться", "to be unwilling to part with"),
        _vocab("后果", "hòuguǒ", "n.", "последствие", "consequence, aftermath"),
        _vocab("屡", "lǚ", "adv.", "неоднократно", "repeatedly, time and again"),
    ]

    grammar = [
        {
            "word": "动词+下来", "pos": "конструкция",
            "explanation": {"ru": "«Глагол + 下来» означает завершение действия, иногда с оттенком отделения или фиксации.",
                            "en": "«Verb + 下来» indicates completion of an action, sometimes with a sense of separation or fixation."},
            "examples": [
                {"zh": "你的论文大概什么时候发表？定下来了吗？", "ru": "Когда примерно опубликуют твою диссертацию? Уже решено?", "en": "When will your thesis be published? Is it settled?"},
                {"zh": "你看，那张纸是从这本书里撕下来的。", "ru": "Смотри, этот лист вырван из этой книги.", "en": "Look, that page was torn out of this book."},
                {"zh": "几局下来，基本上都是不到10分钟我就败下阵来。", "ru": "После нескольких партий я в основном сдавался меньше чем за 10 минут.", "en": "After several games, I usually lost in under ten minutes."},
            ],
            "exercises": [{"type": "fill_blank", "question": "房间里太热了，__。", "answer": "把外套脱下来吧"}],
        },
        {
            "word": "舍不得", "pos": "v.",
            "explanation": {"ru": "«舍不得» — «жаль, не хочется расставаться / тратить / использовать». Утвердительная форма «舍得» обычно в вопросах или сравнениях.",
                            "en": "«舍不得» means 'to be unwilling to part with / spend / use'. The affirmative «舍得» is usually in questions or comparisons."},
            "examples": [
                {"zh": "把你最喜欢的玩具送给小朋友，你舍得吗？", "ru": "Ты готов отдать свою любимую игрушку малышу?", "en": "Would you give your favourite toy to a child?"},
                {"zh": "可惜，大部分人都像你这样，开始不考虑得失，等到后来失去得多了，又开始舍不得，后果就是屡下屡败。", "ru": "Увы, большинство людей, как и ты: сначала не думают о потерях, а позже, потеряв много, начинают жалеть — и в итоге терпят поражение за поражением.", "en": "Alas, most people are like you: at first they ignore gains and losses; later, having lost much, they begrudge — and lose again and again."},
            ],
            "exercises": [{"type": "fill_blank", "question": "这么好的工作，你怎么__？！", "answer": "舍得辞职"}],
        },
    ]

    comparisons = [
        {
            "word_a": "损失", "word_b": "失去",
            "common": {"ru": "Оба глагола означают, что что-то было и исчезло.", "en": "Both verbs mean something that existed is gone."},
            "differences": [
                {"ru": "«损失» — «уменьшение»; может быть существительным.", "en": "«损失» — 'reduction'; can be a noun."},
                {"ru": "«失去» — обычно «полностью лишиться»; не может быть существительным.", "en": "«失去» — usually 'completely lose'; can't be a noun."},
            ],
        },
    ]

    expansion = {
        "topic": {"zh": "家居2 (Домашние принадлежности 2)", "ru": "Домашние принадлежности 2", "en": "Household items 2"},
        "words": [
            {"hanzi": "夹子", "pinyin": "jiāzi", "meaning": {"zh": "", "ru": "зажим, прищепка", "en": "clip, clamp"}},
            {"hanzi": "梳子", "pinyin": "shūzi", "meaning": {"zh": "", "ru": "расчёска", "en": "comb"}},
            {"hanzi": "肥皂", "pinyin": "féizào", "meaning": {"zh": "", "ru": "мыло", "en": "soap"}},
            {"hanzi": "扇子", "pinyin": "shànzi", "meaning": {"zh": "", "ru": "веер", "en": "fan"}},
            {"hanzi": "剪刀", "pinyin": "jiǎndāo", "meaning": {"zh": "", "ru": "ножницы", "en": "scissors"}},
            {"hanzi": "绳子", "pinyin": "shéngzi", "meaning": {"zh": "", "ru": "верёвка", "en": "rope"}},
            {"hanzi": "锁", "pinyin": "suǒ", "meaning": {"zh": "", "ru": "замок; запирать", "en": "lock"}},
            {"hanzi": "叉子", "pinyin": "chāzi", "meaning": {"zh": "", "ru": "вилка", "en": "fork"}},
            {"hanzi": "锅", "pinyin": "guō", "meaning": {"zh": "", "ru": "кастрюля, котёл", "en": "pot, pan"}},
            {"hanzi": "壶", "pinyin": "hú", "meaning": {"zh": "", "ru": "чайник, кувшин", "en": "kettle, pot"}},
            {"hanzi": "盆", "pinyin": "pén", "meaning": {"zh": "", "ru": "таз, миска", "en": "basin, tub"}},
            {"hanzi": "火柴", "pinyin": "huǒchái", "meaning": {"zh": "", "ru": "спички", "en": "matches"}},
        ],
    }

    workbook = {
        "listening": [
            {"type": "mc", "audio": "workbook_27_1.mp3",
             "prompt": {"zh": "男的遇到什么问题了？", "ru": "С какой проблемой столкнулся мужчина?", "en": "What problem did the man encounter?"},
             "options": ["失去了工作", "面试表现不错", "在找实习单位", "得到了试用机会"], "answer": 1},
            {"type": "mc", "audio": "workbook_27_1.mp3",
             "prompt": {"zh": "女的比赛发挥得怎么样？", "ru": "Как выступила женщина на соревновании?", "en": "How did the woman perform in the competition?"},
             "options": ["状态不稳定", "发挥很出色", "成绩不够理想", "一定能拿冠军"], "answer": 0},
        ],
        "reading": [
            {"type": "cloze",
             "text_zh": "有一个韩国家庭，收到别人送的两箱苹果。其中一箱苹果已有些15成熟了，如果不马上吃掉，很快就会烂掉；另一箱比较新鲜，还可以16长一点儿的时间。",
             "blanks": [
                 {"position": 15, "answer": "过分", "options": ["明显", "格外", "过分", "极其"]},
                 {"position": 16, "answer": "保存", "options": ["持续", "保存", "延长", "推迟"]},
             ]},
        ],
        "writing": [
            {"type": "make_sentence", "words": ["估计", "需要", "准确的", "事先做出", "我们"], "answer": "我们需要事先做出准确的估计。"},
            {"type": "make_sentence", "words": ["你", "已经", "一切", "拥有的", "请珍惜"], "answer": "请珍惜你已经拥有的一切。"},
            {"type": "make_sentence", "words": ["把", "吓坏了", "都", "老板的责备", "职员们"], "answer": "老板的责备把职员们都吓坏了。"},
            {"type": "short_essay", "words": ["教训", "把握", "吸取", "原则", "后果"], "min_length": 80},
        ],
    }

    return {
        "title": _t("下棋", "Игра в шахматы", "", "Playing chess", ""),
        "audio_files": {"textbook_1": "textbook_27_1.mp3", "vocab": "vocab_27.mp3", "workbook_27_1": "workbook_27_1.mp3"},
        "warmup": {
            "question": _t("下图中的棋类，你认识多少？请说一说它们的名称。除了这些以外，你还知道其他棋牌运动吗？",
                           "Какие настольные игры на картинках вы знаете? Назовите их. Знаете ли вы другие?",
                           "", "How many board games in the picture do you know? Name them. Do you know other board and card games?"),
            "answers": ["围棋", "国际象棋", "中国象棋"],
        },
        "text_zh": "我父亲是一位象棋教练。那一年，我大学放假回家，父亲要跟我下棋，我高兴地答应了。\n父亲让我先走三步。不到三分钟，我的棋子损失大半，棋盘上空空的，只剩下几个子了。没办法，眼睁睁看着父亲“将军”，我输了。\n我不服气，说：“这次运气不好，再来！”第二局又输了，“这次没发挥好，我们再来”！几局下来，基本上都是不到10分钟我就败下阵来。我有些灰心。父亲看看我说：“你初学棋，输是正常的。但是你要知道输在什么地方，要吸取教训。否则，你就再上下10年，也未必能赢。”\n“我知道，我技术没你好，经验也不足。”\n“这只是次要因素，不是最重要的。”\n“那最重要的是什么？”我奇怪地问。\n“最重要的问题在于你心态不对。你不够珍惜你的棋子。”\n“怎么不珍惜呀？我每走一步，都想半天。”我否认说。\n“那是后来。开始你是这样吗？我仔细观察过，你三分之二的棋子是在前三分之一的时间失去的。这期间你好像很有把握，下棋时不假思索，拿起来就走，失去了也不觉得可惜。因为你觉得棋子很多，失一两个不算什么。后三分之二的时间，你又犯了相反的错误：对棋子过于珍惜，每走一步都过于谨慎，一个棋子也不想失，反而一个一个都失去了。”\n说到这，父亲停下来，把棋子重新在棋盘上摆好，抬起头，看着我，问：“这是一盘待下的棋。我问你，下棋的基本原则是什么？”\n我想也没想，脱口而出：“赢啊！”\n“那是目的。”父亲用责备的眼光看了我一眼，“至于原则，是要考虑得失。有得必然有失，有失才会有得。每走一步，你事先都应该想清楚：为了赢得什么，你愿意失去什么，这样才可能赢。可惜，大部分人都像你这样，开始不考虑得失，等到后来失去得多了，又开始舍不得，后果就是屡下屡败。其实不仅是下棋，人生也是如此啊！”",
        "text_translation": {
            "zh": "",
            "ru": "Мой отец — тренер по сянци. В тот год я приехал домой на университетские каникулы, отец предложил сыграть, и я с радостью согласился.\nОтец дал мне фору в три хода. Не прошло и трёх минут, как я потерял больше половины фигур, доска опустела — остались лишь несколько. Ничего не поделаешь: беспомощно глядя, как отец объявляет «шах!», я проиграл.\nНе смирившись, я сказал: «В этот раз не повезло, ещё раз!» Вторая партия — снова поражение. «На этот раз не вошёл в форму, ещё!» После нескольких партий я в основном сдавался меньше чем за десять минут. Я пал духом. Отец посмотрел на меня и сказал: «Ты только начинаешь играть, проигрывать — нормально. Но ты должен понимать, где проиграл, и извлекать урок. Иначе, сколько бы ты ни играл ещё десять лет, победы можешь так и не добиться».\n«Я знаю, моя техника хуже твоей, и опыта мало».\n«Это лишь второстепенные факторы, не самое главное».\n«А что самое главное?» — удивился я.\n«Самое главное — у тебя неправильный настрой. Ты недостаточно бережёшь свои фигуры».\n«Как это не берегу? Я над каждым ходом думаю по полдня», — возразил я.\n«Это позже. А в начале ты так делал? Я внимательно наблюдал: две трети твоих фигур потеряны в первую треть времени. В тот период ты будто был уверен в себе, играл не задумываясь, хватал и двигал — и о потерях не жалел. Потому что считал: фигур много, потерять одну-две ничего не значит. А в последние две трети ты совершил противоположную ошибку: стал слишком дорожить фигурами, над каждым ходом чрезмерно осторожничал, ни одну фигуру не хотел терять — и растерял их одну за другой».\nТут отец остановился, снова расставил фигуры на доске, поднял голову, взглянул на меня и спросил: «Это партия, которую предстоит играть. Скажи, каков основной принцип игры в шахматы?»\nЯ, не задумываясь, выпалил: «Победить!»\n«Это цель». Отец укоризненно взглянул на меня: «А принцип — это учитывать приобретения и потери. Где приобретение — там неизбежна потеря; есть потеря — будет и приобретение. Перед каждым ходом ты должен заранее ясно понимать: ради какого приобретения ты готов чем пожертвовать — тогда только возможна победа. Увы, большинство людей, как и ты: сначала не думают о приобретениях и потерях, а когда позже теряют много — начинают жалеть; результат — поражение за поражением. И не только в шахматах — в жизни то же самое!»",
            "tk": "", "en": "My father is a Chinese chess coach. That year I came home from university for the holidays; father wanted to play chess with me, and I happily agreed.\nFather gave me three moves' head start. In under three minutes I'd lost most of my pieces — the board was nearly empty, only a few left. Helplessly watching father announce 'check!', I lost.\nUnconvinced, I said: 'Bad luck this time — again!' Second game lost too. 'Didn't play well this time, again!' After several games, I usually lost in under ten minutes. I got discouraged. Father looked at me: 'You're a beginner — losing is normal. But you must know where you lost and learn the lesson. Otherwise, even ten more years of playing may not bring victory.'\n'I know — my skill is worse, and my experience lacking.'\n'Those are secondary factors, not the most important.'\n'Then what is?' I asked, puzzled.\n'The key problem is your attitude. You don't value your pieces enough.'\n'How so? I think half a day over every move!' I protested.\n'That's later. Was it like that at the start? I watched carefully: two-thirds of your pieces were lost in the first third of the time. During that period you seemed confident, playing without thinking, picking up and moving — and not regretting the losses. Because you thought: plenty of pieces, losing one or two is nothing. In the last two-thirds you made the opposite mistake: you valued the pieces too much, were too cautious with every move, unwilling to lose a single one — and lost them one by one.'\nFather paused, reset the pieces on the board, lifted his head, looked at me and asked: 'This is a game yet to be played. Tell me, what is the basic principle of chess?'\nWithout thinking I blurted: 'To win!' 'That's the goal.' Father glanced at me reproachfully. 'The principle is to weigh gains and losses. Where there's gain there is inevitably loss; only with loss comes gain. Before every move you should know clearly: for what gain are you willing to lose what? Only then can you win. Alas, most people are like you: at first they don't weigh gains and losses; later, having lost much, they begrudge — and lose again and again. And not only in chess — in life too!'",
            "uz": "", "tg": "", "id": "", "tr": "",
        },
        "vocabulary": vocab, "grammar": grammar, "comparisons": comparisons, "expansion": expansion,
        "application": {
            "discussion": _t("人生如棋：课文中父亲是怎样教育孩子的？你同意父亲的观点吗？你对“得”与“失”有什么看法？",
                           "Жизнь как шахматы: как отец в тексте воспитывал сына? Согласны ли вы с ним? Что вы думаете о «приобретениях» и «потерях»?",
                           "", "Life is like chess: how did the father educate his child in the text? Do you agree with him? What's your view on 'gains' and 'losses'?"),
            "writing_prompt": {"zh": "请以“得与失”为题，谈谈你的看法。尽量用上本课所学的生词，字数不少于100字。",
                              "ru": "Напишите эссе на тему «Приобретения и потери», используя слова урока, не менее 100 иероглифов.",
                              "en": "Write an essay titled 'Gains and losses', using this lesson's vocabulary, at least 100 characters."},
        },
        "workbook": workbook,
    }


if __name__ == "__main__":
    save(9, 25, lesson25())
    save(9, 26, lesson26())
    save(9, 27, lesson27())
    print("Done.")
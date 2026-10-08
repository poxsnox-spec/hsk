# -*- coding: utf-8 -*-
"""Уроки 22-24 (Unit 8 — 体会教育)."""
from build_hsk5_lower import _vocab, _t, save


def lesson22():
    vocab = [
        _vocab("过分", "guòfèn", "adj.", "чрезмерный", "excessive"),
        _vocab("强调", "qiángdiào", "v.", "подчёркивать", "to emphasize"),
        _vocab("作文", "zuòwén", "n.", "сочинение", "essay, composition"),
        _vocab("观点", "guāndiǎn", "n.", "точка зрения", "idea, opinion"),
        _vocab("客观", "kèguān", "adj.", "объективный", "objective"),
        _vocab("全面", "quánmiàn", "adj.", "всесторонний", "all-round, comprehensive"),
        _vocab("转变", "zhuǎnbiàn", "v.", "менять(ся)", "to change, to transform"),
        _vocab("观念", "guānniàn", "n.", "представление, понятие", "mentality, concept"),
        _vocab("火柴", "huǒchái", "n.", "спичка", "match"),
        _vocab("灰", "huī", "n./adj.", "пепел; серый", "dust; gray"),
        _vocab("一旦", "yídàn", "adv.", "как только; если вдруг", "once, when"),
        _vocab("王宫", "wánggōng", "n.", "королевский дворец", "royal palace"),
        _vocab("王子", "wángzǐ", "n.", "принц", "prince"),
        _vocab("属于", "shǔyú", "v.", "принадлежать", "to belong to"),
        _vocab("对待", "duìdài", "v.", "относиться, обращаться", "to treat, to adopt an attitude"),
        _vocab("交换", "jiāohuàn", "v.", "обменивать(ся)", "to exchange"),
        _vocab("拥有", "yōngyǒu", "v.", "владеть, обладать", "to own, to possess"),
        _vocab("巨大", "jùdà", "adj.", "огромный", "huge, tremendous"),
        _vocab("承认", "chéngrèn", "v.", "признавать", "to admit, to acknowledge"),
        _vocab("人性", "rénxìng", "n.", "человеческая природа", "human nature"),
        _vocab("完美", "wánměi", "adj.", "идеальный", "perfect, flawless"),
        _vocab("难免", "nánmiǎn", "adj.", "неизбежный", "hard to avoid"),
        _vocab("疼爱", "téng'ài", "v.", "горячо любить", "to love dearly"),
        _vocab("平等", "píngděng", "adj.", "равный", "equal"),
        _vocab("自私", "zìsī", "adj.", "эгоистичный", "selfish"),
        _vocab("倾向", "qīngxiàng", "v./n.", "склоняться; тенденция", "to be inclined to; tendency"),
        _vocab("理由", "lǐyóu", "n.", "причина, основание", "reason, ground"),
        _vocab("道德", "dàodé", "n.", "мораль, этика", "morality, ethics"),
        _vocab("自从", "zìcóng", "prep.", "с тех пор как", "ever since"),
        _vocab("童话", "tónghuà", "n.", "сказка", "fairy tale"),
        _vocab("价值", "jiàzhí", "n.", "ценность", "value"),
        _vocab("单纯", "dānchún", "adj.", "простой, чистый", "simple, mere"),
        _vocab("主张", "zhǔzhāng", "v./n.", "настаивать; точка зрения", "to hold, to advocate; view"),
        _vocab("知感", "zhīgǎn", "n.", "восприятие, осознание", "sense, perception"),
    ]

    grammar = [
        {
            "word": "一旦", "pos": "adv.",
            "explanation": {"ru": "«一旦» — наречие, «как только», «если вдруг». Выражает неопределённое время, внезапно наступивший день, либо гипотетическую ситуацию.",
                            "en": "«一旦» is an adverb meaning 'once', 'if ever'. Expresses indefinite time or hypothetical situation."},
            "formula": {"ru": "一旦 + условие, 就 ...", "en": "一旦 + condition, 就 ..."},
            "examples": [
                {"zh": "灰姑娘一旦进了这个王宫，应该怎样对待她的继母？", "ru": "Как только Золушка войдёт во дворец, как ей относиться к мачехе?", "en": "Once Cinderella enters the palace, how should she treat her stepmother?"},
                {"zh": "所谓私人空间，是指我们身体周围的一定的空间，一旦有人闯入这个空间，我们就会感觉不舒服。", "ru": "Личное пространство — это определённое пространство вокруг тела; как только в него вторгается кто-то, нам становится некомфортно.", "en": "Personal space is a certain space around our body; once someone intrudes, we feel uncomfortable."},
            ],
            "exercises": [{"type": "fill_blank", "question": "天冷了，多穿点儿，__。", "answer": "一旦感冒就麻烦了。"}],
        },
        {
            "word": "难免", "pos": "adj.",
            "explanation": {"ru": "«难免» — прилагательное, «трудно избежать, неизбежно».",
                            "en": "«难免» is an adjective meaning 'hard to avoid, inevitable'."},
            "examples": [
                {"zh": "刚开始工作，这样的错误是难免的。", "ru": "В начале работы такие ошибки неизбежны.", "en": "Such mistakes are unavoidable at the start of a job."},
                {"zh": "朋友间难免会产生矛盾、误会甚至是伤害。", "ru": "Между друзьями неизбежно возникают конфликты, недоразумения и даже обиды.", "en": "Between friends there will inevitably be conflicts, misunderstandings, even hurt."},
            ],
            "exercises": [{"type": "fill_blank", "question": "刚刚退休的老人__。", "answer": "难免有些不习惯。"}],
        },
        {
            "word": "自从", "pos": "prep.",
            "explanation": {"ru": "«自从» — предлог, «с тех пор как», указывает на начало действия в прошлом.",
                            "en": "«自从» is a preposition meaning 'ever since', pointing to a past starting point."},
            "formula": {"ru": "自从 + время/событие, ...", "en": "自从 + time/event, ..."},
            "examples": [
                {"zh": "自从城市出现后，它就成为人类生活的中心。", "ru": "С момента появления городов они стали центром человеческой жизни.", "en": "Since cities appeared, they have become the centre of human life."},
                {"zh": "自从我听说了这件事，就开始思考应该如何阅读。", "ru": "С тех пор как я услышал эту историю, я стал думать, как нужно читать.", "en": "Ever since I heard this story, I've been thinking about how to read."},
            ],
            "exercises": [{"type": "fill_blank", "question": "自从我来中国以后，__。", "answer": "我的汉语进步了很多。"}],
        },
    ]

    comparisons = [
        {
            "word_a": "平等", "word_b": "公平",
            "common": {"ru": "Оба прилагательных близки по смыслу, иногда взаимозаменяемы.",
                        "en": "Both adjectives have similar meanings; sometimes interchangeable."},
            "differences": [
                {"ru": "«平等» — акцент на равные права/положение.", "en": "«平等» focuses on equal rights/status."},
                {"ru": "«公平» — акцент на справедливости, беспристрастности.", "en": "«公平» focuses on fairness, impartiality."},
            ],
        },
    ]

    expansion = {
        "topic": {"zh": "写作表达 (Письмо и речь)", "ru": "Письмо и речь", "en": "Writing and expression"},
        "words": [
            {"hanzi": "论文", "pinyin": "lùnwén", "meaning": {"zh": "", "ru": "научная статья", "en": "thesis, paper"}},
            {"hanzi": "主题", "pinyin": "zhǔtí", "meaning": {"zh": "", "ru": "тема", "en": "theme"}},
            {"hanzi": "题目", "pinyin": "tímù", "meaning": {"zh": "", "ru": "заголовок, тема", "en": "title"}},
            {"hanzi": "话题", "pinyin": "huàtí", "meaning": {"zh": "", "ru": "тема разговора", "en": "topic"}},
            {"hanzi": "目录", "pinyin": "mùlù", "meaning": {"zh": "", "ru": "содержание", "en": "contents"}},
            {"hanzi": "提纲", "pinyin": "tígāng", "meaning": {"zh": "", "ru": "план, конспект", "en": "outline"}},
            {"hanzi": "标点", "pinyin": "biāodiǎn", "meaning": {"zh": "", "ru": "пунктуация", "en": "punctuation"}},
            {"hanzi": "废话", "pinyin": "fèihuà", "meaning": {"zh": "", "ru": "болтовня", "en": "nonsense"}},
            {"hanzi": "胡说", "pinyin": "húshuō", "meaning": {"zh": "", "ru": "говорить вздор", "en": "to talk nonsense"}},
        ],
    }

    workbook = {
        "listening": [
            {"type": "mc", "audio": "workbook_22_1.mp3",
             "prompt": {"zh": "女的是什么意思？", "ru": "Что имеет в виду женщина?", "en": "What does the woman mean?"},
             "options": ["要多读书", "要多练习写作", "多读书就能写好作文", "多读书不一定能写好作文"], "answer": 3},
            {"type": "mc", "audio": "workbook_22_1.mp3",
             "prompt": {"zh": "关于这些资料，男的是什么意思？", "ru": "Что мужчина говорит о материалах?", "en": "What does the man say about the materials?"},
             "options": ["这些资料很重要", "报名后就不能改", "女的不太仔细", "男的还没看过"], "answer": 1},
        ],
        "reading": [
            {"type": "cloze",
             "text_zh": "各持己见往往是人与人之间矛盾冲突的重要原因。人们在生活中15会与家人、朋友产生这样那样的矛盾。要避免这种情况出现，需要心理换位——16位置，试着站到对方立场上去思考。",
             "blanks": [
                 {"position": 15, "answer": "难免", "options": ["难道", "难免", "难过", "难受"]},
                 {"position": 16, "answer": "交换", "options": ["转变", "变化", "变", "交换"]},
             ]},
        ],
        "writing": [
            {"type": "make_sentence", "words": ["不强调思考", "而", "单纯地", "是片面的", "主张阅读"], "answer": "单纯地主张阅读而不强调思考是片面的。"},
            {"type": "make_sentence", "words": ["他为公司", "有价值的", "提供了", "很多", "建议"], "answer": "他为公司提供了很多有价值的建议。"},
            {"type": "make_sentence", "words": ["存在着", "仍然", "现在", "男女不平等的", "现象"], "answer": "现在仍然存在着男女不平等的现象。"},
            {"type": "short_essay", "words": ["平等", "观念", "对待", "一旦", "自私"], "min_length": 80},
        ],
    }

    return {
        "title": _t("阅读与思考", "Чтение и размышление", "", "Reading and thinking", ""),
        "audio_files": {"textbook_1": "textbook_22_1.mp3", "vocab": "vocab_22.mp3", "workbook_22_1": "workbook_22_1.mp3"},
        "warmup": {
            "question": _t("请看下面的图片并说说你知道的颜色。你喜欢写作文吗？你觉得有哪些提高写作水平的好方法？请给老师和同学们介绍一下。",
                           "Посмотрите на картинки и назовите цвета. Любите ли вы писать сочинения? Какие есть способы улучшить письмо? Расскажите.",
                           "", "Look at the pictures and name the colors. Do you like writing essays? What methods can improve writing? Tell the class."),
            "answers": ["红", "黄", "绿", "蓝"],
        },
        "text_zh": "很多家长可能过分强调阅读的作用，觉得多读书就能够把作文写得特别好。这个观点是不客观、不全面的，我们需要转变自己的观念。\n我曾经听一位美国的小学老师说，他们十分重视和学生一起讨论问题。比如，他们讨论过《卖火柴的小女孩儿》是写给谁看的，还讨论过灰姑娘的故事。老师讲完故事之后，问同学们：灰姑娘一旦进了这个王宫，成为王子的心上人，她的梦想实现了，一切幸福都属于她之后，这时她应该怎样对待她的继母，应该怎样对待她的两个姐姐？\n为什么要讨论这个问题呢？因为这是一种情感交换。老师和学生通过讨论得出的结论是：一个已经拥有巨大幸福的人，应该原谅和理解那些伤害过自己的人。另外还要承认人性中一些先天的不完美，就是说作为一个母亲，在自己的亲生女儿和不是亲生的灰姑娘之间，难免会更疼爱自己亲生的女儿，很难完全平等地对待她们。可能你觉得继母很自私，但这种行为有自然倾向的理由，与道德没有必然的关系。\n自从我听说了这件事，就开始思考应该如何阅读，除了阅读还应该做什么。你看这个老师在讲童话的时候，已经在有意识地把这种情感影响，甚至把人性的价值判断，都给了孩子们。如果只是单纯地主张阅读而不强调思考，那是片面的。\n“知识”两个字我始终认为它是要分开来谈的，“知”就是知感，“识”就是认识。所谓“知感”就是别人告诉你、说给你听、要求你记住的那一部分。但只有这一部分是不够的，还要有认识、思考。",
        "text_translation": {
            "zh": "",
            "ru": "Многие родители, возможно, слишком подчёркивают роль чтения, полагая, что чем больше читаешь, тем лучше пишешь сочинения. Эта точка зрения необъективна и неполна — нам нужно изменить свои представления.\nЯ как-то слышал от американского учителя начальной школы, что они уделяют большое внимание обсуждению вопросов вместе с учениками. Например, они обсуждали, для кого написана «Девочка со спичками», и сказку о Золушке. После рассказа учитель спросил: как только Золушка войдёт во дворец, станет возлюбленной принца, её мечта осуществится и всё счастье будет ей принадлежать — как ей тогда относиться к мачехе и двум сводным сёстрам?\nЗачем обсуждать это? Потому что это обмен чувствами. Учитель и ученики пришли к выводу: человек, уже обладающий огромным счастьем, должен простить и понять тех, кто его ранил. Кроме того, нужно признать врождённое несовершенство человеческой природы: как мать между родной дочерью и неродной Золушкой непременно будет больше любить свою родную дочь, трудно относиться к ним полностью одинаково. Возможно, вы считаете мачеху эгоистичной, но такое поведение имеет естественные причины и не обязательно связано с моралью.\nС тех пор как я услышал эту историю, я стал думать, как нужно читать и что ещё, кроме чтения, нужно делать. Видите, этот учитель, рассказывая сказку, уже сознательно передавал детям это эмоциональное влияние и даже ценностные суждения о человеческой природе. Если только настаивать на чтении, не подчёркивая размышление, — это односторонне.\nЯ всегда считал, что слово «знание» нужно разделять: «зна-» — это восприятие, «-ние» — это понимание. Восприятие — то, что тебе сказали, сообщили, попросили запомнить. Но этого недостаточно — нужны ещё понимание и размышление.",
            "tk": "", "en": "Many parents may overemphasize the role of reading, thinking that the more one reads, the better one writes. This view is neither objective nor complete — we need to change our mindset.\nI once heard an American primary school teacher say they attach great importance to discussing questions together with students. For example, they discussed for whom The Little Match Girl was written, and the Cinderella story. After telling the story, the teacher asked: once Cinderella enters the palace and becomes the prince's beloved, once her dream is fulfilled and all happiness belongs to her — how should she then treat her stepmother and her two stepsisters?\nWhy discuss this? Because it is an exchange of feelings. Through discussion, teacher and students concluded: a person who already possesses great happiness should forgive and understand those who hurt them. Also, one must acknowledge certain innate imperfections in human nature — as a mother, between her own daughter and non-biological Cinderella, she will inevitably love her own daughter more, hard to treat them entirely equally. You may find the stepmother selfish, but such behaviour has natural grounds and isn't necessarily a matter of morality.\nEver since I heard about this, I began to think about how one should read and what else to do besides reading. See — this teacher, telling a fairy tale, was already consciously passing on this emotional influence and even value judgments about human nature. Merely advocating reading without emphasizing thinking is one-sided.\nI've always held that the word 'knowledge' should be split: 'know-' is perception, '-ledge' is understanding. Perception is the part others tell you, say to you, ask you to remember. But that alone is not enough — you need understanding and reflection.",
            "uz": "", "tg": "", "id": "", "tr": "",
        },
        "vocabulary": vocab, "grammar": grammar, "comparisons": comparisons, "expansion": expansion,
        "application": {
            "discussion": _t("灰姑娘应该怎么做：你读过《灰姑娘》这篇童话吗？如果你是灰姑娘，进入王宫以后，你会怎么对待继母和姐姐？作者认为应该承认人性中一些先天的不完美，你同意他的看法吗？",
                           "Как должна поступить Золушка? Читали ли вы эту сказку? Как бы вы поступили на её месте? Согласны ли вы с автором о врождённом несовершенстве человеческой природы?",
                           "", "What should Cinderella do? Have you read this fairy tale? If you were Cinderella, how would you treat your stepmother and sister? Do you agree with the author's view on innate imperfections?"),
            "writing_prompt": {"zh": "请以“假如我是灰姑娘”为题，谈谈你的看法。尽量用上本课所学的生词，字数不少于100字。",
                              "ru": "Напишите эссе на тему «Если бы я была Золушкой», используя слова урока, не менее 100 иероглифов.",
                              "en": "Write an essay titled 'If I were Cinderella', using this lesson's vocabulary, at least 100 characters."},
        },
        "workbook": workbook,
    }


def lesson23():
    vocab = [
        _vocab("乖", "guāi", "adj.", "послушный", "obedient, well-behaved"),
        _vocab("刻苦", "kèkǔ", "adj.", "усердный", "hardworking, assiduous"),
        _vocab("遵守", "zūnshǒu", "v.", "соблюдать", "to abide by, to observe"),
        _vocab("纪律", "jìlǜ", "n.", "дисциплина", "discipline, rule"),
        _vocab("征求", "zhēngqiú", "v.", "спрашивать (мнение)", "to seek, to ask for"),
        _vocab("念", "niàn", "v.", "учиться, изучать", "to study"),
        _vocab("基本", "jīběn", "adv.", "в основном", "basically, on the whole"),
        _vocab("阶段", "jiēduàn", "n.", "этап", "stage, phase"),
        _vocab("亲爱", "qīn'ài", "adj.", "дорогой, любимый", "dear, beloved"),
        _vocab("违反", "wéifǎn", "v.", "нарушать", "to violate, to go against"),
        _vocab("规矩", "guīju", "n.", "правило, устои", "rule, established practice"),
        _vocab("能干", "nénggàn", "adj.", "способный", "capable"),
        _vocab("讲座", "jiǎngzuò", "n.", "лекция", "lecture"),
        _vocab("出席", "chūxí", "v.", "присутствовать", "to attend, to be present"),
        _vocab("酒吧", "jiǔbā", "n.", "бар", "bar"),
        _vocab("担任", "dānrèn", "v.", "занимать должность", "to serve as, to hold the post of"),
        _vocab("主席", "zhǔxí", "n.", "председатель", "chairperson"),
        _vocab("组织", "zǔzhī", "v.", "организовывать", "to organize"),
        _vocab("外交", "wàijiāo", "n.", "дипломатия", "diplomacy"),
        _vocab("经商", "jīngshāng", "v.", "заниматься торговлей", "to do business"),
        _vocab("目标", "mùbiāo", "n.", "цель", "goal, objective"),
        _vocab("系", "xì", "n.", "факультет", "department (of a university)"),
        _vocab("名牌", "míngpái", "n.", "известный бренд", "famous brand"),
        _vocab("录取", "lùqǔ", "v.", "зачислить, принять", "to enroll, to admit"),
        _vocab("面临", "miànlín", "v.", "стоять перед лицом", "to face, to confront"),
        _vocab("一致", "yízhì", "adj.", "единодушный", "identical, unanimous"),
        _vocab("让步", "ràngbù", "v.", "уступать", "to concede, to give in"),
        _vocab("隐约", "yǐnyuē", "adj.", "смутный, неясный", "indistinct, vague"),
        _vocab("陌生", "mòshēng", "adj.", "незнакомый", "strange, unfamiliar"),
        _vocab("某", "mǒu", "pron.", "некий, некоторый", "some, certain"),
        _vocab("建立", "jiànlì", "v.", "создавать, устанавливать", "to build, to establish"),
        _vocab("单独", "dāndú", "adv.", "отдельно, один", "alone, by oneself"),
        _vocab("沟通", "gōutōng", "v.", "общаться", "to communicate"),
        _vocab("横", "héng", "adj.", "поперёк", "across"),
        _vocab("沙滩", "shātān", "n.", "пляж", "sand beach"),
        _vocab("沉默", "chénmò", "v.", "молчать", "to be silent"),
        _vocab("吻", "wěn", "v.", "целовать", "to kiss"),
        _vocab("忍不住", "rěnbuzhù", "v.", "не удержаться", "cannot help (doing sth.)"),
        _vocab("幸亏", "xìngkuī", "adv.", "к счастью", "fortunately"),
        _vocab("暗", "àn", "adj.", "тёмный", "dark, dim"),
    ]

    grammar = [
        {
            "word": "一致", "pos": "adj./adv.",
            "explanation": {"ru": "«一致» — прилагательное, «без разногласий, единодушный». Как наречие — «вместе, единодушно».",
                            "en": "«一致» is an adjective meaning 'without disagreement, unanimous'. As an adverb — 'together, unanimously'."},
            "examples": [
                {"zh": "但文文跟他们的意见不一致，她坚持要去美国。", "ru": "Но Вэньвэнь была не согласна — она настаивала на поездке в США.", "en": "But Wenwen disagreed — she insisted on going to the US."},
                {"zh": "专家们一致认为这是一种成功的产品，可以放心使用。", "ru": "Специалисты единодушно признали продукт успешным и безопасным в использовании.", "en": "Experts unanimously agreed the product is successful and safe to use."},
            ],
            "exercises": [{"type": "fill_blank", "question": "她是一名酒店服务员，工作很勤奋，__。", "answer": "和大家关系一致很好。"}],
        },
        {
            "word": "某", "pos": "pron.",
            "explanation": {"ru": "«某» — указательное местоимение, «некий, некоторый». Может стоять после фамилии, выражая «некто (не называя)», иногда с негативным оттенком.",
                            "en": "«某» is a demonstrative pronoun meaning 'some, a certain'. Can follow a surname for 'someone (unspecified)', sometimes pejorative."},
            "examples": [
                {"zh": "公司业务员李某闻之大喜，以为自己碰到了一个大买主。", "ru": "Услышав это, некий Ли, торговый агент компании, обрадовался, решив, что нашёл крупного покупателя.", "en": "Hearing this, a certain salesman surnamed Li rejoiced, thinking he'd found a big buyer."},
                {"zh": "在这个陌生的地方，妈妈感到她们好像交换了某种身份。", "ru": "В этом незнакомом месте маме казалось, что они словно поменялись какими-то ролями.", "en": "In this unfamiliar place, mother felt they had somehow swapped roles."},
            ],
            "exercises": [{"type": "translate", "question": "Один известный профессор читал лекцию в некоем университете.", "answer": "一位著名的教授到某大学做演讲。"}],
        },
        {
            "word": "幸亏", "pos": "adv.",
            "explanation": {"ru": "«幸亏» — наречие, «к счастью, благодаря чему-то удалось избежать нежелательного».",
                            "en": "«幸亏» is an adverb meaning 'fortunately, thanks to which something undesirable was avoided'."},
            "examples": [
                {"zh": "幸亏你提醒了我，我今天就去报名。", "ru": "Хорошо, что ты напомнил — сегодня же пойду записываться.", "en": "Good thing you reminded me — I'll register today."},
                {"zh": "医生说这个病人是心脏问题，幸亏送来得及时。", "ru": "Врач сказал, что у пациента проблема с сердцем; к счастью, его доставили вовремя.", "en": "The doctor said it was a heart problem; fortunately he was brought in time."},
            ],
            "exercises": [{"type": "fill_blank", "question": "__，我们今天才没走错路。", "answer": "幸亏你带了地图"}],
        },
    ]

    comparisons = [
        {
            "word_a": "单独", "word_b": "独自",
            "common": {"ru": "Оба наречия означают «один, самостоятельно».", "en": "Both adverbs mean 'alone, by oneself'."},
            "differences": [
                {"ru": "«单独» — акцент на «не вместе с другими».", "en": "«单独» focuses on 'not together with others'."},
                {"ru": "«独自» — акцент на «делать что-то самостоятельно».", "en": "«独自» focuses on 'doing something independently'."},
                {"ru": "«单独» может использоваться с предметами и быть прилагательным.", "en": "«单独» can be used for objects and can be an adjective."},
            ],
        },
    ]

    expansion = {
        "topic": {"zh": "教学 (Обучение)", "ru": "Обучение", "en": "Teaching and study"},
        "words": [
            {"hanzi": "教材", "pinyin": "jiàocái", "meaning": {"zh": "", "ru": "учебник", "en": "textbook"}},
            {"hanzi": "课程", "pinyin": "kèchéng", "meaning": {"zh": "", "ru": "курс", "en": "course"}},
            {"hanzi": "实习", "pinyin": "shíxí", "meaning": {"zh": "", "ru": "практика", "en": "internship"}},
            {"hanzi": "学历", "pinyin": "xuélì", "meaning": {"zh": "", "ru": "образование (уровень)", "en": "academic qualification"}},
            {"hanzi": "本科", "pinyin": "běnkē", "meaning": {"zh": "", "ru": "бакалавриат", "en": "undergraduate"}},
            {"hanzi": "学术", "pinyin": "xuéshù", "meaning": {"zh": "", "ru": "наука, наука академическая", "en": "academic"}},
            {"hanzi": "学问", "pinyin": "xuéwèn", "meaning": {"zh": "", "ru": "знания, учёность", "en": "learning, knowledge"}},
            {"hanzi": "理论", "pinyin": "lǐlùn", "meaning": {"zh": "", "ru": "теория", "en": "theory"}},
            {"hanzi": "资料", "pinyin": "zīliào", "meaning": {"zh": "", "ru": "материалы", "en": "materials"}},
            {"hanzi": "修改", "pinyin": "xiūgǎi", "meaning": {"zh": "", "ru": "править, исправлять", "en": "to revise"}},
            {"hanzi": "发表", "pinyin": "fābiǎo", "meaning": {"zh": "", "ru": "публиковать", "en": "to publish"}},
        ],
    }

    workbook = {
        "listening": [
            {"type": "mc", "audio": "workbook_23_1.mp3",
             "prompt": {"zh": "关于这件事，男的和女的是什么态度？", "ru": "Как относятся к этому мужчина и женщина?", "en": "What are the man's and woman's attitudes?"},
             "options": ["同意他的做法", "反对他的做法", "相信父母会支持他", "应该问父母的意见"], "answer": 3},
            {"type": "mc", "audio": "workbook_23_1.mp3",
             "prompt": {"zh": "牛津大学怎么样？", "ru": "Что известно об Оксфорде?", "en": "What about Oxford?"},
             "options": ["牛津大学不太好", "牛津大学是名校", "她不想去牛津大学", "她没被牛津大学录取"], "answer": 1},
        ],
        "reading": [
            {"type": "cloze",
             "text_zh": "有人哭，是因为伤心；有人哭，是因为激动。而我15，是因为同学们带给我的感动。那天我要代表我们16去参加全校的书法比赛。",
             "blanks": [
                 {"position": 15, "answer": "最难忘的那一次哭", "options": ["每次哭", "最难忘的那一次哭", "从来不哭", "最伤心的那一次哭"]},
                 {"position": 16, "answer": "系", "options": ["系", "某", "念", "暗"]},
             ]},
        ],
        "writing": [
            {"type": "make_sentence", "words": ["她", "遵守纪律的", "是", "乖孩子", "个"], "answer": "她是个遵守纪律的乖孩子。"},
            {"type": "make_sentence", "words": ["被", "是", "我的目标", "录取", "名牌大学"], "answer": "被名牌大学录取是我的目标。"},
            {"type": "make_sentence", "words": ["很善于", "他", "和", "沟通", "陌生人"], "answer": "他很善于和陌生人沟通。"},
            {"type": "short_essay", "words": ["目标", "单独", "基本", "面临", "幸亏"], "min_length": 80},
        ],
    }

    return {
        "title": _t("放手", "Отпустить", "", "Letting go", ""),
        "audio_files": {"textbook_1": "textbook_23_1.mp3", "vocab": "vocab_23.mp3", "workbook_23_1": "workbook_23_1.mp3"},
        "warmup": {
            "question": _t("你觉得这幅图片想告诉我们什么？说说你对这幅图片的理解。请从本课的生词中找出与学校生活有关的词语，试试用它们各说一句话。",
                           "Как вы думаете, что хочет сказать эта картинка? Найдите в словаре урока слова, связанные со школьной жизнью, и составьте с ними предложения.",
                           "", "What do you think this picture tells us? Find school-related words in this lesson's vocabulary and use each in a sentence."),
            "answers": ["主席", "大学"],
        },
        "text_zh": "文文从小是个乖乖女，学习刻苦，遵守纪律。大事小事，尽管妈妈表示也要征求她的意见，但上哪所学校、念什么专业，甚至跟什么人交朋友，基本上都是妈妈说了算。\n可是到了大学阶段，亲爱的女儿竟然违反了乖乖女的各种规矩，越来越有自己的主见，越来越能干、独立了。尽管她的成绩仍然是第一名，但她不再甘于当“好学生”：她逃课去听各种讲座，出席欧盟商会的鸡尾酒会，做志愿者，拍电影，学摄影，泡酒吧，参加了学生会并担任了学生会主席，还组织各种社会活动。妈妈以前要她当外交官的计划，在她眼里“实在没什么意思”，她觉得经商才是自己的目标。\n她放弃了本系保送研究生、放弃了各种工作的面试，坚持要去国外留学，结果12所世界名牌大学录取了她。当面临是否选择牛津大学时，她们全家开会，爸爸妈妈认为应该去，但文文跟他们的意见不一致，她坚持要去美国。\n这一次妈妈让步了。她隐隐约约觉得：自己该完全放手了。没想到，正是妈妈的放手，让风筝越飞越高。\n几年后，文文在美国工作，妈妈去洛杉矶看她。在这个陌生的地方，妈妈感到她们好像交换了某种身份：自己倒像女儿，而文文倒像妈妈。她们建立了一种新的关系。\n最初，妈妈哪儿也不敢去，不能单独出门，不能与人沟通，什么都要靠女儿。后来文文工作忙，就给她地图、车钥匙、机票，鼓励她自己出去。从家门口的超市开始，妈妈越走越远，最后竟然独自把美国横穿了一遍。她说，是女儿的“放手”，让她走得更远。做妈妈的，这才算是真正明白了“放手”的重要。\n2010年3月的一个夜晚，母女俩躺在夏威夷的沙滩上谈心。妈妈第一次为以前对女儿的“不放手”而道歉。文文沉默了很久，最后吻了妈妈一下，轻轻地说：“妈妈，我真的很喜欢现在的你。”妈妈忍不住流下了眼泪。她说：“幸亏那晚天色很暗。”",
        "text_translation": {
            "zh": "",
            "ru": "Вэньвэнь с детства была послушной девочкой: усердно училась, соблюдала дисциплину. По любым вопросам, хотя мама и говорила, что советуется с ней, — какую школу выбрать, какую специальность изучать, даже с кем дружить — в основном решала мама.\nНо в университете дорогая дочь вдруг нарушила все правила примерной девочки, стала всё более самостоятельной, способной и независимой. Хотя её оценки оставались лучшими, она больше не хотела быть «хорошей ученицей»: прогуливала занятия ради лекций, посещала коктейли Торговой палаты ЕС, работала волонтёром, снимала кино, училась фотографии, ходила в бары, вошла в студсовет и стала его председателем, организовывала общественные мероприятия. Мамин план сделать её дипломатом в её глазах был «совсем неинтересен» — она считала своей целью бизнес.\nОна отказалась от рекомендованного поступления в магистратуру на своём факультете, от собеседований на разные работы и настояла на учёбе за границей. В итоге её приняли 12 престижных университетов мира. Когда встал вопрос об Оксфорде, семья собралась на совет: родители считали, что надо ехать туда, но Вэньвэнь была не согласна — она настаивала на США.\nНа этот раз мама уступила. Она смутно почувствовала: пора полностью отпустить. И именно мамино «отпускание» позволило воздушному змею взлететь ещё выше.\nНесколько лет спустя Вэньвэнь работала в США, и мама поехала к ней в Лос-Анджелес. В этом незнакомом месте маме показалось, что они словно поменялись ролями: она стала как дочь, а Вэньвэнь — как мать. Они выстроили новые отношения.\nСначала мама никуда не решалась идти, не могла выйти одна, не могла общаться с людьми — всё приходилось делать через дочь. Потом Вэньвэнь, занятая работой, давала ей карты, ключи от машины, билеты — и подбадривала выходить самой. Начав с магазина у дома, мама уходила всё дальше и в конце концов одна пересекла всю Америку. Она говорит, что именно «отпускание» дочери позволило ей зайти так далеко. Только тогда мама по-настоящему поняла важность «отпускания».\nВ одну ночь марта 2010 года мать и дочь лежали на гавайском пляже и разговаривали по душам. Мама впервые извинилась за прежнее «неотпускание». Вэньвэнь долго молчала, потом поцеловала маму и тихо сказала: «Мама, ты мне сейчас очень нравишься». Мама не удержалась от слёз. Она сказала: «К счастью, в ту ночь было темно».",
            "tk": "", "en": "Wenwen was a well-behaved girl from childhood: she studied hard and followed the rules. About everything, though her mother said she'd consult her, — which school, which major, even which friends — it was basically the mother who decided.\nBut at university, the dear daughter violated every rule of a good girl, becoming more opinionated, more capable, more independent. Though still ranked first, she was no longer content to be a 'good student': she skipped classes to attend lectures, went to EU Chamber cocktail parties, volunteered, made films, studied photography, went to bars, joined the student council and became its chair, and organized various social activities. Her mother's plan for her to become a diplomat seemed to her 'utterly uninteresting' — she thought business was her goal.\nShe gave up a guaranteed graduate spot in her department and interviews for various jobs, insisting on studying abroad. In the end, twelve world-famous universities admitted her. When it came to choosing Oxford, the family held a meeting: her parents thought she should go, but Wenwen disagreed — she insisted on America.\nThis time mother gave in. She vaguely felt: she should completely let go. Unexpectedly, it was precisely mother's letting go that let the kite fly higher.\nA few years later, Wenwen worked in America, and mother went to see her in Los Angeles. In this unfamiliar place, mother felt they had somehow swapped identities: she herself was like the daughter, and Wenwen like the mother. They built a new relationship.\nAt first, mother dared not go anywhere, could not go out alone, could not communicate with people — everything depended on her daughter. Later Wenwen, busy with work, gave her maps, car keys, plane tickets, and encouraged her to go out on her own. Starting from a supermarket near home, mother went further and further, until she actually crossed all of America on her own. She said it was her daughter's 'letting go' that let her go so far. Only then did the mother truly understand the importance of 'letting go.'\nOne night in March 2010, mother and daughter lay on a Hawaiian beach and talked heart to heart. Mother apologised for the first time for her earlier 'not letting go'. Wenwen was silent a long time, then kissed her mother and said softly: 'Mom, I really like the you of now.' Mother couldn't hold back her tears. She said: 'Good thing it was so dark that night.'",
            "uz": "", "tg": "", "id": "", "tr": "",
        },
        "vocabulary": vocab, "grammar": grammar, "comparisons": comparisons, "expansion": expansion,
        "application": {
            "discussion": _t("子女教育：在学习问题上，你和父母有过争吵吗？你和父母交流时，你感觉你们是平等的吗？当你遇到问题或犯了错误时，父母是怎么帮助你的？举例说明。",
                           "Воспитание детей: ссорились ли вы с родителями из-за учёбы? Чувствуете ли вы равенство в общении с ними? Как они помогали вам в трудностях? Приведите пример.",
                           "", "Children's education: have you quarrelled with your parents about studies? Do you feel equal when talking to them? How did they help when you had problems? Give examples."),
            "writing_prompt": {"zh": "请以“我想对父母说的是……”为题，谈谈你和父母之间的关系。尽量用上本课所学的生词，字数不少于100字。",
                              "ru": "Напишите эссе на тему «Что я хочу сказать родителям...», используя слова урока, не менее 100 иероглифов.",
                              "en": "Write an essay titled 'What I want to say to my parents...', using this lesson's vocabulary, at least 100 characters."},
        },
        "workbook": workbook,
    }


def lesson24():
    vocab = [
        _vocab("支教", "zhījiào", "v.", "работать учителем в глубинке", "to volunteer to teach in a backward region"),
        _vocab("行动", "xíngdòng", "n.", "действие, акция", "action, activity"),
        _vocab("家访", "jiāfǎng", "v.", "ходить по домам учеников", "to visit the parents of schoolchildren"),
        _vocab("发言", "fāyán", "v.", "выступать, говорить", "to speak, to make a speech"),
        _vocab("及格", "jígé", "v.", "сдать (экзамен)", "to pass an exam"),
        _vocab("交往", "jiāowǎng", "v.", "общаться, поддерживать отношения", "to associate, to contact"),
        _vocab("家务", "jiāwù", "n.", "домашние дела", "household duties"),
        _vocab("体贴", "tǐtiē", "adj.", "чуткий, заботливый", "thoughtful, considerate"),
        _vocab("排练", "páiliàn", "v.", "репетировать", "to rehearse"),
        _vocab("蝴蝶", "húdié", "n.", "бабочка", "butterfly"),
        _vocab("舞蹈", "wǔdǎo", "n.", "танец", "dance"),
        _vocab("冠军", "guànjūn", "n.", "чемпион, первое место", "champion, first-prize winner"),
        _vocab("鼓掌", "gǔzhǎng", "v.", "аплодировать", "to applaud"),
        _vocab("用功", "yònggōng", "adj.", "старательный, прилежный", "hardworking, diligent"),
        _vocab("进步", "jìnbù", "v.", "делать успехи", "to make progress, to improve"),
        _vocab("题目", "tímù", "n.", "заголовок, тема", "title"),
        _vocab("朗读", "lǎngdú", "v.", "читать вслух", "to read aloud"),
        _vocab("温柔", "wēnróu", "adj.", "нежный, мягкий", "gentle"),
        _vocab("热烈", "rèliè", "adj.", "горячий, бурный", "enthusiastic, ardent"),
        _vocab("勇气", "yǒngqì", "n.", "смелость", "courage"),
        _vocab("青壮年", "qīng-zhuàngnián", "n.", "молодёжь и люди среднего возраста", "young and middle-aged adults"),
        _vocab("闯", "chuǎng", "v.", "пробиваться, идти в большой мир", "to go around to accomplish goals"),
        _vocab("留守", "liúshǒu", "v.", "оставаться дома (о детях, стариках)", "to stay behind"),
        _vocab("主题", "zhǔtí", "n.", "тема", "theme, subject"),
        _vocab("地理", "dìlǐ", "n.", "география", "geography"),
        _vocab("采访", "cǎifǎng", "v.", "интервьюировать", "to interview"),
        _vocab("利用", "lìyòng", "v.", "использовать", "to utilize, to make use of"),
        _vocab("空闲", "kòngxián", "adj.", "свободный, досуг", "leisurely, free"),
        _vocab("指导", "zhǐdǎo", "v.", "руководить, направлять", "to guide, to instruct"),
        _vocab("培训", "péixùn", "v.", "обучать, тренировать", "to train"),
        _vocab("建设", "jiànshè", "v.", "строить, развивать", "to build, to construct"),
        _vocab("操心", "cāoxīn", "v.", "беспокоиться, заботиться", "to worry about, to be concerned"),
        _vocab("承担", "chéngdān", "v.", "брать на себя", "to undertake, to shoulder"),
        _vocab("义务", "yìwù", "n.", "обязанность, долг", "duty, obligation"),
        _vocab("艰巨", "jiānjù", "adj.", "трудный, ответственный", "arduous, formidable"),
        _vocab("力量", "lìliàng", "n.", "сила, мощь", "strength, capability"),
        _vocab("收获", "shōuhuò", "n.", "урожай; приобретение", "gain"),
    ]

    grammar = [
        {
            "word": "行动", "pos": "v./n.",
            "explanation": {"ru": "«行动» как глагол — «двигаться, действовать». Как существительное — «действие, акция».",
                            "en": "«行动» as a verb means 'to move, to act'. As a noun — 'action, activity'."},
            "examples": [
                {"zh": "他运动时受伤了，行动不便。", "ru": "Он получил травму на тренировке — двигаться неудобно.", "en": "He was injured exercising — hard to move."},
                {"zh": "郝老师到云南参加支教行动。", "ru": "Учительница Хао отправилась в Юньнань участвовать в программе добровольного преподавания.", "en": "Teacher Hao went to Yunnan to join a volunteer teaching programme."},
                {"zh": "我们应该勇敢面对困难，迅速采取行动，主动承担责任。", "ru": "Мы должны смело встречать трудности, быстро действовать и активно брать на себя ответственность.", "en": "We should face difficulties bravely, act quickly, and shoulder responsibility."},
            ],
            "exercises": [{"type": "fill_blank", "question": "好久不见了，你最近在忙什么呢？__。", "answer": "我参加了一个公益行动。"}],
        },
        {
            "word": "义务", "pos": "n./adj.",
            "explanation": {"ru": "«义务» как существительное — «юридическая или моральная обязанность». Как прилагательное — «бесплатный, неоплачиваемый».",
                            "en": "«义务» as a noun — 'legal or moral duty'. As an adjective — 'unpaid, voluntary'."},
            "examples": [
                {"zh": "不过，现在我们明白了，建设家乡，人人有责，我们也要承担这个义务。", "ru": "Но теперь мы поняли: строить родной край — дело каждого, мы тоже должны нести эту обязанность.", "en": "But now we understand: building our hometown is everyone's responsibility — we must shoulder this duty too."},
                {"zh": "我们每个学期都要至少参加三次义务劳动。", "ru": "Каждый семестр мы должны не менее трёх раз участвовать в субботниках.", "en": "Every semester we must take part in at least three voluntary work sessions."},
            ],
            "exercises": [{"type": "translate", "question": "Родители обязаны заботиться о детях.", "answer": "父母对子女有抚养的义务。"}],
        },
    ]

    comparisons = [
        {
            "word_a": "发言", "word_b": "发表",
            "common": {"ru": "Оба глагола связаны с выражением мнений.", "en": "Both verbs relate to expressing opinions."},
            "differences": [
                {"ru": "«发言» — говорить на собрании/уроке; может быть существительным (высказывание).", "en": "«发言» — to speak at a meeting/class; can be a noun (statement)."},
                {"ru": "«发表» — публично излагать мнение или печатать статью.", "en": "«发表» — to publicly state an opinion or publish an article."},
                {"ru": "«发言» — разделяемый глагол (можно вставить элементы), не принимает дополнение.", "en": "«发言» is a separable verb (elements can be inserted), doesn't take an object."},
            ],
        },
    ]

    expansion = {
        "topic": {"zh": "教学2 (Обучение 2)", "ru": "Обучение 2", "en": "Teaching 2"},
        "words": [
            {"hanzi": "测验", "pinyin": "cèyàn", "meaning": {"zh": "", "ru": "тест, проверка", "en": "test, quiz"}},
            {"hanzi": "实验", "pinyin": "shíyàn", "meaning": {"zh": "", "ru": "эксперимент", "en": "experiment"}},
            {"hanzi": "抄", "pinyin": "chāo", "meaning": {"zh": "", "ru": "списывать, копировать", "en": "to copy"}},
            {"hanzi": "试卷", "pinyin": "shìjuàn", "meaning": {"zh": "", "ru": "экзаменационный лист", "en": "exam paper"}},
            {"hanzi": "夏令营", "pinyin": "xiàlìngyíng", "meaning": {"zh": "", "ru": "летний лагерь", "en": "summer camp"}},
            {"hanzi": "操场", "pinyin": "cāochǎng", "meaning": {"zh": "", "ru": "спортплощадка", "en": "playground"}},
            {"hanzi": "用功", "pinyin": "yònggōng", "meaning": {"zh": "", "ru": "прилежный", "en": "hardworking"}},
            {"hanzi": "辅导", "pinyin": "fǔdǎo", "meaning": {"zh": "", "ru": "репетиторство", "en": "to tutor"}},
            {"hanzi": "收获", "pinyin": "shōuhuò", "meaning": {"zh": "", "ru": "приобретение, урожай", "en": "gain, harvest"}},
            {"hanzi": "铃", "pinyin": "líng", "meaning": {"zh": "", "ru": "звонок", "en": "bell"}},
            {"hanzi": "退步", "pinyin": "tuìbù", "meaning": {"zh": "", "ru": "регресс", "en": "to regress"}},
            {"hanzi": "改正", "pinyin": "gǎizhèng", "meaning": {"zh": "", "ru": "исправлять", "en": "to correct"}},
        ],
    }

    workbook = {
        "listening": [
            {"type": "mc", "audio": "workbook_24_1.mp3",
             "prompt": {"zh": "赵福根是什么样的人？", "ru": "Каким был Чжао Фугэнь?", "en": "What kind of person was Zhao Fugen?"},
             "options": ["成绩很好", "不爱发言", "喜欢逃课", "交坏朋友"], "answer": 1},
            {"type": "mc", "audio": "workbook_24_1.mp3",
             "prompt": {"zh": "女的在做什么？", "ru": "Что делает женщина?", "en": "What is the woman doing?"},
             "options": ["考虑上网课", "报名上网课", "在试听网课", "正在上网课"], "answer": 0},
        ],
        "reading": [
            {"type": "cloze",
             "text_zh": "各位老师，我院五年前曾经公开征集听力考试试题，进行试题库15，当时工作取得了很好的效果。本学期，学院计划开展新题库的有关工作。",
             "blanks": [
                 {"position": 15, "answer": "建设", "options": ["建立", "建筑", "建设", "建议"]},
             ]},
        ],
        "writing": [
            {"type": "make_sentence", "words": ["是", "每个人的", "促进", "义务", "社会进步"], "answer": "促进社会进步是每个人的义务。"},
            {"type": "make_sentence", "words": ["经常利用", "我们", "刘老师", "来指导", "空闲时间"], "answer": "刘老师经常利用空闲时间来指导我们。"},
            {"type": "make_sentence", "words": ["既温柔", "的人", "又体贴", "是个", "她丈夫"], "answer": "她丈夫是个既温柔又体贴的人。"},
            {"type": "short_essay", "words": ["义务", "勇气", "利用", "承担", "行动"], "min_length": 80},
        ],
    }

    return {
        "title": _t("支教行动", "Помощь сельским школам", "", "Volunteer teaching", ""),
        "audio_files": {"textbook_1": "textbook_24_1.mp3", "vocab": "vocab_24.mp3", "workbook_24_1": "workbook_24_1.mp3"},
        "warmup": {
            "question": _t("中国有这样一些志愿者，他们会去经济不太发达的地区或农村的学校当老师，帮助那里的孩子学习。你听说过没有？你对志愿者有什么看法？",
                           "В Китае есть волонтёры, которые едут в отстающие регионы и сельские школы учить детей. Слышали ли вы о них? Что вы думаете о добровольцах?",
                           "", "In China, some volunteers go to underdeveloped regions or rural schools to teach and help children. Have you heard of them? What do you think of volunteers?"),
            "answers": ["冠军", "支教"],
        },
        "text_zh": "来云南支教一年多，郝琳硕老师自己也记不清有多少次家访了。刚到时，一位叫赵福根的男生引起了她的注意。他上课从不发言，很多课不及格，平时也几乎不和同学交往。\n郝老师家访后得知，赵福根的父亲去世了，姐姐在外打工，他家里很穷，还得帮着妈妈做家务，是个体贴孝顺的孩子。“和他妈妈聊天才知道他很喜欢跳舞，”郝老师说，“我觉得这是个机会！”她鼓励福根在学校艺术节上表演，每周二带着他一起去找音乐老师排练。表演时，福根的蝴蝶舞得了舞蹈组的冠军，台下的同学们鼓起掌来，齐声地喊着“福根”的名字……\n之后，赵福根学习用功了，成绩也逐渐进步。他写了一篇题目为《那天的舞蹈和掌声》的作文，得了全班最高分，他朗读了自己的作文：“郝老师来到我家，那是第一次有老师来。她非常温柔……我永远都忘不了那热烈的掌声和同学们送我的糖，甜甜的。我感觉在学校也有人爱我了，我开始有勇气……”\n郝老师发现，山里的青壮年都出去闯世界，只有老人、孩子留守，“他们出去了还回来吗？大山以后谁来负责”？于是，郝老师组织了一个8周的研究型学习活动，主题是“让家乡的明天更美好”。她鼓励学生寻找村子的问题，通过了解历史地理情况、采访村里的老人、小组讨论等，最终提出解决方案。她和其他志愿者利用午休、周末等空闲时间给学生们指导和培训。\n学生们说：“以前，我们总认为建设家乡是大人的事，用不着我们操心。不过，现在我们明白了，建设家乡，人人有责，我们也要承担这个义务。这个任务很艰巨，我们要尽自己最大的力量。”\n郝琳硕觉得自己的收获远多于给孩子们的。“不管以后在哪儿，我都会继续用我的力量影响山里的孩子们，因为他们是国家的未来与希望。”",
        "text_translation": {
            "zh": "",
            "ru": "Приехав в Юньнань учительствовать больше года назад, Хао Линьшо и сама не могла сосчитать, сколько раз ходила по домам учеников. Приехав, она заметила мальчика по имени Чжао Фугэнь. Он никогда не выступал на уроках, по многим предметам не сдавал, почти не общался с одноклассниками.\nПосле визита домой Хао узнала: отец Чжао Фугэня умер, старшая сестра работает в городе, семья очень бедная — мальчик помогает матери по дому, чуткий и почтительный ребёнок. «Поговорив с его матерью, я поняла — он очень любит танцевать», — сказала учительница Хао. — «Я почувствовала: вот шанс!» Она подбодрила Фугэня выступить на школьном празднике искусств, каждое воскресенье водила его к учителю музыки на репетицию. На выступлении танец бабочки Фугэня взял первое место в танцевальной категории; ученики в зале зааплодировали и хором выкрикивали его имя...\nПосле этого Чжао Фугэнь стал старательнее учиться, оценки постепенно улучшались. Он написал сочинение «Тот танец и аплодисменты» и получил высший балл в классе; мальчик прочёл его вслух: «Учительница Хао пришла к нам домой — первый раз учитель пришёл к нам. Она очень нежная... Я никогда не забуду те бурные аплодисменты и конфеты, что подарили одноклассники — такие сладкие. Я почувствовал, что в школе меня тоже любят, у меня появилась смелость...»\nУчительница Хао заметила: все молодые и взрослые мужчины в горах уходят «покорять мир», остаются лишь старики да дети — «вернутся ли они? Кто возьмёт на себя ответственность за горы в будущем?» Тогда Хао организовала 8-недельную исследовательскую учебную программу на тему «Сделать завтра родного края прекраснее». Она подбадривала учеников искать проблемы деревни, изучать историю и географию, брать интервью у стариков, обсуждать в группах и в итоге предлагать решения. Вместе с другими волонтёрами она использовала обеденные перерывы и выходные, чтобы консультировать и обучать школьников.\nУченики говорили: «Раньше мы считали, что строить родной край — дело взрослых, нам не о чем беспокоиться. Но теперь мы поняли: строить родной край — дело каждого, мы тоже должны нести эту обязанность. Задача очень трудная — мы приложим все свои силы».\nХао Линьшо считала, что получила гораздо больше, чем дала детям. «Где бы я ни была в будущем, я продолжу своими силами влиять на детей в горах — ведь они будущее и надежда страны».",
            "tk": "", "en": "Having spent over a year volunteering in Yunnan, Teacher Hao Linshuo could no longer count how many home visits she'd made. On arriving, one boy caught her attention — Zhao Fugen. He never spoke in class, failed many subjects, and hardly socialized with classmates.\nAfter visiting his home, Teacher Hao learned: Fugen's father had died, his older sister worked away, the family was very poor, and he helped his mother with housework — a thoughtful and filial child. 'Only after chatting with his mother did I learn he loves dancing,' said Teacher Hao. 'I felt this was an opportunity!' She encouraged Fugen to perform at the school arts festival, taking him every Tuesday to rehearse with the music teacher. During the performance, Fugen's butterfly dance won first prize in the dance category; classmates applauded and chanted his name...\nAfterwards, Zhao Fugen studied harder, his grades gradually improving. He wrote an essay titled 'That Day's Dance and Applause' and got the top score in class; he read it aloud: 'Teacher Hao came to my home — it was the first time a teacher had come. She was very gentle... I'll never forget the enthusiastic applause and the sweets my classmates gave me — so sweet. I felt that at school someone loved me too, and I began to have courage...'\nTeacher Hao noticed that young adults in the mountains all went out to seek their fortunes, leaving only the elderly and children behind — 'Will they come back? Who will take responsibility for the mountains?' So Teacher Hao organized an 8-week research-learning activity themed 'Making our hometown's tomorrow better.' She encouraged students to find the village's problems, understand its history and geography, interview the elderly, hold group discussions, and ultimately propose solutions. She and other volunteers used lunch breaks and weekends to guide and train the students.\nThe students said: 'We used to think building our hometown was adults' business, nothing for us to worry about. But now we understand: building our hometown is everyone's responsibility, and we must shoulder this duty. This task is arduous — we will do our utmost.'\nHao Linshuo felt her gains far exceeded what she gave the children. 'Wherever I go from now on, I will continue to use my strength to influence the children in the mountains — for they are the future and hope of the nation.'",
            "uz": "", "tg": "", "id": "", "tr": "",
        },
        "vocabulary": vocab, "grammar": grammar, "comparisons": comparisons, "expansion": expansion,
        "application": {
            "discussion": _t("外出的农民工：青壮年外出打工对农村可能产生什么影响？对城市可能产生什么影响？你认为，政府应该怎么帮助这些老人、孩子和农民工？",
                           "Уезжающие на заработки: как отъезд молодёжи влияет на деревню? На город? Как государство должно помогать оставшимся старикам и детям?",
                           "", "Migrant workers: what impact does young people leaving to work have on villages? On cities? How should the government help the elderly, children, and migrant workers?"),
            "writing_prompt": {"zh": "请以“大山的未来谁负责”为题，谈谈你的看法。尽量用上本课所学的生词，字数不少于100字。",
                              "ru": "Напишите эссе на тему «Кто в ответе за будущее гор», используя слова урока, не менее 100 иероглифов.",
                              "en": "Write an essay titled 'Who is responsible for the future of the mountains', using this lesson's vocabulary, at least 100 characters."},
        },
        "workbook": workbook,
    }


if __name__ == "__main__":
    save(8, 22, lesson22())
    save(8, 23, lesson23())
    save(8, 24, lesson24())
    print("Done.")
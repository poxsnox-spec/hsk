# -*- coding: utf-8 -*-
"""Дополнительные уроки HSK 5 (下册) — 20, 21 (Unit 7)."""
from build_hsk5_lower import _vocab, _t, save


def lesson20():
    vocab = [
        _vocab("摊", "tān", "n.", "ларёк, палатка", "stall, stand"),
        _vocab("出版", "chūbǎn", "v.", "публиковать", "to publish"),
        _vocab("连环画", "liánhuánhuà", "n.", "комикс", "picture-story book"),
        _vocab("年代", "niándài", "n.", "десятилетие, годы", "decade of a century"),
        _vocab("单调", "dāndiào", "adj.", "однообразный", "monotonous, dull"),
        _vocab("网络", "wǎngluò", "n.", "интернет, сеть", "network, web"),
        _vocab("动画片", "dònghuàpiàn", "n.", "мультфильм", "animated cartoon"),
        _vocab("娱乐", "yúlè", "n./v.", "развлечение; развлекать", "entertainment; to entertain"),
        _vocab("无数", "wúshù", "adj.", "бесчисленный", "countless, innumerable"),
        _vocab("青少年", "qīng-shàonián", "n.", "подростки, молодёжь", "youngsters, teenagers"),
        _vocab("从事", "cóngshì", "v.", "заниматься чем-л.", "to engage in"),
        _vocab("毫无", "háowú", "adv.", "вовсе не, ничуть", "not in the least"),
        _vocab("疑问", "yíwèn", "n.", "сомнение, вопрос", "question, doubt"),
        _vocab("棚子", "péngzi", "n.", "навес, лачуга", "shed, shack"),
        _vocab("砖头", "zhuāntou", "n.", "кирпич", "brick"),
        _vocab("支", "zhī", "v.", "подпирать; счётное слово", "to prop up; classifier for sticks"),
        _vocab("粗糙", "cūcāo", "adj.", "грубый, шероховатый", "rough, crude"),
        _vocab("木头", "mùtou", "n.", "дерево, древесина", "wood, timber"),
        _vocab("题材", "tícái", "n.", "тема, сюжет", "theme, subject matter"),
        _vocab("翻", "fān", "v.", "переворачивать, листать", "to turn over"),
        _vocab("搭", "dā", "v.", "вешать, класть поверх", "to hang over, to lay over"),
        _vocab("整齐", "zhěngqí", "adj.", "аккуратный, ровный", "tidy, orderly"),
        _vocab("年纪", "niánjì", "n.", "возраст", "age"),
        _vocab("身材", "shēncái", "n.", "фигура, телосложение", "figure, stature"),
        _vocab("成人", "chéngrén", "n.", "взрослый", "adult"),
        _vocab("册", "cè", "m.", "том, книга (счётн.)", "volume"),
        _vocab("假如", "jiǎrú", "conj.", "если, предположим", "if, in case"),
        _vocab("登记", "dēngjì", "v.", "регистрировать", "to register"),
        _vocab("记录", "jìlù", "n./v.", "запись; записывать", "record; to record"),
        _vocab("手续", "shǒuxù", "n.", "процедура, формальности", "procedure"),
        _vocab("办理", "bànlǐ", "v.", "оформлять, вести дела", "to handle, to deal with"),
        _vocab("押金", "yājīn", "n.", "залог", "cash pledge, deposit"),
        _vocab("凭", "píng", "v./prep.", "полагаться; на основании", "to rely on; on the basis of"),
        _vocab("印刷", "yìnshuā", "v.", "печатать", "to print"),
        _vocab("涨", "zhǎng", "v.", "расти, подниматься", "to rise, to go up"),
        _vocab("收藏", "shōucáng", "v.", "коллекционировать", "to collect, to store up"),
    ]

    grammar = [
        {
            "word": "动词+得/不+起", "pos": "конструкция",
            "explanation": {
                "ru": "Конструкция «глагол + 得/不 + 起» означает, что субъект (не) может позволить себе или (не) способен выдержать какое-либо действие.",
                "en": "The pattern 'verb + 得/不 + 起' means the subject can (or cannot) afford or endure a certain action.",
            },
            "formula": {"ru": "глагол + 得/不 + 起", "en": "verb + 得/不 + 起"},
            "examples": [
                {"zh": "这对于那些想看又买不起书的人来说，只用很少的钱就能看一本。", "ru": "Для тех, кто хочет читать, но не может позволить себе покупать книги, — можно прочесть за копейки.", "en": "For those who want to read but can't afford books, they can read one for very little money."},
                {"zh": "古时候，有个十分好学的年轻人，但他家里很穷，买不起灯。", "ru": "В древности был очень любознательный юноша, но семья его была так бедна, что не могла позволить себе лампу.", "en": "In ancient times, a studious young man's family was too poor to afford a lamp."},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "我们应该降低价格，__。", "answer": "让老百姓买得起。"},
            ],
        },
        {
            "word": "支", "pos": "v./m.",
            "explanation": {
                "ru": "«支» как глагол означает «подпирать, поддерживать». Как счётное слово используется для музыкальных произведений, отрядов и продолговатых предметов.",
                "en": "«支» as a verb means 'to prop up'. As a classifier it's used for musical works, teams, or stick-like objects.",
            },
            "examples": [
                {"zh": "他的两只手放在桌上，支着脑袋，正在想事情。", "ru": "Он положил руки на стол и подпёр голову — о чём-то думал.", "en": "He rested his hands on the table, propping up his head, thinking."},
                {"zh": "给他十支枪，他就能拉起一支军队来。", "ru": "Дайте ему десять ружей — и он соберёт целую армию.", "en": "Give him ten rifles, and he can raise an army."},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "快，这张桌子坏了，__。", "answer": "用砖头支一下。"},
            ],
        },
        {
            "word": "凭", "pos": "v./prep.",
            "explanation": {
                "ru": "«凭» как глагол — «опираться, полагаться». Как предлог — «на основании, по», в конструкции «凭 + объект + глагол».",
                "en": "«凭» as a verb means 'to rely on'. As a preposition — 'on the basis of', in the pattern '凭 + object + verb'.",
            },
            "formula": {"ru": "凭 + сущ. + глагол", "en": "凭 + noun + verb"},
            "examples": [
                {"zh": "干工作不能光凭经验，还要有创新。", "ru": "В работе нельзя полагаться только на опыт — нужны и инновации.", "en": "You can't rely only on experience in work — you also need innovation."},
                {"zh": "印象中似乎没有什么押金，全凭信用。", "ru": "Кажется, залога не было — всё на доверии.", "en": "I don't recall any deposit — it was all based on trust."},
                {"zh": "请旅客们准备好车票，凭票进站。", "ru": "Пассажиры, приготовьте билеты — вход по билетам.", "en": "Passengers, please have your tickets ready — entry by ticket."},
            ],
            "exercises": [
                {"type": "translate", "question": "Как вы нашли этот дом?", "answer": "你是凭什么找到这座房子的？"},
            ],
        },
    ]

    comparisons = [
        {
            "word_a": "记录", "word_b": "纪录",
            "common": {"ru": "Оба могут обозначать «запись, документация». Часто путают.", "en": "Both can mean 'record, documentation' and are often confused."},
            "differences": [
                {"ru": "«记录» — глагол «записывать» или существительное «запись» (материал, человек).", "en": "«记录» — verb 'to record' or noun 'record' (material, person)."},
                {"ru": "«纪录» — существительное, обозначает «рекорд» или документальный фильм.", "en": "«纪录» — noun meaning 'record (best result)' or documentary."},
            ],
        },
    ]

    expansion = {
        "topic": {"zh": "单位、场所 (Организации и места)", "ru": "Организации и места", "en": "Organizations and places"},
        "words": [
            {"hanzi": "俱乐部", "pinyin": "jùlèbù", "meaning": {"zh": "", "ru": "клуб", "en": "club"}},
            {"hanzi": "幼儿园", "pinyin": "yòu'éryuán", "meaning": {"zh": "", "ru": "детский сад", "en": "kindergarten"}},
            {"hanzi": "博物馆", "pinyin": "bówùguǎn", "meaning": {"zh": "", "ru": "музей", "en": "museum"}},
            {"hanzi": "酒吧", "pinyin": "jiǔbā", "meaning": {"zh": "", "ru": "бар", "en": "bar"}},
            {"hanzi": "法院", "pinyin": "fǎyuàn", "meaning": {"zh": "", "ru": "суд", "en": "court"}},
            {"hanzi": "海关", "pinyin": "hǎiguān", "meaning": {"zh": "", "ru": "таможня", "en": "customs"}},
            {"hanzi": "生产", "pinyin": "shēngchǎn", "meaning": {"zh": "", "ru": "производить", "en": "to produce"}},
            {"hanzi": "发明", "pinyin": "fāmíng", "meaning": {"zh": "", "ru": "изобретать", "en": "to invent"}},
            {"hanzi": "设计", "pinyin": "shèjì", "meaning": {"zh": "", "ru": "проектировать", "en": "to design"}},
            {"hanzi": "业务", "pinyin": "yèwù", "meaning": {"zh": "", "ru": "дело, бизнес", "en": "business"}},
            {"hanzi": "项目", "pinyin": "xiàngmù", "meaning": {"zh": "", "ru": "проект", "en": "project"}},
            {"hanzi": "效率", "pinyin": "xiàolù", "meaning": {"zh": "", "ru": "эффективность", "en": "efficiency"}},
            {"hanzi": "合法", "pinyin": "héfǎ", "meaning": {"zh": "", "ru": "законный", "en": "legal"}},
            {"hanzi": "公平", "pinyin": "gōngpíng", "meaning": {"zh": "", "ru": "справедливый", "en": "fair"}},
        ],
    }

    workbook = {
        "listening": [
            {
                "type": "mc", "audio": "workbook_20_1.mp3",
                "prompt": {"zh": "男的是什么意思？", "ru": "Что имеет в виду мужчина?", "en": "What does the man mean?"},
                "options": ["很有收藏价值", "内容过时陈旧", "不值得再保留", "《西游记》最好看"],
                "answer": 0,
            },
            {
                "type": "mc", "audio": "workbook_20_1.mp3",
                "prompt": {"zh": "女的遇到什么问题了？", "ru": "С какой проблемой столкнулась женщина?", "en": "What problem did the woman run into?"},
                "options": ["没带够押金", "办理的人多", "图书馆闭馆", "手续太复杂"],
                "answer": 1,
            },
        ],
        "reading": [
            {
                "type": "cloze",
                "text_zh": "世界球王贝利在20多年的足球生涯里，15过1364场比赛，共踢进1282个球，并创造了一个队员在一场比赛中射进8个球的16。",
                "blanks": [
                    {"position": 15, "answer": "参加", "options": ["参加", "参与", "投入", "举办"]},
                    {"position": 16, "answer": "纪录", "options": ["记录", "纪录", "成果", "机会"]},
                ],
            },
        ],
        "writing": [
            {"type": "make_sentence", "words": ["了", "史学家", "提出", "不少疑问", "对这个问题"], "answer": "史学家对这个问题提出了不少疑问。"},
            {"type": "make_sentence", "words": ["的", "粗糙", "这本书", "比较", "印刷质量"], "answer": "这本书的印刷质量比较粗糙。"},
            {"type": "make_sentence", "words": ["了", "从事", "周先生", "文艺创作", "已经很多年"], "answer": "周先生从事文艺创作已经很多年了。"},
            {"type": "short_essay", "words": ["手续", "押金", "记录", "办理", "登记"], "min_length": 80},
        ],
    }

    return {
        "title": _t("小人书摊", "Ларьки с комиксами", "", "Picture-story book stalls", ""),
        "audio_files": {"textbook_1": "textbook_20_1.mp3", "vocab": "vocab_20.mp3", "workbook_20_1": "workbook_20_1.mp3"},
        "warmup": {
            "question": _t(
                "请看下面的图片，试着找出本课跟它们有关的生词。请问问你的同学或朋友，他们小时候有哪些印象深刻的娱乐活动？现在还有没有这样的活动？",
                "Посмотрите на картинки и найдите слова из словаря урока. Спросите друзей, какие развлечения были яркими в их детстве. Есть ли они сейчас?",
                "",
                "Look at the pictures and find related vocabulary. Ask friends what entertainment left an impression in their childhood. Does it still exist?",
            ),
            "answers": ["成人", "连环画"],
        },
        "text_zh": "小人书，是一种以书的形式出版的连环画。在二十世纪五六十年代，那时候生活很单调，没有网络，没有动画片，读小人书是儿童最主要的娱乐之一。不仅小孩子爱看，还有无数的青少年和大人也爱看。\n随着小人书的流行，出现了从事租书业务的小人书摊，这对于那些想看又买不起书的人来说，只用很少的钱就能看一本，毫无疑问是件大好事。\n记得小时候，我家附近就有个小人书摊，就是一进街口靠墙的一个小棚子，里面用几块砖头支着粗糙的木头板子供人们坐着看书。棚子里有一张床板摆着各种题材的小人书，墙边还拉了几根绳子，一本书翻开搭在上面，五颜六色的，很好看。为了减少损坏程度，每本小人书都用牛皮纸加了层封皮，封皮上用毛笔写上书名，整齐漂亮的毛笔字能充分地显示出书摊主人的文化水平。摊主是位上了年纪、身材瘦小的老人，总是穿着一件灰色长衫，静静地坐在一边，陪着看书的人们。\n在这里看书的人大部分是附近住户的孩子，也有一些喜欢小人书的成人。租借小人书很便宜，在摊里看，每册1分钱，选好书坐下就看，看完连书带钱交给摊主；假如借走回家看，则每本每天2分钱，挑好书后交给摊主，摊主仔细地将租书人的姓名、地址和所借小人书的书名登记在本子上，收了租金就可以拿走了，第二天还书时再把记录一个一个地画掉，还书手续就算是办理好了。印象中似乎没有什么押金，全凭信用。我每天放学回家总要经过这家书摊，都要进去看看。\n然而，这种影响了数代人的小人书，如今只能在北京的潘家园、护国寺等地的旧书摊上找到，一些印刷精美、有特色的作品则身价大涨，成了收藏品，甚至进了博物馆。小人书和小人书摊已成为历史的记忆。",
        "text_translation": {
            "zh": "",
            "ru": "«Сяожэньшу» — это комиксы, изданные в виде книги. В 1950-60-е годы жизнь была однообразной — ни интернета, ни мультфильмов; чтение комиксов было одним из главных развлечений детей. Их любили не только дети, но и бесчисленные подростки и взрослые.\nС ростом популярности комиксов появились ларьки по их прокату. Для тех, кто хотел читать, но не мог позволить себе купить книгу, — за копейки можно было прочесть один выпуск, что, безусловно, было большим благом.\nПомню, в детстве рядом с домом был такой ларёк — небольшой навес у стены в начале улицы, где грубые деревянные доски для сидения подпирали кирпичами. Внутри на щите были разложены комиксы на разные темы; у стены натянуты верёвки, на которых, как бельё, висели раскрытые книжки — пёстро и очень красиво. Чтобы книги меньше изнашивались, каждую обернули бумагой и подписали название кистью: аккуратный, красивый почерк выдавал культурный уровень хозяина. Хозяин — пожилой худощавый старик в сером халате — тихо сидел в стороне, составляя компанию читателям.\nЧитателями были в основном дети соседей, а также взрослые любители комиксов. Прокат был дешёвым: на месте — 1 фэнь за выпуск; можно было сесть и читать; вернув книгу, отдать деньги хозяину. Если брали домой — 2 фэня за книгу в день: выбрав, отдавали хозяину, тот аккуратно записывал в тетрадь имя, адрес и название книги, брал плату — и можно было уходить. Назавтра при возврате записи вычёркивались по одной — процедура завершалась. Помнится, залога не было — всё на доверии. Каждый день, возвращаясь из школы, я проходил мимо этого ларька и обязательно заглядывал.\nОднако эти комиксы, повлиявшие на несколько поколений, сегодня можно найти лишь на барахолках вроде Паньцзяюань или Хугоусы в Пекине. Некоторые изящно напечатанные, характерные издания сильно поднялись в цене и стали предметами коллекционирования, попали даже в музеи. Комиксы и их ларьки стали воспоминанием истории.",
            "tk": "", "en": "Xiaorenshu are picture-story books published in book form. In the 1950s-60s life was monotonous — no internet, no cartoons — so reading them was one of children's main entertainments. Not only kids loved them, but also countless teenagers and adults.\nWith their popularity came rental stalls. For those who wanted to read but couldn't afford to buy, one could read a book for very little money — undoubtedly a great thing.\nI remember there was such a stall near my home — a small shed against a wall at the street entrance, with rough wooden planks propped up by bricks for seating. Inside, a bed board displayed picture-story books on all kinds of subjects; strings were stretched along the wall, with open books draped over them — colourful and lovely. To reduce wear, each book was wrapped in kraft paper with the title written in brush characters — neat and beautiful handwriting revealed the owner's cultural level. The owner, a small elderly man in a grey gown, always sat quietly to one side, keeping the readers company.\nMost readers were neighbourhood children, along with some adults who loved the books. Rental was cheap: 1 fen per volume to read on the spot — sit down and read, then hand the book and money to the owner. If borrowed home, it cost 2 fen per book per day — after choosing, you handed the book to the owner, who carefully recorded your name, address and the book's title, took the fee — and off you went. Returning the next day, records were crossed out one by one — the return procedure done. As far as I recall there was no deposit — all based on trust. Every day after school I'd pass this stall and go in for a look.\nYet today these books, which influenced several generations, can only be found at second-hand stalls in Beijing's Panjiayuan or Huguosi. Some beautifully printed, distinctive editions have soared in value, becoming collector's items, even entering museums. Picture-story books and their stalls have become memories of history.",
            "uz": "", "tg": "", "id": "", "tr": "",
        },
        "vocabulary": vocab,
        "grammar": grammar,
        "comparisons": comparisons,
        "expansion": expansion,
        "application": {
            "discussion": _t(
                "童年的生活与记忆：你的童年是在什么地方度过的？哪些人、事、东西给你留下了深刻印象？为什么？",
                "Детство и воспоминания: где прошло ваше детство? Какие люди, события, вещи оставили глубокий след? Почему?",
                "",
                "Childhood and memories: where did you spend your childhood? Which people, events or things left a deep impression? Why?",
            ),
            "writing_prompt": {
                "zh": "请以“我的童年”为题，谈一谈你的童年时代。尽量用上本课所学的生词，字数不少于100字。",
                "ru": "Напишите эссе на тему «Моё детство», используя слова урока, не менее 100 иероглифов.",
                "en": "Write an essay titled 'My childhood', using this lesson's vocabulary, at least 100 characters.",
            },
        },
        "workbook": workbook,
    }


def lesson21():
    vocab = [
        _vocab("情缘", "qíngyuán", "n.", "судьба, связь", "predestined love, sentimental bond"),
        _vocab("逻辑", "luójí", "n.", "логика", "logic"),
        _vocab("硬", "yìng", "adv.", "твёрдо, упрямо", "rigidly, mechanically"),
        _vocab("死记硬背", "sǐjì-yìngbèi", "идиом", "зазубривать", "to memorize mechanically"),
        _vocab("偶然", "ǒurán", "adj./adv.", "случайный; случайно", "accidental; by chance"),
        _vocab("演变", "yǎnbiàn", "v.", "эволюционировать", "to change, to evolve"),
        _vocab("遗憾", "yíhàn", "adj./n.", "сожаление", "regretful; deep regret"),
        _vocab("心脏", "xīnzàng", "n.", "сердце", "heart"),
        _vocab("思考", "sīkǎo", "v.", "размышлять", "to think deeply, to ponder"),
        _vocab("抓紧", "zhuājǐn", "v.", "крепко схватить; успеть", "to firmly grasp"),
        _vocab("尽快", "jǐnkuài", "adv.", "как можно скорее", "as soon as possible"),
        _vocab("经典", "jīngdiǎn", "n./adj.", "классика; классический", "classics; classical"),
        _vocab("库", "kù", "n.", "хранилище", "storehouse, bank"),
        _vocab("输入", "shūrù", "v.", "вводить", "to input"),
        _vocab("元旦", "yuándàn", "n.", "Новый год (1 января)", "New Year's Day"),
        _vocab("疾病", "jíbìng", "n.", "болезнь", "disease, illness"),
        _vocab("创办", "chuàngbàn", "v.", "основать", "to establish, to set up"),
        _vocab("公开", "gōngkāi", "v./adj.", "обнародовать; открытый", "to make known; open"),
        _vocab("最初", "zuìchū", "n.", "вначале, сначала", "first, earliest"),
        _vocab("痛苦", "tòngkǔ", "adj.", "мучительный", "painful, suffering"),
        _vocab("微博", "wēibó", "n.", "вейбо (микроблог)", "microblog"),
        _vocab("称呼", "chēnghu", "v./n.", "называть; обращение", "to call; form of address"),
        _vocab("克服", "kèfú", "v.", "преодолевать", "to overcome, to conquer"),
        _vocab("收集", "shōují", "v.", "собирать", "to collect, to gather"),
        _vocab("包含", "bāohán", "v.", "содержать", "to contain, to include"),
        _vocab("繁体（字）", "fántǐ(zì)", "n.", "традиционные иероглифы", "complex form, traditional characters"),
        _vocab("简体（字）", "jiǎntǐ(zì)", "n.", "упрощённые иероглифы", "simplified form"),
        _vocab("方言", "fāngyán", "n.", "диалект", "dialect"),
        _vocab("称赞", "chēngzàn", "v.", "хвалить", "to praise, to commend"),
        _vocab("真相", "zhēnxiàng", "n.", "правда, истина", "truth, fact"),
        _vocab("佩服", "pèifú", "v.", "восхищаться", "to admire"),
        _vocab("开放", "kāifàng", "v.", "открывать (доступ)", "to open to the public"),
        _vocab("下载", "xiàzài", "v.", "скачивать", "to download"),
        _vocab("单位", "dānwèi", "n.", "организация, учреждение", "company, employer"),
        _vocab("识别", "shíbié", "v.", "распознавать", "to recognize, to identify"),
        _vocab("查询", "cháxún", "v.", "запрашивать, искать", "to search, to retrieve"),
        _vocab("物理", "wùlǐ", "n.", "физика", "physics"),
        _vocab("完善", "wánshàn", "v./adj.", "совершенствовать; совершенный", "to improve; perfect"),
        _vocab("退休", "tuìxiū", "v.", "выходить на пенсию", "to retire"),
        _vocab("日程", "rìchéng", "n.", "расписание, график", "schedule"),
        _vocab("追求", "zhuīqiú", "v.", "стремиться, добиваться", "to pursue, to go after"),
        _vocab("梦想", "mèngxiǎng", "n./v.", "мечта; мечтать", "dream; to dream"),
    ]

    grammar = [
        {
            "word": "硬", "pos": "adv.",
            "explanation": {
                "ru": "«硬» как наречие означает «настойчиво, упорно», а также «через силу, стиснув зубы».",
                "en": "«硬» as an adverb means 'stubbornly, persistently' or 'by force, gritting one's teeth'.",
            },
            "examples": [
                {"zh": "在中国历史故事“指鹿为马”中，赵高把鹿硬说成马。", "ru": "В исторической притче «выдать оленя за коня» Чжао Гао упорно называл оленя конём.", "en": "In the tale 'call a stag a horse', Zhao Gao stubbornly called a deer a horse."},
                {"zh": "虽然中药汤有点儿苦，但为了治病，他还是硬把它喝下去了。", "ru": "Хотя отвар был горьким, ради лечения он через силу его выпил.", "en": "Though the herbal decoction was bitter, he forced himself to drink it for his health."},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "明明是他忘了，他却__。", "answer": "硬说是我没提醒他。"},
            ],
        },
        {
            "word": "偶然", "pos": "adj./adv.",
            "explanation": {
                "ru": "«偶然» как прилагательное — «случайный, неожиданный». Как наречие — «случайно, изредка».",
                "en": "«偶然» as an adjective means 'accidental, unexpected'. As an adverb — 'by chance, occasionally'.",
            },
            "examples": [
                {"zh": "一个偶然的机会，他发现如果了解汉字的来源和演变过程，再学习它就变得轻松、容易。", "ru": "Случайно он обнаружил: если понять происхождение и эволюцию иероглифов, учить их становится легко.", "en": "By chance he discovered that understanding the origin and evolution of characters makes learning easy."},
                {"zh": "她专心地织着毛衣，偶然也会抬眼看一下墙上的挂钟。", "ru": "Она сосредоточенно вязала свитер, изредка поднимая взгляд на настенные часы.", "en": "She knitted intently, occasionally glancing at the wall clock."},
            ],
            "exercises": [
                {"type": "fill_blank", "question": "__彻底改变了他的命运。", "answer": "一次偶然的相遇"},
            ],
        },
        {
            "word": "尽快", "pos": "adv.",
            "explanation": {
                "ru": "«尽快» — наречие, «как можно быстрее».",
                "en": "«尽快» is an adverb meaning 'as soon as possible'.",
            },
            "examples": [
                {"zh": "我要抓紧时间尽快把《说文解字》电脑化。", "ru": "Я должен использовать время и как можно скорее оцифровать «Шовэнь цзецзы».", "en": "I must hurry to digitize Shuowen Jiezi as soon as possible."},
                {"zh": "新产品出了点儿问题，你和严经理尽快商量一下这事。", "ru": "С новым продуктом проблемы — обсуди это с менеджером Янем как можно быстрее.", "en": "There's a problem with the new product — discuss it with Manager Yan as soon as possible."},
            ],
            "exercises": [
                {"type": "translate", "question": "Ситуация у пациента опасная, отправьте его в больницу как можно скорее.", "answer": "病人的情况很危险，尽快送他去医院。"},
            ],
        },
    ]

    comparisons = [
        {
            "word_a": "偶然", "word_b": "偶尔",
            "common": {"ru": "Оба наречия означают «не часто», иногда взаимозаменяемы.", "en": "Both adverbs mean 'not often'; sometimes interchangeable."},
            "differences": [
                {"ru": "«偶然» — акцент на «внезапно, неожиданно», антоним к «必然».", "en": "«偶然» focuses on 'suddenly, unexpectedly'; antonym of 必然."},
                {"ru": "«偶尔» — акцент на «редко», антоним к «经常».", "en": "«偶尔» focuses on 'rarely'; antonym of 经常."},
            ],
        },
    ]

    expansion = {
        "topic": {"zh": "学科 (Дисциплины)", "ru": "Учебные дисциплины", "en": "Academic subjects"},
        "words": [
            {"hanzi": "哲学", "pinyin": "zhéxué", "meaning": {"zh": "", "ru": "философия", "en": "philosophy"}},
            {"hanzi": "化学", "pinyin": "huàxué", "meaning": {"zh": "", "ru": "химия", "en": "chemistry"}},
            {"hanzi": "物理", "pinyin": "wùlǐ", "meaning": {"zh": "", "ru": "физика", "en": "physics"}},
            {"hanzi": "政治", "pinyin": "zhèngzhì", "meaning": {"zh": "", "ru": "политика", "en": "politics"}},
            {"hanzi": "粘贴", "pinyin": "zhāntiē", "meaning": {"zh": "", "ru": "вставить (в файл)", "en": "to paste"}},
            {"hanzi": "复制", "pinyin": "fùzhì", "meaning": {"zh": "", "ru": "копировать", "en": "to copy"}},
            {"hanzi": "浏览", "pinyin": "liúlǎn", "meaning": {"zh": "", "ru": "просматривать", "en": "to browse"}},
            {"hanzi": "删除", "pinyin": "shānchú", "meaning": {"zh": "", "ru": "удалять", "en": "to delete"}},
            {"hanzi": "搜索", "pinyin": "sōusuǒ", "meaning": {"zh": "", "ru": "искать", "en": "to search"}},
            {"hanzi": "文件", "pinyin": "wénjiàn", "meaning": {"zh": "", "ru": "файл, документ", "en": "file"}},
        ],
    }

    workbook = {
        "listening": [
            {
                "type": "mc", "audio": "workbook_21_1.mp3",
                "prompt": {"zh": "男的遇到了什么问题？", "ru": "С какой проблемой столкнулся мужчина?", "en": "What problem did the man run into?"},
                "options": ["修改套餐", "设置密码", "查询话费", "下载文件"],
                "answer": 2,
            },
            {
                "type": "mc", "audio": "workbook_21_1.mp3",
                "prompt": {"zh": "女的打算干什么？", "ru": "Что планирует делать женщина?", "en": "What does the woman plan to do?"},
                "options": ["参加期末考试", "准备演讲比赛", "查找论文资料", "组织球赛活动"],
                "answer": 2,
            },
        ],
        "reading": [
            {
                "type": "cloze",
                "text_zh": "不可否认，传统纸质出版有着不可避免的局限。随着技术的发展和平书自身的15，从长远来看，很难说人们两千多年的阅读习惯不会改变。",
                "blanks": [
                    {"position": 15, "answer": "完善", "options": ["先进", "完善", "深入", "开放"]},
                ],
            },
        ],
        "writing": [
            {"type": "make_sentence", "words": ["都需要", "任何", "行动之前", "有完善的计划", "采取"], "answer": "任何行动之前都需要采取有完善的计划。"},
            {"type": "make_sentence", "words": ["值得", "成就", "称赞", "刘校长", "在教改方面的"], "answer": "刘校长在教改方面的成就值得称赞。"},
            {"type": "make_sentence", "words": ["勇气", "是为了", "培养学生", "活动的目的", "克服困难的"], "answer": "活动的目的是为了培养学生克服困难的勇气。"},
            {"type": "short_essay", "words": ["梦想", "抓紧", "思考", "遗憾", "追求"], "min_length": 80},
        ],
    }

    return {
        "title": _t(
            "汉字叔叔：一个美国人的汉字情缘",
            "Дядюшка Ханьцзы: история любви американца к китайским иероглифам",
            "", "Uncle Hanzi: The predestined love of an American for Chinese characters", "",
        ),
        "audio_files": {"textbook_1": "textbook_21_1.mp3", "vocab": "vocab_21.mp3", "workbook_21_1": "workbook_21_1.mp3"},
        "warmup": {
            "question": _t(
                "说说你母语所使用的文字和中文有什么不同。简单介绍一下你在学习汉字时，遇到了哪些困难或问题，你是怎么解决的。",
                "Расскажите, чем письменность вашего языка отличается от китайской. Какие трудности вы испытывали при изучении иероглифов и как их решали?",
                "",
                "Tell how your native script differs from Chinese. What difficulties did you meet learning characters and how did you solve them?",
            ),
            "answers": ["逻辑", "死记硬背", "演变"],
        },
        "text_zh": "1972年，22岁的理查德·希尔斯爱上了中文，但是他感觉汉字很复杂，汉字的一笔一画没有任何逻辑，只能死记硬背。一个偶然的机会，他发现如果了解汉字的来源和演变过程，再学习它就变得轻松、容易。但是他遗憾地发现，几乎没有一本英文书能充分解释汉字的字源。1994年，理查德得了心脏病，当时医生说他剩下的时间可能不多了。那时，他开始思考自己的人生，“我该怎么办？我该做什么？”“如果只能活24小时，我会打电话和朋友们说再见；如果我还能活一年，我要抓紧时间尽快把《说文解字》电脑化。”就这样，一部部古汉字经典进入他的资料库，仅仅复印、整理和把这些资料输入电脑就用了8年。2002年元旦，战胜疾病的他决定把自己创办的网站公开，让更多喜欢中文的人在学习汉字时，不再像他最初那样学得那么痛苦。\n2011年，有人把他的故事放到微博上，引起了广泛关注，他也因此被网友亲切地称呼为“汉字叔叔”。\n打开汉字叔叔克服种种困难、花光全部积蓄创办的网站，可以看到他收集整理的近10万个汉字，包含了它们演变的全部字形，当然也包括繁体字形和简体字形，还有普通话和部分方言读音、英文释义等内容，被网友称赞为“有图有真相”。\n更让人佩服的是，汉字叔叔将网站上的内容全部开放给网友免费下载。现在，有很多单位向理查德发出了工作邀请，而理查德选择了去北京师范大学教书，因为那里也有人在做汉字识别查询的研究。在北师大，他除了教物理，还有充分的时间继续研究他的汉字，完善他的网站。在中国，60多岁已经是退休的年纪了。但汉字叔叔每天的日程却安排得很满。他说：“我不会退休，我还要继续追求我的梦想，我要‘活到老，学到老’。”",
        "text_translation": {
            "zh": "",
            "ru": "В 1972 году 22-летний Ричард Сирс влюбился в китайский, но иероглифы казались ему крайне сложными: в чертах не было никакой логики, приходилось зубрить. Случайно он обнаружил: если понять происхождение и эволюцию иероглифов, учить их становится легко. Но, к сожалению, почти ни одна книга на английском не объясняла этимологию в полной мере. В 1994 году у Ричарда случился сердечный приступ; врач сказал, что времени осталось немного. Тогда он задумался о жизни: «Что мне делать? Что я должен сделать?» — «Если мне осталось 24 часа — позвоню друзьям попрощаться. Если год — постараюсь как можно скорее оцифровать „Шовэнь цзецзы“». Так в его базу вошли классические труды по древним иероглифам; только копирование, упорядочивание и ввод в компьютер заняли восемь лет. 1 января 2002 года, победив болезнь, он решил открыть свой сайт для публики — чтобы как можно больше любителей китайского учили иероглифы без тех страданий, что выпали ему вначале.\nВ 2011 году кто-то выложил его историю в вейбо — она привлекла широкое внимание, и интернет-пользователи ласково прозвали его «Дядюшка Ханьцзы».\nОткрыв созданный им сайт — плод преодоления множества трудностей и всех его сбережений — можно увидеть почти 100 тысяч собранных и упорядоченных им иероглифов, включая все графические варианты их эволюции, конечно и традиционные, и упрощённые формы, а также чтения на путунхуа и в некоторых диалектах, английские толкования. Пользователи называют сайт «с картинками и правдой».\nЕщё более восхищает то, что Дядюшка Ханьцзы сделал всё содержимое сайта свободно доступным для скачивания. Сегодня многие организации приглашают Ричарда на работу, а он выбрал преподавание в Пекинском педагогическом университете, потому что там тоже ведутся исследования по распознаванию и поиску иероглифов. В БНУ он не только учит физике, но и имеет достаточно времени продолжать исследования и совершенствовать сайт. В Китае в 60 с лишним лет уже выходят на пенсию, но расписание Дядюшки Ханьцзы по-прежнему плотное. Он говорит: «Я не уйду на пенсию — продолжу pursue свою мечту. Я хочу учиться, пока жив».",
            "tk": "", "en": "In 1972, 22-year-old Richard Sears fell in love with Chinese, but found characters extremely complex — strokes had no logic, only rote memorization worked. By chance he discovered that understanding the origin and evolution of characters makes learning them easy. Yet regretfully, almost no English book explained their etymology fully. In 1994, Richard had a heart attack; the doctor said he might not have much time left. He began to ponder his life: 'What should I do? What should I do?' — 'If I only have 24 hours, I'll call friends to say goodbye; if I have a year, I'll hurry to digitize Shuowen Jiezi.' So classic works on ancient characters entered his database; simply copying, organizing, and inputting them took eight years. On New Year's Day 2002, having overcome his illness, he decided to open his website to the public — so that more Chinese lovers could learn characters without the pain he first endured.\nIn 2011, someone posted his story on Weibo — it drew wide attention, and netizens affectionately dubbed him 'Uncle Hanzi'.\nOpening the website he founded — the fruit of overcoming countless difficulties and spending all his savings — one can see nearly 100,000 characters he collected and organized, including all their evolutionary forms, both traditional and simplified, plus Mandarin and some dialect readings, English glosses, and more — netizens praise it as 'with pictures and the truth'.\nEven more admirable is that Uncle Hanzi made the entire site freely downloadable. Now many organizations have offered Richard jobs, and he chose to teach at Beijing Normal University, because research on character recognition and retrieval is also done there. At BNU he not only teaches physics but also has ample time to continue his research and perfect his site. In China, 60+ is retirement age, yet Uncle Hanzi's schedule is full. He says: 'I won't retire — I'll keep pursuing my dream. I want to learn as long as I live.'",
            "uz": "", "tg": "", "id": "", "tr": "",
        },
        "vocabulary": vocab,
        "grammar": grammar,
        "comparisons": comparisons,
        "expansion": expansion,
        "application": {
            "discussion": _t(
                "学汉语：出于什么目的或原因，你做出了学汉语的决定？你在学习过程中遇到过什么困难？你是怎么克服的？学汉语给你的生活带来了哪些改变？",
                "Изучение китайского: почему вы решили учить китайский? Какие трудности встретили и как преодолели? Как изменилась ваша жизнь?",
                "",
                "Learning Chinese: why did you decide to learn Chinese? What difficulties did you meet and how did you overcome them? How has your life changed?",
            ),
            "writing_prompt": {
                "zh": "请以“我为什么学汉语”为题，谈一谈你的想法和经历。尽量用上本课所学的生词，字数不少于100字。",
                "ru": "Напишите эссе на тему «Почему я учу китайский», используя слова урока, не менее 100 иероглифов.",
                "en": "Write an essay titled 'Why I learn Chinese', using this lesson's vocabulary, at least 100 characters.",
            },
        },
        "workbook": workbook,
    }


if __name__ == "__main__":
    save(7, 20, lesson20())
    save(7, 21, lesson21())
    print("Done.")
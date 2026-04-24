import os
import random
from datetime import timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes
)

ADMIN_ID = 604663433

TOKEN = os.environ.get("BOT_TOKEN", "ВАШ_ТОКЕН_ЗДЕСЬ")

# ──────────────────────────────────────────────
#  БАЗА ВОПРОСОВ
# ──────────────────────────────────────────────
QUESTIONS = {
    "A": [
        {
            "ru": "Компания ABC наняла аудиторскую фирму для проверки отчётности. Кто является 'предполагаемым пользователем' (intended user)?",
            "en": 'Who are the intended users in an assurance engagement?',
            "opts_ru": ['Аудиторы проводящие проверку', 'Менеджмент компании ABC', 'Акционеры и банки использующие отчётность для принятия решений', 'Налоговые органы которым подаётся декларация'],
            "opts_en": ["","","",""],
            "correct": 2,
            "explain_ru": 'Предполагаемые пользователи (intended users) — третьи стороны: акционеры, банки, инвесторы. Менеджмент — ответственная сторона (responsible party). Аудиторы — практики (practitioners). Это три обязательные стороны ассюранс-задания.',
            "explain_en": 'Intended users are the parties who rely on the conclusion: shareholders, banks, investors. Management is the responsible party; auditors are practitioners. These are the three mandatory parties in any assurance engagement.'
        },
        {
            "ru": "Аудитор Иван 10 лет работает с одним клиентом. Обнаружил ошибку в оценке запасов и подумал: 'Они честные — навряд ли умышленно'. Какую угрозу демонстрирует Иван?",
            "en": 'What ethical threat does Ivan demonstrate after 10 years with one client?',
            "opts_ru": ['Угрозу близости — длительные отношения снижают профессиональный скептицизм', 'Угрозу самопроверки — Иван проверял запасы в прошлом году', 'Угрозу адвокации — Иван защищает интересы клиента', 'Угрозу запугивания — клиент давит на Ивана'],
            "opts_en": ["","","",""],
            "correct": 0,
            "explain_ru": 'Угроза близости (familiarity threat) — из-за длительных отношений аудитор начинает симпатизировать клиенту и теряет профессиональный скептицизм. Вместо критической оценки доказательств Иван делает предположения об честности клиента.',
            "explain_en": 'Familiarity threat: long relationships cause the auditor to become sympathetic, losing professional scepticism. Ivan is assuming good faith rather than critically evaluating the evidence — exactly what familiarity threat looks like.'
        },
        {
            "ru": 'Фирма предлагает клиенту: аудит + составление финансовой отчётности. Какая угроза возникает?',
            "en": 'What threat arises from providing audit AND preparing financial statements?',
            "opts_ru": ['Угроза запугивания — клиент может угрожать разрывом контракта', 'Угроза самопроверки — аудитор проверяет отчётность которую сам составил', 'Угроза близости — много услуг сближает аудитора с клиентом', 'Угроза личной заинтересованности — высокий гонорар влияет на мнение'],
            "opts_en": ["","","",""],
            "correct": 1,
            "explain_ru": 'Угроза самопроверки (self-review threat) — аудитор составляет отчётность и потом её же аудирует. Он не сможет объективно критиковать свою собственную работу. Это нарушает независимость.',
            "explain_en": 'Self-review threat: the auditor audits financial statements they helped prepare. The auditor cannot objectively critique their own work — a fundamental independence problem.'
        },
        {
            "ru": 'Что из следующего НЕ является фундаментальным принципом этики ACCA?',
            "en": 'Which is NOT a fundamental ethical principle of ACCA?',
            "opts_ru": ['Честность (Integrity)', 'Конфиденциальность (Confidentiality)', 'Объективность (Objectivity)', 'Независимость (Independence)'],
            "opts_en": ["","","",""],
            "correct": 3,
            "explain_ru": 'Независимость (independence) НЕ входит в пять принципов ACCA. Пять принципов: честность, объективность, профессиональная компетентность и должная осмотрительность, конфиденциальность, профессиональное поведение. Независимость — требование вытекающее из объективности.',
            "explain_en": 'Independence is NOT one of the five fundamental principles. The five are: integrity, objectivity, professional competence and due care, confidentiality, professional behaviour. Independence is a consequence of objectivity, not a separate principle.'
        },
        {
            "ru": "Директор клиента угрожает: 'Не выдашь чистое заключение — сменим аудитора и скажем всем что вы некомпетентны'. Как должен поступить аудитор?",
            "en": 'Director threatens to change auditor if no clean opinion is given. What should the auditor do?',
            "opts_ru": ['Выдать чистое заключение чтобы сохранить клиента', 'Обратиться в полицию так как это шантаж', 'Запросить дополнительные доказательства по спорным вопросам', 'Сообщить руководству фирмы и рассмотреть отказ от задания — угроза создаёт угрозу запугивания'],
            "opts_en": ["","","",""],
            "correct": 3,
            "explain_ru": 'Угроза запугивания (intimidation threat) — клиент давит угрозами. Правильный ответ: сообщить руководству фирмы, рассмотреть отказ от задания (resignation). Нельзя уступать давлению — это разрушает независимость.',
            "explain_en": 'Intimidation threat. The auditor should escalate to firm leadership, consider withdrawing from the engagement, and never modify the opinion under pressure. Yielding destroys independence.'
        },
        {
            "ru": 'Аудитор владеет 0.1% акций клиента. Какую угрозу это создаёт и как устранить?',
            "en": 'Auditor owns 0.1% of client shares. What threat and safeguard apply?',
            "opts_ru": ['Угрозу самопроверки; устраняется привлечением другого партнёра', 'Угрозу близости; устраняется ротацией аудитора', 'Угрозу адвокации; устраняется отказом от консультационных услуг', 'Угрозу личной заинтересованности; устраняется продажей акций до начала аудита'],
            "opts_en": ["","","",""],
            "correct": 3,
            "explain_ru": 'Владение акциями клиента — угроза личной заинтересованности (self-interest threat): аудитор финансово заинтересован в успехе клиента. Единственное решение: продажа акций (disposal of shares) до начала задания.',
            "explain_en": "Self-interest threat — the auditor has a financial stake in the client's success. The only effective safeguard is disposal of the shares before the engagement commences."
        },
        {
            "ru": 'Чем внутренний аудитор принципиально отличается от внешнего?',
            "en": 'What is the key difference between internal and external auditors?',
            "opts_ru": ['Внешний назначается акционерами и независим; внутренний является сотрудником компании', 'Внешний работает бесплатно; внутренний получает зарплату', 'Оба назначаются советом директоров', 'Внешний проверяет только финансы; внутренний проверяет все процессы'],
            "opts_en": ["","","",""],
            "correct": 0,
            "explain_ru": 'Внешний аудитор назначается акционерами, независим от менеджмента — отсюда его ценность. Внутренний — сотрудник компании, отвечает перед менеджментом или комитетом по аудиту. Разные цели, разная независимость.',
            "explain_en": 'External auditor: appointed by shareholders, independent — this is the source of value. Internal auditor: employee, accountable to management/audit committee. Different objectives, different levels of independence.'
        },
        {
            "ru": 'Что означает профессиональный скептицизм при получении объяснений от менеджмента?',
            "en": 'What does professional scepticism mean when receiving management explanations?',
            "opts_ru": ['Критически оценивать объяснения и искать подтверждающие доказательства из независимых источников', 'Отвергать все объяснения менеджмента и искать только внешние источники', 'Принимать объяснения так как менеджмент несёт ответственность за отчётность', 'Записывать объяснения и не задавать дополнительных вопросов'],
            "opts_en": ["","","",""],
            "correct": 0,
            "explain_ru": 'Профессиональный скептицизм — аудитор критически оценивает объяснения и ищет подтверждающие доказательства. Не слепое доверие, но и не автоматическое недоверие — это баланс.',
            "explain_en": 'Professional scepticism: critically assess explanations and seek corroborating evidence from independent sources. Not blind trust, not automatic rejection — a critical and questioning mind.'
        },
        {
            "ru": 'Аудитор раскрывает финансовую информацию клиента своему другому клиенту. Какой принцип нарушен?',
            "en": "Auditor discloses one client's financial information to another client. Which principle is violated?",
            "opts_ru": ['Объективность — аудитор предвзят', 'Честность — аудитор действует нечестно', 'Профессиональное поведение — это дискредитирует профессию', 'Конфиденциальность — информация раскрыта без разрешения третьим лицам'],
            "opts_en": ["","","",""],
            "correct": 3,
            "explain_ru": 'Конфиденциальность (confidentiality) — аудитор не вправе раскрывать информацию клиента третьим лицам без надлежащего разрешения. Раскрытие другому клиенту без согласия — прямое нарушение.',
            "explain_en": 'Confidentiality: the auditor cannot disclose client information to third parties without authority. Disclosing to another client without consent is a direct and clear violation of this fundamental principle.'
        },
        {
            "ru": 'Аудит финансовой отчётности предоставляет какой уровень ассюранса?',
            "en": 'An audit of financial statements provides what level of assurance?',
            "opts_ru": ['Разумный — высокий уровень уверенности но не абсолютный вывод в позитивной форме', "Ограниченный — вывод в негативной форме ('ничего не обнаружено')", 'Абсолютный — аудитор гарантирует отсутствие ошибок', 'Нулевой — аудитор только собирает информацию'],
            "opts_en": ["","","",""],
            "correct": 0,
            "explain_ru": "Аудит: разумный ассюранс (reasonable assurance) — высокий но не абсолютный уровень. Вывод в позитивной форме: 'отчётность достоверна'. Ограниченный ассюранс (обзорная проверка) — вывод в негативной форме: 'ничего не привлекло нашего внимания'.",
            "explain_en": "Audit: reasonable assurance — high but not absolute, expressed positively: 'the statements give a true and fair view'. Limited assurance (review): expressed negatively: 'nothing came to our attention to suggest otherwise'."
        },
        {
            "ru": 'Что такое угроза адвокации (advocacy threat)?',
            "en": 'What is an advocacy threat?',
            "opts_ru": ['Аудитор настолько активно продвигает позицию клиента что это компрометирует его объективность', 'Аудитор имеет акции клиента', 'Клиент угрожает аудитору отрицательными последствиями', 'Аудитор слишком хорошо знает бизнес клиента'],
            "opts_en": ["","","",""],
            "correct": 0,
            "explain_ru": 'Угроза адвокации — аудитор настолько активно защищает интересы клиента (в суде, переговорах), что теряет объективность. Примеры: представление клиента в суде, участие в переговорах о сделках слияния.',
            "explain_en": "Advocacy threat: the auditor promotes a client's position so strongly that objectivity is compromised. Examples: representing client in legal proceedings or acting as negotiator in M&A deals."
        },
        {
            "ru": 'Комитет по аудиту состоит из трёх исполнительных директоров и одного независимого. Какая проблема?',
            "en": 'Audit committee has 3 executive directors and 1 independent. What is the problem?',
            "opts_ru": ['Комитет должен состоять только из независимых неисполнительных директоров', 'Проблем нет — один независимый директор достаточно', 'Комитет слишком маленький — нужно минимум пять человек', 'Исполнительные директора не могут быть членами комитета по закону'],
            "opts_en": ["","","",""],
            "correct": 0,
            "explain_ru": 'Комитет по аудиту должен состоять исключительно из независимых неисполнительных директоров. Исполнительные директора не могут эффективно надзирать за собственным менеджментом — это конфликт интересов.',
            "explain_en": 'The audit committee should consist entirely of independent non-executive directors. Executive directors cannot effectively oversee their own management — this is a fundamental conflict of interest.'
        },
        {
            "ru": 'Принцип профессиональной компетентности требует от аудитора:',
            "en": 'Professional competence requires the auditor to:',
            "opts_ru": ['Никогда не привлекать экспертов и решать всё самостоятельно', 'Проводить аудит быстрее конкурентов', 'Знать все стандарты наизусть без исключений', 'Поддерживать знания на актуальном уровне и действовать добросовестно в соответствии со стандартами'],
            "opts_en": ["","","",""],
            "correct": 3,
            "explain_ru": 'Профессиональная компетентность и должная осмотрительность: поддерживать знания (включая изменения стандартов) и действовать добросовестно. При необходимости привлекать специалистов — это тоже часть компетентности.',
            "explain_en": 'Professional competence and due care: maintain knowledge at the needed level (staying current with standards) and act diligently. Using specialists when needed is part of competence, not a weakness.'
        },
        {
            "ru": 'Аудиторская фирма предлагает клиенту скидку 50% в обмен на направление других клиентов. Какую угрозу это создаёт?',
            "en": '50% discount offered in exchange for client referrals. What threat does this create?',
            "opts_ru": ['Угрозу адвокации — аудитор становится партнёром клиента', 'Угрозу запугивания — клиент может отказать в направлениях', 'Угрозу личной заинтересованности — аудитор финансово заинтересован сохранить выгодные отношения', 'Угрозу близости — скидка сближает аудитора и клиента'],
            "opts_en": ["","","",""],
            "correct": 2,
            "explain_ru": 'Угроза личной заинтересованности — аудитор заинтересован сохранить выгодный реферальный договор что может повлиять на его объективность при формировании мнения о клиенте.',
            "explain_en": 'Self-interest threat: the auditor has a financial interest in maintaining the referral arrangement, which may compromise objectivity when forming the audit opinion on that client.'
        },
        {
            "ru": 'Какая роль внутреннего аудита НЕ является его основной функцией?',
            "en": 'Which is NOT a primary function of internal audit?',
            "opts_ru": ['Проверка эффективности системы внутреннего контроля', 'Оценка системы управления рисками компании', 'Выражение независимого мнения о финансовой отчётности для акционеров', 'Расследование случаев мошенничества внутри компании'],
            "opts_en": ["","","",""],
            "correct": 2,
            "explain_ru": 'Выражение независимого мнения о финансовой отчётности для акционеров — функция ВНЕШНЕГО аудитора. Внутренний аудит: оценка рисков, контролей, консультирование менеджмента, расследование мошенничества.',
            "explain_en": "Expressing an independent opinion on financial statements for shareholders is the EXTERNAL auditor's role. Internal audit evaluates risks, controls, provides consulting and investigates fraud — all internal functions."
        },
        {
            "ru": 'Аудитор обнаружил что клиент нарушил закон. При каком условии аудитор ОБЯЗАН раскрыть без согласия клиента?',
            "en": 'When is the auditor REQUIRED to disclose without client consent?',
            "opts_ru": ['Только если нарушение связано с суммой превышающей существенность', 'Когда существует законодательное требование или профессиональная обязанность раскрыть', 'Никогда — конфиденциальность абсолютна', 'Всегда — все нарушения закона должны раскрываться'],
            "opts_en": ["","","",""],
            "correct": 1,
            "explain_ru": 'Конфиденциальность не абсолютна. Обязательное раскрытие при: законодательном требовании (отмывание денег), профессиональной обязанности, защите общественных интересов. Отсутствие согласия клиента не является препятствием.',
            "explain_en": 'Confidentiality is not absolute. Required disclosure includes: legal requirements (e.g. money laundering regulations), professional duties, and public interest cases. Client consent is not needed in these circumstances.'
        },
        {
            "ru": 'Тон сверху (tone at the top) влияет на систему внутреннего контроля потому что:',
            "en": 'Tone at the top affects internal control because:',
            "opts_ru": ['Контроли работают автоматически без участия людей', 'Если руководство само нарушает правила сотрудники следуют примеру и контроли теряют эффективность', 'Тон сверху влияет только на внешнюю репутацию компании', 'Формальные процедуры всегда работают независимо от поведения руководства'],
            "opts_en": ["","","",""],
            "correct": 1,
            "explain_ru": 'Тон сверху определяет реальную культуру. Если руководство обходит контроли — сотрудники делают то же самое. Никакая формальная система не работает при плохом тоне сверху. Это фундамент всей системы контроля.',
            "explain_en": 'Tone at the top determines real behaviour. If management circumvents controls, employees follow. No formal control system works with poor tone at the top — it is the foundation of the entire control environment.'
        },
        {
            "ru": 'Почему аудитор НЕ несёт ответственности за предотвращение мошенничества?',
            "en": 'Why is the auditor NOT responsible for preventing fraud?',
            "opts_ru": ['Аудитор не может предотвратить мошенничество так как работает лишь раз в год', 'Предотвращение мошенничества — функция полиции', 'Аудитор несёт ответственность — предотвращение мошенничества его главная цель', 'Предотвращение мошенничества — обязанность менеджмента; аудитор лишь оценивает риски и выявляет существенные искажения'],
            "opts_en": ["","","",""],
            "correct": 3,
            "explain_ru": 'Предотвращение мошенничества — ответственность менеджмента через систему внутреннего контроля. Аудитор отвечает за обнаружение существенных искажений (включая мошенничество) в ходе аудита.',
            "explain_en": "Fraud prevention is management's responsibility through internal controls. The auditor is responsible for detecting material misstatements due to fraud during the audit — not for preventing fraud from occurring."
        },
        {
            "ru": 'Что такое объективность (objectivity) как принцип этики ACCA?',
            "en": 'What is objectivity as an ACCA ethical principle?',
            "opts_ru": ['Аудитор объективно сравнивает данные разных периодов', 'Аудитор всегда должен соглашаться с объективными данными рынка', 'Аудитор не позволяет предвзятости конфликту интересов или чужому влиянию переопределять профессиональные суждения', 'Аудитор должен быть объективно быстрым и эффективным'],
            "opts_en": ["","","",""],
            "correct": 2,
            "explain_ru": 'Объективность — аудитор не позволяет предвзятости, конфликту интересов или внешнему влиянию управлять его профессиональными суждениями. Это фундаментальное требование для доверия к аудиторскому мнению.',
            "explain_en": 'Objectivity requires the auditor not to allow bias, conflict of interest or undue influence to override professional judgements. Without this, users cannot trust the audit opinion.'
        },
        {
            "ru": 'Чем положительный ассюранс (positive) отличается от отрицательного (negative)?',
            "en": 'How does positive assurance differ from negative assurance?',
            "opts_ru": ['Положительный при внешнем аудите; отрицательный при внутреннем', 'Разницы нет — оба означают одно', 'Положительный: прямое утверждение что всё верно; отрицательный: ничего не обнаружено что указывало бы на ошибку', 'Положительный — при хорошей отчётности; отрицательный при плохой'],
            "opts_en": ["","","",""],
            "correct": 2,
            "explain_ru": "Положительный: 'В нашем мнении отчётность достоверна' — прямое утверждение (аудит). Отрицательный: 'Ничего не привлекло нашего внимания' — более слабое (обзорная проверка). Разный уровень работы и доверия.",
            "explain_en": "Positive: 'In our opinion the statements give a true and fair view' — direct assertion (audit). Negative: 'Nothing came to our attention' — weaker assertion (review). Different levels of work and assurance."
        },
    ],
    "B": [
        {
            "ru": 'Неотъемлемый риск высокий, контроли надёжны и протестированы. Что происходит с риском необнаружения (DR)?',
            "en": 'IR is high, controls reliable and tested. What happens to detection risk?',
            "opts_ru": ['DR уменьшается — нужно больше процедур по существу несмотря на контроли', 'DR увеличивается — надёжные контроли позволяют проводить меньше процедур по существу', 'DR не меняется — он фиксирован независимо от других компонентов', 'DR равен нулю — надёжные контроли устраняют риск полностью'],
            "opts_en": ["","","",""],
            "correct": 1,
            "explain_ru": 'AR = IR × CR × DR. При высоком IR но низком CR (контроли работают) — DR может быть выше, то есть аудитор может проводить меньше процедур по существу. Это и есть логика модели аудиторского риска.',
            "explain_en": 'AR = IR × CR × DR. With high IR but low CR (controls are reliable), DR can be set higher, meaning fewer substantive procedures are needed. This is the fundamental logic of the audit risk model.'
        },
        {
            "ru": 'Выручка компании 50 млн руб., существенность 2%. Аудитор планирует существенность исполнения на уровне 75% от общей. Зачем нужен этот дополнительный уровень?',
            "en": 'Overall materiality is 1m (2% of 50m). Performance materiality set at 75%. Why?',
            "opts_ru": ['75% — обязательный процент установленный международными стандартами', 'Чтобы уменьшить объём работы — чем ниже существенность тем меньше проверок', 'Чтобы применять более строгие требования только к крупным статьям баланса', 'Чтобы снизить риск накопления несущественных ошибок которые совокупно превысят общую существенность'],
            "opts_en": ["","","",""],
            "correct": 3,
            "explain_ru": 'Существенность исполнения (performance materiality) — буфер. Если каждая статья проверяется с порогом 750 тыс. вместо 1 млн, снижается риск что множество мелких ошибок совокупно превысят 1 млн.',
            "explain_en": 'Performance materiality acts as a buffer. By testing each area at 750k rather than 1m, the auditor reduces the risk that uncorrected misstatements from multiple areas aggregate to exceed overall materiality.'
        },
        {
            "ru": 'Директор предлагает аудитору использовать анализ рисков компании вместо собственного. Как должен поступить аудитор?',
            "en": 'Management offers their risk analysis for the auditor to use instead of doing their own. What should the auditor do?',
            "opts_ru": ['Самостоятельно провести оценку риска используя анализ менеджмента как один из источников', 'Принять — менеджмент лучше знает свой бизнес', 'Принять но проверить несколько ключевых допущений для формальности', 'Отказаться полностью — любой документ от клиента ненадёжен'],
            "opts_en": ["","","",""],
            "correct": 0,
            "explain_ru": 'Аудитор ОБЯЗАН самостоятельно провести оценку риска. Анализ менеджмента — один из источников информации, но не замена независимой оценке. Профессиональный скептицизм требует независимого суждения.',
            "explain_en": "The auditor MUST perform their own risk assessment. Management's analysis is one input but cannot replace the auditor's independent assessment — professional scepticism requires independent judgement."
        },
        {
            "ru": 'Компания работает в сфере криптовалют, применяет субъективные оценки справедливой стоимости. Как это влияет на неотъемлемый риск (IR)?',
            "en": 'Company operates in crypto with subjective fair value estimates. How does this affect IR?',
            "opts_ru": ['IR повышается — волатильность и субъективность оценок увеличивают вероятность искажений', 'IR не меняется — зависит только от истории компании', 'IR снижается — специализированные инструменты лучше регулируются', 'IR повышается только при слабых контролях'],
            "opts_en": ["","","",""],
            "correct": 0,
            "explain_ru": 'Неотъемлемый риск повышается при: волатильности (крипто), сложности (деривативы), субъективности (справедливая стоимость). IR оценивается ДО учёта контролей — он отражает природу самих операций.',
            "explain_en": 'IR increases with volatility (crypto), complexity and subjectivity (fair value estimates). IR is assessed independently of controls — it reflects the susceptibility of the subject matter to misstatement before any controls are considered.'
        },
        {
            "ru": 'ГД компании единолично авторизует любые платежи без лимита. Что это означает для рисков?',
            "en": 'CEO can authorise any payments alone with no limit. What are the risk implications?',
            "opts_ru": ['Стандартная практика не влияющая на риск', 'Снижает риск — ГД несёт полную личную ответственность', 'Повышает только риск необнаружения', 'Повышает риск контроля и риск мошенничества — нет разделения обязанностей и есть угроза обхода контролей руководством'],
            "opts_en": ["","","",""],
            "correct": 3,
            "explain_ru": 'Единоличная авторизация без лимита = высокий CR (нет разделения обязанностей) + высокий риск мошенничества (management override). Это классический элемент треугольника мошенничества — возможность (opportunity).',
            "explain_en": 'Unlimited unilateral authorisation = high CR (no segregation) + high fraud risk (management override opportunity). This is a classic fraud triangle element — opportunity for fraud without detection.'
        },
        {
            "ru": 'Выручка в Q4 выросла на 40%, тогда как в Q1-Q3 рост был 5-8%. Что должен заключить аудитор?',
            "en": 'Revenue grew 40% in Q4 vs 5-8% in prior quarters. What should the auditor conclude?',
            "opts_ru": ['Это нормально — сезонность может объяснить рост', 'Это признак высокого риска завышения выручки требующий дополнительных процедур', 'Принять объяснение менеджмента без дополнительной проверки', 'Рост выручки снижает аудиторский риск'],
            "opts_en": ["","","",""],
            "correct": 1,
            "explain_ru": 'Необъяснённый резкий рост выручки в конце года — красный флаг мошенничества с финансовой отчётностью. Аудитор должен применить усиленный скептицизм и расширить процедуры по существу для выручки.',
            "explain_en": 'Unexplained sharp year-end revenue increase is a red flag for fraudulent financial reporting. The auditor must apply heightened scepticism and design additional substantive procedures specifically targeting revenue.'
        },
        {
            "ru": 'Компания: убытки 2 года подряд, отрицательный денежный поток, нарушение ковенантов по кредиту. Как квалифицировать?',
            "en": 'Company has 2 years of losses, negative cash flows, breached loan covenants. How should this be classified?',
            "opts_ru": ['Аудитор должен немедленно выдать отрицательное заключение', 'Признаки существенной неопределённости в отношении непрерывности деятельности (going concern)', 'Обычные деловые риски не требующие специального внимания', 'Повышает только неотъемлемый риск без влияния на заключение'],
            "opts_en": ["","","",""],
            "correct": 1,
            "explain_ru": 'Убытки + отрицательный денежный поток + нарушение ковенантов — классические индикаторы угрозы going concern. Аудитор должен оценить планы менеджмента и рассмотреть влияние на заключение.',
            "explain_en": "Losses + negative cash flows + covenant breaches are classic going concern indicators. The auditor must assess management's plans, obtain written representations, and consider the impact on the audit report."
        },
        {
            "ru": 'Что такое риск необнаружения (detection risk) и как аудитор им управляет?',
            "en": 'What is detection risk and how does the auditor manage it?',
            "opts_ru": ['Риск того что выборка нерепрезентативна; управляется увеличением её размера', 'Риск того что аудиторские процедуры не обнаружат существенное искажение; управляется изменением объёма характера и сроков процедур', 'Риск того что менеджмент скроет мошенничество; управляется внезапными проверками', 'Риск того что контроли компании не работают; управляется тестированием контролей'],
            "opts_en": ["","","",""],
            "correct": 1,
            "explain_ru": 'Риск необнаружения — единственный компонент которым управляет аудитор: через изменение характера (какие процедуры), сроков (когда) и объёма (сколько). При высоком IR и CR аудитор снижает DR расширяя процедуры.',
            "explain_en": 'Detection risk is the only component the auditor controls — by changing the nature (what procedures), timing (when performed) and extent (how many). High IR and CR → auditor must lower DR by expanding procedures.'
        },
        {
            "ru": 'Аудитор планирует полагаться на контроли в продажах. Что нужно сделать ПРЕЖДЕ чем сокращать процедуры по существу?',
            "en": 'Before reducing substantive procedures based on sales controls, what must the auditor first do?',
            "opts_ru": ['Изучить дизайн контролей без проверки их фактической работы', 'Сразу сократить процедуры если аудитор доверяет менеджменту', 'Получить устные заверения менеджмента что контроли работают', 'Провести тесты контроля (tests of controls) чтобы убедиться что контроли работали эффективно в течение всего периода'],
            "opts_en": ["","","",""],
            "correct": 3,
            "explain_ru": 'Прежде чем полагаться на контроли, аудитор ОБЯЗАН провести тесты контроля (tests of controls). Только фактически подтверждённая эффективность позволяет сокращать процедуры по существу.',
            "explain_en": 'Before reducing substantive procedures, the auditor MUST perform tests of controls to confirm they operated effectively throughout the period. Assumed effectiveness without testing is insufficient.'
        },
        {
            "ru": 'Признаки мошенничества включают всё КРОМЕ:',
            "en": 'Fraud red flags include all of the following EXCEPT:',
            "opts_ru": ['Доминирующий ГД без эффективного надзора совета директоров', 'Чистая аудиторская история компании за 15 лет', 'Менеджмент давит на аудитора выдать заключение быстрее обычного', 'Необычно высокая текучесть кадров в бухгалтерии'],
            "opts_en": ["","","",""],
            "correct": 1,
            "explain_ru": 'Чистая история за 15 лет — нейтральный или позитивный факт, НЕ красный флаг. Красные флаги: давление на аудитора, высокая текучесть в бухгалтерии, доминирующий ГД без надзора.',
            "explain_en": 'A 15-year clean audit history is NOT a red flag — it is neutral or positive. Red flags: pressure on the auditor, high accounting turnover, and a dominant CEO without effective board oversight.'
        },
        {
            "ru": 'Компания впервые применила новый МСФО меняющий признание выручки. Как это влияет на аудит?',
            "en": 'Company applies a new IFRS changing revenue recognition for the first time. Effect on audit?',
            "opts_ru": ['Снижает риск так как менеджмент уделил выручке больше внимания', 'Влияет только на раскрытие но не на аудиторские процедуры', 'Повышает неотъемлемый риск в области выручки и требует дополнительных процедур для проверки правильности применения', 'Не влияет — новые стандарты лучше старых'],
            "opts_en": ["","","",""],
            "correct": 2,
            "explain_ru": 'Первое применение нового стандарта повышает IR: менеджмент может неправильно применить требования или допустить ошибки в переходных расчётах. Требуются дополнительные специфические процедуры.',
            "explain_en": 'First-time adoption increases IR: management may misapply requirements or make transition calculation errors. Additional procedures are needed to verify correct application of the new standard.'
        },
        {
            "ru": 'Аналитические процедуры применяются на каких этапах аудита?',
            "en": 'At which stages of an audit are analytical procedures used?',
            "opts_ru": ['Только на этапе завершения для финальной проверки', 'На этапе планирования по существу и завершения аудита', 'Только на этапе по существу как замена детальным тестам', 'Только на этапе планирования для выявления рисков'],
            "opts_en": ["","","",""],
            "correct": 1,
            "explain_ru": 'Аналитические процедуры применяются на трёх этапах: планирование (выявление рисков), по существу (как один из видов процедур по существу), завершение (финальный общий обзор согласованности отчётности).',
            "explain_en": 'Analytical procedures are used at three stages: planning (risk identification), substantive testing (as substantive analytical procedures), and completion (overall review to confirm consistency of the financial statements).'
        },
        {
            "ru": 'Аудитор ожидает валовую прибыль 35%, но по отчётности 42%. Что делать?',
            "en": 'Expected gross margin is 35% but reported is 42%. What should the auditor do?',
            "opts_ru": ['Принять 42% — менеджмент лучше знает бизнес', 'Исследовать расхождение: запросить объяснения и получить подтверждающие доказательства', 'Скорректировать свой ожидаемый показатель до 42%', 'Автоматически сделать вывод о завышении выручки и выдать оговорку'],
            "opts_en": ["","","",""],
            "correct": 1,
            "explain_ru": 'Расхождение — сигнал риска. Аудитор исследует: запрашивает объяснения менеджмента, ищет подтверждающие доказательства. Если объяснение неудовлетворительное — расширяет процедуры. Немедленная оговорка без расследования была бы преждевременной.',
            "explain_en": "A discrepancy is a risk signal requiring investigation. The auditor obtains management's explanation and seeks corroborating evidence. If unsatisfied, extend procedures. Immediately qualifying without investigation is premature."
        },
        {
            "ru": 'Два типа мошенничества в контексте аудита:',
            "en": 'What are the two types of fraud in auditing?',
            "opts_ru": ['Умышленное и неумышленное мошенничество', 'Внутреннее и внешнее мошенничество', 'Мошеннические финансовые отчёты и присвоение активов', 'Налоговое и бухгалтерское мошенничество'],
            "opts_en": ["","","",""],
            "correct": 2,
            "explain_ru": 'Два типа: мошеннические финансовые отчёты (fraudulent financial reporting) — манипуляция отчётностью менеджментом; присвоение активов (misappropriation of assets) — кража денег или имущества сотрудниками.',
            "explain_en": 'Two types: fraudulent financial reporting (management manipulates financial statements to deceive users) and misappropriation of assets (employees steal cash, inventory or other assets).'
        },
        {
            "ru": 'Треугольник мошенничества включает три элемента. Какой из вариантов правильный?',
            "en": 'The fraud triangle has three elements. Which option is correct?',
            "opts_ru": ['Менеджмент, сотрудники, третьи стороны', 'Давление/мотив, возможность, оправдание/рационализация', 'Риск, контроль, обнаружение', 'Возможность, ошибка, халатность'],
            "opts_en": ["","","",""],
            "correct": 1,
            "explain_ru": 'Треугольник мошенничества: давление (pressure/incentive) — мотив; возможность (opportunity) — слабые контроли; оправдание (rationalisation) — человек убеждает себя что это нормально. Все три должны присутствовать.',
            "explain_en": 'Fraud triangle: pressure/incentive (motive to commit fraud), opportunity (weak controls allowing it), rationalisation (person justifies the action). All three are typically present when fraud occurs.'
        },
        {
            "ru": 'Письмо об условиях задания (engagement letter) подписывается:',
            "en": 'When is an engagement letter signed?',
            "opts_ru": ['В середине аудита после выявления ключевых рисков', 'После завершения аудита как подтверждение результатов', 'До начала аудита как контракт фиксирующий условия задания', 'Одновременно с аудиторским заключением'],
            "opts_en": ["","","",""],
            "correct": 2,
            "explain_ru": 'Письмо об условиях задания — контракт между аудитором и клиентом. Подписывается ДО начала аудита. Содержит: объём задания, ответственность сторон, гонорар, сроки, формат отчётности.',
            "explain_en": 'The engagement letter is a contract agreed and signed BEFORE audit work commences. It covers: scope of the audit, responsibilities of each party, fee arrangements, reporting timelines and expected form of reports.'
        },
        {
            "ru": 'Что делает аудитор при выявлении мошенничества в ходе аудита?',
            "en": 'What does the auditor do when fraud is discovered during the audit?',
            "opts_ru": ['Немедленно сообщает в полицию', 'Прекращает аудит немедленно не завершая работу', 'Сообщает тем кто наделён полномочиями и оценивает влияние на аудит и заключение', 'Скрывает информацию чтобы не навредить клиенту'],
            "opts_en": ["","","",""],
            "correct": 2,
            "explain_ru": 'При выявлении мошенничества: сообщить тем кто наделён полномочиями (those charged with governance), оценить влияние на аудит и заключение. В ряде юрисдикций может потребоваться раскрытие регулятору.',
            "explain_en": 'When fraud is discovered: report to those charged with governance, consider the impact on the audit and opinion. In some jurisdictions disclosure to regulators may also be required regardless of client consent.'
        },
        {
            "ru": 'Существенный риск (significant risk) отличается от обычного тем что:',
            "en": 'A significant risk differs from other risks because:',
            "opts_ru": ['Это риск связанный только с мошенничеством', 'Аудитор должен сообщить об этом риске в заключении', 'Это риск превышающий уровень существенности', 'Для него обязательно нужно оценить контроли И провести процедуры по существу нельзя полагаться только на контроли'],
            "opts_en": ["","","",""],
            "correct": 3,
            "explain_ru": 'Для существенных рисков: аудитор ОБЯЗАН оценить дизайн контролей И провести процедуры по существу. В отличие от обычных рисков — нельзя полагаться только на контроли, процедуры по существу обязательны.',
            "explain_en": 'For significant risks: the auditor MUST evaluate control design AND perform substantive procedures. Unlike other risks, controls alone are insufficient — substantive procedures are always required for significant risks.'
        },
        {
            "ru": 'Менеджмент сообщает что планирует закрыть завод после 31 декабря. Как это должно быть отражено в отчётности за текущий год?',
            "en": 'Management plans to close a factory after 31 December. How should this appear in the current year statements?',
            "opts_ru": ['Как условное обязательство в балансе', 'Не отражать так как событие после отчётной даты', 'Как некорректирующее событие — раскрытие в примечаниях если существенно без изменения сумм', 'Как корректирующее событие — снизить стоимость активов завода'],
            "opts_en": ["","","",""],
            "correct": 2,
            "explain_ru": 'Закрытие завода после отчётной даты — некорректирующее событие (non-adjusting): условие возникло ПОСЛЕ отчётной даты. Требует только раскрытия в примечаниях если существенно.',
            "explain_en": 'Post-year-end factory closure is non-adjusting: the condition arose AFTER the reporting date. It requires disclosure in the notes if material but no adjustment to the financial statement figures.'
        },
        {
            "ru": 'Какую стратегию аудита выбрать при хорошо спроектированных и работающих контролях?',
            "en": 'Which audit strategy is preferred when controls are well-designed and operating effectively?',
            "opts_ru": ['Стратегия не имеет значения — объём работы одинаков', 'Полагаться на контроли после их тестирования что позволяет сократить процедуры по существу', 'Всегда только процедуры по существу — так надёжнее', 'Полагаться на контроли без их тестирования для экономии времени'],
            "opts_en": ["","","",""],
            "correct": 1,
            "explain_ru": 'При надёжных контролях: тестировать их (tests of controls) → подтвердить эффективность → сократить процедуры по существу. Это более эффективная стратегия чем чисто субстантивный подход при сложных операциях.',
            "explain_en": 'With reliable controls: test them → confirm effectiveness → reduce substantive procedures. This controls-based strategy is more efficient than a purely substantive approach when dealing with high-volume, complex transactions.'
        },
    ],
    "C": [
        {
            "ru": 'Один бухгалтер ведёт и учёт и платежи. Какой ключевой недостаток контроля?',
            "en": 'One accountant both records transactions AND makes payments. What key control weakness?',
            "opts_ru": ['Недостаток IT-контролей — нужна автоматизация', 'Отсутствие разделения обязанностей — один человек контролирует всю цепочку создавая риск мошенничества', 'Недостаток физических контролей — нужен сейф', 'Недостаток кадровой политики — нужен второй бухгалтер'],
            "opts_en": ["","","",""],
            "correct": 1,
            "explain_ru": 'Отсутствие разделения обязанностей (segregation of duties) — один человек контролирует всю цепочку: запись + платёж. Это создаёт возможность (opportunity) для мошенничества которое невозможно обнаружить.',
            "explain_en": 'Lack of segregation of duties — one person controls the entire cycle (recording + payment). This creates opportunity for undetected fraud — a key fraud triangle element and a fundamental control weakness.'
        },
        {
            "ru": 'Тестируя авторизацию, аудитор обнаружил что 15 из 50 операций не имели надлежащей авторизации. Что делать?',
            "en": '15 out of 50 tested transactions lacked proper authorisation. What should the auditor do?',
            "opts_ru": ['Расширить тестирование до 100 операций и пересмотреть вывод', 'Принять контроль как эффективный — всего 30% ошибок это нормально', 'Признать контроль неэффективным и существенно расширить процедуры по существу', 'Сообщить только об этих 15 операциях'],
            "opts_en": ["","","",""],
            "correct": 2,
            "explain_ru": '30% уровень ошибок — контроль явно неэффективен. Аудитор должен: не полагаться на контроль, существенно расширить процедуры по существу, сообщить о недостатке контроля руководству.',
            "explain_en": '30% exception rate clearly indicates ineffective controls. The auditor must: not rely on the control, significantly expand substantive procedures, and report the deficiency to those charged with governance.'
        },
        {
            "ru": 'Менеджер по продажам авторизует кредитные лимиты, выставляет счета И получает платежи. Какую конкретную угрозу создаёт совмещение?',
            "en": 'Sales manager authorises credit limits, issues invoices AND receives payments. What specific threat?',
            "opts_ru": ['Угрозу медленной обработки платежей', 'Угрозу ошибок при выставлении счетов', 'Угрозу неправильной классификации выручки', 'Возможность создать фиктивного клиента выставить ему счёт и присвоить оплату — нет разделения обязанностей'],
            "opts_en": ["","","",""],
            "correct": 3,
            "explain_ru": 'Совмещение трёх функций: возможность создать фиктивного клиента, установить лимит, выставить счёт, получить деньги. Классический пример почему разделение обязанностей критично — каждая функция должна быть у разного лица.',
            "explain_en": 'Combining three functions creates a fraud opportunity: create fictitious customer → set credit limit → issue fake invoice → pocket payment. This illustrates exactly why segregation of duties is fundamental to control.'
        },
        {
            "ru": 'В платёжной ведомости обнаружен сотрудник не числящийся в кадровом реестре. Что это означает?',
            "en": 'An employee receives pay but is not in the HR register. What does this indicate?',
            "opts_ru": ['Наличие подставного сотрудника (ghost employee) — классическое мошенничество с зарплатой', 'Новый сотрудник не успел пройти регистрацию', 'Технический сбой в системе учёта персонала', 'Сотрудник переведён из другого подразделения'],
            "opts_en": ["","","",""],
            "correct": 0,
            "explain_ru": 'Подставной сотрудник (ghost employee) — фиктивное лицо добавленное в платёжную ведомость для хищения. Ключевой контроль: сверка платёжной ведомости с кадровым реестром HR. Требует срочного расследования.',
            "explain_en": 'Ghost employee — a fictitious person added to payroll to divert funds. Key control: reconciling the payroll to the HR register. This is a classic payroll fraud requiring immediate investigation.'
        },
        {
            "ru": 'Банковские сверки не проводились 6 месяцев. Какой вывод должен сделать аудитор?',
            "en": 'Bank reconciliations not performed for 6 months. What should the auditor conclude?',
            "opts_ru": ['Повышает только операционный риск но не аудиторский', 'Нормальная практика для небольших компаний', 'Незначительный недостаток — банк хранит все записи', 'Существенный недостаток ключевого детективного контроля повышающий риск для денежных средств и требующий расширения процедур'],
            "opts_en": ["","","",""],
            "correct": 3,
            "explain_ru": 'Отсутствие банковских сверок — существенный недостаток детективного контроля. Повышает риск контроля для денежных средств. Требует расширения процедур по существу и сообщения руководству.',
            "explain_en": 'No bank reconciliations is a significant control deficiency in a key detective control. This increases control risk for cash, requiring expanded substantive procedures and communication to those charged with governance.'
        },
        {
            "ru": 'Трёхстороннее сопоставление (three-way match) в системе закупок означает:',
            "en": 'Three-way matching in the purchases system means:',
            "opts_ru": ['Платёж обрабатывается тремя банками', 'Сопоставление заказа на покупку + накладной о получении + счёта поставщика перед оплатой', 'Три менеджера авторизуют каждый платёж', 'Каждая операция проверяется тремя сотрудниками'],
            "opts_en": ["","","",""],
            "correct": 1,
            "explain_ru": 'Трёхстороннее сопоставление: заказ на покупку (PO) + накладная о получении (GRN) + счёт поставщика (invoice). Все три должны совпасть до оплаты. Предотвращает оплату непоставленных или незаказанных товаров.',
            "explain_en": 'Three-way matching: PO + GRN + supplier invoice must all agree before payment is made. This prevents payment for goods not ordered or not received — the key preventive control in the purchases cycle.'
        },
        {
            "ru": 'Чтобы полагаться на IT-контроли что должно быть верным?',
            "en": 'What must be true to rely on IT application controls?',
            "opts_ru": ['IT-директор письменно подтвердил надёжность системы', 'Система не обновлялась в течение периода', 'IT-система куплена у известного поставщика', 'Общие IT-контроли (доступ управление изменениями) эффективны так как они — фундамент надёжности контролей приложений'],
            "opts_en": ["","","",""],
            "correct": 3,
            "explain_ru": 'Надёжность контролей приложений зависит от общих IT-контролей. Если доступ к системе не контролируется или изменения программ не управляются — контроли приложений ненадёжны независимо от их дизайна.',
            "explain_en": 'Application controls rely on effective general IT controls. If access controls are weak or change management is ineffective, application controls cannot be relied upon regardless of how well they are designed.'
        },
        {
            "ru": 'Небольшая компания не может позволить разделение обязанностей. Какой компенсирующий контроль?',
            "en": 'Small company cannot afford segregation of duties. What compensating control?',
            "opts_ru": ['Отказаться от проверки этой области в аудите', 'Застраховать компанию от мошенничества', 'Активное участие владельца/директора в проверке операций банковских сверок и авторизации платежей', 'Нанять дополнительного сотрудника только для контроля'],
            "opts_en": ["","","",""],
            "correct": 2,
            "explain_ru": 'В малом бизнесе разделение обязанностей часто невозможно. Компенсирующий контроль: активный надзор владельца — личная проверка выписок, сверок, подписание чеков. Частично компенсирует отсутствие разделения.',
            "explain_en": 'In small businesses, segregation is impractical. Compensating control: active owner oversight — personally reviewing bank statements, reconciliations and authorising payments — partially compensates for the lack of segregation.'
        },
        {
            "ru": 'Правильная пара: превентивный контроль — детективный контроль:',
            "en": 'Correct pair: preventive control — detective control:',
            "opts_ru": ['Оба: физическая охрана склада', 'Внутренний аудит — система паролей', 'Банковская сверка — авторизация платежей', 'Авторизация заказов на покупку — банковская сверка'],
            "opts_en": ["","","",""],
            "correct": 3,
            "explain_ru": 'Авторизация заказов — превентивный (предотвращает до совершения). Банковская сверка — детективный (обнаруживает после). Ключевое различие: до или после возникновения ошибки/мошенничества.',
            "explain_en": 'Purchase order authorisation is preventive (stops unauthorised purchases before they happen). Bank reconciliation is detective (identifies errors and fraud after transactions have occurred). Timing is the key distinction.'
        },
        {
            "ru": 'Что является контролем приложения (application control) а не общим IT-контролем?',
            "en": 'Which is an application control rather than a general IT control?',
            "opts_ru": ['Процедуры резервного копирования данных', 'Ограничение физического доступа к серверному помещению', 'Автоматическая проверка что сумма накладной не превышает авторизованный лимит заказа', 'Управление паролями и правами пользователей'],
            "opts_en": ["","","",""],
            "correct": 2,
            "explain_ru": 'Автоматическая проверка лимита — контроль приложения (встроен в конкретную программу, обеспечивает точность обработки данных). Физический доступ, резервное копирование, управление паролями — общие IT-контроли.',
            "explain_en": 'Automatic limit checking is an application control (built into a specific program to ensure accurate data processing). Physical access, backup procedures and password management are general IT controls.'
        },
        {
            "ru": 'Поставщик получает платежи на личный счёт директора. Что это означает?',
            "en": "A supplier is paid into the director's personal account. What does this indicate?",
            "opts_ru": ['Директор — акционер поставщика и это разрешено', 'Потенциальное мошенничество — фиктивный поставщик или аффилированная сделка; требует расследования', 'Нормальная практика для малого бизнеса', 'Ошибка в банковских реквизитах'],
            "opts_en": ["","","",""],
            "correct": 1,
            "explain_ru": 'Платёж поставщику на личный счёт директора — серьёзный красный флаг: возможно фиктивный поставщик или нераскрытая аффилированная сделка. Требует немедленного расследования и сообщения комитету по аудиту.',
            "explain_en": "Supplier payments to the director's personal account is a major fraud red flag: likely a fictitious supplier or undisclosed related party transaction. Requires immediate investigation and reporting to the audit committee."
        },
        {
            "ru": 'Управление изменениями программ (change management) важно для аудитора потому что:',
            "en": 'Program change management matters to the auditor because:',
            "opts_ru": ['Это часть управления бюджетом IT-проектов', 'Аудитор должен тестировать каждое обновление программы', 'Несанкционированные изменения в программах могут исказить результаты обработки данных создав риск ошибок или мошенничества', 'Это влияет только на скорость обработки операций'],
            "opts_en": ["","","",""],
            "correct": 2,
            "explain_ru": 'Несанкционированные изменения программ могут внести ошибки в расчёты или создать возможности для мошенничества. Аудитор должен убедиться что изменения тестировались и авторизовывались до внедрения.',
            "explain_en": 'Unauthorised program changes can introduce calculation errors or create fraud opportunities. The auditor must ensure changes were properly tested and authorised before implementation to maintain data integrity.'
        },
        {
            "ru": 'Обход контроля руководством (management override) — главный риск мошенничества потому что:',
            "en": 'Management override is the primary fraud risk because:',
            "opts_ru": ['Менеджмент не знает о контролях и случайно их нарушает', 'Это риск только в крупных компаниях', 'Менеджмент создал контроли и знает как их обойти делая их неэффективными против собственного мошенничества', 'Контроли устаревают и менеджмент вынужден их обходить'],
            "opts_en": ["","","",""],
            "correct": 2,
            "explain_ru": 'Менеджмент СОЗДАЛ контроли и знает как их обойти. Никакая система не защитит от намеренного обхода теми кто стоит выше неё. Это объясняет почему контроль даёт лишь разумную а не абсолютную уверенность.',
            "explain_en": 'Management CREATED the controls and knows exactly how to circumvent them. No control system protects against intentional override by those in authority — this is why controls provide reasonable, not absolute, assurance.'
        },
        {
            "ru": 'Тест на контроль показал 5% уровень ошибок (2 из 40 операций без авторизации). Как классифицировать?',
            "en": 'Control testing showed 5% error rate (2 of 40 without authorisation). How to classify?',
            "opts_ru": ['Существенный недостаток требующий немедленного сообщения акционерам', 'Неприемлемый уровень — автоматически выдать оговорку', 'Незначительный недостаток — рассмотреть характер ошибок и сообщить менеджменту но частичная эффективность контроля возможна', 'Существенная слабость требующая полного отказа от тестирования контролей'],
            "opts_en": ["","","",""],
            "correct": 2,
            "explain_ru": '5% — пограничный уровень. Аудитор рассматривает характер ошибок (случайные или систематические?). 2 случайных ошибки без признаков умысла — вероятно незначительный недостаток: сообщить менеджменту, контроль частично эффективен.',
            "explain_en": '5% is borderline. The auditor considers whether exceptions are random or systematic. Two random errors without fraud indicators suggests a minor deficiency — report to management but the control may still be partially effective.'
        },
        {
            "ru": 'Нумерация документов (sequential numbering) является контролем:',
            "en": 'Sequential numbering of documents is a control over:',
            "opts_ru": ['Оценки — правильность сумм в документах', 'Авторизации — кто подписал документ', 'Существования — подтверждает что каждый документ реален', 'Полноты — пропущенные номера указывают на незарегистрированные операции'],
            "opts_en": ["","","",""],
            "correct": 3,
            "explain_ru": 'Порядковая нумерация — контроль полноты (completeness control). Пропущенные номера указывают на потенциально незарегистрированные операции. Применяется к счетам, заказам, накладным.',
            "explain_en": 'Sequential numbering is a completeness control. Missing numbers indicate potentially unrecorded transactions. Applied to invoices, purchase orders and despatch notes to ensure all transactions are captured.'
        },
        {
            "ru": 'Среда контроля (control environment) влияет на всю систему контроля потому что:',
            "en": 'The control environment affects the entire control system because:',
            "opts_ru": ['Это самый дорогостоящий элемент системы контроля', 'Это единственный элемент который аудитор может протестировать', 'Это фундамент — если руководство не ценит контроли никакие формальные процедуры не будут работать по-настоящему', 'Это влияет только на IT-контроли'],
            "opts_en": ["","","",""],
            "correct": 2,
            "explain_ru": 'Среда контроля — фундамент всего. Тон сверху, этические ценности, стиль управления определяют будут ли формальные контроли работать на практике. Слабая среда подрывает даже хорошо спроектированные контроли.',
            "explain_en": 'The control environment is the foundation. Tone at the top, ethical values and management style determine whether formal controls will work in practice. A weak environment undermines even well-designed controls.'
        },
        {
            "ru": 'Контроли в системе продаж включают ежемесячные выписки клиентам. Что это за вид контроля?',
            "en": 'Monthly statements sent to customers is what type of control?',
            "opts_ru": ['Авторизационный — подтверждение продаж', 'Детективный — клиенты обнаруживают расхождения и сообщают о них', 'Превентивный — предотвращает ошибки в выставлении счетов', 'Физический — физическая безопасность документов'],
            "opts_en": ["","","",""],
            "correct": 1,
            "explain_ru": 'Ежемесячные выписки клиентам — детективный контроль. Клиенты проверяют свои остатки и сообщают о расхождениях. Это позволяет выявить ошибки в выставлении счетов и потенциальные хищения.',
            "explain_en": 'Monthly customer statements are a detective control. Customers check their balances and dispute discrepancies, helping identify billing errors, unrecorded cash receipts, and potential misappropriation.'
        },
        {
            "ru": 'Почему аудитор не может полностью устранить аудиторский риск?',
            "en": 'Why cannot the auditor eliminate audit risk completely?',
            "opts_ru": ['Из-за неизбежных ограничений: выборка не покрывает 100% суждения могут ошибаться мошенничество может быть скрыто', 'Стандарты запрещают проверку 100% операций', 'Из-за ограниченного бюджета и времени', 'Клиент не предоставляет доступ ко всем документам'],
            "opts_en": ["","","",""],
            "correct": 0,
            "explain_ru": 'Абсолютная уверенность недостижима из-за: выборки (не все операции проверены), погрешности суждений, возможности сговора и сложного мошенничества, ограничений контроля. Поэтому аудит даёт разумную а не абсолютную уверенность.',
            "explain_en": 'Absolute assurance is unachievable due to: sampling (not all items tested), fallibility of judgements, possibility of sophisticated fraud, and limitations of internal controls. Hence only reasonable assurance is possible.'
        },
        {
            "ru": 'Ключевые контроли в системе закупок. Что из следующего является наиболее важным для предотвращения несанкционированных закупок?',
            "en": 'Which is the most important control for preventing unauthorised purchases?',
            "opts_ru": ['Проверка качества получаемых товаров', 'Страхование от кредитного риска поставщиков', 'Ежегодная проверка реестра поставщиков', 'Авторизация заказов на покупку уполномоченным лицом ДО размещения заказа'],
            "opts_en": ["","","",""],
            "correct": 3,
            "explain_ru": 'Авторизация заказов на покупку ДО их размещения — ключевой превентивный контроль. Он гарантирует что только авторизованные закупки производятся предотвращая мошенничество и нецелевые расходы.',
            "explain_en": 'Authorisation of purchase orders BEFORE placement is the key preventive control. It ensures only approved purchases are made, preventing fraud and unauthorised expenditure before it occurs.'
        },
        {
            "ru": 'Контроли приложений в IT-системе включают всё КРОМЕ:',
            "en": 'Application controls include all of the following EXCEPT:',
            "opts_ru": ['Отчёты об исключениях для операций превышающих лимит (output controls)', 'Проверка что введённые данные соответствуют заданному формату (input validation)', 'Автоматические расчёты налогов и скидок (processing controls)', 'Резервное копирование данных ежедневно'],
            "opts_en": ["","","",""],
            "correct": 3,
            "explain_ru": 'Ежедневное резервное копирование — общий IT-контроль (general IT control), применяется ко всей IT-среде. Проверка ввода, расчёты, отчёты об исключениях — контроли приложений (встроены в конкретную программу).',
            "explain_en": 'Daily backup is a general IT control applying to the whole IT environment. Input validation, processing controls and exception reports are application controls built into specific programs.'
        },
    ],
    "D": [
        {
            "ru": 'Лучшая комбинация процедур для покрытия всех утверждений по дебиторской задолженности:',
            "en": 'Best combination to cover all assertions for receivables:',
            "opts_ru": ['Только проверка последующих поступлений', 'Только внешнее подтверждение от всех дебиторов', 'Внешнее подтверждение (существование) + анализ возраста (оценка) + последующие поступления (оценка и полнота)', 'Только инспекция договоров с покупателями'],
            "opts_en": ["","","",""],
            "correct": 2,
            "explain_ru": 'Комплексный подход: внешнее подтверждение → existence; анализ возраста → valuation резерва; последующие поступления → valuation + completeness. Каждая процедура закрывает разные утверждения.',
            "explain_en": 'Comprehensive approach: circularisation → existence; aged analysis → valuation of bad debt provision; subsequent receipts → valuation and completeness. Each procedure addresses different assertions.'
        },
        {
            "ru": 'Физический счёт запасов показал остаток на 15% ниже учётного. Что нужно сделать?',
            "en": 'Physical count is 15% below book value. What is required?',
            "opts_ru": ['Автоматически выдать оговорку из-за расхождения', 'Исследовать расхождение: проверить записи проследить движение оценить необходимость резерва или списания', 'Принять учётные данные так как ошибка могла быть при пересчёте', 'Попросить клиента пересчитать без присутствия аудитора'],
            "opts_en": ["","","",""],
            "correct": 1,
            "explain_ru": 'Расхождение 15% существенно. Аудитор исследует причину (ошибка учёта? кража? порча?), прослеживает движение, оценивает необходимость резерва или списания. Влияет на утверждение valuation.',
            "explain_en": 'A 15% discrepancy is material. The auditor must investigate the cause (recording error? theft? damage?), trace movements, and assess whether write-downs or provisions are needed — directly affecting the valuation assertion.'
        },
        {
            "ru": '30% дебиторов не ответили на запросы о подтверждении (circularisation). Что делать?',
            "en": '30% of debtors did not respond to circularisation. What should the auditor do?',
            "opts_ru": ['Применить альтернативные процедуры: проверить последующие оплаты счета договоры накладные', 'Увеличить резерв по сомнительным долгам на 30% автоматически', 'Выдать оговорку из-за ограничения объёма', 'Считать неответившие суммы подтверждёнными — молчание означает согласие'],
            "opts_en": ["","","",""],
            "correct": 0,
            "explain_ru": 'Отсутствие ответа НЕ является подтверждением. Альтернативные процедуры для неответивших: проверка последующих денежных поступлений, инспекция счетов и договоров, накладных на отгрузку.',
            "explain_en": 'Non-response is NOT confirmation. For non-respondents apply alternative procedures: test subsequent cash receipts, inspect invoices and contracts, review despatch documentation.'
        },
        {
            "ru": 'Продажа на 5 млн руб. учтена 31 декабря, но товар отгружен 4 января. Какое нарушение?',
            "en": '5m sale recorded 31 Dec, goods shipped 4 Jan. What violation?',
            "opts_ru": ['Нарушение классификации — в неправильной статье', 'Нарушение оценки — сделка оценена неправильно', 'Нарушение полноты — сделка учтена не полностью', 'Нарушение среза (cut-off) — выручка признана в неправильном периоде'],
            "opts_en": ["","","",""],
            "correct": 3,
            "explain_ru": 'Нарушение среза (cut-off): выручка признана 31 декабря, но контроль перешёл покупателю 4 января. Это завышение выручки текущего года и занижение следующего.',
            "explain_en": 'Cut-off violation: revenue recorded 31 Dec but goods delivered 4 Jan. Revenue should be recognised when control passes to the buyer — 4 January. Current year revenue overstated, next year understated.'
        },
        {
            "ru": 'Расположите доказательства от наиболее к наименее надёжным:',
            "en": 'Rank from most to least reliable:',
            "opts_ru": ['Устное заявление директора > банковское подтверждение > внутренний документ', 'Все три одинаково надёжны', 'Банковское подтверждение > устное заявление директора > внутренний документ клиента', 'Внутренний документ > устное заявление > банковское подтверждение'],
            "opts_en": ["","","",""],
            "correct": 2,
            "explain_ru": 'Банковское подтверждение (от независимого третьего лица напрямую аудитору) > внутренний документ (создан клиентом но документально) > устное заявление директора (устное, от заинтересованной стороны).',
            "explain_en": 'Bank confirmation (external, independent, directly to auditor) > internal client document (client-generated but documented) > oral director statement (oral, from interested party — least reliable).'
        },
        {
            "ru": 'Какая процедура наиболее эффективна для поиска незарегистрированных обязательств?',
            "en": 'Most effective procedure for finding unrecorded liabilities:',
            "opts_ru": ['Проверка счетов ДО отчётной даты', 'Сверка с реестром одобренных поставщиков', 'Внешнее подтверждение от всех поставщиков', 'Проверка платежей произведённых ПОСЛЕ отчётной даты и сопоставление с кредиторкой на конец года'],
            "opts_en": ["","","",""],
            "correct": 3,
            "explain_ru": 'Проверка послеотчётных платежей (subsequent payments): платёж после 31 декабря за товар/услугу до этой даты = обязательство было на конец года. Самая прямая проверка утверждения completeness для кредиторки.',
            "explain_en": 'Testing subsequent payments: payment after year-end for goods/services received before year-end reveals unrecorded year-end liabilities. This is the most direct test of the completeness assertion for payables.'
        },
        {
            "ru": 'Что снижает надёжность аналитических процедур по существу для выручки?',
            "en": 'What reduces reliability of substantive analytical procedures for revenue?',
            "opts_ru": ['Использование данных предыдущих периодов', 'Использование детальных данных вместо агрегированных', 'Слабая предсказуемость взаимосвязей или высокий риск манипуляций именно в этой статье', 'Привлечение аудитора со знанием отрасли'],
            "opts_en": ["","","",""],
            "correct": 2,
            "explain_ru": 'Надёжность аналитических процедур снижается при слабой предсказуемости взаимосвязей и высоком риске манипуляций. При высоком риске мошенничества с выручкой — детальные тесты надёжнее аналитики.',
            "explain_en": 'Reliability reduces with unpredictable relationships and high fraud risk. For high-risk revenue, detailed tests of individual transactions are more appropriate than relying primarily on analytical procedures.'
        },
        {
            "ru": 'Запасы оценены по ФИФО, часть устарела, резерва нет. Какое утверждение под угрозой?',
            "en": 'Inventory at FIFO; some items obsolete, no provision. Which assertion is at risk?',
            "opts_ru": ['Оценка — запасы могут быть завышены выше чистой стоимости реализации (NRV)', 'Полнота — не все запасы учтены', 'Права — компания не владеет запасами', 'Существование — запасы физически отсутствуют'],
            "opts_en": ["","","",""],
            "correct": 0,
            "explain_ru": 'Устаревшие запасы без резерва — угроза оценке (valuation). Запасы должны учитываться по наименьшей из cost и NRV. Без резерва активы завышены, прибыль завышена.',
            "explain_en": 'Obsolete inventory without provision threatens the valuation assertion: inventory must be at the lower of cost and NRV. Without a write-down, assets are overstated, which also overstates profit.'
        },
        {
            "ru": 'Для активов направление тестирования — сверху вниз. Почему?',
            "en": 'For assets, directional testing goes top-down. Why?',
            "opts_ru": ['Потому что так быстрее и эффективнее', 'Потому что основной риск для активов — завышение; тест сверху вниз проверяет что отражённые активы существуют', 'Потому что стандарты требуют этого направления', 'Потому что снизу вверх тест слишком сложен для активов'],
            "opts_en": ["","","",""],
            "correct": 1,
            "explain_ru": 'Для активов основной риск — завышение (overstatement). Тест сверху вниз: берём статью из отчётности → ищем подтверждающий документ (existence). Снизу вверх тестирует полноту — для обязательств где риск занижения.',
            "explain_en": 'Assets risk overstatement. Top-down: take item from statements → trace to source documents (tests existence). Bottom-up tests completeness — appropriate for liabilities where understatement is the primary risk.'
        },
        {
            "ru": 'Аудитор не смог присутствовать на инвентаризации запасов так как назначен после её проведения. Что делать?',
            "en": "Auditor couldn't attend inventory count as appointed afterwards. What to do?",
            "opts_ru": ['Автоматически выдать отказ от выражения мнения', 'Принять данные без проверки', 'Применить альтернативные процедуры: наблюдение за последующей инвентаризацией и тестирование движения запасов', 'Попросить клиента повторить инвентаризацию'],
            "opts_en": ["","","",""],
            "correct": 2,
            "explain_ru": 'Если присутствие невозможно: наблюдение за промежуточной инвентаризацией + тестирование движения запасов от промежуточной даты до отчётной. Отказ от мнения — крайний случай только если альтернативы недостаточны.',
            "explain_en": 'If attendance impossible: observe a subsequent count + test movements from that date to year-end. A disclaimer is only a last resort if alternative procedures cannot provide sufficient evidence.'
        },
        {
            "ru": 'Тест на полноту кредиторской задолженности — направление:',
            "en": 'Testing completeness of payables — direction:',
            "opts_ru": ['От кредиторки к накладным — убеждаемся что отражённые суммы существуют', 'Направление не важно при детальном тестировании', 'В обоих направлениях одновременно', 'От накладных о получении к кредиторке — убеждаемся что обязательства отражены'],
            "opts_en": ["","","",""],
            "correct": 3,
            "explain_ru": 'Тест на полноту (completeness) — снизу вверх: от первичных документов (GRN) к отчётности. Взять накладные о получении → убедиться что соответствующие счета отражены в кредиторке. Противоположное тестирует существование.',
            "explain_en": 'Completeness testing goes bottom-up: from source documents (GRNs) to financial statements. Take GRNs → check corresponding liabilities are recorded in payables. The opposite direction tests existence/occurrence.'
        },
        {
            "ru": 'При аудите выручки тест occurrence (реальность) проводится в направлении:',
            "en": 'When testing revenue occurrence, the direction is:',
            "opts_ru": ['От первичных документов к отражённой выручке (снизу вверх)', 'От отражённой выручки к первичным документам (сверху вниз)', 'В обоих направлениях', 'Направление не имеет значения'],
            "opts_en": ["","","",""],
            "correct": 1,
            "explain_ru": 'Тест на реальность (occurrence) — сверху вниз: берём записи из учётной системы → ищем подтверждающие документы. Выявляет завышение (фиктивные продажи). Снизу вверх тестирует полноту (пропущенные продажи).',
            "explain_en": 'Testing occurrence goes top-down: take recorded sales → trace to supporting documents. This detects overstatement (fictitious sales). Bottom-up testing detects understatement (missed sales) — completeness.'
        },
        {
            "ru": 'Компания переоценивает недвижимость по справедливой стоимости. Оценку проводит независимый оценщик. Что должен сделать аудитор?',
            "en": 'Property revalued by independent valuer. What must the auditor do?',
            "opts_ru": ['Провести собственную независимую оценку', 'Принять оценку без проверки так как оценщик независим', 'Оценить компетентность объективность и методологию оценщика и проверить корректность входных данных', 'Запросить второе мнение от другого оценщика'],
            "opts_en": ["","","",""],
            "correct": 2,
            "explain_ru": 'При использовании работы эксперта (specialist): оценить компетентность, объективность, независимость; понять методологию; проверить входные данные. Аудитор несёт ответственность за заключение даже при привлечении экспертов.',
            "explain_en": "When using a specialist: assess competence, objectivity and independence; understand the methodology; test input data. The auditor remains responsible for the opinion — using experts doesn't transfer responsibility."
        },
        {
            "ru": 'Письма-представления менеджмента (written representations) достаточны как единственное доказательство?',
            "en": 'Are management representations sufficient as sole evidence?',
            "opts_ru": ['Нет — они дополняют другие процедуры но не заменяют их', 'Да — при долгосрочных отношениях с клиентом', 'Нет только для сумм превышающих существенность', 'Да — подпись директора делает это юридически обязывающим'],
            "opts_en": ["","","",""],
            "correct": 0,
            "explain_ru": 'Письма-представления НЕ являются достаточным доказательством сами по себе. Они дополняют другие процедуры. Полагаться только на них без других доказательств — недостаточное основание для мнения.',
            "explain_en": 'Written representations are NOT sufficient evidence on their own. They supplement but cannot replace other audit procedures. Relying solely on them without corroborating evidence is insufficient to support an audit opinion.'
        },
        {
            "ru": 'Аналитические процедуры на этапе завершения служат для:',
            "en": 'Analytical procedures at the completion stage serve to:',
            "opts_ru": ['Выявить области риска для планирования следующего аудита', 'Установить уровень существенности на следующий год', 'Финальный общий обзор — убедиться что отчётность согласована и нет необъяснённых расхождений', 'Заменить детальные тесты не проведённые ранее'],
            "opts_en": ["","","",""],
            "correct": 2,
            "explain_ru": 'На этапе завершения аналитические процедуры — финальный общий обзор: убедиться что отчётность согласована, все расхождения объяснены, нет ничего что противоречит выводам аудита.',
            "explain_en": 'At completion, analytical procedures provide an overall review: confirm the financial statements are consistent and all unexpected variations have been explained before the audit opinion is signed.'
        },
        {
            "ru": 'Наиболее убедительное доказательство существования крупной дебиторской задолженности:',
            "en": 'Most persuasive evidence of existence for a large receivable:',
            "opts_ru": ['Прямое письменное подтверждение от дебитора полученное аудитором напрямую на отчётную дату', 'Инспекция договора с клиентом начала года', 'Запрос менеджменту о статусе клиента', 'Проверка что оплата поступила в следующем месяце'],
            "opts_en": ["","","",""],
            "correct": 0,
            "explain_ru": 'Прямое внешнее подтверждение — наиболее надёжное для существования. Независимая сторона напрямую подтверждает задолженность на отчётную дату. Договор доказывает только существование отношений, не остаток на 31 декабря.',
            "explain_en": 'Direct external confirmation is most persuasive for existence: an independent party directly confirms the balance at the reporting date. A contract only proves a relationship existed, not the year-end balance.'
        },
        {
            "ru": "Как проверяется утверждение 'права' (rights) для основных средств?",
            "en": "How is the 'rights' assertion tested for non-current assets?",
            "opts_ru": ['Пересчёт амортизации', 'Физический осмотр активов', 'Проверка правоустанавливающих документов: свидетельства о регистрации договоры страховые полисы', 'Сверка с реестром активов'],
            "opts_en": ["","","",""],
            "correct": 2,
            "explain_ru": "Утверждение 'права' (rights) — активы принадлежат компании. Процедуры: проверка свидетельств о собственности, договоров купли-продажи, страховых полисов (страхуют только собственное имущество).",
            "explain_en": 'Rights assertion: entity owns/controls the assets. Procedures: inspect title deeds, purchase contracts, registration documents and insurance policies (entities only insure their own assets).'
        },
        {
            "ru": 'Когда денежная выборка единиц (MUS) предпочтительнее случайной?',
            "en": 'When is monetary unit sampling preferred over random sampling?',
            "opts_ru": ['Когда все операции одинаковы по сумме', 'Когда нужно акцентироваться на крупных суммах так как каждая денежная единица имеет равную вероятность попасть в выборку', 'Когда нужно проверить небольшое число операций', 'Когда выборка только для тестирования контролей'],
            "opts_en": ["","","",""],
            "correct": 1,
            "explain_ru": 'MUS: каждая денежная единица имеет равную вероятность — крупные суммы автоматически имеют больший шанс попасть в выборку. Логично для аудита: крупные ошибки более материальны.',
            "explain_en": 'MUS gives each monetary unit equal probability, so larger value items have proportionally higher chance of selection. Appropriate when objective is to detect material overstatements — larger amounts carry more audit risk.'
        },
        {
            "ru": 'Запрос (inquiry) как метод получения доказательств:',
            "en": 'Inquiry as an audit procedure:',
            "opts_ru": ['Используется только для тестирования контролей', 'Заменяет внешнее подтверждение если клиент заслуживает доверия', 'Самый надёжный вид доказательств так как информация получена напрямую', 'Не является достаточным единственным доказательством — должен подкрепляться другими процедурами'],
            "opts_en": ["","","",""],
            "correct": 3,
            "explain_ru": 'Запрос (inquiry) — один из наименее надёжных видов доказательств когда используется в одиночку. Должен подкрепляться инспекцией, подтверждением или пересчётом. Исходит от заинтересованной стороны.',
            "explain_en": 'Inquiry alone is one of the least reliable forms of evidence — it comes from the interested party. It must be corroborated by inspection, confirmation or recalculation to provide sufficient appropriate audit evidence.'
        },
        {
            "ru": 'Аудитор проверяет что амортизация основных средств рассчитана правильно. Какой метод использует?',
            "en": 'Auditor tests that depreciation is correctly calculated. Which procedure is used?',
            "opts_ru": ['Внешнее подтверждение — запрос от банка', 'Наблюдение — аудитор наблюдает за процессом начисления амортизации', 'Запрос — аудитор спрашивает бухгалтера как рассчитана амортизация', 'Пересчёт — независимая проверка арифметической точности расчётов'],
            "opts_en": ["","","",""],
            "correct": 3,
            "explain_ru": 'Пересчёт (recalculation) — аудитор независимо проверяет арифметическую точность. Для амортизации: берёт стоимость актива, срок полезного использования, метод и пересчитывает сам. Прямая проверка точности (accuracy assertion).',
            "explain_en": 'Recalculation — the auditor independently checks mathematical accuracy. For depreciation: takes cost, useful life and method, recalculates independently. This directly tests the accuracy assertion for depreciation charges.'
        },
    ],
    "E": [
        {
            "ru": 'Запасы завышены на 8 млн руб. (существенность 10 млн). Менеджмент отказывается исправить. Какое заключение?',
            "en": 'Inventory overstated 8m (materiality 10m). Management refuses to adjust. What opinion?',
            "opts_ru": ['Отрицательное мнение (adverse) — любой отказ исправить требует adverse', 'Заключение с оговоркой (qualified) — искажение существенно но ограничено одной статьей', 'Отказ от мнения — аудитор не может сформировать мнение', 'Немодифицированное — сумма ниже существенности поэтому нет проблем'],
            "opts_en": ["","","",""],
            "correct": 1,
            "explain_ru": "8 млн существенно (близко к 10 млн). Искажение в одной статье — не повсеместное. Менеджмент отказывается исправить → оговорка (qualified: 'кроме влияния...'). Adverse — только если искажение пронизывает всю отчётность.",
            "explain_en": "8m is material (near 10m threshold). Single line item misstatement is not pervasive. Management refuses to correct → qualified opinion ('except for the effect of...'). Adverse only if misstatement pervades the financial statements."
        },
        {
            "ru": 'Going concern uncertainty адекватно раскрыта в примечаниях. Аудитор согласен. Какое заключение?',
            "en": 'Going concern uncertainty adequately disclosed. Auditor agrees. What opinion?',
            "opts_ru": ['Отрицательное — going concern всегда требует adverse opinion', 'Отказ от мнения — будущее неизвестно', 'Оговорка — неопределённость является существенным искажением', 'Немодифицированное с параграфом Emphasis of Matter привлекающим внимание к раскрытию'],
            "opts_en": ["","","",""],
            "correct": 3,
            "explain_ru": 'Если going concern uncertainty адекватно раскрыта — немодифицированное мнение + Emphasis of Matter. Это привлекает внимание не изменяя мнения. Adverse и disclaimer — при отсутствии или недостаточности раскрытия.',
            "explain_en": 'Adequate disclosure → unmodified opinion + Emphasis of Matter paragraph. This draws attention without modifying the opinion. Adverse or disclaimer are appropriate only when disclosure is absent or inadequate.'
        },
        {
            "ru": 'Судебный иск на 50 млн (существенность 10 млн). Менеджмент не предоставляет документы. Какое заключение?',
            "en": '50m lawsuit (materiality 10m). Management withholds documents. What opinion?',
            "opts_ru": ['Отказ от выражения мнения (disclaimer) — ограничение объёма существенно и повсеместно', 'Оговорка — иск существенен но можно ограничить объём', 'Отрицательное — аудитор уверен что есть искажение', 'Немодифицированное — менеджмент обещал решить вопрос'],
            "opts_en": ["","","",""],
            "correct": 0,
            "explain_ru": '50 млн >> 10 млн. Аудитор не может получить доказательства (scope limitation). Влияние потенциального искажения повсеместно (может затронуть многие статьи). → Disclaimer (отказ от мнения).',
            "explain_en": '50m >> 10m materiality. Auditor cannot get evidence (scope limitation) and the potential effect is pervasive (could affect liabilities, profit, equity). → Disclaimer of opinion.'
        },
        {
            "ru": 'Какое событие является КОРРЕКТИРУЮЩИМ (adjusting) и требует изменения отчётности?',
            "en": 'Which is an ADJUSTING subsequent event requiring changes to the financial statements?',
            "opts_ru": ['Покупатель объявил о банкротстве в феврале подтвердив что был неплатёжеспособен уже на 31 декабря', 'Пожар на заводе произошедший в январе', 'Подписание крупного нового контракта в феврале', 'Объявление о дивидендах советом директоров в январе'],
            "opts_en": ["","","",""],
            "correct": 0,
            "explain_ru": 'Банкротство покупателя в феврале подтверждает неплатёжеспособность на 31 декабря → корректирующее: нужно доначислить резерв. Пожар, дивиденды, контракт — некорректирующие (возникли ПОСЛЕ отчётной даты).',
            "explain_en": 'Debtor bankruptcy confirming insolvency at 31 Dec → adjusting: increase bad debt provision. Fire, dividends and new contract arose AFTER year-end → non-adjusting: disclosure only.'
        },
        {
            "ru": 'Аудитор подписал заключение 15 марта. 20 марта узнал о существенном факте. Что обязан сделать?',
            "en": 'Report signed 15 March. 20 March: material fact discovered. What must the auditor do?',
            "opts_ru": ['Немедленно отозвать заключение и уведомить всех', 'Обсудить с менеджментом необходимость изменения отчётности и уведомления пользователей', 'Ничего — после подписания ответственность переходит к менеджменту', 'Выдать новое заключение с более ранней датой'],
            "opts_en": ["","","",""],
            "correct": 1,
            "explain_ru": 'После подписания у аудитора нет активной обязанности искать новые факты. Но если факт стал известен — обсудить с менеджментом изменение отчётности и уведомление пользователей о переиздании.',
            "explain_en": 'After signing, no active duty to seek new facts. But if a material fact becomes known: discuss amendment with management, financial statements should be reissued, and users notified of the restatement.'
        },
        {
            "ru": 'KAM (Key Audit Matters) — кто обязан включать в заключение?',
            "en": 'KAM (Key Audit Matters) — who must include them in the report?',
            "opts_ru": ['Все компании обязаны включать KAM в заключение', 'Только компании с высоким риском мошенничества', 'Только листинговые компании (listed entities)', 'Только крупные компании с выручкой свыше 1 млрд'],
            "opts_en": ["","","",""],
            "correct": 2,
            "explain_ru": 'KAM обязательны только для листинговых компаний (listed entities). Для нелистинговых — по усмотрению аудитора или если требует законодательство. KAM повышают прозрачность аудита для пользователей.',
            "explain_en": 'KAM are mandatory only for listed entities. For non-listed entities they are optional unless required by regulation. KAM improve transparency by communicating what the auditor focused on most significantly.'
        },
        {
            "ru": 'Менеджмент изменил учётную политику без раскрытия в примечаниях. Влияние 3% от существенности. Как это влияет на заключение?',
            "en": 'Policy change undisclosed in notes. Impact is 3% of materiality. Effect on opinion?',
            "opts_ru": ['Параграф Emphasis of Matter', 'Отрицательное мнение', 'Потенциальная оговорка — нераскрытие изменения учётной политики нарушает стандарты', 'Никакого — сумма ниже существенности'],
            "opts_en": ["","","",""],
            "correct": 2,
            "explain_ru": 'Нераскрытое изменение учётной политики нарушает МСФО (требует раскрытия и ретроспективного применения). Даже при малом числовом влиянии нераскрытие может быть существенным для понимания. → Разногласие с менеджментом → потенциальная оговорка.',
            "explain_en": "Undisclosed accounting policy change violates IFRS (requires disclosure and retrospective application). Even if numeric impact is small, failure to disclose may be material to users' understanding → disagreement with management → potential qualified opinion."
        },
        {
            "ru": 'В прошлом году — adverse opinion. Все искажения исправлены. Какое заключение выдать в этом году?',
            "en": 'Last year adverse opinion. All misstatements corrected this year. What opinion now?',
            "opts_ru": ['Немодифицированное если текущая отчётность во всех существенных аспектах достоверна', 'Снова adverse — нельзя перейти к чистому после adverse', 'Оговорка как промежуточный шаг', 'Аудитор не может работать с клиентом после adverse opinion'],
            "opts_en": ["","","",""],
            "correct": 0,
            "explain_ru": 'Тип заключения определяется состоянием ТЕКУЩЕЙ отчётности. Если все исправления внесены и текущий год достоверен → немодифицированное. Прошлые adverse opinions не влияют на текущий аудит.',
            "explain_en": "The opinion is determined by the CURRENT year's statements. If all corrections made and current statements are true and fair → unmodified opinion. Prior adverse opinions do not affect the current year's audit."
        },
        {
            "ru": 'Разница между Emphasis of Matter и Other Matter:',
            "en": 'Difference between Emphasis of Matter and Other Matter:',
            "opts_ru": ['Оба означают одно и то же', 'Emphasis обязателен; Other Matter по усмотрению', 'Emphasis изменяет мнение; Other Matter нет', 'Emphasis — вопрос УЖЕ РАСКРЫТ в отчётности; Other Matter — вопрос НЕ раскрыт в отчётности но важен для понимания аудита'],
            "opts_en": ["","","",""],
            "correct": 3,
            "explain_ru": 'Ключевое: Emphasis of Matter — вопрос есть в отчётности, аудитор лишь привлекает внимание. Other Matter — вопрос НЕ в отчётности (например ограничение распространения заключения). Оба не изменяют мнение.',
            "explain_en": 'Key distinction: Emphasis of Matter — matter IS disclosed in statements, auditor draws attention. Other Matter — matter NOT in statements (e.g. restriction on report distribution). Neither modifies the opinion.'
        },
        {
            "ru": 'Нераскрытые операции со связанными сторонами на 20 млн (существенность 15 млн). Менеджмент отказывается раскрывать. Что делает аудитор?',
            "en": 'Undisclosed related party transactions 20m (materiality 15m). Management refuses to disclose. What does auditor do?',
            "opts_ru": ['Добавляет Other Matter', 'Не меняет заключение — раскрытие необязательно', 'Выдаёт оговорку или отрицательное мнение в зависимости от того повсеместно ли влияние', 'Добавляет Emphasis of Matter'],
            "opts_en": ["","","",""],
            "correct": 2,
            "explain_ru": 'Нераскрытие RPT на 20 млн > 15 млн (существенности) = существенное нарушение. Если влияние ограничено → оговорка. Если повсеместно (RPT составляют значительную часть деятельности) → отрицательное мнение.',
            "explain_en": 'Undisclosed RPTs of 20m exceed materiality (15m) → material misstatement. If effect limited to this area → qualified. If pervasive (RPTs represent a significant portion of the business) → adverse opinion.'
        },
        {
            "ru": "Раздел 'Существенная неопределённость по going concern' добавляется когда:",
            "en": "The 'Material Uncertainty Related to Going Concern' section is added when:",
            "opts_ru": ['Существенная неопределённость идентифицирована И адекватно раскрыта в отчётности', 'Компания не представила план устранения проблем', 'Всегда когда у компании есть убытки', 'Только при планировании выдать отрицательное мнение'],
            "opts_en": ["","","",""],
            "correct": 0,
            "explain_ru": 'Специальный раздел добавляется когда: 1) существенная неопределённость по going concern идентифицирована И 2) менеджмент адекватно её раскрыл. Мнение остаётся немодифицированным — раскрытие достаточно.',
            "explain_en": 'Added when: 1) material going concern uncertainty exists AND 2) management has adequately disclosed it. The opinion remains unmodified — adequate disclosure means no modification is needed.'
        },
        {
            "ru": 'Ответственность менеджмента в аудиторском заключении включает:',
            "en": "Management's responsibility in the audit report covers:",
            "opts_ru": ['Оплату аудиторского гонорара', 'Подготовку финансовой отчётности по стандартам и поддержание внутреннего контроля', 'Проведение аудита и выбор аудиторских процедур', 'Выбор аудиторской фирмы'],
            "opts_en": ["","","",""],
            "correct": 1,
            "explain_ru": 'В заключении указывается ответственность менеджмента за: подготовку отчётности в соответствии со стандартами и поддержание системы внутреннего контроля необходимой для достоверной отчётности.',
            "explain_en": "Management's responsibility covers: preparing financial statements per the applicable framework, and maintaining internal controls necessary for reliable financial reporting."
        },
        {
            "ru": 'Через 3 месяца после подписания найдена существенная ошибка о которой аудитор не знал. Последствия:',
            "en": "3 months after signing, material error found that auditor didn't know about. Consequences:",
            "opts_ru": ['Автоматическая финансовая ответственность перед всеми пользователями', 'Никакой ответственности после подписания', 'Профессиональная ответственность если стандарты не соблюдались; при соблюдении — ограниченная ответственность так как аудит даёт разумную уверенность', 'Ответственность только если ошибка превышает существенность в 10 раз'],
            "opts_en": ["","","",""],
            "correct": 2,
            "explain_ru": 'Ключевой вопрос: соблюдались ли стандарты? Если да и ошибка не обнаруживаема при надлежащем аудите — ответственность ограничена. Аудит не обеспечивает абсолютную уверенность. При нарушении стандартов — профессиональная ответственность.',
            "explain_en": "Key question: were standards followed? If yes and the error was undetectable in a properly conducted audit, liability is limited — reasonable assurance doesn't mean perfection. If standards breached, professional liability may arise."
        },
        {
            "ru": 'Qualified opinion из-за ограничения объёма прошлого года. В этом году ограничение устранено. Заключение:',
            "en": "Qualified opinion due to scope limitation last year. Limitation removed this year. This year's opinion:",
            "opts_ru": ['Нужно пересмотреть заключение прошлого года', 'Сравнительные цифры должны быть переаудированы', 'Обязательно оговорка снова как минимум год', 'Немодифицированное если текущий аудит полноценен и отчётность достоверна'],
            "opts_en": ["","","",""],
            "correct": 3,
            "explain_ru": 'Каждый год независим. Если ограничение устранено и текущий аудит проведён полноценно → немодифицированное. Возможно потребуется рассмотреть сравнительные данные.',
            "explain_en": 'Each year is assessed independently. If limitation removed and current audit fully completed → unmodified opinion. The auditor may need to consider the effect on comparative figures.'
        },
        {
            "ru": 'Принцип true and fair view означает:',
            "en": 'True and fair view means:',
            "opts_ru": ['Отчётность достоверно отражает финансовое положение результаты и денежные потоки в соответствии со стандартами', 'Аудитор положительно оценивает бизнес клиента', 'Отчётность абсолютно точна без погрешностей', 'Менеджмент честный и справедливый человек'],
            "opts_en": ["","","",""],
            "correct": 0,
            "explain_ru": 'True and fair: отчётность правдиво (true — соответствует фактам) и справедливо (fair — не вводит в заблуждение) отражает финансовое положение, результаты и денежные потоки согласно применимым стандартам.',
            "explain_en": 'True and fair: statements faithfully represent (true — factually correct) and are not misleading (fair — properly presented) the financial position, performance and cash flows per the applicable framework.'
        },
        {
            "ru": 'Other Matter параграф добавляется когда:',
            "en": 'An Other Matter paragraph is added when:',
            "opts_ru": ['Аудитор не согласен с учётной политикой', 'Аудитор хочет подчеркнуть качество своей работы', 'Нужно привлечь внимание к вопросу НЕ в отчётности но важному для понимания аудита или ответственности аудитора', 'Аудитор хочет дать дополнительные рекомендации'],
            "opts_en": ["","","",""],
            "correct": 2,
            "explain_ru": 'Other Matter привлекает внимание к вопросу НЕ в финансовой отчётности, но важному для понимания: например ограничение распространения заключения или ссылка на другое заключение.',
            "explain_en": "Other Matter draws attention to a matter NOT in the financial statements but relevant to users' understanding — e.g. restriction on report distribution or reference to another auditor's report."
        },
        {
            "ru": 'Adverse opinion выдаётся когда:',
            "en": 'An adverse opinion is issued when:',
            "opts_ru": ['Менеджмент не предоставил письма-представления', 'Аудитор не может получить достаточные доказательства', 'Искажение существенно И повсеместно — отчётность в целом недостоверна', 'Искажение существенно но ограничено одной областью'],
            "opts_en": ["","","",""],
            "correct": 2,
            "explain_ru": 'Ключевое слово — pervasive (повсеместный). Adverse: искажение существенно И повсеместно — значит вся отчётность как целое недостоверна. Qualified: существенно НО не повсеместно. Disclaimer: нельзя получить доказательства.',
            "explain_en": 'Key word: pervasive. Adverse: misstatement is material AND pervasive — financial statements as a whole are misleading. Qualified: material but NOT pervasive. Disclaimer: cannot obtain sufficient evidence.'
        },
    ],
}

BLOCK_NAMES = {
    "A": "Блок A · Суть аудита",
    "B": "Блок B · Риски и планирование",
    "C": "Блок C · Внутренний контроль",
    "D": "Блок D · Доказательства ★",
    "E": "Блок E · Заключение аудитора",
    "ALL": "Все блоки вместе",
}


# ──────────────────────────────────────────────
#  HELPERS
# ──────────────────────────────────────────────
def get_main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 Все блоки", callback_data="start_ALL")],
        [
            InlineKeyboardButton("A · Суть", callback_data="start_A"),
            InlineKeyboardButton("B · Риски", callback_data="start_B"),
        ],
        [
            InlineKeyboardButton("C · Контроль", callback_data="start_C"),
            InlineKeyboardButton("E · Заключение", callback_data="start_E"),
        ],
        [InlineKeyboardButton("🔬 D · Доказательства (отдельно)", callback_data="start_D")],
        [InlineKeyboardButton("📊 Мой прогресс", callback_data="stats")],
        [InlineKeyboardButton("📜 История ответов", callback_data="history")],
    ])


def show_question_text(q, num, total):
    letters = ["А", "Б", "В", "Г"]
    opts_text = "\n".join([f"{letters[i]}. {opt}" for i, opt in enumerate(q["opts_ru"])])
    text = (
        f"📝 *Вопрос {num}/{total}*\n"
        f"_{q['en']}_\n\n"
        f"*{q['ru']}*\n\n"
        f"{opts_text}"
    )
    return text


def build_answer_keyboard(question_idx):
    letters = ["А", "Б", "В", "Г"]
    rows = [[
        InlineKeyboardButton(letters[i], callback_data=f"ans_{question_idx}_{i}")
        for i in range(4)
    ]]
    return InlineKeyboardMarkup(rows)


def save_history(context, entry: str):
    history = context.user_data.setdefault("history", [])
    history.append(entry)
    # Храним последние 50 записей
    if len(history) > 50:
        context.user_data["history"] = history[-50:]


def init_session(context, mode):
    if mode == "ALL":
        pool = []
        for block_questions in QUESTIONS.values():
            pool.extend(block_questions)
    else:
        pool = list(QUESTIONS.get(mode, []))
    random.shuffle(pool)
    context.user_data["session"] = {
        "mode": mode,
        "pool": pool,
        "idx": 0,
        "correct": 0,
        "wrong": 0,
        "total": len(pool),
    }


def get_stats(context):
    s = context.user_data.get("stats", {"correct": 0, "wrong": 0, "sessions": 0})
    return s


def update_stats(context, correct: bool):
    s = context.user_data.setdefault("stats", {"correct": 0, "wrong": 0, "sessions": 0})
    if correct:
        s["correct"] += 1
    else:
        s["wrong"] += 1


# ──────────────────────────────────────────────
#  HANDLERS
# ──────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name or "Привет"
    await update.message.reply_text(
        f"👋 {name}!\n\n"
        "Это тренажёр по *ACCA AA* — Audit & Assurance.\n\n"
        "После каждого ответа ты получишь:\n"
        "• объяснение на *русском*\n"
        "• то же самое на *английском* — чтобы привыкать к терминам\n\n"
        "Выбери режим:",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # ── START SESSION ──
    if data.startswith("start_"):
        mode = data.split("_")[1]
        init_session(context, mode)
        s = context.user_data["session"]
        context.user_data["stats"] = context.user_data.get("stats", {"correct": 0, "wrong": 0, "sessions": 0})
        context.user_data["stats"]["sessions"] += 1
        await query.edit_message_text(
            f"✅ Режим: *{BLOCK_NAMES[mode]}*\n"
            f"Вопросов: *{s['total']}*\n\n"
            "Поехали! 🚀",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("▶️ Начать", callback_data="next")
            ]])
        )
        return

    # ── NEXT QUESTION ──
    if data == "next":
        s = context.user_data.get("session")
        if not s or s["idx"] >= s["total"]:
            await query.edit_message_text(
                "Сессия завершена! Нажми /start чтобы начать заново.",
                reply_markup=get_main_keyboard()
            )
            return
        q = s["pool"][s["idx"]]
        num = s["idx"] + 1
        total = s["total"]
        text = show_question_text(q, num, total)
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=build_answer_keyboard(s["idx"])
        )
        return

    # ── ANSWER ──
    if data.startswith("ans_"):
        _, q_idx_str, ans_str = data.split("_")
        q_idx = int(q_idx_str)
        ans = int(ans_str)
        s = context.user_data.get("session")
        if not s or s["idx"] != q_idx:
            return
        q = s["pool"][q_idx]
        correct = q["correct"]
        is_correct = ans == correct
        letters = ["А", "Б", "В", "Г"]

        if is_correct:
            result_line = "✅ *Верно!*"
            s["correct"] += 1
        else:
            result_line = (
                f"❌ *Неверно.*\n"
                f"Правильный ответ: *{letters[correct]}. {q['opts_ru'][correct]}*"
            )
            s["wrong"] += 1

        update_stats(context, is_correct)
        s["idx"] += 1

        # Сохраняем в историю
        history_entry = (
            f"❓ {q['ru']}\n"
            f"{'✅' if is_correct else '❌'} Твой ответ: {letters[ans]}. {q['opts_ru'][ans]}"
            + (f"\n✔️ Правильно: {letters[correct]}. {q['opts_ru'][correct]}" if not is_correct else "")
        )
        save_history(context, history_entry)

        pct = round((s["correct"] / s["idx"]) * 100) if s["idx"] > 0 else 0
        progress = f"Прогресс: {s['correct']}/{s['idx']} ({pct}%)"

        text = (
            f"{result_line}\n\n"
            f"📖 *RU:* {q['explain_ru']}\n\n"
            f"🇬🇧 *EN:* _{q['explain_en']}_\n\n"
            f"─────────────\n{progress}"
        )

        if s["idx"] >= s["total"]:
            # Session finished
            pct_final = round((s["correct"] / s["total"]) * 100)
            emoji = "🏆" if pct_final >= 80 else "📚" if pct_final >= 50 else "💪"
            text += (
                f"\n\n{emoji} *Раунд завершён!*\n"
                f"Результат: *{s['correct']}/{s['total']} ({pct_final}%)*\n\n"
                f"Проходной балл AA: 50% — "
                + ("ты уже там! 🎉" if pct_final >= 50 else "ещё немного!")
            )
            await query.edit_message_text(
                text,
                parse_mode="Markdown",
                reply_markup=get_main_keyboard()
            )
        else:
            await query.edit_message_text(
                text,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("➡️ Следующий вопрос", callback_data="next"),
                    InlineKeyboardButton("🏠 Меню", callback_data="menu")
                ]])
            )
        return

    # ── STATS ──
    if data == "stats":
        s_all = get_stats(context)
        total = s_all["correct"] + s_all["wrong"]
        pct = round((s_all["correct"] / total) * 100) if total > 0 else 0
        text = (
            f"📊 *Твоя статистика*\n\n"
            f"✅ Верно: {s_all['correct']}\n"
            f"❌ Неверно: {s_all['wrong']}\n"
            f"📝 Всего ответов: {total}\n"
            f"🎯 Точность: {pct}%\n"
            f"🔄 Сессий: {s_all['sessions']}\n\n"
            f"Проходной балл на AA — 50%"
        )
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("⬅️ Назад", callback_data="menu")
            ]])
        )
        return

    # ── HISTORY ──
    if data == "history":
        history = context.user_data.get("history", [])
        if not history:
            await query.edit_message_text(
                "📜 История пока пуста — начни отвечать на вопросы!",
                reply_markup=get_main_keyboard()
            )
            return
        text = "📜 *Твоя история ответов (последние 10):*\n\n"
        text += "\n\n".join(history[-10:])
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("⬅️ Назад", callback_data="menu")
            ]])
        )
        return

    # ── MENU ──
    if data == "menu":
        await query.edit_message_text(
            "Выбери режим:",
            reply_markup=get_main_keyboard()
        )
        return


# ──────────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────────
async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    history = context.user_data.get("history", [])
    if not history:
        await update.message.reply_text(
            "📜 История пока пуста — начни отвечать на вопросы!",
            reply_markup=get_main_keyboard()
        )
        return
    text = "📜 *Твоя история ответов (последние):*\n\n"
    text += "\n\n".join(history[-10:])
    await update.message.reply_text(text, parse_mode="Markdown")


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("history", history_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Бот запущен ✅")
    app.run_polling()


if __name__ == "__main__":
    main()

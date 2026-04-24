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
            "ru": "Что такое ассюранс-задание?",
            "en": "What is an assurance engagement?",
            "opts_ru": [
                "Аудитор составляет отчётность вместо клиента",
                "Профессионал выражает заключение, повышающее доверие к предмету проверки",
                "Консультация по налогам",
                "Внутренняя проверка компанией своих процессов"
            ],
            "opts_en": [
                "The auditor prepares financial statements for the client",
                "A practitioner expresses a conclusion to enhance confidence in a subject matter",
                "A tax advisory service",
                "An internal review of company processes"
            ],
            "correct": 1,
            "explain_ru": "Ассюранс-задание (assurance engagement) — задание, в котором независимый профессионал изучает предмет (например, финансовую отчётность) и выдаёт заключение для повышения уверенности пользователей.",
            "explain_en": "An assurance engagement is one in which a practitioner expresses a conclusion designed to enhance the degree of confidence of intended users about the outcome of the evaluation of a subject matter."
        },
        {
            "ru": "Главная цель внешнего аудита финансовой отчётности?",
            "en": "What is the primary objective of an external audit?",
            "opts_ru": [
                "Найти все мошенничества в компании",
                "Выразить независимое мнение о достоверности финансовой отчётности",
                "Подготовить отчётность для налоговой",
                "Проверить эффективность работы сотрудников"
            ],
            "opts_en": [
                "To detect all fraud in the company",
                "To express an independent opinion on whether the financial statements give a true and fair view",
                "To prepare financial statements for tax purposes",
                "To assess employee performance"
            ],
            "correct": 1,
            "explain_ru": "Главная цель внешнего аудита — выразить независимое мнение (opinion) о том, отражает ли отчётность достоверно положение дел. Аудитор НЕ гарантирует нахождение всего мошенничества.",
            "explain_en": "The primary objective of an external audit is to express an opinion on whether the financial statements give a true and fair view. The auditor does NOT guarantee detection of all fraud."
        },
        {
            "ru": "Что означает профессиональный скептицизм (professional scepticism)?",
            "en": "What does professional scepticism mean?",
            "opts_ru": [
                "Аудитор не доверяет никому и думает, что клиент всегда врёт",
                "Аудитор критически оценивает доказательства, не принимая их слепо на веру",
                "Аудитор соглашается со всем, что говорит клиент",
                "Аудитор отказывается от задания при любых рисках"
            ],
            "opts_en": [
                "The auditor trusts no one and assumes the client always lies",
                "The auditor critically assesses evidence without blind acceptance",
                "The auditor agrees with everything management says",
                "The auditor refuses any engagement with risks"
            ],
            "correct": 1,
            "explain_ru": "Профессиональный скептицизм — баланс: аудитор не верит всему слепо, но и не подозревает всех автоматически. Он критически проверяет доказательства.",
            "explain_en": "Professional scepticism is an attitude that includes a questioning mind and critical assessment of audit evidence. It is a balance — not blind trust, but not automatic suspicion either."
        },
        {
            "ru": "Почему независимость аудитора важна?",
            "en": "Why is auditor independence important?",
            "opts_ru": [
                "Чтобы аудитор мог брать задания от одного клиента бесконечно",
                "Без независимости мнение аудитора теряет ценность для пользователей",
                "Независимость нужна только для госкомпаний",
                "Чтобы аудитор не платил налоги с гонорара"
            ],
            "opts_en": [
                "So the auditor can work for one client indefinitely",
                "Without independence, the auditor's opinion loses its value to users",
                "Independence is only required for public sector audits",
                "So the auditor pays no tax on fees"
            ],
            "correct": 1,
            "explain_ru": "Независимость бывает двух видов: в мышлении (independence of mind) и внешняя (independence in appearance). Если пользователи думают, что аудитор зависит от клиента — они не будут доверять его заключению.",
            "explain_en": "Independence has two aspects: independence of mind and independence in appearance. If users believe the auditor is not independent, they will not trust the audit opinion — making it worthless."
        },
        {
            "ru": "Какие три стороны есть в ассюранс-задании?",
            "en": "What are the three parties in an assurance engagement?",
            "opts_ru": ["Аудитор, клиент, налоговая", "Практик, ответственная сторона, предполагаемые пользователи", "Директор, бухгалтер, аудитор", "Инвестор, банк, регулятор"],
            "correct": 1,
            "explain_ru": "Три стороны: практик (practitioner) — аудитор; ответственная сторона (responsible party) — менеджмент, готовящий предмет проверки; предполагаемые пользователи (intended users) — акционеры, банки, инвесторы.",
            "explain_en": "Three parties: practitioner (auditor), responsible party (management who prepares the subject matter), and intended users (shareholders, banks, investors who rely on the conclusion)."
        },
        {
            "ru": "Что такое угроза близости (familiarity threat)?",
            "en": "What is a familiarity threat?",
            "opts_ru": ["Аудитор хорошо знает стандарты аудита", "Аудитор становится слишком лояльным из-за длительных отношений с клиентом", "Клиент угрожает сменить аудитора", "Аудитор работает в одном здании с клиентом"],
            "correct": 1,
            "explain_ru": "Угроза близости — из-за длительных отношений аудитор становится слишком симпатизирующим интересам клиента и перестаёт критически оценивать информацию.",
            "explain_en": "A familiarity threat arises when a long relationship causes the auditor to become too sympathetic to the client's interests, compromising objectivity and professional scepticism."
        },
        {
            "ru": "Что такое угроза запугивания (intimidation threat)?",
            "en": "What is an intimidation threat?",
            "opts_ru": ["Клиент агрессивен на переговорах", "Аудитор испытывает давление влияющее на его объективность", "Аудитор боится сложных расчётов", "Клиент подаёт жалобу на аудитора"],
            "correct": 1,
            "explain_ru": "Угроза запугивания — клиент оказывает давление на аудитора (угрожает сменить аудитора, подать в суд), что может повлиять на его независимость.",
            "explain_en": "An intimidation threat arises when the auditor is deterred from acting objectively by actual or perceived threats such as dismissal or legal action."
        },
        {
            "ru": "Что такое угроза самопроверки (self-review threat)?",
            "en": "What is a self-review threat?",
            "opts_ru": ["Аудитор проверяет свои рабочие документы", "Аудитор проверяет работу которую сам ранее выполнял для клиента", "Аудитор оценивает свои профессиональные навыки", "Аудитор повторно читает стандарты"],
            "correct": 1,
            "explain_ru": "Угроза самопроверки — когда аудитор проверяет работу которую сам ранее принимал для клиента. Например: составлял отчётность, а потом её же аудирует.",
            "explain_en": "A self-review threat arises when the auditor reviews their own previous work or judgements — e.g. auditing financial statements they helped to prepare."
        },
        {
            "ru": "Что такое угроза личной заинтересованности (self-interest threat)?",
            "en": "What is a self-interest threat?",
            "opts_ru": ["Аудитор хочет повышение", "Финансовый или иной личный интерес аудитора может повлиять на суждение", "Аудитор хочет изучить новый стандарт", "Клиент предлагает скидку"],
            "correct": 1,
            "explain_ru": "Угроза личной заинтересованности — когда у аудитора есть финансовый или иной личный интерес в клиенте (например, акции клиента), влияющий на объективность.",
            "explain_en": "A self-interest threat arises when the auditor has a financial or personal interest in the client — e.g. owning shares — which could improperly influence professional judgement."
        },
        {
            "ru": "Что такое угроза адвокации (advocacy threat)?",
            "en": "What is an advocacy threat?",
            "opts_ru": ["Аудитор нанимает адвоката", "Аудитор продвигает позицию клиента что угрожает его объективности", "Клиент нанимает адвоката против аудитора", "Аудитор консультирует по юридическим вопросам"],
            "correct": 1,
            "explain_ru": "Угроза адвокации — когда аудитор продвигает точку зрения клиента настолько, что это ставит под угрозу его объективность. Пример: аудитор представляет клиента в суде.",
            "explain_en": "An advocacy threat arises when the auditor promotes a client's position to the point that objectivity is compromised — e.g. representing the client in legal proceedings or negotiations."
        },
        {
            "ru": "Какие пять принципов этики определяет ACCA?",
            "en": "What are the five fundamental ethical principles of ACCA?",
            "opts_ru": ["Честность, справедливость, точность, скорость, эффективность", "Честность, объективность, профессиональная компетентность, конфиденциальность, профессиональное поведение", "Независимость, скептицизм, точность, осторожность, честность", "Справедливость, независимость, объективность, честность, точность"],
            "correct": 1,
            "explain_ru": "Пять принципов ACCA: честность (integrity), объективность (objectivity), профессиональная компетентность и должная осмотрительность (professional competence and due care), конфиденциальность (confidentiality), профессиональное поведение (professional behaviour).",
            "explain_en": "Five ACCA principles: integrity, objectivity, professional competence and due care, confidentiality, and professional behaviour. These form the framework for ethical decision-making."
        },
        {
            "ru": "Что такое конфиденциальность (confidentiality) как принцип этики?",
            "en": "What is confidentiality as an ethical principle?",
            "opts_ru": ["Аудитор не разговаривает с коллегами", "Аудитор не раскрывает информацию о клиенте без надлежащего разрешения", "Аудитор хранит рабочие документы в сейфе", "Аудитор не публикует своё мнение"],
            "correct": 1,
            "explain_ru": "Конфиденциальность — аудитор не раскрывает информацию о клиенте третьим лицам без разрешения, за исключением случаев предусмотренных законом или профессиональным долгом.",
            "explain_en": "Confidentiality requires the auditor not to disclose client information to third parties without authority, unless there is a legal or professional right or duty to disclose."
        },
        {
            "ru": "Что такое внутренний аудит (internal audit)?",
            "en": "What is internal audit?",
            "opts_ru": ["Аудит проводимый налоговой", "Независимая функция внутри организации для оценки и улучшения её деятельности", "Проверка финансовой отчётности внешним аудитором", "Проверка только кассовых операций"],
            "correct": 1,
            "explain_ru": "Внутренний аудит — независимая функция внутри организации, оценивающая и улучшающая эффективность управления рисками, контроля и корпоративного управления.",
            "explain_en": "Internal audit is an independent assurance and consulting function within an organisation designed to add value by evaluating risk management, controls and governance."
        },
        {
            "ru": "Чем внутренний аудит отличается от внешнего?",
            "en": "How does internal audit differ from external audit?",
            "opts_ru": ["Ничем", "Внутренний — сотрудник компании; внешний — независим; разные цели и аудитории", "Внутренний всегда лучше внешнего", "Внешний проводится чаще внутреннего"],
            "correct": 1,
            "explain_ru": "Внутренний аудитор — сотрудник, отвечает перед менеджментом/комитетом. Внешний — независим, назначается акционерами, цель — мнение о финансовой отчётности.",
            "explain_en": "Internal auditors are employees reporting to management/audit committee. External auditors are independent, appointed by shareholders, focused on the truth and fairness of financial statements."
        },
        {
            "ru": "Что такое комитет по аудиту (audit committee)?",
            "en": "What is an audit committee?",
            "opts_ru": ["Государственный орган надзора за аудиторами", "Подкомитет совета директоров из независимых директоров надзирающих за аудитом", "Группа внутренних аудиторов компании", "Комиссия по выбору аудиторской фирмы"],
            "correct": 1,
            "explain_ru": "Комитет по аудиту — подкомитет совета директоров из независимых неисполнительных директоров. Надзирает за финансовой отчётностью, внутренним и внешним аудитом.",
            "explain_en": "An audit committee is a sub-committee of the board of independent non-executive directors overseeing financial reporting, internal audit and the external auditor relationship."
        },
        {
            "ru": "Что такое корпоративное управление (corporate governance)?",
            "en": "What is corporate governance?",
            "opts_ru": ["Управление только государственными компаниями", "Система правил и процессов с помощью которых компания направляется и контролируется", "Налоговое планирование компании", "Структура отдела бухгалтерии"],
            "correct": 1,
            "explain_ru": "Корпоративное управление — система правил, практик и процессов, с помощью которых компания направляется и контролируется в интересах всех заинтересованных сторон.",
            "explain_en": "Corporate governance is the system by which companies are directed and controlled, balancing interests of shareholders, management, employees and other stakeholders."
        },
        {
            "ru": "Что означает принцип профессионального поведения (professional behaviour)?",
            "en": "What does professional behaviour mean?",
            "opts_ru": ["Носить деловой костюм", "Соблюдать законы и правила и избегать действий дискредитирующих профессию", "Всегда приходить вовремя", "Вести себя формально с клиентом"],
            "correct": 1,
            "explain_ru": "Профессиональное поведение — аудитор должен соблюдать законы и избегать действий дискредитирующих профессию или ACCA.",
            "explain_en": "Professional behaviour requires compliance with relevant laws and regulations and avoiding any action that discredits the profession or ACCA."
        },
        {
            "ru": "Что такое профессиональная компетентность и должная осмотрительность?",
            "en": "What is professional competence and due care?",
            "opts_ru": ["Аудитор должен быть очень умным", "Аудитор должен поддерживать профессиональные знания и действовать добросовестно", "Аудитор никогда не должен ошибаться", "Аудитор должен проверять всё дважды"],
            "correct": 1,
            "explain_ru": "Профессиональная компетентность и должная осмотрительность — аудитор должен поддерживать профессиональные знания на уровне позволяющем компетентно обслуживать клиентов, и действовать добросовестно в соответствии со стандартами.",
            "explain_en": "Professional competence and due care require the auditor to maintain professional knowledge at the level needed to provide competent service and act diligently in accordance with applicable standards."
        },
    ],
    "B": [
        {
            "ru": "Из каких трёх компонентов состоит аудиторский риск?",
            "en": "What are the three components of audit risk?",
            "opts_ru": [
                "Риск мошенничества, риск ошибки, риск банкротства",
                "Неотъемлемый риск, риск контроля, риск необнаружения",
                "Налоговый риск, операционный риск, финансовый риск",
                "Риск клиента, риск аудитора, риск рынка"
            ],
            "opts_en": [
                "Fraud risk, error risk, bankruptcy risk",
                "Inherent risk, control risk, detection risk",
                "Tax risk, operational risk, financial risk",
                "Client risk, auditor risk, market risk"
            ],
            "correct": 1,
            "explain_ru": "Аудиторский риск = Неотъемлемый риск (IR) × Риск контроля (CR) × Риск необнаружения (DR). Первые два аудитор оценивает, третий — контролирует сам через процедуры.",
            "explain_en": "Audit Risk = Inherent Risk × Control Risk × Detection Risk. The auditor assesses IR and CR, then sets DR accordingly by choosing the nature, timing and extent of audit procedures."
        },
        {
            "ru": "Что такое существенность (materiality)?",
            "en": "What is materiality in auditing?",
            "opts_ru": [
                "Сумма всех активов компании",
                "Порог, при превышении которого ошибка влияет на решения пользователей",
                "Минимальная сумма дебиторской задолженности для проверки",
                "Размер аудиторского гонорара"
            ],
            "opts_en": [
                "The total value of company assets",
                "The threshold above which a misstatement could influence users' decisions",
                "The minimum receivable balance subject to testing",
                "The size of the audit fee"
            ],
            "correct": 1,
            "explain_ru": "Существенность (materiality) — пороговое значение. Если ошибка выше этого порога, она может изменить решение пользователя. Аудитор устанавливает уровень существенности сам — обычно % от выручки, прибыли или активов.",
            "explain_en": "Materiality is the threshold above which a misstatement, individually or in aggregate, could influence the economic decisions of users. It is typically set as a percentage of revenue, profit or total assets."
        },
        {
            "ru": "Что описывает высокий неотъемлемый риск (inherent risk)?",
            "en": "Which best describes high inherent risk?",
            "opts_ru": [
                "Компания использует надёжную систему внутреннего контроля",
                "Компания работает в волатильной отрасли со сложными операциями",
                "Аудитор хорошо знает отрасль клиента",
                "Компания давно на рынке со стабильными показателями"
            ],
            "opts_en": [
                "The company has a reliable internal control system",
                "The company operates in a volatile industry with complex transactions",
                "The auditor has strong industry knowledge",
                "The company has been in business for years with stable results"
            ],
            "correct": 1,
            "explain_ru": "Неотъемлемый риск (inherent risk) — риск того, что статья отчётности подвержена ошибкам по своей природе, независимо от контроля. Волатильные активы, субъективные оценки, сложные операции — всё это повышает IR.",
            "explain_en": "Inherent risk is the susceptibility of an assertion to a material misstatement, assuming no related controls. Complex transactions, subjective estimates and volatile industries increase inherent risk."
        },
        {
            "ru": "Что означает принцип непрерывности деятельности (going concern)?",
            "en": "What does the going concern principle mean?",
            "opts_ru": [
                "Компания планирует продать бизнес в течение года",
                "Предположение о том, что компания будет работать минимум 12 месяцев",
                "Компания обязана публиковать отчётность каждый квартал",
                "Аудитор проверяет компанию непрерывно без перерывов"
            ],
            "opts_en": [
                "The company plans to sell its business within one year",
                "The assumption that the entity will continue operating for at least 12 months",
                "The company must publish quarterly reports",
                "The auditor monitors the company on a continuous basis"
            ],
            "correct": 1,
            "explain_ru": "Going concern — базовое допущение: компания будет работать минимум 12 месяцев с даты отчётности. Аудитор обязан оценить угрозы этому принципу. Признаки угрозы: убытки, потеря клиентов, судебные иски.",
            "explain_en": "Going concern is the assumption that the entity will continue in operational existence for at least 12 months from the balance sheet date. The auditor must evaluate whether this assumption is appropriate."
        },
        {
            "ru": "Что такое существенность исполнения (performance materiality)?",
            "en": "What is performance materiality?",
            "opts_ru": ["Уровень существенности для всей отчётности", "Сумма ниже общей существенности используемая для проверки отдельных статей", "Существенность для оценки работы сотрудников", "Минимальный размер ошибки для сообщения менеджменту"],
            "correct": 1,
            "explain_ru": "Существенность исполнения — сумма ниже общей существенности. Используется при проверке отдельных статей чтобы снизить риск того что совокупность мелких ошибок превысит общую существенность.",
            "explain_en": "Performance materiality is set below overall materiality and used when auditing individual items to reduce the risk that aggregate uncorrected misstatements exceed overall materiality."
        },
        {
            "ru": "Что такое письмо об условиях задания (engagement letter)?",
            "en": "What is an engagement letter?",
            "opts_ru": ["Письмо с отказом от задания", "Документ фиксирующий условия аудиторского задания между аудитором и клиентом", "Отчёт аудитора о недостатках контроля", "Письмо акционерам о результатах аудита"],
            "correct": 1,
            "explain_ru": "Письмо об условиях задания — договор между аудитором и клиентом. Включает: объём аудита, ответственность сторон, гонорар, сроки. Подписывается до начала аудита.",
            "explain_en": "An engagement letter is a contract covering the scope of the audit, responsibilities of each party, fee arrangements and reporting timelines. It is agreed and signed before audit work begins."
        },
        {
            "ru": "Что такое треугольник мошенничества (fraud triangle)?",
            "en": "What is the fraud triangle?",
            "opts_ru": ["Три вида аудиторского риска", "Три условия для мошенничества: давление, возможность и оправдание", "Три стороны аудиторского задания", "Три уровня существенности"],
            "correct": 1,
            "explain_ru": "Треугольник мошенничества: давление/мотив (pressure), возможность (opportunity) — слабые контроли, и оправдание (rationalisation). При наличии всех трёх риск мошенничества высок.",
            "explain_en": "The fraud triangle: pressure/incentive (motive), opportunity (weak controls), and rationalisation (the person justifies their actions). All three are typically present when fraud occurs."
        },
        {
            "ru": "Чем отличается ошибка (error) от мошенничества (fraud)?",
            "en": "What is the difference between error and fraud?",
            "opts_ru": ["Ничем", "Ошибка — непреднамеренная; мошенничество — преднамеренное действие", "Ошибка крупнее мошенничества", "Мошенничество совершают только менеджеры"],
            "correct": 1,
            "explain_ru": "Ошибка (error) — непреднамеренное искажение. Мошенничество (fraud) — преднамеренное действие с использованием обмана для получения нечестного преимущества.",
            "explain_en": "Error is an unintentional misstatement. Fraud involves intentional action by one or more individuals using deception to obtain an unjust or illegal advantage."
        },
        {
            "ru": "Каковы признаки угрозы непрерывности деятельности?",
            "en": "What are indicators of going concern problems?",
            "opts_ru": ["Рост выручки и прибыли", "Убытки, потеря клиентов, судебные иски, отказ банка в кредите", "Увеличение штата сотрудников", "Открытие новых офисов"],
            "correct": 1,
            "explain_ru": "Признаки угрозы going concern: операционные убытки, отрицательный денежный поток, потеря ключевых клиентов, судебные иски, отказ банка в кредите, задолженность по налогам.",
            "explain_en": "Going concern indicators: operating losses, negative cash flows, loss of key customers/suppliers, legal proceedings, bank refusing to renew credit facilities, and overdue tax liabilities."
        },
        {
            "ru": "Что такое существенный риск (significant risk)?",
            "en": "What is a significant risk?",
            "opts_ru": ["Любой риск выше нуля", "Риск требующий особого внимания из-за высокой вероятности или последствий", "Риск потери аудиторского контракта", "Риск ошибки в расчёте гонорара"],
            "correct": 1,
            "explain_ru": "Существенный риск — идентифицированный риск требующий особого внимания. Для таких рисков аудитор обязан оценить контроли клиента и провести процедуры по существу.",
            "explain_en": "A significant risk is an identified risk requiring special audit consideration. Controls must be evaluated and substantive procedures must be performed regardless of control effectiveness."
        },
        {
            "ru": "Что такое два типа мошенничества в аудите?",
            "en": "What are the two types of fraud in auditing?",
            "opts_ru": ["Налоговое и бухгалтерское мошенничество", "Мошеннические финансовые отчёты и присвоение активов", "Внутреннее и внешнее мошенничество", "Преднамеренное и случайное"], "correct": 1,
            "explain_ru": "Два типа: мошеннические финансовые отчёты (fraudulent financial reporting) — искажение отчётности менеджментом; присвоение активов (misappropriation of assets) — кража активов сотрудниками.",
            "explain_en": "Two types: fraudulent financial reporting (management manipulates financial statements) and misappropriation of assets (employees steal cash, inventory or other assets)."
        },
        {
            "ru": "Что такое аналитические процедуры на этапе планирования?",
            "en": "What are analytical procedures at planning?",
            "opts_ru": ["Детальная проверка каждой операции", "Анализ финансовых данных для выявления необычных колебаний и областей риска", "Составление аудиторского заключения", "Проверка системы контроля"],
            "correct": 1,
            "explain_ru": "Аналитические процедуры на этапе планирования — сравнение показателей с прошлыми периодами, бюджетами, отраслевыми данными. Помогают выявить области риска для фокусировки аудита.",
            "explain_en": "Analytical procedures at planning compare financial data with prior periods, budgets and industry data to identify unusual fluctuations that indicate areas of audit risk."
        },
        {
            "ru": "Что такое знание бизнеса клиента (knowledge of client's business)?",
            "en": "What is knowledge of the client's business?",
            "opts_ru": ["Личная дружба с директором", "Понимание отрасли операций структуры и среды клиента для выявления рисков", "Знание всех сотрудников клиента", "Доступ к базам данных клиента"],
            "correct": 1,
            "explain_ru": "Знание бизнеса — аудитор понимает отрасль, операции, структуру, стратегию и среду клиента. Это основа для выявления рисков и планирования аудита.",
            "explain_en": "Knowledge of the client's business includes understanding industry, operations, ownership, governance and strategy to identify risk areas and plan appropriate audit procedures."
        },
        {
            "ru": "Что такое процедуры оценки риска?",
            "en": "What are risk assessment procedures?",
            "opts_ru": ["Процедуры для проверки остатков счетов", "Процедуры для понимания клиента и его среды с целью выявления рисков искажения", "Тесты работы системы контроля", "Процедуры завершения аудита"],
            "correct": 1,
            "explain_ru": "Процедуры оценки риска проводятся на этапе планирования. Включают: запросы менеджменту (inquiries), аналитические процедуры (analytical procedures), наблюдение и инспекцию (observation and inspection).",
            "explain_en": "Risk assessment procedures are performed to understand the entity and its environment. They include inquiries to management, analytical procedures, and observation and inspection of documents."
        },
        {
            "ru": "Что аудитор делает при выявлении мошенничества?",
            "en": "What does the auditor do when fraud is identified?",
            "opts_ru": ["Немедленно сообщает в полицию", "Сообщает тем кто наделён полномочиями и рассматривает влияние на аудит", "Скрывает информацию чтобы не навредить клиенту", "Немедленно прекращает аудит"],
            "correct": 1,
            "explain_ru": "При выявлении мошенничества аудитор сообщает тем кто наделён полномочиями (those charged with governance) и оценивает влияние на аудит и заключение. В некоторых случаях — раскрытие регулятору.",
            "explain_en": "When fraud is identified the auditor reports to those charged with governance and considers the impact on the audit and opinion. In some jurisdictions disclosure to regulators may also be required."
        },
    ],
    "C": [
        {
            "ru": "Главная цель системы внутреннего контроля?",
            "en": "What is the main purpose of internal controls?",
            "opts_ru": [
                "Полностью исключить ошибки и мошенничество",
                "Дать разумную уверенность в достижении целей и надёжности отчётности",
                "Заменить работу внешнего аудитора",
                "Контролировать личные расходы сотрудников"
            ],
            "opts_en": [
                "To completely eliminate errors and fraud",
                "To provide reasonable assurance regarding achievement of objectives",
                "To replace the work of the external auditor",
                "To monitor personal employee expenses"
            ],
            "correct": 1,
            "explain_ru": "Внутренний контроль даёт только разумную уверенность (reasonable assurance), но не абсолютную. Причины: сговор сотрудников (collusion), нарушение правил, обход контроля руководством (management override).",
            "explain_en": "Internal controls provide only reasonable, not absolute, assurance. Limitations include collusion between employees, management override of controls, and human error."
        },
        {
            "ru": "Что такое разделение обязанностей (segregation of duties)?",
            "en": "What is segregation of duties?",
            "opts_ru": [
                "Разделение работы для повышения скорости",
                "Один человек не контролирует всю цепочку операции — снижает риск мошенничества",
                "Распределение задач по сложности между сотрудниками",
                "Система отпусков в бухгалтерии"
            ],
            "opts_en": [
                "Splitting work between departments to increase speed",
                "No single person controls an entire transaction — reduces fraud risk",
                "Allocating tasks by complexity among staff",
                "A leave management system for the finance team"
            ],
            "correct": 1,
            "explain_ru": "Разделение обязанностей (segregation of duties) — ключевой контроль: один человек не должен авторизовывать, выполнять и записывать одну операцию. Пример: тот, кто заказывает товар, не должен его и оплачивать.",
            "explain_en": "Segregation of duties ensures that no single individual controls all stages of a transaction (authorisation, execution, recording). Example: the person ordering goods should not also approve payment."
        },
        {
            "ru": "Что делает аудитор при обнаружении существенного недостатка контроля?",
            "en": "What does the auditor do when a significant control deficiency is found?",
            "opts_ru": [
                "Немедленно прекращает аудит",
                "Сообщает лицам, наделённым полномочиями (комитету по аудиту / руководству)",
                "Самостоятельно исправляет недостаток",
                "Игнорирует, если это не влияет на мнение"
            ],
            "opts_en": [
                "Immediately terminates the audit",
                "Reports it to those charged with governance (audit committee / management)",
                "Fixes the deficiency themselves",
                "Ignores it if it does not affect the opinion"
            ],
            "correct": 1,
            "explain_ru": "При обнаружении недостатков контроля аудитор сообщает тем, кто наделён полномочиями (those charged with governance) — совет директоров или комитет по аудиту. Аудитор НЕ исправляет сам — это угрожало бы независимости.",
            "explain_en": "The auditor must communicate significant deficiencies to those charged with governance (e.g. audit committee or board). The auditor must NOT fix deficiencies — doing so would compromise independence."
        },
        {
            "ru": "Что такое среда контроля (control environment)?",
            "en": "What is the control environment?",
            "opts_ru": ["Физическое место хранения документов", "Установки и действия руководства создающие основу для всей системы контроля", "Программное обеспечение для учёта", "Правила охраны офиса"],
            "correct": 1,
            "explain_ru": "Среда контроля — фундамент всей системы контроля. Включает: тон руководства (tone at the top), этические ценности, компетентность сотрудников, стиль управления.",
            "explain_en": "The control environment is the foundation of internal control. It includes tone at the top, ethical values, commitment to competence, governance structure and management's operating style."
        },
        {
            "ru": "Что такое физические контроли (physical controls)?",
            "en": "What are physical controls?",
            "opts_ru": ["Контроли проверяемые аудитором физически", "Меры по физической защите активов: замки, сейфы, системы доступа", "Медицинские проверки сотрудников", "Контроль физического состояния оборудования"],
            "correct": 1,
            "explain_ru": "Физические контроли — защита активов: замки на сейфах, охрана склада, системы видеонаблюдения, ограниченный доступ к кассе. Предотвращают кражу и несанкционированный доступ.",
            "explain_en": "Physical controls protect assets from theft and unauthorised access — safes, locks, restricted access, CCTV, security guards. They are key preventive controls over physical assets."
        },
        {
            "ru": "Что такое авторизация (authorisation) как элемент контроля?",
            "en": "What is authorisation as a control?",
            "opts_ru": ["Разрешение программного обеспечения", "Утверждение операций уполномоченным лицом до их исполнения", "Подпись директора на любом документе", "Разрешение налоговой на операции"],
            "correct": 1,
            "explain_ru": "Авторизация — операции должны быть одобрены уполномоченным лицом до исполнения. Пример: заказ одобряет менеджер по закупкам, платёж — финансовый директор.",
            "explain_en": "Authorisation requires transactions to be approved by an authorised person before execution. Example: purchase orders approved by procurement manager, payments approved by the CFO."
        },
        {
            "ru": "Что такое сверка (reconciliation) как контроль?",
            "en": "What is reconciliation as a control?",
            "opts_ru": ["Согласование условий с клиентами", "Сравнение двух независимых источников данных для выявления расхождений", "Подписание договоров с поставщиками", "Проверка расчётов зарплаты"],
            "correct": 1,
            "explain_ru": "Сверка — сравнение двух независимых источников. Пример: банковская выписка сверяется с кассовой книгой, остатки по счетам — с данными в системе. Выявляет ошибки и мошенничество.",
            "explain_en": "Reconciliation compares two independent sources of data to identify discrepancies — e.g. bank statement vs cash book. It detects both errors and fraud."
        },
        {
            "ru": "Что такое тесты контроля (tests of controls)?",
            "en": "What are tests of controls?",
            "opts_ru": ["Тесты для проверки остатков", "Процедуры для проверки что контроли работали эффективно в течение периода", "Процедуры планирования аудита", "Тесты компетентности персонала"],
            "correct": 1,
            "explain_ru": "Тесты контроля — аудиторские процедуры для проверки что контроли работали эффективно на протяжении всего периода. Эффективные контроли позволяют снизить объём процедур по существу.",
            "explain_en": "Tests of controls evaluate whether controls operated effectively throughout the period. Effective controls allow the auditor to reduce the extent of substantive testing required."
        },
        {
            "ru": "Что такое превентивные и детективные контроли?",
            "en": "What is the difference between preventive and detective controls?",
            "opts_ru": ["Это одно и то же", "Превентивные предотвращают ошибки; детективные обнаруживают уже произошедшие", "Превентивные дешевле", "Детективные работают только в IT"],
            "correct": 1,
            "explain_ru": "Превентивные (preventive) предотвращают ошибки до их возникновения (авторизация, пароли, разделение обязанностей). Детективные (detective) обнаруживают после (сверки, внутренний аудит).",
            "explain_en": "Preventive controls stop errors before they occur (authorisation, passwords, segregation of duties). Detective controls identify errors after they have occurred (reconciliations, reviews, internal audit)."
        },
        {
            "ru": "Что такое ключевые контроли в системе закупок (purchases)?",
            "en": "What are key controls in the purchases system?",
            "opts_ru": ["Только контроль цен", "Авторизация заказов, трёхстороннее сопоставление, разделение закупки и оплаты", "Только проверка поставщиков", "Только контроль качества"],
            "correct": 1,
            "explain_ru": "Ключевые контроли в закупках: авторизация заказов (purchase order authorisation), трёхстороннее сопоставление (three-way match: заказ + накладная + счёт), разделение функций закупки и оплаты.",
            "explain_en": "Key purchase controls: authorisation of purchase orders, three-way matching (PO vs GRN vs invoice), segregation of purchasing and payment functions, and authorisation of payments."
        },
        {
            "ru": "Что такое ключевые контроли в системе продаж (sales)?",
            "en": "What are key controls in the sales system?",
            "opts_ru": ["Только контроль цен продаж", "Авторизация кредитных лимитов, нумерация счетов, контроль дебиторки", "Только проверка покупателей", "Только контроль скидок"],
            "correct": 1,
            "explain_ru": "Ключевые контроли в продажах: авторизация кредитных лимитов, последовательная нумерация счетов, сверка отгрузки со счётом, ежемесячные выписки клиентам, мониторинг просроченной задолженности.",
            "explain_en": "Key sales controls: authorisation of credit limits, sequential invoice numbering, matching despatch notes to invoices, monthly customer statements, and monitoring of overdue debts."
        },
        {
            "ru": "Что такое ключевые контроли в системе расчёта зарплаты (payroll)?",
            "en": "What are key controls in the payroll system?",
            "opts_ru": ["Только проверка ставок оплаты", "Авторизация изменений, разделение расчёта и выплаты, контроль подставных сотрудников", "Только проверка трудовых договоров", "Только контроль сверхурочных"],
            "correct": 1,
            "explain_ru": "Ключевые контроли в расчёте зарплаты: авторизация изменений данных сотрудников, разделение расчёта и выплаты зарплаты, контроль подставных сотрудников (ghost employees), сверка с прошлым периодом.",
            "explain_en": "Key payroll controls: authorisation of changes to employee data, segregation of payroll preparation and payment, controls over ghost employees, and comparison of payroll totals with prior periods."
        },
        {
            "ru": "Что такое IT общие контроли (general IT controls)?",
            "en": "What are general IT controls?",
            "opts_ru": ["Контроли только для IT-компаний", "Контроли доступа к системам, управление изменениями, резервное копирование", "Проверка компьютеров на вирусы", "IT-образование сотрудников"],
            "correct": 1,
            "explain_ru": "Общие IT-контроли: контроль доступа к системам (access controls), управление изменениями программ (change management), процедуры резервного копирования и восстановления данных.",
            "explain_en": "General IT controls: access controls (passwords, user rights), change management (testing before implementation), backup and recovery procedures, and physical security of IT infrastructure."
        },
        {
            "ru": "Что такое обход контроля руководством (management override)?",
            "en": "What is management override of controls?",
            "opts_ru": ["Руководство улучшает контроли", "Руководство намеренно обходит установленные контроли", "Руководство проверяет работу контролей", "Руководство делегирует контроль сотрудникам"],
            "correct": 1,
            "explain_ru": "Обход контроля руководством — ключевое ограничение. Руководство может обойти контроли которые само установило. Это основная причина почему контроль не даёт абсолютной уверенности и является главным фактором риска мошенничества.",
            "explain_en": "Management override is a key limitation — management can circumvent the very controls they established. This is why controls cannot provide absolute assurance and is a primary fraud risk factor."
        },
        {
            "ru": "Что такое нумерация документов (sequential numbering) как контроль полноты?",
            "en": "What is sequential numbering as a completeness control?",
            "opts_ru": ["Нумерация страниц в отчёте", "Порядковая нумерация документов позволяющая выявить пропущенные или дублированные", "Номера сотрудников в системе", "Нумерация активов на складе"],
            "correct": 1,
            "explain_ru": "Порядковая нумерация (sequential numbering) — контроль полноты. Все документы (счета, заказы, накладные) нумеруются подряд. Пропущенные номера указывают на незарегистрированные операции.",
            "explain_en": "Sequential numbering is a completeness control. All documents (invoices, orders, despatch notes) are pre-numbered. Missing numbers indicate potentially unrecorded transactions."
        },
        {
            "ru": "Что такое контроли приложений (application controls) в IT?",
            "en": "What are application controls in IT?",
            "opts_ru": ["Контроли над приложениями на телефоне", "Контроли встроенные в конкретные программы для обеспечения точности обработки данных", "Правила установки программ", "Правила использования корпоративного ПО"],
            "correct": 1,
            "explain_ru": "Контроли приложений — контроли входных данных (input), обработки (processing) и выходных данных (output) в конкретных программах. Обеспечивают точность и полноту обработки транзакций.",
            "explain_en": "Application controls are built into specific programs covering input controls (data validation), processing controls (calculations) and output controls (reports). They ensure accuracy and completeness."
        },
    ],
    "D": [
        {
            "ru": "Какие доказательства считаются наиболее надёжными?",
            "en": "Which type of audit evidence is most reliable?",
            "opts_ru": [
                "Устные объяснения менеджмента клиента",
                "Документы от третьих лиц, полученные аудитором напрямую",
                "Внутренние документы, подготовленные бухгалтерией клиента",
                "Личные наблюдения аудитора без документального подтверждения"
            ],
            "opts_en": [
                "Oral explanations from client management",
                "Documents from third parties obtained directly by the auditor",
                "Internal documents prepared by the client's accounting team",
                "Auditor observations without documentary support"
            ],
            "correct": 1,
            "explain_ru": "Доказательства от третьих лиц, полученные напрямую аудитором (external evidence obtained directly) — наиболее надёжные. Пример: банковское подтверждение, пришедшее от банка напрямую. Менее надёжны внутренние документы клиента.",
            "explain_en": "External evidence obtained directly by the auditor is the most reliable. Example: a bank confirmation sent directly to the auditor by the bank. Client-generated internal documents are less reliable."
        },
        {
            "ru": "Что такое процедуры по существу (substantive procedures)?",
            "en": "What are substantive procedures?",
            "opts_ru": [
                "Тесты, проверяющие работу систем внутреннего контроля",
                "Процедуры, направленные на выявление существенных искажений в отчётности",
                "Анализ организационной структуры клиента",
                "Проверка квалификации сотрудников бухгалтерии"
            ],
            "opts_en": [
                "Tests that check whether internal controls are operating effectively",
                "Procedures designed to detect material misstatements in financial statements",
                "Analysis of the client's organisational structure",
                "Assessment of the qualifications of accounting staff"
            ],
            "correct": 1,
            "explain_ru": "Процедуры по существу (substantive procedures) делятся на: аналитические процедуры (analytical procedures) — сравнение цифр, коэффициентов; и детальные тесты (tests of detail) — проверка конкретных документов и остатков.",
            "explain_en": "Substantive procedures consist of: analytical procedures (comparing figures and ratios) and tests of detail (examining specific transactions, balances and disclosures). Both aim to detect material misstatements."
        },
        {
            "ru": "Почему аудиторы проверяют выборку (sample), а не 100% операций?",
            "en": "Why do auditors test a sample rather than 100% of transactions?",
            "opts_ru": [
                "Закон запрещает проверять все документы клиента",
                "Проверка всех операций нецелесообразна по времени и стоимости",
                "Клиент разрешает смотреть не более 50% документов",
                "Аудиторские стандарты требуют проверять ровно 25%"
            ],
            "opts_en": [
                "The law prohibits auditors from examining all client documents",
                "Testing 100% is impractical in terms of time and cost",
                "The client only permits access to 50% of documents",
                "Auditing standards require exactly 25% to be tested"
            ],
            "correct": 1,
            "explain_ru": "Аудиторская выборка (audit sampling) применяется когда проверка 100% нецелесообразна. По выборке аудитор делает выводы обо всей совокупности. Риск выборки (sampling risk) — вывод может не совпасть с реальностью всей совокупности.",
            "explain_en": "Audit sampling is used when it is not practical to test 100% of items. The auditor draws conclusions about the entire population from the sample. Sampling risk is the risk that the conclusion differs from what a 100% test would show."
        },
        {
            "ru": "Что проверяет аудитор при аудите запасов (inventory)?",
            "en": "What does the auditor test when auditing inventory?",
            "opts_ru": [
                "Только цены закупок",
                "Существование, полноту, оценку и права собственности на запасы",
                "Только физическое наличие запасов",
                "Только документы на отгрузку"
            ],
            "opts_en": [
                "Purchase prices only",
                "Existence, completeness, valuation and rights over inventory",
                "Physical presence of inventory only",
                "Delivery documents only"
            ],
            "correct": 1,
            "explain_ru": "При аудите запасов аудитор проверяет: существование (физический подсчёт), полноту (всё ли учтено), оценку (правильность стоимости, NRV), права собственности (принадлежит ли компании). Физическое наблюдение (physical observation) — ключевая процедура.",
            "explain_en": "When auditing inventory, the auditor tests: existence (physical count observation), completeness (all items recorded), valuation (cost vs NRV), and rights (ownership belongs to the entity). Physical observation is the key procedure."
        },
        {
            "ru": "Что такое внешнее подтверждение (external confirmation) и когда оно используется?",
            "en": "What is external confirmation and when is it used?",
            "opts_ru": [
                "Письмо от менеджмента клиента аудитору",
                "Прямой запрос аудитора третьей стороне для подтверждения данных",
                "Внутренняя проверка данных компанией",
                "Запрос в налоговую о задолженности клиента"
            ],
            "opts_en": [
                "A letter from client management to the auditor",
                "A direct request from the auditor to a third party to confirm information",
                "An internal data check by the company",
                "A request to the tax authority about the client's liabilities"
            ],
            "correct": 1,
            "explain_ru": "Внешнее подтверждение (external confirmation) — аудитор напрямую обращается к третьей стороне. Примеры: банковское подтверждение (bank confirmation), подтверждение дебиторской задолженности (debtor circularisation). Это одно из самых надёжных доказательств.",
            "explain_en": "External confirmation is a direct written response from a third party to the auditor. Examples: bank confirmation, debtor circularisation. It is among the most reliable forms of audit evidence because it comes from an independent source."
        },
        {
            "ru": "Как аудитор проверяет выручку (revenue)?",
            "en": "How does the auditor test revenue?",
            "opts_ru": [
                "Только запрашивает объяснения у менеджмента",
                "Аналитические процедуры + детальные тесты на реальность и полноту операций",
                "Только сверяет данные с налоговой декларацией",
                "Только проверяет банковские выписки"
            ],
            "opts_en": [
                "Only asks management for explanations",
                "Analytical procedures + tests of detail for occurrence and completeness",
                "Only reconciles to the tax return",
                "Only reviews bank statements"
            ],
            "correct": 1,
            "explain_ru": "При аудите выручки: аналитические процедуры (сравнение с прошлым годом, расчёт средней цены × объём), тесты на реальность операций (occurrence — подтверждение что продажи были), полноту (completeness — всё ли учтено). Риск завышения выручки всегда высокий.",
            "explain_en": "For revenue: analytical procedures (compare to prior year, price × volume analysis) plus tests of detail for occurrence (sales actually happened) and completeness (all sales recorded). Revenue is high-risk as management may overstate it."
        },
        {
            "ru": "Что такое утверждения (assertions) в аудите?",
            "en": "What are assertions in auditing?",
            "opts_ru": ["Заявления аудитора о квалификации", "Явные или неявные утверждения менеджмента о статьях отчётности которые проверяет аудитор", "Гарантии аудитора пользователям", "Заявления менеджмента о стратегии"],
            "correct": 1,
            "explain_ru": "Утверждения — явные или неявные заявления менеджмента в финансовой отчётности. Для операций: occurrence, completeness, accuracy, cut-off, classification. Для остатков: existence, rights, completeness, valuation.",
            "explain_en": "Assertions are explicit or implicit claims by management in the financial statements. For transactions: occurrence, completeness, accuracy, cut-off, classification. For balances: existence, rights, completeness, valuation."
        },
        {
            "ru": "Что такое утверждение 'существование' (existence)?",
            "en": "What is the existence assertion?",
            "opts_ru": ["Все активы отражены в отчётности", "Активы и обязательства отражённые в отчётности реально существуют на отчётную дату", "Все операции за период отражены", "Активы оценены правильно"],
            "correct": 1,
            "explain_ru": "Существование (existence) — активы в балансе реально существуют. Риск: завышение активов (overstatement). Процедуры: физический осмотр, подтверждения от третьих лиц.",
            "explain_en": "Existence: assets and liabilities shown exist at the reporting date. Risk: overstatement of assets. Procedures: physical inspection, third-party confirmations."
        },
        {
            "ru": "Что такое утверждение 'полнота' (completeness)?",
            "en": "What is the completeness assertion?",
            "opts_ru": ["Все операции правильно оценены", "Все активы обязательства и операции которые должны быть отражены действительно отражены", "Все статьи правильно классифицированы", "Все раскрытия сделаны"],
            "correct": 1,
            "explain_ru": "Полнота (completeness) — всё что должно быть отражено действительно отражено. Риск: занижение обязательств (understatement). Процедуры: поиск незарегистрированных обязательств, анализ событий после отчётной даты.",
            "explain_en": "Completeness: all transactions and balances that should be recorded are included. Risk: understatement of liabilities. Procedures: search for unrecorded liabilities, review post-year-end payments."
        },
        {
            "ru": "Что такое утверждение 'оценка' (valuation)?",
            "en": "What is the valuation assertion?",
            "opts_ru": ["Активы оценены по рыночной стоимости", "Активы обязательства и капитал отражены по правильным суммам согласно стандартам", "Аудитор оценивает стоимость бизнеса", "Активы переоцениваются ежегодно"],
            "correct": 1,
            "explain_ru": "Оценка (valuation) — статьи отражены по правильным суммам согласно стандартам. Риск: неправильная оценка запасов (cost vs NRV), дебиторки (резерв по сомнительным долгам), нематериальных активов.",
            "explain_en": "Valuation: assets, liabilities and equity are included at appropriate amounts. Risk: incorrect measurement of inventory (cost vs NRV), receivables (bad debt provision) or intangibles (impairment)."
        },
        {
            "ru": "Что такое внешнее подтверждение (external confirmation)?",
            "en": "What is external confirmation?",
            "opts_ru": ["Письмо от менеджмента аудитору", "Прямой запрос аудитора третьей стороне для подтверждения данных", "Внутренняя проверка данных компанией", "Запрос в налоговую о задолженности"],
            "correct": 1,
            "explain_ru": "Внешнее подтверждение — аудитор напрямую обращается к третьей стороне. Примеры: банковское подтверждение (bank confirmation), подтверждение дебиторской задолженности (debtor circularisation). Одно из самых надёжных доказательств.",
            "explain_en": "External confirmation is a direct written response from a third party. Examples: bank confirmation, debtor circularisation. One of the most reliable audit evidence sources as it comes from an independent party."
        },
        {
            "ru": "Как аудитор проверяет запасы (inventory)?",
            "en": "How does the auditor test inventory?",
            "opts_ru": ["Только проверяет цены закупок", "Наблюдает за инвентаризацией проверяет оценку (cost vs NRV) и права собственности", "Только проверяет документы на отгрузку", "Только запрашивает объяснения у кладовщика"],
            "correct": 1,
            "explain_ru": "Аудит запасов: наблюдение за инвентаризацией (physical count observation), проверка оценки (cost vs net realisable value), тест на права собственности, проверка учётных записей. Наблюдение за инвентаризацией обязательно если запасы существенны.",
            "explain_en": "Inventory audit: attend and observe the count, test valuation (cost vs NRV), confirm ownership rights, and agree count results to inventory records and financial statements."
        },
        {
            "ru": "Как аудитор проверяет дебиторскую задолженность (receivables)?",
            "en": "How does the auditor test receivables?",
            "opts_ru": ["Только проверяет договоры с покупателями", "Внешнее подтверждение, анализ возраста задолженности, проверка последующих оплат", "Только сверяет с налоговой отчётностью", "Только проверяет кредитные лимиты"],
            "correct": 1,
            "explain_ru": "Аудит дебиторки: внешнее подтверждение (circularisation), анализ возраста задолженности (aged receivables listing), проверка последующих поступлений (subsequent receipts), оценка резерва по сомнительным долгам.",
            "explain_en": "Receivables audit: circularisation (external confirmation), aged receivables analysis, subsequent receipts testing, and evaluation of the provision for doubtful debts."
        },
        {
            "ru": "Как аудитор проверяет кредиторскую задолженность (payables)?",
            "en": "How does the auditor test payables?",
            "opts_ru": ["Только проверяет договоры с поставщиками", "Сверка с выписками поставщиков, поиск незарегистрированных обязательств, проверка среза", "Только запрашивает подтверждения от поставщиков", "Только проверяет платёжные поручения"],
            "correct": 1,
            "explain_ru": "Аудит кредиторки: сверка с выписками поставщиков (supplier statement reconciliation), поиск незарегистрированных обязательств (unrecorded liabilities), проверка среза (cut-off testing) вокруг отчётной даты.",
            "explain_en": "Payables audit: supplier statement reconciliation, search for unrecorded liabilities (reviewing post-year-end payments), and cut-off testing around the year-end date."
        },
        {
            "ru": "Как аудитор проверяет денежные средства (cash and bank)?",
            "en": "How does the auditor test cash and bank?",
            "opts_ru": ["Только пересчитывает наличные в кассе", "Банковская сверка, подтверждение от банка, проверка ограниченных средств", "Только запрашивает выписки у банка", "Только проверяет наличные"],
            "correct": 1,
            "explain_ru": "Аудит денежных средств: проверка банковской сверки (bank reconciliation), внешнее подтверждение от банка (bank confirmation), проверка ограниченных средств (restricted cash), пересчёт наличных в кассе.",
            "explain_en": "Cash audit: review bank reconciliation, obtain external bank confirmation, test restricted cash, perform physical cash count, and test cut-off around the year-end."
        },
        {
            "ru": "Как аудитор проверяет основные средства (non-current assets)?",
            "en": "How does the auditor test non-current assets?",
            "opts_ru": ["Только проверяет счета поставщиков", "Физический осмотр, проверка права собственности оценки и амортизации", "Только сверяет с реестром активов", "Только проверяет страховые полисы"],
            "correct": 1,
            "explain_ru": "Аудит основных средств: физический осмотр (physical inspection), подтверждение права собственности (title deeds), проверка оценки (cost/revaluation), расчёта амортизации, теста на обесценение (impairment).",
            "explain_en": "Non-current assets audit: physical inspection, verification of title/ownership documents, testing valuation (cost or revaluation model), depreciation calculations, and impairment assessment."
        },
        {
            "ru": "Что такое аудиторская выборка (audit sampling)?",
            "en": "What is audit sampling?",
            "opts_ru": ["Аудитор берёт образцы продукции", "Применение процедур менее чем к 100% совокупности с целью выводов обо всей совокупности", "Аудитор проверяет только крупные операции", "Случайный отбор без цели"],
            "correct": 1,
            "explain_ru": "Аудиторская выборка — применение процедур менее чем к 100% совокупности. По выборке аудитор делает выводы обо всей совокупности. Риск выборки (sampling risk) — вывод может не совпасть с реальностью.",
            "explain_en": "Audit sampling applies procedures to less than 100% of items and uses results to draw conclusions about the whole population. Sampling risk is the risk that conclusions differ from a 100% examination."
        },
        {
            "ru": "Что такое проверка среза (cut-off testing)?",
            "en": "What is cut-off testing?",
            "opts_ru": ["Аудитор проверяет период с 1 по 15 числа", "Проверка что операции отражены в правильном учётном периоде", "Аудитор урезает выборку", "Проверка первых и последних операций"],
            "correct": 1,
            "explain_ru": "Проверка среза (cut-off) — проверка что операции отражены в правильном учётном периоде. Аудитор проверяет операции около отчётной даты чтобы убедиться в правильной принадлежности периоду.",
            "explain_en": "Cut-off testing checks that transactions are recorded in the correct accounting period. The auditor tests transactions around the year-end to ensure proper period allocation."
        },
        {
            "ru": "Что такое направленное тестирование (directional testing)?",
            "en": "What is directional testing?",
            "opts_ru": ["Тестирование только в одном направлении", "Тестирование с учётом вероятного направления искажения по конкретному утверждению", "Аудитор направляет запросы поставщикам", "Аудитор проверяет только дебет или только кредит"],
            "correct": 1,
            "explain_ru": "Направленное тестирование — аудитор проверяет утверждения с учётом вероятного направления искажения. Активы — риск завышения (тест на существование), обязательства — риск занижения (тест на полноту).",
            "explain_en": "Directional testing considers the likely direction of misstatement. Assets risk overstatement (test existence), liabilities risk understatement (test completeness). This focuses effort on the most likely risks."
        },
        {
            "ru": "Что такое письмо-представление менеджмента (management representation letter)?",
            "en": "What is a management representation letter?",
            "opts_ru": ["Письмо аудитора менеджменту о гонораре", "Письменное подтверждение менеджментом ключевых заявлений сделанных аудитору в ходе аудита", "Рекомендации по улучшению бизнеса", "Отчёт менеджмента акционерам"],
            "correct": 1,
            "explain_ru": "Письмо-представление — письменное подтверждение менеджментом ключевых заявлений. Снижает риск отрицания устных заявлений. Само по себе НЕ является достаточным доказательством и должно подкрепляться другими процедурами.",
            "explain_en": "A management representation letter is written confirmation of key assertions made during the audit. It reduces the risk of denial but is NOT sufficient evidence on its own and must be corroborated."
        },
        {
            "ru": "Что такое инспекция (inspection) как метод получения доказательств?",
            "en": "What is inspection as an audit procedure?",
            "opts_ru": ["Аудитор осматривает офис клиента", "Изучение записей документов или физических активов", "Аудитор проверяет сотрудников", "Аудитор проверяет IT-системы"],
            "correct": 1,
            "explain_ru": "Инспекция — изучение записей или документов (внутренних и внешних) или физическая проверка активов. Один из основных методов получения аудиторских доказательств.",
            "explain_en": "Inspection involves examining records or documents (internal or external) or physically examining tangible assets. It is a primary method of obtaining audit evidence."
        },
        {
            "ru": "Что такое наблюдение (observation) как метод получения доказательств?",
            "en": "What is observation as an audit procedure?",
            "opts_ru": ["Аудитор наблюдает за рынком", "Аудитор наблюдает за выполнением процесса или процедуры другим лицом", "Аудитор наблюдает за акциями клиента", "Аудитор наблюдает за конкурентами"],
            "correct": 1,
            "explain_ru": "Наблюдение — аудитор наблюдает за тем как другое лицо выполняет процесс. Пример: наблюдение за инвентаризацией запасов. Ограничение: работает только в момент наблюдения.",
            "explain_en": "Observation involves looking at a process being performed by others. Example: attending inventory count. Limitation: only provides evidence at the point in time of observation."
        },
        {
            "ru": "Что такое пересчёт (recalculation) как метод получения доказательств?",
            "en": "What is recalculation as an audit procedure?",
            "opts_ru": ["Аудитор пересчитывает сотрудников", "Проверка арифметической точности документов или записей", "Аудитор пересчитывает запасы на складе", "Аудитор пересчитывает гонорар"],
            "correct": 1,
            "explain_ru": "Пересчёт — проверка арифметической точности документов или записей. Примеры: пересчёт начисленной амортизации, расчёта зарплаты, итогов в ведомости запасов.",
            "explain_en": "Recalculation checks the mathematical accuracy of documents or records. Examples: recalculating depreciation, payroll calculations, or inventory valuation totals."
        },
        {
            "ru": "Что такое запрос (inquiry) как метод получения доказательств?",
            "en": "What is inquiry as an audit procedure?",
            "opts_ru": ["Аудитор запрашивает документы в архиве", "Получение информации от осведомлённых лиц внутри или вне организации", "Аудитор направляет запросы в налоговую", "Аудитор запрашивает гонорар"],
            "correct": 1,
            "explain_ru": "Запрос (inquiry) — получение информации от осведомлённых лиц. Само по себе НЕ даёт достаточных доказательств и должно подкрепляться другими процедурами (инспекцией, подтверждением).",
            "explain_en": "Inquiry involves seeking information from knowledgeable persons. It alone does NOT provide sufficient evidence and must be corroborated by other procedures such as inspection or confirmation."
        },
    ],
    "E": [
        {
            "ru": "Когда аудитор выдаёт немодифицированное заключение (unmodified opinion)?",
            "en": "When does the auditor issue an unmodified opinion?",
            "opts_ru": [
                "Когда компания является государственной",
                "Когда финансовая отчётность достоверна во всех существенных аспектах",
                "Когда аудит проводится впервые",
                "Когда клиент платит гонорар вовремя"
            ],
            "opts_en": [
                "When the company is state-owned",
                "When the financial statements give a true and fair view in all material respects",
                "When it is the first audit of the entity",
                "When the client pays the audit fee on time"
            ],
            "correct": 1,
            "explain_ru": "Немодифицированное заключение (unmodified / clean opinion) выдаётся, когда отчётность составлена верно во всех существенных аспектах. Это лучший результат для клиента. Модифицированные: Qualified, Adverse, Disclaimer.",
            "explain_en": "An unmodified (clean) opinion is issued when the financial statements give a true and fair view in all material respects. Modified opinions include: qualified, adverse, and disclaimer of opinion."
        },
        {
            "ru": "Разница между Qualified и Adverse opinion?",
            "en": "What is the difference between a qualified and an adverse opinion?",
            "opts_ru": [
                "Разницы нет, это одно и то же",
                "Qualified — искажения существенны, но не повсеместны. Adverse — существенны И повсеместны",
                "Qualified — мошенничество найдено, Adverse — нет",
                "Qualified для малого бизнеса, Adverse для крупного"
            ],
            "opts_en": [
                "There is no difference, they are the same",
                "Qualified — misstatements are material but not pervasive. Adverse — material AND pervasive",
                "Qualified means fraud found, Adverse means no fraud",
                "Qualified is for small businesses, Adverse for large ones"
            ],
            "correct": 1,
            "explain_ru": "Ключевое слово — pervasive (повсеместный). Qualified: проблема существенна, но ограничена конкретной областью. Adverse: проблема настолько серьёзна и пронизывает всю отчётность, что она в целом недостоверна.",
            "explain_en": "The key word is 'pervasive'. Qualified opinion: misstatement is material but NOT pervasive (limited to one area). Adverse opinion: misstatement is both material AND pervasive — the financial statements as a whole are misleading."
        },
        {
            "ru": "Что такое Emphasis of Matter (акцент на важных вопросах)?",
            "en": "What is an Emphasis of Matter paragraph?",
            "opts_ru": [
                "Часть отрицательного заключения аудитора",
                "Дополнительный абзац в чистом заключении, привлекающий внимание к важному вопросу",
                "Рекомендации по улучшению бизнеса клиента",
                "Требование повторно провести аудит"
            ],
            "opts_en": [
                "Part of an adverse audit opinion",
                "An additional paragraph in an unmodified report drawing attention to an important matter",
                "Business improvement recommendations for the client",
                "A requirement to repeat the audit"
            ],
            "correct": 1,
            "explain_ru": "Emphasis of Matter — абзац, добавляемый к ЧИСТОМУ заключению. Мнение аудитора не меняется, но он привлекает внимание к важному вопросу, уже раскрытому в отчётности. Типичный пример — существенная неопределённость going concern.",
            "explain_en": "An Emphasis of Matter paragraph is added to an UNMODIFIED opinion. The auditor's opinion is not changed, but attention is drawn to a matter already disclosed in the financial statements — e.g. a material uncertainty about going concern."
        },
        {
            "ru": "Что такое отказ от выражения мнения (disclaimer of opinion)?",
            "en": "What is a disclaimer of opinion?",
            "opts_ru": ["Аудитор отказывается от задания", "Аудитор не может выразить мнение из-за невозможности получить достаточные доказательства", "Аудитор выражает отрицательное мнение", "Аудитор отказывается подписывать заключение"],
            "correct": 1,
            "explain_ru": "Отказ от выражения мнения (disclaimer) — когда аудитор не может получить достаточные доказательства и возможное влияние искажений настолько существенно и повсеместно, что невозможно выразить мнение.",
            "explain_en": "A disclaimer of opinion is issued when the auditor cannot obtain sufficient evidence and the possible effects are so material and pervasive that no opinion can be expressed."
        },
        {
            "ru": "Что такое события после отчётной даты (subsequent events)?",
            "en": "What are subsequent events?",
            "opts_ru": ["События до начала аудита", "События после отчётной даты но до даты аудиторского заключения", "События после выдачи заключения", "События запланированные на следующий год"],
            "correct": 1,
            "explain_ru": "Последующие события — события после отчётной даты. Корректирующие (adjusting) требуют изменения отчётности. Некорректирующие (non-adjusting) требуют только раскрытия.",
            "explain_en": "Subsequent events occur after the reporting date. Adjusting events require changes to financial statements. Non-adjusting events require disclosure only."
        },
        {
            "ru": "Что такое корректирующее последующее событие (adjusting event)?",
            "en": "What is an adjusting subsequent event?",
            "opts_ru": ["Любое событие после отчётной даты", "Событие подтверждающее условия существовавшие на отчётную дату и требующее изменения отчётности", "Событие произошедшее до отчётной даты", "Событие требующее только раскрытия"],
            "correct": 1,
            "explain_ru": "Корректирующее событие подтверждает условия на отчётную дату и требует изменения отчётности. Пример: банкротство крупного дебитора после отчётной даты.",
            "explain_en": "An adjusting event provides evidence of conditions at the reporting date and requires adjustment. Example: bankruptcy of a major debtor after year-end confirms the receivable was bad at year-end."
        },
        {
            "ru": "Что такое некорректирующее событие (non-adjusting event)?",
            "en": "What is a non-adjusting subsequent event?",
            "opts_ru": ["Событие не влияющее на отчётность", "Событие указывающее на условия возникшие ПОСЛЕ отчётной даты требующее только раскрытия", "Событие которое нельзя исправить", "Мелкое событие которое игнорируется"],
            "correct": 1,
            "explain_ru": "Некорректирующее событие указывает на условия возникшие ПОСЛЕ отчётной даты. Не требует изменения отчётности но требует раскрытия если существенно. Пример: пожар на складе после отчётной даты.",
            "explain_en": "A non-adjusting event is indicative of conditions arising after the reporting date. No adjustment is required but disclosure is needed if material. Example: fire destroying a warehouse after year-end."
        },
        {
            "ru": "Что включает стандартное аудиторское заключение?",
            "en": "What does a standard audit report include?",
            "opts_ru": ["Только мнение аудитора", "Заголовок, адресат, мнение, основу для мнения, ключевые вопросы аудита, ответственность сторон, подпись и дату", "Только перечень процедур", "Финансовую отчётность клиента"],
            "correct": 1,
            "explain_ru": "Стандартное заключение: заголовок (title), адресат (addressee), мнение (opinion), основу для мнения (basis for opinion), ключевые вопросы аудита (KAM), непрерывность деятельности, ответственность сторон, подпись, дату.",
            "explain_en": "Standard audit report includes: title, addressee, opinion, basis for opinion, key audit matters (KAM), going concern, management's and auditor's responsibilities, signature, date and location."
        },
        {
            "ru": "Что такое ключевые вопросы аудита (Key Audit Matters / KAM)?",
            "en": "What are Key Audit Matters (KAM)?",
            "opts_ru": ["Жалобы клиента на аудит", "Наиболее значимые вопросы при аудите раскрываемые в заключении для листинговых компаний", "Секретная информация аудитора", "Ошибки найденные в ходе аудита"],
            "correct": 1,
            "explain_ru": "KAM — наиболее значимые вопросы при проведении аудита. Раскрываются в заключении для листинговых компаний (listed entities). Повышают прозрачность аудита для пользователей.",
            "explain_en": "Key Audit Matters are the most significant matters in the auditor's judgement. Disclosed in the audit report of listed entities to improve transparency and communicate audit focus areas."
        },
        {
            "ru": "Что делает аудитор если менеджмент не исправляет существенные ошибки?",
            "en": "What does the auditor do if management refuses to correct material misstatements?",
            "opts_ru": ["Исправляет ошибки самостоятельно", "Модифицирует заключение — оговорка или отрицательное мнение", "Продолжает аудит как ни в чём не бывало", "Немедленно прекращает аудит"],
            "correct": 1,
            "explain_ru": "Если менеджмент не исправляет существенные ошибки аудитор модифицирует заключение: оговорка (qualified) если искажение существенно но не повсеместно; отрицательное мнение (adverse) если повсеместно.",
            "explain_en": "If management refuses to correct material misstatements the auditor modifies the opinion: qualified if material but not pervasive; adverse if material AND pervasive."
        },
        {
            "ru": "Каков правильный порядок дат в аудиторском процессе?",
            "en": "What is the correct sequence of dates in an audit?",
            "opts_ru": ["Дата заключения → отчётная дата → дата одобрения", "Отчётная дата → дата одобрения отчётности → дата аудиторского заключения", "Дата начала аудита → отчётная дата → дата заключения", "Дата заключения всегда совпадает с отчётной датой"],
            "correct": 1,
            "explain_ru": "Правильный порядок: отчётная дата (year-end) → одобрение отчётности менеджментом → дата аудиторского заключения. Аудитор несёт ответственность за последующие события до даты заключения.",
            "explain_en": "Correct sequence: reporting date (year-end) → management approval → date of auditor's report (not before approval). The auditor is responsible for subsequent events up to the report date."
        },
        {
            "ru": "Что такое письменные заявления менеджмента (written representations)?",
            "en": "What are written representations?",
            "opts_ru": ["Письма аудитора клиенту", "Письменные подтверждения менеджментом ключевых заявлений которые нельзя подтвердить иначе", "Письма акционерам от аудитора", "Официальные жалобы клиента"],
            "correct": 1,
            "explain_ru": "Письменные заявления (written representations) используются для подтверждения что менеджмент раскрыл все известные факты. Сами по себе НЕ являются достаточным доказательством.",
            "explain_en": "Written representations confirm that management has disclosed all relevant information. They are NOT sufficient evidence on their own and must be supported by other audit evidence."
        },
        {
            "ru": "Что такое Other Matter параграф?",
            "en": "What is an Other Matter paragraph?",
            "opts_ru": ["Параграф о других видах аудита", "Параграф привлекающий внимание к вопросу НЕ раскрытому в отчётности но важному для понимания аудита", "Параграф о конкурентах клиента", "Информация о гонораре аудитора"],
            "correct": 1,
            "explain_ru": "Other Matter параграф привлекает внимание к вопросу НЕ раскрытому в финансовой отчётности но важному для понимания аудита. Отличие от Emphasis of Matter: там вопрос раскрыт в отчётности.",
            "explain_en": "An Other Matter paragraph draws attention to a matter NOT disclosed in the financial statements but relevant to users' understanding of the audit. Unlike Emphasis of Matter where the matter IS in the statements."
        },
        {
            "ru": "Что такое существенная неопределённость по непрерывности (going concern uncertainty)?",
            "en": "What is a material uncertainty related to going concern?",
            "opts_ru": ["Любые сомнения в работе компании", "Неопределённость которая может вызвать сомнения в способности компании продолжать деятельность и которая должна быть раскрыта", "Банкротство компании", "Временные финансовые трудности"],
            "correct": 1,
            "explain_ru": "Существенная неопределённость по going concern — события или условия могут вызвать сомнения в способности компании продолжать деятельность. Если раскрыта в отчётности — аудитор добавляет Emphasis of Matter.",
            "explain_en": "A material going concern uncertainty exists when events or conditions may cast significant doubt on the entity's ability to continue. If adequately disclosed, the auditor adds an Emphasis of Matter paragraph."
        },
        {
            "ru": "Что такое ответственность менеджмента в контексте финансовой отчётности?",
            "en": "What is management's responsibility regarding financial statements?",
            "opts_ru": ["Проводить аудит самостоятельно", "Подготовка финансовой отчётности и поддержание внутреннего контроля", "Выбор аудиторских процедур", "Выражение мнения о достоверности отчётности"],
            "correct": 1,
            "explain_ru": "Менеджмент несёт ответственность за: подготовку финансовой отчётности по стандартам, поддержание системы внутреннего контроля, предоставление аудитору доступа к информации.",
            "explain_en": "Management is responsible for: preparing financial statements per the applicable framework, maintaining internal controls, and providing the auditor with access to all necessary information."
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
    text = (
        "⏰ *Напоминание от твоего ACCA AA тренажёра!*\n\n"
        "Прошло 2 недели — пора добавить новые вопросы в бота! 📚\n\n"
        "Что сделать:\n"
        "1. Напиши мне в Claude — я добавлю новые вопросы\n"
        "2. Вставь код в GitHub → бот обновится автоматически\n\n"
        "Не останавливайся — ты молодец! 💪"
    )
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=text,
        parse_mode="Markdown"
    )


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("history", history_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Бот запущен ✅")
    app.run_polling()


if __name__ == "__main__":
    main()

import streamlit as st
import datetime
import calendar
from collections import defaultdict
from urllib.parse import urlencode
from html import escape


# =========================================================
# 1. 페이지 설정
# =========================================================

st.set_page_config(
    page_title="경찰과도둑 모여라",
    page_icon="📅",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# =========================================================
# 2. 기본 설정
# =========================================================

YEAR = 2026
MONTHS = [8, 9]

KOR_WEEKDAYS = [
    "일", "월", "화", "수", "목", "금", "토"
]


# =========================================================
# 3. CSS
# =========================================================

st.markdown("""
<style>

@import url(
    'https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css'
);

/* ---------------------------------------------------------
   전체 페이지
--------------------------------------------------------- */

html,
body,
[class*="css"] {
    font-family:
        'Pretendard',
        -apple-system,
        BlinkMacSystemFont,
        system-ui,
        sans-serif;
}

body {
    background: #f5f7fb;
}

[data-testid="stAppViewContainer"] {
    background: #f5f7fb;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stToolbar"] {
    display: none;
}


/* ---------------------------------------------------------
   중앙 영역
--------------------------------------------------------- */

.main .block-container {
    max-width: 520px !important;
    padding: 18px 12px 50px 12px !important;
}


/* ---------------------------------------------------------
   카드
--------------------------------------------------------- */

.card {
    background: #ffffff;
    border: 1px solid #dfe5ee;
    border-radius: 14px;
    padding: 18px 15px;
    margin-bottom: 14px;
    box-shadow:
        0 1px 3px rgba(15, 23, 42, 0.04);
}


/* ---------------------------------------------------------
   헤더
--------------------------------------------------------- */

.header-card {
    text-align: center;
    padding: 24px 18px 20px;
}

.header-icon {
    font-size: 27px;
    line-height: 1;
    margin-bottom: 8px;
}

.main-title {
    font-size: 20px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 7px;
}

.main-description {
    font-size: 11px;
    color: #64748b;
}


/* ---------------------------------------------------------
   이름 영역
--------------------------------------------------------- */

.name-label {
    font-size: 12px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 7px;
}

.required {
    color: #ef4444;
}

div[data-testid="stTextInput"] {
    margin-bottom: 0 !important;
}

div[data-testid="stTextInput"] label {
    display: none;
}

div[data-testid="stTextInput"] input {
    height: 42px;
    border-radius: 8px;
    border: 1px solid #dce3ed;
    background: #f8fafc;
    color: #111827;
    font-size: 12px;
    padding-left: 12px;
}

div[data-testid="stTextInput"] input::placeholder {
    color: #94a3b8;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #6366f1;
    box-shadow:
        0 0 0 1px #6366f1;
}


/* ---------------------------------------------------------
   섹션 제목
--------------------------------------------------------- */

.section-title {
    font-size: 13px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 4px;
}

.section-description {
    font-size: 10px;
    color: #64748b;
    margin-bottom: 13px;
}


/* ---------------------------------------------------------
   달력 상단
--------------------------------------------------------- */

.calendar-top {
    display: grid;
    grid-template-columns: 38px 1fr 38px;
    align-items: center;
    gap: 7px;
    margin-bottom: 9px;
}

.month-title {
    height: 36px;
    background: #f1f5f9;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 800;
    color: #111827;
}

.month-nav {
    height: 36px;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    background: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    text-decoration: none !important;
    color: #94a3b8 !important;
    font-size: 18px;
    font-weight: 500;
}

.month-nav:hover {
    background: #f8fafc;
    color: #4f46e5 !important;
}


/* ---------------------------------------------------------
   요일
--------------------------------------------------------- */

.weekday-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 5px;
    margin-bottom: 5px;
}

.weekday {
    text-align: center;
    font-size: 10px;
    font-weight: 700;
    padding: 3px 0;
}

.weekday.sun {
    color: #ef4444;
}

.weekday.sat {
    color: #2563eb;
}

.weekday.normal {
    color: #64748b;
}


/* ---------------------------------------------------------
   날짜 달력
--------------------------------------------------------- */

.calendar-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 5px;
}

.calendar-empty {
    min-height: 58px;
}


/* ---------------------------------------------------------
   날짜 버튼
--------------------------------------------------------- */

.date-button {
    min-height: 58px;
    border-radius: 9px;
    border: 1px solid #dce3ed;
    background: #f8fafc;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    text-decoration: none !important;

    transition:
        border-color 0.1s,
        background 0.1s,
        transform 0.1s;
}

.date-button:hover {
    border-color: #818cf8;
    background: #eef2ff;
    transform: translateY(-1px);
}

.date-number {
    font-size: 11px;
    font-weight: 600;
    color: #111827;
    line-height: 1.3;
}

.date-count {
    font-size: 10px;
    color: #cbd5e1;
    line-height: 1.3;
    margin-top: 2px;
}


/* ---------------------------------------------------------
   주말
--------------------------------------------------------- */

.date-button.sun .date-number {
    color: #ef4444;
}

.date-button.sat .date-number {
    color: #2563eb;
}


/* ---------------------------------------------------------
   선택된 날짜
--------------------------------------------------------- */

.date-button.selected {
    background: #eef2ff;
    border: 1.5px solid #6366f1;
}

.date-button.selected .date-number {
    color: #4f46e5;
    font-weight: 800;
}

.date-button.selected .date-count {
    color: #4f46e5;
    font-weight: 800;
}


/* ---------------------------------------------------------
   선택 날짜 영역
--------------------------------------------------------- */

.selected-area {
    border-top: 1px solid #dfe5ee;
    margin-top: 14px;
    padding-top: 11px;
}

.selected-title {
    font-size: 10px;
    font-weight: 800;
    color: #334155;
    margin-bottom: 8px;
}

.selected-count {
    color: #4f46e5;
}

.selected-empty {
    border: 1px dashed #d9e0e9;
    border-radius: 8px;
    background: #f8fafc;
    color: #94a3b8;

    padding: 11px;

    text-align: center;
    font-size: 10px;
}

.selected-dates {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
}

.date-tag {
    background: #eef2ff;
    color: #4f46e5;
    border-radius: 6px;
    padding: 5px 7px;
    font-size: 9px;
    font-weight: 700;
}


/* ---------------------------------------------------------
   제출 버튼
--------------------------------------------------------- */

div[data-testid="stButton"] > button {
    width: 100%;
    height: 42px;

    border-radius: 8px;

    font-size: 12px;
    font-weight: 800;

    border: none;

    background: #4f46e5;
    color: white;

    box-shadow:
        0 4px 10px rgba(79, 70, 229, 0.25);
}

div[data-testid="stButton"] > button:hover {
    background: #4338ca;
    color: white;
    border: none;
}


/* ---------------------------------------------------------
   결과 영역
--------------------------------------------------------- */

.result-card {
    background: #ffffff;
    border: 1px solid #dfe5ee;
    border-radius: 14px;
    padding: 17px 15px;
    margin-top: 14px;
}

.result-title {
    font-size: 14px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 4px;
}

.result-description {
    font-size: 10px;
    color: #64748b;
    margin-bottom: 12px;
}

.rank-item {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 9px;
    padding: 11px;
    margin-bottom: 7px;
}

.rank-header {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 5px;
}

.rank-badge {
    background: #4f46e5;
    color: white;
    border-radius: 5px;
    padding: 3px 6px;
    font-size: 9px;
    font-weight: 800;
}

.rank-date {
    font-size: 12px;
    font-weight: 800;
    color: #1e1b4b;
}

.rank-count {
    font-size: 10px;
    color: #4f46e5;
    font-weight: 700;
}

.rank-people {
    font-size: 10px;
    color: #64748b;
    margin-top: 6px;
}


/* ---------------------------------------------------------
   참여자 영역
--------------------------------------------------------- */

.participant-card {
    background: #ffffff;
    border: 1px solid #dfe5ee;
    border-radius: 14px;
    padding: 17px 15px;
    margin-top: 14px;
}

.participant-title {
    font-size: 14px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 4px;
}

.participant-count {
    font-size: 10px;
    color: #64748b;
    margin-bottom: 12px;
}


/* ---------------------------------------------------------
   모바일
--------------------------------------------------------- */

@media (max-width: 600px) {

    .main .block-container {
        padding: 10px 9px 35px 9px !important;
    }

    .card {
        border-radius: 13px;
        padding: 16px 12px;
    }

    .header-card {
        padding: 22px 12px 18px;
    }

    .main-title {
        font-size: 19px;
    }

    .date-button {
        min-height: 54px;
    }

    .calendar-empty {
        min-height: 54px;
    }

    .calendar-grid {
        gap: 4px;
    }

    .weekday-grid {
        gap: 4px;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 4. 날짜 관련 함수
# =========================================================

def get_days_in_month(year, month):
    number_of_days = calendar.monthrange(year, month)[1]

    return [
        datetime.date(year, month, day)
        for day in range(1, number_of_days + 1)
    ]


def format_date_kor(date_value):

    if isinstance(date_value, str):
        date_value = datetime.datetime.strptime(
            date_value,
            "%Y-%m-%d"
        ).date()

    weekday = KOR_WEEKDAYS[
        int(date_value.strftime("%w"))
    ]

    return (
        f"{date_value.month}월 "
        f"{date_value.day}일 "
        f"({weekday})"
    )


def get_weekday_index(date_value):
    """
    일요일=0
    월요일=1
    ...
    토요일=6
    """

    return int(date_value.strftime("%w"))


ALL_DATES = (
    get_days_in_month(YEAR, 8)
    + get_days_in_month(YEAR, 9)
)

ALL_DATE_STRS = [
    d.strftime("%Y-%m-%d")
    for d in ALL_DATES
]


# =========================================================
# 5. Session State
# =========================================================

if "participants" not in st.session_state:

    st.session_state.participants = [

        {
            "name": "혜진",
            "available_dates": [
                "2026-08-15",
                "2026-08-16",
                "2026-08-22",
                "2026-08-23",
                "2026-09-05",
                "2026-09-06"
            ]
        },

        {
            "name": "민수",
            "available_dates": [
                "2026-08-15",
                "2026-08-22",
                "2026-08-23",
                "2026-08-29",
                "2026-09-05"
            ]
        },

        {
            "name": "지훈",
            "available_dates": [
                "2026-08-15",
                "2026-08-16",
                "2026-08-22",
                "2026-09-05",
                "2026-09-06",
                "2026-09-12"
            ]
        },

        {
            "name": "서연",
            "available_dates": [
                "2026-08-22",
                "2026-08-23",
                "2026-08-29",
                "2026-09-05",
                "2026-09-06"
            ]
        },

        {
            "name": "동현",
            "available_dates": [
                "2026-08-15",
                "2026-08-22",
                "2026-08-23",
                "2026-09-05",
                "2026-09-19"
            ]
        }
    ]


if "selected_dates_input" not in st.session_state:
    st.session_state.selected_dates_input = []


if "current_month" not in st.session_state:
    st.session_state.current_month = 9


# =========================================================
# 6. URL Query Parameter 처리
# =========================================================

query_params = st.query_params


# 선택된 날짜가 URL에 있으면 반영
if "selected" in query_params:

    selected_raw = query_params.get(
        "selected",
        ""
    )

    if selected_raw:

        selected_from_url = [
            x
            for x in selected_raw.split(",")
            if x in ALL_DATE_STRS
        ]

        st.session_state.selected_dates_input = sorted(
            list(set(selected_from_url))
        )

    else:
        st.session_state.selected_dates_input = []


# 현재 월
if "month" in query_params:

    try:

        month_from_url = int(
            query_params.get("month")
        )

        if month_from_url in MONTHS:
            st.session_state.current_month = (
                month_from_url
            )

    except:
        pass


# =========================================================
# 7. URL 생성 함수
# =========================================================

def make_calendar_url(
    month,
    selected_dates
):

    params = {
        "month": month,
        "selected": ",".join(
            sorted(selected_dates)
        )
    }

    return "?" + urlencode(params)


# =========================================================
# 8. 참여자 날짜 집계
# =========================================================

date_counts = defaultdict(list)

for participant in st.session_state.participants:

    for date_str in participant["available_dates"]:

        date_counts[date_str].append(
            participant["name"]
        )


# =========================================================
# 9. 순위 계산
# =========================================================

ranked_entries = []

for date_str in ALL_DATE_STRS:

    count = len(
        date_counts[date_str]
    )

    if count > 0:

        ranked_entries.append({

            "date": date_str,

            "formatted": format_date_kor(
                date_str
            ),

            "count": count,

            "participants": date_counts[date_str]
        })


ranked_entries.sort(
    key=lambda x: (
        -x["count"],
        x["date"]
    )
)


unique_counts = sorted(
    list(
        set(
            x["count"]
            for x in ranked_entries
        )
    ),
    reverse=True
)


top3_counts = unique_counts[:3]


rank_groups = {
    1: [],
    2: [],
    3: []
}


for entry in ranked_entries:

    if entry["count"] in top3_counts:

        rank = (
            top3_counts.index(
                entry["count"]
            ) + 1
        )

        entry["rank"] = rank

        rank_groups[rank].append(
            entry
        )


total_participants = len(
    st.session_state.participants
)


# =========================================================
# 10. 상단 제목
# =========================================================

st.markdown("""
<div class="card header-card">

    <div class="header-icon">
        📅
    </div>

    <div class="main-title">
        경찰과도둑 모여라
    </div>

    <div class="main-description">
        2026년 8월 ~ 9월 중 친구들과 만날 최적의 날짜를 조율해보세요.
    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# 11. 이름 입력
# =========================================================

st.markdown("""
<div class="card">

    <div class="name-label">
        이름 <span class="required">*</span>
    </div>

""", unsafe_allow_html=True)


name_input = st.text_input(
    "이름",
    placeholder="이름을 입력해주세요",
    label_visibility="collapsed",
    key="user_name_input"
)


st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# =========================================================
# 12. 날짜 선택 카드
# =========================================================

st.markdown("""
<div class="card">

    <div class="section-title">
        📅 참여 가능한 날짜를 선택해주세요.
    </div>

    <div class="section-description">
        달력의 날짜를 클릭하여 복수 선택할 수 있습니다.
    </div>

""", unsafe_allow_html=True)


current_month = st.session_state.current_month


# =========================================================
# 13. 달력 상단
# =========================================================

prev_month = 8 if current_month == 9 else 9
next_month = 9 if current_month == 8 else 8


selected_query = st.session_state.selected_dates_input


prev_url = make_calendar_url(
    prev_month,
    selected_query
)

next_url = make_calendar_url(
    next_month,
    selected_query
)


st.markdown(
    f"""
    <div class="calendar-top">

        <a
            class="month-nav"
            href="{escape(prev_url)}"
        >
            ‹
        </a>

        <div class="month-title">
            {YEAR}년 {current_month}월
        </div>

        <a
            class="month-nav"
            href="{escape(next_url)}"
        >
            ›
        </a>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 14. 요일
# =========================================================

weekday_html = ""

for i, weekday in enumerate(
    KOR_WEEKDAYS
):

    if i == 0:

        css_class = "sun"

    elif i == 6:

        css_class = "sat"

    else:

        css_class = "normal"

    weekday_html += (
        f"""
        <div class="weekday {css_class}">
            {weekday}
        </div>
        """
    )


st.markdown(
    f"""
    <div class="weekday-grid">
        {weekday_html}
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 15. 실제 달력
# =========================================================

number_of_days = calendar.monthrange(
    YEAR,
    current_month
)[1]


first_weekday = (
    calendar.monthrange(
        YEAR,
        current_month
    )[0] + 1
) % 7


calendar_html = """
<div class="calendar-grid">
"""


# ---------------------------------------------------------
# 빈칸
# ---------------------------------------------------------

for _ in range(first_weekday):

    calendar_html += """
    <div class="calendar-empty"></div>
    """


# ---------------------------------------------------------
# 날짜
# ---------------------------------------------------------

for day in range(
    1,
    number_of_days + 1
):

    date_obj = datetime.date(
        YEAR,
        current_month,
        day
    )

    date_str = date_obj.strftime(
        "%Y-%m-%d"
    )

    weekday_index = get_weekday_index(
        date_obj
    )


    # 선택 여부
    is_selected = (
        date_str
        in st.session_state.selected_dates_input
    )


    # 주말 class
    if weekday_index == 0:

        weekend_class = "sun"

    elif weekday_index == 6:

        weekend_class = "sat"

    else:

        weekend_class = ""


    selected_class = (
        "selected"
        if is_selected
        else ""
    )


    # 참여 가능 인원
    count = len(
        date_counts[date_str]
    )


    if count > 0:

        count_text = f"{count}명"

    else:

        count_text = "0명"


    # 클릭했을 때 추가/삭제할 날짜
    if is_selected:

        new_selected = [
            d
            for d in st.session_state.selected_dates_input
            if d != date_str
        ]

    else:

        new_selected = sorted(
            st.session_state.selected_dates_input
            + [date_str]
        )


    date_url = make_calendar_url(
        current_month,
        new_selected
    )


    calendar_html += f"""
    <a
        class="date-button
               {weekend_class}
               {selected_class}"
        href="{escape(date_url)}"
    >

        <div class="date-number">
            {day}일
        </div>

        <div class="date-count">
            {count_text}
        </div>

    </a>
    """


# ---------------------------------------------------------
# 마지막 빈칸
# ---------------------------------------------------------

last_weekday = (
    first_weekday
    + number_of_days
) % 7


if last_weekday != 0:

    for _ in range(
        7 - last_weekday
    ):

        calendar_html += """
        <div class="calendar-empty"></div>
        """


calendar_html += """
</div>
"""


st.markdown(
    calendar_html,
    unsafe_allow_html=True
)


# =========================================================
# 16. 선택한 날짜
# =========================================================

selected_dates = (
    st.session_state.selected_dates_input
)


selected_count = len(
    selected_dates
)


st.markdown(
    f"""
    <div class="selected-area">

        <div class="selected-title">
            선택한 날짜
            <span class="selected-count">
                ({selected_count}개)
            </span>
        </div>

    """,
    unsafe_allow_html=True
)


if selected_count == 0:

    st.markdown("""
        <div class="selected-empty">
            아직 선택한 날짜가 없습니다.
        </div>
    """, unsafe_allow_html=True)


else:

    selected_html = """
    <div class="selected-dates">
    """

    for date_str in selected_dates:

        selected_html += (
            f"""
            <span class="date-tag">
                {format_date_kor(date_str)}
            </span>
            """
        )

    selected_html += """
    </div>
    """

    st.markdown(
        selected_html,
        unsafe_allow_html=True
    )


st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# 날짜 카드 종료
st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# =========================================================
# 17. 제출 버튼
# =========================================================

submit_clicked = st.button(
    "참여 가능한 날짜 제출하기",
    type="primary",
    use_container_width=True,
    key="submit_dates"
)


if submit_clicked:

    trimmed_name = (
        name_input.strip()
    )


    if not trimmed_name:

        st.error(
            "이름을 입력해주세요."
        )


    elif len(selected_dates) == 0:

        st.error(
            "최소 1개 이상의 날짜를 선택해주세요."
        )


    else:

        # 기존 이름 확인
        existing_idx = next(
            (
                i
                for i, participant
                in enumerate(
                    st.session_state.participants
                )
                if participant["name"]
                == trimmed_name
            ),
            None
        )


        # 기존 참가자 수정
        if existing_idx is not None:

            st.session_state.participants[
                existing_idx
            ]["available_dates"] = sorted(
                selected_dates
            )

            message = (
                f"'{trimmed_name}'님의 "
                "참여 일정이 수정되었습니다!"
            )


        # 신규 참가자 추가
        else:

            st.session_state.participants.append({

                "name": trimmed_name,

                "available_dates": sorted(
                    selected_dates
                )

            })

            message = (
                f"'{trimmed_name}'님의 "
                "참여 일정이 등록되었습니다!"
            )


        # 선택 초기화
        st.session_state.selected_dates_input = []


        # URL도 초기화
        st.query_params.clear()


        st.success(message)

        st.rerun()


# =========================================================
# 18. 참여자 결과
# =========================================================

st.markdown("""
<div class="result-card">

    <div class="result-title">
        🏆 가장 많은 사람이 참여 가능한 날짜
    </div>

    <div class="result-description">
        참여 인원이 많은 날짜 TOP 3를 확인하세요.
    </div>

""", unsafe_allow_html=True)


if len(ranked_entries) == 0:

    st.markdown("""
        <div class="selected-empty">
            아직 제출된 투표 데이터가 없습니다.
        </div>
    """, unsafe_allow_html=True)


else:

    for rank_num in [1, 2, 3]:

        items = rank_groups[rank_num]


        if not items:
            continue


        for item in items:

            count = item["count"]

            percentage = round(
                count
                / total_participants
                * 100
            )


            people = ", ".join(
                item["participants"]
            )


            st.markdown(
                f"""
                <div class="rank-item">

                    <div class="rank-header">

                        <span class="rank-badge">
                            {rank_num}순위
                        </span>

                        <span class="rank-date">
                            {item["formatted"]}
                        </span>

                        <span class="rank-count">
                            {count}명 참여 가능
                            ({percentage}%)
                        </span>

                    </div>

                    <div class="rank-people">
                        👥 {people}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# =========================================================
# 19. 전체 참여자
# =========================================================

st.markdown("""
<div class="participant-card">

    <div class="participant-title">
        👥 전체 참여자
    </div>

""", unsafe_allow_html=True)


st.markdown(
    f"""
    <div class="participant-count">
        현재 총 {total_participants}명 참여 중
    </div>
    """,
    unsafe_allow_html=True
)


for idx, participant in enumerate(
    st.session_state.participants
):

    name = participant["name"]

    available_dates = participant[
        "available_dates"
    ]


    dates_text = ", ".join(
        format_date_kor(d)
        for d in available_dates
    )


    with st.expander(
        f"{name} · {len(available_dates)}개 일자"
    ):

        st.write(
            "선택 날짜:",
            dates_text
        )


        delete_clicked = st.button(
            f"'{name}' 삭제",
            key=f"delete_{idx}"
        )


        if delete_clicked:

            st.session_state.participants.pop(
                idx
            )

            st.rerun()


st.markdown(
    "</div>",
    unsafe_allow_html=True
)

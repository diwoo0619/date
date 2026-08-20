import streamlit as st
import pandas as pd
import datetime
import calendar
from collections import defaultdict

# -------------------------------------------------------------
# 1. Page Configuration & Custom CSS
# -------------------------------------------------------------
st.set_page_config(
    page_title="2026 모임 날짜 정하기",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom minimal styling
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    html, body, [class*="css"] {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }
    
    .main-title {
        font-size: 1.6rem;
        font-weight: 800;
        color: #1e1b4b;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 0.9rem;
        color: #64748b;
        margin-bottom: 1.2rem;
    }
    .rank-box {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 14px;
    }
    .rank-badge-1 {
        background-color: #4f46e5;
        color: white;
        padding: 3px 9px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.8rem;
    }
    .rank-badge-2 {
        background-color: #1e293b;
        color: white;
        padding: 3px 9px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.8rem;
    }
    .rank-badge-3 {
        background-color: #e2e8f0;
        color: #475569;
        padding: 3px 9px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.8rem;
    }
    .date-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 12px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
    .cal-cell {
        text-align: center;
        padding: 8px 4px;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        background: white;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 2. Date Utilities (2026-08 & 2026-09)
# -------------------------------------------------------------
YEAR = 2026
MONTHS = [8, 9]
KOR_WEEKDAYS = ["일", "월", "화", "수", "목", "금", "토"]

def get_days_in_month(year, month):
    num_days = calendar.monthrange(year, month)[1]
    return [datetime.date(year, month, day) for day in range(1, num_days + 1)]

ALL_DATES = get_days_in_month(YEAR, 8) + get_days_in_month(YEAR, 9)
ALL_DATE_STRS = [d.strftime("%Y-%m-%d") for d in ALL_DATES]

def format_date_kor(date_obj):
    if isinstance(date_obj, str):
        date_obj = datetime.datetime.strptime(date_obj, "%Y-%m-%d").date()
    weekday_str = KOR_WEEKDAYS[int(date_obj.strftime("%w"))]
    return f"{date_obj.month}월 {date_obj.day}일 ({weekday_str})"

def is_weekend(date_obj):
    if isinstance(date_obj, str):
        date_obj = datetime.datetime.strptime(date_obj, "%Y-%m-%d").date()
    return date_obj.weekday() in [5, 6] # 5 is Saturday, 6 is Sunday

# -------------------------------------------------------------
# 3. Session State Initialization
# -------------------------------------------------------------
if "participants" not in st.session_state:
    st.session_state.participants = [
        {"name": "혜진", "available_dates": ["2026-08-15", "2026-08-16", "2026-08-22", "2026-08-23", "2026-09-05", "2026-09-06"]},
        {"name": "민수", "available_dates": ["2026-08-15", "2026-08-22", "2026-08-23", "2026-08-29", "2026-09-05"]},
        {"name": "지훈", "available_dates": ["2026-08-15", "2026-08-16", "2026-08-22", "2026-09-05", "2026-09-06", "2026-09-12"]},
        {"name": "서연", "available_dates": ["2026-08-22", "2026-08-23", "2026-08-29", "2026-09-05", "2026-09-06"]},
        {"name": "동현", "available_dates": ["2026-08-15", "2026-08-22", "2026-08-23", "2026-09-05", "2026-09-19"]}
    ]

if "selected_dates_input" not in st.session_state:
    st.session_state.selected_dates_input = []

# -------------------------------------------------------------
# 4. Header Section
# -------------------------------------------------------------
st.markdown('<div class="main-title">📅 2026 모임 날짜 정하기</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">2026년 8월 ~ 9월 중 친구들과 만날 최적의 날짜를 조율해보세요.</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# 5. Calculation Logic
# -------------------------------------------------------------
date_counts = defaultdict(list)
for p in st.session_state.participants:
    for d in p["available_dates"]:
        date_counts[d].append(p["name"])

# Rank calculations
ranked_entries = []
for d_str in ALL_DATE_STRS:
    count = len(date_counts[d_str])
    if count > 0:
        ranked_entries.append({
            "date": d_str,
            "formatted": format_date_kor(d_str),
            "count": count,
            "participants": date_counts[d_str]
        })

ranked_entries.sort(key=lambda x: (-x["count"], x["date"]))

# Dense Ranking for 1st, 2nd, 3rd
unique_counts = sorted(list(set([x["count"] for x in ranked_entries])), reverse=True)
top3_counts = unique_counts[:3]

rank_groups = {1: [], 2: [], 3: []}
for entry in ranked_entries:
    if entry["count"] in top3_counts:
        rank_idx = top3_counts.index(entry["count"]) + 1
        entry["rank"] = rank_idx
        rank_groups[rank_idx].append(entry)

total_participants = len(st.session_state.participants)

# -------------------------------------------------------------
# 6. Layout: Sidebar (Input) + Main Area (Results)
# -------------------------------------------------------------
with st.sidebar:
    st.subheader("✏️ 참여 날짜 제출")
    name_input = st.text_input("내 이름", placeholder="예: 홍길동", key="user_name_input")
    
    st.write("**가능한 날짜 선택 (2026년 8~9월)**")
    
    # Shortcut buttons
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🏖️ 8월 주말 선택", use_container_width=True):
            aug_weekends = [d.strftime("%Y-%m-%d") for d in get_days_in_month(2026, 8) if is_weekend(d)]
            st.session_state.selected_dates_input = sorted(list(set(st.session_state.selected_dates_input + aug_weekends)))
            st.rerun()
    with col_btn2:
        if st.button("🍁 9월 주말 선택", use_container_width=True):
            sept_weekends = [d.strftime("%Y-%m-%d") for d in get_days_in_month(2026, 9) if is_weekend(d)]
            st.session_state.selected_dates_input = sorted(list(set(st.session_state.selected_dates_input + sept_weekends)))
            st.rerun()
            
    col_btn3, col_btn4 = st.columns(2)
    with col_btn3:
        if st.button("✨ 전체 주말", use_container_width=True):
            all_weekends = [d.strftime("%Y-%m-%d") for d in ALL_DATES if is_weekend(d)]
            st.session_state.selected_dates_input = sorted(list(set(st.session_state.selected_dates_input + all_weekends)))
            st.rerun()
    with col_btn4:
        if st.button("🔄 선택 초기화", use_container_width=True):
            st.session_state.selected_dates_input = []
            st.rerun()

    # Multiselect widget for dates
    date_options = {d_str: format_date_kor(d_str) for d_str in ALL_DATE_STRS}
    
    selected_keys = st.multiselect(
        "날짜 목록에서 직접 체크:",
        options=ALL_DATE_STRS,
        default=st.session_state.selected_dates_input,
        format_func=lambda x: date_options[x]
    )
    st.session_state.selected_dates_input = selected_keys

    st.write(f"선택한 날짜: **{len(st.session_state.selected_dates_input)}개 일자**")

    # Submit button
    if st.button("🚀 참여 가능 날짜 제출하기", type="primary", use_container_width=True):
        trimmed_name = name_input.strip()
        if not trimmed_name:
            st.error("이름을 입력해주세요.")
        elif len(st.session_state.selected_dates_input) == 0:
            st.error("최소 1개 이상의 참여 가능 날짜를 선택해주세요.")
        else:
            # Check if name already exists (update) or add new
            existing_idx = next((i for i, p in enumerate(st.session_state.participants) if p["name"] == trimmed_name), None)
            if existing_idx is not None:
                st.session_state.participants[existing_idx]["available_dates"] = sorted(st.session_state.selected_dates_input)
                st.success(f"'{trimmed_name}'님의 참여 일정이 수정되었습니다!")
            else:
                st.session_state.participants.append({
                    "name": trimmed_name,
                    "available_dates": sorted(st.session_state.selected_dates_input)
                })
                st.success(f"'{trimmed_name}'님의 참여 일정이 등록되었습니다!")
            st.session_state.selected_dates_input = []
            st.rerun()

# -------------------------------------------------------------
# 7. Main Dashboard Area
# -------------------------------------------------------------

# Section 1: 전체 참여자 날짜별 현황 (달력 뷰 & 표)
st.markdown("### 📊 1. 전체 참여자 날짜별 현황")
st.caption("각 날짜별로 참여 가능한 인원수를 한눈에 확인하세요.")

tab_aug, tab_sept = st.tabs(["2026년 8월 현황", "2026년 9월 현황"])

def render_month_calendar(month_num):
    num_days = calendar.monthrange(YEAR, month_num)[1]
    first_weekday = (calendar.monthrange(YEAR, month_num)[0] + 1) % 7 # 0 is Sunday
    
    cols = st.columns(7)
    for idx, day_name in enumerate(["일", "월", "화", "수", "목", "금", "토"]):
        if idx == 0:
            cols[idx].markdown(f"<span style='color:#ef4444;font-weight:700'>{day_name}</span>", unsafe_allow_html=True)
        elif idx == 6:
            cols[idx].markdown(f"<span style='color:#3b82f6;font-weight:700'>{day_name}</span>", unsafe_allow_html=True)
        else:
            cols[idx].markdown(f"<span style='color:#64748b;font-weight:700'>{day_name}</span>", unsafe_allow_html=True)
    
    current_day = 1
    total_cells = first_weekday + num_days
    num_rows = (total_cells + 6) // 7
    
    for row in range(num_rows):
        row_cols = st.columns(7)
        for col_idx in range(7):
            cell_idx = row * 7 + col_idx
            if cell_idx < first_weekday or current_day > num_days:
                row_cols[col_idx].write("")
            else:
                d_str = f"2026-{month_num:02d}-{current_day:02d}"
                attendees = date_counts[d_str]
                count = len(attendees)
                
                # Highlight top dates
                is_top = count > 0 and len(top3_counts) > 0 and count == top3_counts[0]
                bg_style = "background:#eef2ff;border:1.5px solid #4f46e5;" if is_top else ("background:white;border:1px solid #e2e8f0;" if count > 0 else "background:#f8fafc;border:1px solid #f1f5f9;")
                badge_style = "color:#4f46e5;font-weight:800;" if count > 0 else "color:#cbd5e1;"
                
                with row_cols[col_idx]:
                    st.markdown(f"""
                    <div style="{bg_style}border-radius:10px;padding:6px;text-align:center;min-height:55px;">
                        <div style="font-size:0.75rem;color:#64748b;">{current_day}일</div>
                        <div style="font-size:0.85rem;{badge_style}">{count}명</div>
                    </div>
                    """, unsafe_allow_html=True)
                current_day += 1

with tab_aug:
    render_month_calendar(8)

with tab_sept:
    render_month_calendar(9)

st.divider()

# Section 2: 가장 많은 사람이 참여 가능한 날짜 (1~3순위 동순위 열 배열)
st.markdown("### 🏆 2. 가장 많은 사람이 참여 가능한 날짜 (1~3순위)")
st.caption("동일한 순위의 날짜들은 같은 열(Row)에 나란히 배치됩니다.")

if total_participants == 0 or len(ranked_entries) == 0:
    st.info("아직 제출된 투표 데이터가 없습니다. 왼쪽 사이드바에서 날짜를 제출해보세요!")
else:
    for rank_num in [1, 2, 3]:
        items = rank_groups[rank_num]
        if not items:
            continue
        
        vote_count = items[0]["count"]
        pct = round((vote_count / total_participants) * 100)
        badge_cls = f"rank-badge-{rank_num}"
        
        st.markdown(f"""
        <div class="rank-box">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; border-bottom:1px solid #e2e8f0; padding-bottom:6px;">
                <div>
                    <span class="{badge_cls}">{rank_num}순위</span>
                    <span style="font-size:0.85rem; font-weight:700; color:#1e293b; margin-left:8px;">{vote_count}명 참여 가능 ({pct}%)</span>
                    {f'<span style="font-size:0.75rem; color:#64748b; margin-left:6px;">(동순위 {len(items)}개 날짜)</span>' if len(items) > 1 else ''}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display tied items side-by-side in columns
        item_cols = st.columns(len(items))
        for idx, item in enumerate(items):
            with item_cols[idx]:
                st.markdown(f"""
                <div class="date-card">
                    <div style="font-size:1.05rem; font-weight:800; color:#1e1b4b; margin-bottom:4px;">
                        {item["formatted"]}
                    </div>
                    <div style="font-size:0.8rem; color:#64748b;">
                        👥 <strong>참여 ({len(item["participants"])}명):</strong> {", ".join(item["participants"])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        st.write("")

st.divider()

# Section 3: 참여자 명단 & 텍스트 복사
col_p1, col_p2 = st.columns([1, 1])

with col_p1:
    st.markdown("### 👥 전체 참여자 명단")
    st.write(f"현재 총 **{total_participants}명** 참여 중")
    
    for idx, p in enumerate(st.session_state.participants):
        with st.expander(f"👤 {p['name']} ({len(p['available_dates'])}개 일자 선택)"):
            st.write("선택 날짜:", ", ".join([format_date_kor(d) for d in p['available_dates']]))
            if st.button(f"'{p['name']}' 삭제", key=f"del_{idx}"):
                st.session_state.participants.pop(idx)
                st.rerun()

with col_p2:
    st.markdown("### 📋 결과 요약 텍스트")
    st.caption("모임 단톡방에 바로 복사하여 공유할 수 있습니다.")
    
    summary_lines = [
        "📅 [2026 모임 날짜 투표 결과 (1~3순위)]",
        f"• 총 참여 인원: {total_participants}명",
        ""
    ]
    for r_num in [1, 2, 3]:
        r_items = rank_groups[r_num]
        if r_items:
            for item in r_items:
                summary_lines.append(f"• [{r_num}순위] {item['formatted']}: {item['count']}명 ({', '.join(item['participants'])})")
    
    summary_lines.append("")
    summary_lines.append(f"👥 참여자: {', '.join([p['name'] for p in st.session_state.participants])}")
    
    summary_text = "\n".join(summary_lines)
    st.code(summary_text, language="markdown")

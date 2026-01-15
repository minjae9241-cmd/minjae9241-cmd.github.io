import streamlit as st
import datetime
import random
import database as db

# 데이터베이스 초기화
db.init_db()

# 페이지 기본 설정
st.set_page_config(page_title="초등학급 경영 도우미", layout="wide")

# --- 세션 상태 초기화 ---
if 'page' not in st.session_state:
    st.session_state.page = "🏠 홈"

def navigate_to(page):
    st.session_state.page = page
    st.rerun()

menu = st.session_state.page

# --- 스타일링 (Cute & Hand-drawn) ---
# --- 스타일링 (Cute & Hand-drawn) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

html, body, [class*="st-"], [class*="css-"], .stApp, button, input, textarea, div, h1, p {
    font-family: 'Jua', sans-serif !important;
}

/* 전체 배경색 (귀여운 노랑) */
.stApp {
    background-color: #FFFDE7;
}

/* 사이드바 숨기기 */
section[data-testid="stSidebar"] {
    display: none;
}

/* 메인 타이틀 */
h1 {
    color: #5D4037;
    text-align: center;
    text-shadow: 2px 2px 0px #FFF9C4;
    font-size: 4.5rem; /* 제일 크게 */
}

/* 서브타이틀, 일반 텍스트 */
p, div {
    text-align: center;
    color: #5D4037;
}

/* 기본 버튼 스타일 */
.stButton > button {
    width: 100%;
    height: 250px;
    background-color: #FFFFFF;
    border: 4px solid #FBC02D;
    border-radius: 30px;
    color: #3E2723;
    font-family: 'Jua', sans-serif;
    box-shadow: 5px 5px 0px 0px #F9A825;
    line-height: 1.5;
    white-space: pre-wrap;
    display: block;
}
.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 3px 3px 0px 0px #F9A825;
    background-color: #FFF9C4;
    color: #E65100;
}

/* 버튼 내부 텍스트 스타일링 (확실하게 적용) */
div.stButton > button p {
    font-size: 1.5rem !important; /* 설명 글씨 (3순위) */
    line-height: 1.3 !important;
}

div.stButton > button p::first-line {
    font-size: 2.8rem !important; /* 제목 글씨 (2순위) */
    font-weight: bold !important;
    line-height: 1.5 !important;
    display: block !important;
}

/* 메인 타이틀 (1순위) */
h1 {
    font-size: 4.5rem !important;
    color: #5D4037 !important;
    text-shadow: 2px 2px 0px #FFF9C4;
    text-align: center;
}

/* 입력 필드 */
.stTextInput>div>div>input, .stTextArea>div>div>textarea {
    background-color: #FFFFFF;
    border: 3px solid #FBC02D;
    border-radius: 15px;
    font-family: 'Jua', sans-serif;
    color: #3E2723;
}
</style>
""", unsafe_allow_html=True)

# 홈이 아닌 페이지에 '홈으로 가기' 버튼 표시 (작고 귀엽게 커스텀 필요하지만 일단 기본 적용)
if menu != "🏠 홈":
    if st.button("🏠 홈으로 가기"):
        navigate_to("🏠 홈")
    st.divider()

# 메뉴 선택에 따른 화면 표시
if menu == "🏠 홈":
    st.title("🍠 군고구마반의 행복한 하루하루 🍠")
    st.markdown("<br>", unsafe_allow_html=True) # 간격 추가
    st.divider()

    c1, c2, c3 = st.columns(3)
    
    with c1:
        if st.button("🏫 오늘의 우리반\n\n일정, 급식, 알림장", key="home_today", use_container_width=True):
            navigate_to("오늘의 우리반")
        
    with c2:
        if st.button("📋 이 달의 우리반\n\n학생 명단, 자리 배치", key="home_manage", use_container_width=True):
            navigate_to("이 달의 우리반")
        
    with c3:
        if st.button("🌱 성장 일지\n\n하루 기록, 선생님 응원", key="home_growth", use_container_width=True):
            navigate_to("성장 일지")
    
    st.divider()


elif menu == "오늘의 우리반":
    st.title("🏫 오늘의 우리반")

    # 날짜 선택
    selected_date = st.date_input("날짜 선택", datetime.date.today())

    # 데이터베이스에서 기존 데이터 조회
    existing_data = db.get_daily_log(selected_date)
    
    # 기본값 설정
    schedule_default = existing_data[0] if existing_data else ""
    lunch_default = existing_data[1] if existing_data else ""
    todo_default = existing_data[2] if existing_data else ""
    supplies_default = existing_data[3] if existing_data else ""

    # 입력 폼
    with st.expander("📝 오늘의 알림 입력하기", expanded=True):
        with st.form("daily_log_form"):
            col1, col2 = st.columns(2)
            with col1:
                schedule = st.text_area("학급 일과", value=schedule_default, height=100)
                lunch = st.text_area("오늘의 급식", value=lunch_default, height=100)
            with col2:
                todo = st.text_area("꼭 해야 할 일", value=todo_default, height=100)
                supplies = st.text_area("준비물", value=supplies_default, height=100)
            
            submit_btn = st.form_submit_button("저장하기")
            
            if submit_btn:
                db.save_daily_log(selected_date, schedule, lunch, todo, supplies)
                st.success(f"{selected_date}의 기록이 저장되었습니다!")
                st.rerun()

    st.divider()

    # 조회 화면 (카드 형태)
    if existing_data:
        st.subheader(f"📅 {selected_date.strftime('%Y년 %m월 %d일')} 알림장")
        
        # 스타일링을 위한 CSS
        st.markdown("""
        <style>
        .info-card {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 5px solid #ff4b4b;
        }
        .info-title {
            font-weight: bold;
            color: #31333F;
            margin-bottom: 10px;
            font-size: 1.1em;
        }
        </style>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="info-card">
                <div class="info-title">🕒 학급 일과</div>
                {schedule_default.replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="info-card" style="border-left-color: #4caf50;">
                <div class="info-title">🍱 오늘의 급식</div>
                {lunch_default.replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""
            <div class="info-card" style="border-left-color: #ff9800;">
                <div class="info-title">✅ 꼭 해야 할 일</div>
                {todo_default.replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown(f"""
            <div class="info-card" style="border-left-color: #2196f3;">
                <div class="info-title">🎒 준비물</div>
                {supplies_default.replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("등록된 정보가 없습니다. 위의 양식을 통해 내용을 입력해주세요.")

elif menu == "이 달의 우리반":
    st.title("📋 이 달의 우리반")
    
    # 탭 생성
    tab1, tab2, tab3 = st.tabs(["👨‍🎓 학생 명단", "🪑 자리 배치", "🧹 1인 1역"])
    
    # 탭 1: 학생 명단 관리
    with tab1:
        st.subheader("우리반 학생 명단")
        
        # 학생 추가 폼
        with st.form("add_student_form", clear_on_submit=True):
            col_input, col_btn = st.columns([4, 1])
            with col_input:
                new_student_name = st.text_input("학생 이름 입력")
            with col_btn:
                submitted = st.form_submit_button("추가")
            
            if submitted and new_student_name:
                db.add_student(new_student_name)
                st.success(f"{new_student_name} 학생이 추가되었습니다.")
                st.rerun()

        # 학생 목록 표시
        students = db.get_all_students()
        if students:
            st.write(f"총 {len(students)}명")
            for student_id, name in students:
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.write(name)
                with c2:
                    if st.button("삭제", key=f"del_{student_id}"):
                        db.delete_student(student_id)
                        st.rerun()
        else:
            st.info("등록된 학생이 없습니다. 학생 이름을 입력하여 추가해주세요.")

    # 탭 2: 자리 배치
    with tab2:
        st.subheader("자리 배치")
        
        col_action, col_display = st.columns([1, 4])
        
        with col_action:
            if st.button("자리 배치하기", type="primary"):
                # 학생 명단 가져오기
                students = db.get_all_students() 
                student_names = [s[1] for s in students]
                
                if student_names:
                    random.shuffle(student_names)
                    db.save_seat_arrangement(student_names)
                    st.success("자리가 배치되었습니다!")
                    st.rerun()
                else:
                    st.warning("먼저 학생 명단 탭에서 학생을 등록해주세요.")

        with col_display:
            # 배치된 자리 표시
            arranged_seats = db.get_seat_arrangement()
            
            if arranged_seats:
                # 6열 그리드로 표시
                cols = st.columns(6)
                for i, name in enumerate(arranged_seats):
                    with cols[i % 6]:
                        st.markdown(f"""
                        <div style="
                            padding: 20px 10px;
                            background-color: #e3f2fd;
                            border-radius: 10px;
                            text-align: center;
                            margin-bottom: 10px;
                            border: 1px solid #90caf9;
                        ">
                            <div style="font-weight:bold;">{name}</div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("아직 배치된 자리가 없습니다. '자리 배치하기' 버튼을 눌러주세요.")

    # 탭 3: 1인 1역
    with tab3:
        st.subheader("1인 1역 (준비 중)")
        st.info("1인 1역 관리 기능이 곧 추가될 예정입니다.")

elif menu == "성장 일지":
    st.title("🌱 성장 일지")
    
    # 사이드바가 없르므로 페이지 상단에서 모드 선택
    user_mode = st.radio("모드 선택", ["학생용", "교사용"], horizontal=True)
    st.divider()
    
    if user_mode == "학생용":
        st.subheader("📝 나의 성장 일지 쓰기")
        
        # 학생 이름 입력을 위한 Session State 활용 (편의성)
        if "student_name" not in st.session_state:
            st.session_state.student_name = ""

        with st.form("growth_log_form", clear_on_submit=True):
            name_input = st.text_input("이름", value=st.session_state.student_name)
            content = st.text_area("오늘 있었던 특별한 일이나 배운 점을 기록해보세요.")
            submitted = st.form_submit_button("저장하기")
            
            if submitted:
                if name_input and content:
                    db.add_growth_log(name_input, content)
                    st.session_state.student_name = name_input # 이름 기억하기
                    st.success("성장 일지가 저장되었습니다!")
                    st.rerun()
                else:
                    st.error("이름과 내용을 모두 입력해주세요.")
        
        st.divider()
        st.subheader("📂 내가 쓴 글")
        
        current_name = st.text_input("조회할 이름 입력", value=st.session_state.student_name, key="view_name_input")
        
        if current_name:
            logs = db.get_student_logs(current_name)
            if logs:
                for log_id, date, content, comment in logs:
                    with st.expander(f"{date}의 기록", expanded=True):
                        st.write(content)
                        if comment:
                            st.info(f"👩‍🏫 선생님 코멘트: {comment}")
                        else:
                            st.caption("아직 코멘트가 없습니다.")
            else:
                st.info("작성된 기록이 없습니다.")

    else: # 교사용 모드
        st.subheader("👨‍🏫 학생들의 성장 일지")
        st.info("학생들이 쓴 글을 확인하고 코멘트를 남길 수 있습니다.")
        
        logs = db.get_all_growth_logs()
        
        if logs:
            for log_id, date, student_name, content, comment in logs:
                with st.container():
                    st.markdown(f"**[{date}] {student_name} 학생**")
                    st.write(content)
                    
                    # 코멘트 입력창
                    with st.expander("코멘트 달기", expanded=False):
                        new_comment = st.text_area("피드백 입력", value=comment if comment else "", key=f"comment_{log_id}")
                        if st.button("코멘트 저장", key=f"save_{log_id}"):
                            db.update_teacher_comment(log_id, new_comment)
                            st.success("코멘트가 저장되었습니다!")
                            st.rerun()
                    st.divider()
        else:
            st.info("아직 등록된 성장 일지가 없습니다.")

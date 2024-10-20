from chatting import persona_agent, RAG_agent
import streamlit as st
import os

from util import CHAT_ICON_LIST, START_LIST

def display_chat_message(profile_image, message, role):
    ''' Streamlit 채팅 UI를 HTML로 수정 후 채팅 내용을 화면에 표시 '''
    st.markdown(
        f'<div style="display: flex; align-items: center;">'
        f'<img src="{profile_image}" style="border-radius:50%; width: 30px; height: 30px; margin-right: 10px;">'
        f'{message}'
        f'</div><br>',
        unsafe_allow_html=True
    )

def chat_page(data, char):
    ''' 대화 화면 구성 '''
    
    # 초기 메세지 세션 설정
    if "messages_char" not in st.session_state:
        st.session_state["messages_char"] = [START_LIST[char]]
    if "messages_rag" not in st.session_state:
        st.session_state["messages_rag"] = []

    col1, col2 = st.columns(2)

    # 기존 메세지 출력
    with col1:
        st.subheader("페르소나 챗봇과의 대화")
        for msg in st.session_state["messages_char"]:
            display_chat_message(msg["profile_image"], msg["content"], msg["role"])
        
    with col2:
        st.subheader("RAG 에이전트와의 대화")
        for msg in st.session_state["messages_rag"]:
            display_chat_message(msg["profile_image"], msg["content"], msg["role"])

    agent = persona_agent(data, char)
    rag_chain = RAG_agent(data)
    
    # 새 인풋에 대한 출력 생성
    if prompt := st.chat_input("메세지를 입력하세요..."):
        st.session_state["messages_char"].append({
            "role": "user",
            "content": prompt, 
            "profile_image": CHAT_ICON_LIST["user"]
        })

        st.session_state["messages_rag"].append({
            "role": "user",
            "content": prompt,
            "profile_image": CHAT_ICON_LIST["user"]
        })

        # 사용자 메세지 표시
        with col1:
            display_chat_message(CHAT_ICON_LIST["user"], prompt, "user")
        with col2:
            display_chat_message(CHAT_ICON_LIST["user"], prompt, "user")

        #assistant_response = agent.receive_chat(prompt)

        # 페르소나 챗봇 응답
        assistant_response = agent.receive_chat(prompt)
        st.session_state["messages_char"].append({
            "role": char,
            "content": assistant_response,
            "profile_image": CHAT_ICON_LIST[char]
        })
        
        with col1:
            display_chat_message(CHAT_ICON_LIST[char], assistant_response, char)
        
        # RAG agent 응답
        response2 = rag_chain.receive_chat(prompt)
        st.session_state["messages_rag"].append({
            "role": "bot",
            "content": response2,
            "profile_image": CHAT_ICON_LIST["bot"]
        })

        with col2:
            display_chat_message(CHAT_ICON_LIST["bot"], response2, char)

def main():
    ''' 메인 화면 구성 '''
    st.subheader("Langchain을 활용한 가상의 인격을 가진 캐릭터 챗봇 서비스 개발 데모")

    st.sidebar.title("캐릭터 선택")
    selected_char = st.sidebar.selectbox(
        "대화할 캐릭터를 선택하세요",
        ["캐릭터 선택",
        "스파이더맨(피터 파커)",
        "전우치",
        "신짱구"]
    )

    if selected_char != "캐릭터 선택":
        if selected_char == "스파이더맨(피터 파커)":
            data = "data/spiderman.txt"
            char = "pp"
            st.sidebar.write("질문 예시: 얼티밋 유니버스가 뭐야?, 웹 슈터는 어떻게 만들어?")
        elif selected_char == "전우치":
            data = "data/jwc.txt"
            char = "jwc"
            st.sidebar.write("질문 예시: 천관대사가 누구야? 초랭이랑은 무슨 사이야?")
        elif selected_char == "신짱구":
            data = "data/szg.txt"
            char = "szg"
            st.sidebar.write("질문 예시: 짱구의 가족에 대해 알려 줄래? 봉미소가 누구야?")

        if "previous_char" not in st.session_state:
            st.session_state.previous_char = selected_char
        elif st.session_state.previous_char != selected_char:
            st.session_state["messages_char"] = [START_LIST[char]]
            st.session_state["messages_rag"] = []
            st.session_state.previous_char = selected_char

        os.environ["OPENAI_API_KEY"] = st.secrets["openai_key"]
        chat_page(data, char)

        

if __name__ == "__main__":
    main()

import random
import streamlit as st

st.set_page_config(
    page_title="猜字谜小游戏",
    page_icon="🧩",
    layout="centered"
)

# 网页样式
st.title("🧩 猜字谜小游戏")
st.write("动动脑筋，看看你能获得多少积分！")

# 题库
RIDDLES = [
    {"question": "一口咬掉牛尾巴，猜一个字。", "answer": "告"},
    {"question": "什么门永远关不上？", "answer": "球门"},
    {"question": "什么东西晚上满天都是？", "answer": "星星"},
    {"question": "一个人搬两块土，猜一个字。", "answer": "佳"},
    {"question": "有水能养鱼虾，有土能种庄稼，猜一个字。", "answer": "也"},
    {"question": "两个人坐在土上，猜一个字。", "answer": "坐"},
    {"question": "什么东西有头无脚？", "answer": "针"},
    {"question": "什么东西越洗越脏？", "answer": "水"},
]

# 初始化游戏数据
if "questions" not in st.session_state:
    questions = RIDDLES.copy()
    random.shuffle(questions)
    st.session_state.questions = questions
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.finished = False

# 重新开始游戏
def restart_game():
    questions = RIDDLES.copy()
    random.shuffle(questions)
    st.session_state.questions = questions
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.finished = False

# 游戏结束页面
if st.session_state.index >= len(st.session_state.questions):
    st.session_state.finished = True

if st.session_state.finished:
    st.success("🎉 所有题目都答完了！")
    st.metric("最终积分", f"{st.session_state.score} 分")
    st.write(f"本轮共完成 {len(st.session_state.questions)} 道题。")
    st.button("🔄 再玩一次", on_click=restart_game)

else:
    index = st.session_state.index
    riddle = st.session_state.questions[index]

    # 显示积分和进度
    st.metric("🏆 当前积分", f"{st.session_state.score} 分")
    st.progress(index / len(st.session_state.questions))
    st.caption(f"第 {index + 1} / {len(st.session_state.questions)} 题")

    st.divider()

    # 显示问题
    st.subheader(riddle["question"])

    # 答题表单
    if not st.session_state.answered:
        with st.form("answer_form", clear_on_submit=False):
            answer = st.text_input("请输入你的答案", key="answer_input")
            submitted = st.form_submit_button(
                "提交答案",
                use_container_width=True
            )

        if submitted:
            if not answer.strip():
                st.warning("请先输入答案！")
            else:
                st.session_state.answered = True

                if answer.strip() == riddle["answer"]:
                    st.session_state.score += 10
                    st.session_state.feedback = "correct"
                else:
                    st.session_state.feedback = "wrong"

                st.rerun()

    # 显示答题反馈
    if st.session_state.answered:
        if st.session_state.feedback == "correct":
            st.success("回答正确！🎉 获得 10 分！")
        else:
            st.error("回答错误，再接再厉！")
            st.info(f"正确答案：{riddle['answer']}")

        st.write(f"当前积分：**{st.session_state.score} 分**")

        if st.button("下一题 ➡️", use_container_width=True):
            st.session_state.index += 1
            st.session_state.answered = False
            st.rerun()

    st.divider()
    st.caption("规则：每题只抽取一次，答对加 10 分，答错不扣分。")
    st.button("🔄 重新开始", on_click=restart_game)

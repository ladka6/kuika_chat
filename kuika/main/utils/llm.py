from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from flask import current_app

store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


class LLMInteraction:
    def __init__(self, session_id):
        self.llm = ChatOpenAI(api_key=current_app.config["OPENAI_API_KEY"])
        self.session_id = session_id
        self.with_message = self._create_chain()
        self.talk_chain = self._talk_chain()
        self.config = {"configurable": {"session_id": self.session_id}}

    def _create_chain(self) -> RunnableWithMessageHistory:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an assistant helping a user to get requirements for a job. \n"
                    "The user will provide a job description and you will ask questions to get the requirements.\n"
                    "The first message you send will be just the requirements for the job description."
                    "The first message should start with 'Requirements' and the rest of the requirements should be separated with new line characters, don't use '-' or bullet points in any requirement.\n"
                    "The user will provide the job description in the first message.\n"
                    "The user will provide the response to the questions in the subsequent messages.",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        chain = prompt | self.llm
        with_message = RunnableWithMessageHistory(
            chain, get_session_history, input_messages_key="messages"
        )
        return with_message

    def _talk_chain(self) -> RunnableWithMessageHistory:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are assisting a user in achieving a specific job role.\n"
                    "The job description is: {job_description}\n"
                    "Here are the specific requirements for the job: {requirements}\n"
                    "Before this conversation, you completed these steps: {completed_steps}\n"
                    "You are currently at step: {current_step}\n"
                    "Please focus on addressing the user's current requirement.\n"
                    "Just talk about the current step. If there is nothing to say, just say it.\n"
                    "Provide a response based on their input.\n",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        chain = prompt | self.llm
        with_message = RunnableWithMessageHistory(
            chain, get_session_history, input_messages_key="messages"
        )
        return with_message

    def get_requirements(self, job_description) -> str:
        res = self.with_message.invoke(
            {"messages": [HumanMessage(job_description)]}, config=self.config
        )
        return res.content

    def chat(
        self, message, job_description, requirements, current_step, completed_steps
    ) -> str:
        context = {
            "job_description": job_description,
            "requirements": requirements,
            "completed_steps": completed_steps,
            "current_step": current_step,
            "messages": [HumanMessage(message)],
        }
        res = self.talk_chain.invoke(context, config=self.config)
        return res.content

    def run_agent_for_job_description(self, job_description):
        pass

    def summarize_job_description(self, job_description):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a database manager that helps to summarize the given job description.\n"
                    "Your summarized version will be saved into a database as a unique key for the job description.\n",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        chain = prompt | self.llm
        res = chain.invoke(
            {"messages": [HumanMessage(job_description)]}, config=self.config
        )
        return res.content

    def select_job_description(self, job_description):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a database manager that helps to insert a summarized job description.\n"
                    "With the given summarized job description and the list of previously saved job descriptions, "
                    "determine if we need to insert this as a new column or not.",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        chain = prompt | self.llm
        res = chain.invoke(
            {"messages": [HumanMessage(job_description)]}, config=self.config
        )
        return res.content

    def generate_report(self):
        report = []
        for message in store[self.session_id].messages:
            if isinstance(message, AIMessage):
                report.append(message.content)
        return report

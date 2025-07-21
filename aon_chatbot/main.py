from aon_chatbot.services import llm_service, ChatbotWithGUI


chatbot_with_gui = ChatbotWithGUI()
llm_service.run_streamlit(chatbot_with_gui)

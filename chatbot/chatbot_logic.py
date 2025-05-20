# import google.generativeai as genai

# API_KEY = "AIzaSyC9zswMwW5Z7f_UADXeJAlvkfQ2uhKV-Nk"
# genai.configure(api_key=API_KEY)

# def chatbot_response(user_input):
#     model = genai.GenerativeModel("gemini-2.0-flash")
#     user_input = user_input + "You are a friendly, casual, and helpful AI who talks like a real human friend. Always reply like you are chatting with a close buddy. Keep it natural, simple, and avoid sounding robotic. Do not add any markdown or formatting, only return plain text."
    
#     try:
#         response = model.generate_content(user_input)
#         print("API Response:", response.text)  # Debugging
#         return response.text  # Ensure it returns valid text
#     except Exception as e:
#         print("Error:", str(e))
#         return "Sorry, something went wrong."
import google.generativeai as genai
import markdown  # ✅ for converting markdown to HTML

API_KEY = "AIzaSyC9zswMwW5Z7f_UADXeJAlvkfQ2uhKV-Nk"
genai.configure(api_key=API_KEY)

def chatbot_response(user_input):
    model = genai.GenerativeModel("gemini-2.0-flash")

    # ✅ Professional personal assistant style with markdown formatting
    instruction = (
        "You are a professional AI-powered personal assistant. "
        "Respond concisely and formally. Format your answers using Markdown. "
        "Use headings, bullet points, sub-points, and spacing to organize the content. "
        "Avoid casual language. For missing data, say 'Not Found'."
    )

    full_prompt = f"{instruction}\n\nUser: {user_input}\nAssistant:"

    try:
        # Get Gemini response in Markdown
        response = model.generate_content(full_prompt)
        raw_markdown = response.text

        # ✅ Convert markdown to HTML for rendering
        html_response = markdown.markdown(raw_markdown)

        print("Markdown Output:\n", raw_markdown)
        return html_response
    except Exception as e:
        print("Error:", str(e))
        return "Sorry, something went wrong."

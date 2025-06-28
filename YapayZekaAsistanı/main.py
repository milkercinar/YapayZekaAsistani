#AIzaSyBIgMPMHpTcqLX7lA18Fs3zRHr9w0Q5pqs

from flask import Flask, render_template, request
import os
import contextlib

with open(os.devnull, 'w') as devnull, contextlib.redirect_stderr(devnull):
    import google.generativeai as genai


app = Flask(__name__)
app.secret_key = "your_secret_key_here"  


genai.configure(api_key = "AIzaSyBIgMPMHpTcqLX7lA18Fs3zRHr9w0Q5pqs")

generation_config = {

    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name = "gemini-2.0-flash",
    generation_config = generation_config
)

corporate_text = (

   """ At ParkEt, we are committed to delivering innovative, reliable, and sustainable solutions tailored to the evolving needs of our clients. Since our establishment in 2025, we have been serving a wide range of industries with a focus on quality, integrity, and long-term partnerships.

    With a dedicated team of professionals and a customer-centric approach, we offer end-to-end services that help our clients grow, adapt, and succeed in a rapidly changing world. Our mission is to create value through excellence in execution, continuous improvement, and cutting-edge technology.

    Vision
    To be a globally trusted brand known for driving meaningful change through innovation and responsible business practices.

    Mission
    To provide exceptional products and services that empower our clients, enrich communities, and protect the environment.

    Core Values

    Integrity and Transparency

    Innovation and Excellence

    Sustainability and Responsibility

    Customer Focus

    Teamwork and Collaboration"""
)

chat_session = model.start_chat(history=[])


conversation = [

    {"sender":"Mustafa İlker Çınar", "message": "Welcome To The ParkEt"}



]


@app.route("/", methods=["GET", "POST"])
def chat():
    global conversation
    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip()
        if user_input.lower() in ["exit", "quit"]:
            conversation.append({"sender": "Sistem", "message": "Sohbet sonlandırıldı."})
            return render_template("chat.html", conversation=conversation)
        
        conversation.append({"sender": "Müşteri", "message": user_input})
        
        combined_input = corporate_text + "\nSoru: " + user_input
        response = chat_session.send_message(combined_input)
        
        conversation.append({"sender": "Tuncay Lore", "message": response.text})
    
    return render_template("chat.html", conversation=conversation)

if __name__ == "__main__":
    app.run(debug=True)
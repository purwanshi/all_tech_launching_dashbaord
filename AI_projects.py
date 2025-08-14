import gradio as gr
from openai import OpenAI

def context_gemini_chat(api_key, prompt):
    try:
        gemini_llm_model = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        msg = [
            {"role": "system", "content": "You are an AI assistant"},
            {"role": "user", "content": prompt}
        ]
        response = gemini_llm_model.chat.completions.create(
            messages=msg, model="gemini-1.5-flash", stream=True
        )
        result = ""
        for chunk in response:
            if hasattr(chunk.choices[0].delta, "content"):
                result += chunk.choices[0].delta.content
        return result
    except Exception as e:
        return f"❌ Error: {e}"

def get_fashion_images(occasion, gender):
    from bs4 import BeautifulSoup
    import requests
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://www.google.com/search?tbm=isch&q={gender}+outfit+for+{occasion}".replace(" ", "+")
    soup = BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")
    return [img["src"] for img in soup.find_all("img") if "src" in img.attrs][1:7]

def get_fashion_tip(occasion, gender):
    tips = {
        "wedding": {"Male": "Sherwani or blazer with shoes", "Female": "Lehenga, saree or gown"},
        "party": {"Male": "Casual shirt + jeans", "Female": "Cocktail dress or jumpsuit"},
        "office": {"Male": "Shirt and trousers", "Female": "Formal blouse + skirt"},
        "casual": {"Male": "T-shirt and jeans", "Female": "Floral dress or top + denim"}
    }
    return tips.get(occasion.lower(), {}).get(gender, "Wear what feels comfy!")

def fashion_chatbot(img, occasion, gender):
    return get_fashion_tip(occasion, gender), get_fashion_images(occasion, gender)

def get_therapy_response(api_key, lover, hobbies, fav_food, indoor_outdoor, emotion, fav_flower):
    model = OpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
    prompt = f"""
    The user is a {lover} lover who enjoys {hobbies}, loves {fav_food}, prefers {indoor_outdoor} environments, feels {emotion}, and likes {fav_flower}.
    Suggest 5 cozy, uplifting tips based on their mood and personality.
    """
    messages = [
        {"role": "system", "content": "You are a warm, therapeutic AI offering cozy and scientifically-backed advice."},
        {"role": "user", "content": prompt}
    ]
    response = model.chat.completions.create(messages=messages, model="gemini-1.5-flash")
    return response.choices[0].message.content

def handle_first_click(api_key, lover, hobbies, fav_food, indoor_outdoor, emotion, fav_flower):
    result = get_therapy_response(api_key, lover, hobbies, fav_food, indoor_outdoor, emotion, fav_flower)
    return result, [api_key, lover, hobbies, fav_food, indoor_outdoor, emotion, fav_flower]

def handle_reload(inputs):
    if not inputs or len(inputs) != 7:
        return "Please submit preferences first.", inputs
    return get_therapy_response(*inputs), inputs

# =====================
# MAIN BLOCK STARTS
# =====================

with gr.Blocks() as demo:
    with gr.Accordion("🤖 AI Projects", open=False):
        gr.Markdown("## 🧠 Unified AI Projects")

        # Shared API key
        gemini_api_input = gr.Textbox(
            label="🔐 Enter your Gemini API Key once",
            type="password",
            placeholder="Paste your Gemini API key here"
        )

        # ------------------- Project 1 -------------------
        gr.Markdown("### 🧠 AI ChatGPT + Context Rememberance")
        context_prompt_input = gr.Textbox(label="🗣️ Your Message")
        context_output = gr.Textbox(label="🧠 Response")

        gr.Button("💬 Chat with Context").click(
            fn=context_gemini_chat,
            inputs=[gemini_api_input, context_prompt_input],
            outputs=context_output
        )

        # ------------------- Project 2 -------------------
        gr.Markdown("### 👗 Fashion Genie: Your Style Assistant")

        with gr.Tab("Get Suggestions"):
            with gr.Row():
                with gr.Column():
                    photo_input = gr.Image(label="Upload Photo", type="filepath")
                    occasion_input = gr.Textbox(label="Occasion (e.g., wedding, office)")
                    gender_input = gr.Radio(choices=["Male", "Female"], label="Gender", value="Female")
                    suggest_btn = gr.Button("🔮 Recommend")

                with gr.Column():
                    fashion_tip = gr.Textbox(label="🎀 Style Tip", lines=2)
                    gallery = gr.Gallery(label="🌂 Outfit Suggestions", columns=3)

            suggest_btn.click(
                fn=fashion_chatbot,
                inputs=[photo_input, occasion_input, gender_input],
                outputs=[fashion_tip, gallery]
            )

        with gr.Tab("About Fashion Genie"):
            gr.Markdown("""
            Fashion Genie gives style recommendations based on occasion and gender.  
            It scrapes Google Images for outfit examples and offers expert tips.  
            """)

        # ------------------- Project 3 -------------------
        gr.Markdown("### 🌸 Gemini Pocket Therapist")

        with gr.Row():
            lover = gr.Textbox(label="💖 Nature/Music/Pet lover?")
            hobbies = gr.Textbox(label="🎨 Hobbies?")
        with gr.Row():
            fav_food = gr.Textbox(label="🍜 Favorite Food?")
            indoor_outdoor = gr.Textbox(label="🏡 Indoor/Outdoor?")
        with gr.Row():
            emotion = gr.Textbox(label="💭 How are you feeling?")
            fav_flower = gr.Textbox(label="🌷 Favorite Flower or Plant?")

        output = gr.Textbox(label="🧠 Cozy Suggestions", lines=12)
        get_btn = gr.Button("✨ Get Suggestions")
        reload_btn = gr.Button("🔄 Reload")
        state_inputs = gr.State([])

        get_btn.click(
            fn=handle_first_click,
            inputs=[gemini_api_input, lover, hobbies, fav_food, indoor_outdoor, emotion, fav_flower],
            outputs=[output, state_inputs]
        )

        reload_btn.click(
            fn=handle_reload,
            inputs=[state_inputs],
            outputs=[output, state_inputs]
        )

# ============ LAUNCH ============

demo.launch()

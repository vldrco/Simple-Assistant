from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import openai

openai.api_key = "Insert your own API key"

@require_http_methods(["GET", "POST"])
def chatbot_view(request):
    conversation = request.session.get('conversation', [])
   
    if request.method == 'POST':
        user_input = request.POST.get('user_input')

        # Inserir o input do utilizador à conversa
        if user_input:
            conversation.append({"role": "user", "content": user_input})

        # Definir e chamar o modelo
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation,
            max_tokens=1000
        )

        # Extrair as respostas 
        chatbot_reply = response.choices[0].message.content

        # Inserir as respostas do chatbot à conversa
        conversation.append({"role": "assistant", "content": chatbot_reply})

        # Atualizar a conversa na sessão
        request.session['conversation'] = conversation

        return render(request, '_chat_conversations.html', {'user_input': user_input, 'chatbot_replies': [chatbot_reply], 'conversation': conversation[-2:]})
    else:
        request.session.clear()
        return render(request, '_chat.html', {'conversation': conversation})
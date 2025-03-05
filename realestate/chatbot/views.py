from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .chat_logic import get_chatbot_response

# View to RENDER THE CHAT HTML PAGE
def chat_interface(request):
    return render(request, 'chatbot/chatbot.html')  # Ensure this template exists

# View to HANDLE POST REQUESTS
@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        user_input = request.POST.get('message', '')
        response = get_chatbot_response(user_input)
        return JsonResponse({'reply': response})
    return JsonResponse({'reply': 'Send a POST request with your message.'})
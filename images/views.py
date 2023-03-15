from django.shortcuts import render
import openai, os, requests
from dotenv import load_dotenv
from django.core.files.base import ContentFile
from .models import *
load_dotenv()

api_ley = os.getenv("OPENAI_KEY", None)
openai.api_key = api_ley

def generate_image_from_txt(request):
    obj=None
    if api_ley is not None and request.method == 'POST':
        user_input = request.POST.get("user_input")
        if user_input:
            response = openai.Image.create(
                prompt=user_input,
                size="256x256"
            )
            img_url = response["data"][0]["url"]
            response = requests.get(img_url)
            print(response)
            img_file = ContentFile(response.content)

            count = Image.objects.count() + 1
            fname = f"image-{count}.jpg"

            obj = Image(phrase=user_input)
            obj.ai_image.save(fname,img_file)
            obj.save()
    return render(request, "main.html", {"object":obj})

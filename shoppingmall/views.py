import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from io import BytesIO
import base64
from django.shortcuts import render
from .models import ShoppingMall, Category
from bs4 import BeautifulSoup

def index(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'shoppingmall/index.html', context)

@csrf_exempt
def fetch_image(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            url = data.get('url')
            if not url:
                return JsonResponse({'error': 'URL not provided'}, status=400)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            # HTML 페이지에서 og:image 메타 태그를 통해 이미지 URL 추출
            soup = BeautifulSoup(response.content, 'html.parser')
            img_url = None
            og_image_tag = soup.find('meta', property='og:image')
            if og_image_tag and 'content' in og_image_tag.attrs:
                img_url = og_image_tag['content']
            
            if img_url:
                img_response = requests.get(img_url, headers=headers)
                img_response.raise_for_status()
                
                # 이미지 파일 유효성 검사
                try:
                    img = Image.open(BytesIO(img_response.content))
                    buffered = BytesIO()
                    img.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
                    return JsonResponse({'image': img_str})
                except Exception as e:
                    return JsonResponse({'error': 'Could not process image file'}, status=400)
            else:
                return JsonResponse({'error': 'No image found at URL'}, status=400)
        except (requests.RequestException, json.JSONDecodeError) as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

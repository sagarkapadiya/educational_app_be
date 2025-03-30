import json
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI, APIError, APIConnectionError, RateLimitError, AuthenticationError
from .models import QuestionAnswer
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class QAView(APIView):
    def post(self, request):
        question = request.data.get('question')
        if not question:
            return Response({'error': 'Question is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get API key from environment
        api_key = os.getenv('OPENAPI_KEY')
        if not api_key:
            return Response({'error': 'OpenAI API key not configured'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        client = OpenAI(api_key=api_key)
        
        try:
            # Make the API call
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful educational assistant. Provide clear and concise answers to questions. I want answer in pure markdown format."},
                    {"role": "user", "content": question}
                ]
            )

            # Get the assistant's response
            answer = response.choices[0].message.content

            # Store the question and answer in the database
            qa = QuestionAnswer.objects.create(
                question=question,
                answer=answer
            )

            return Response({'answer': answer}, status=status.HTTP_200_OK)
                
        except AuthenticationError as e:
            return Response({'error': 'Invalid OpenAI API key'}, status=status.HTTP_401_UNAUTHORIZED)
        except RateLimitError as e:
            return Response({'error': 'Rate limit exceeded. Please try again later.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        except APIConnectionError as e:
            return Response({'error': 'Network connection error. Please check your internet connection.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except APIError as e:
            return Response({'error': f'OpenAI API error: {str(e)}'}, status=status.HTTP_502_BAD_GATEWAY)
        except Exception as e:
            return Response({'error': f'An unexpected error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class QAListView(APIView):
    def get(self, request):
        qas = QuestionAnswer.objects.all().order_by('-created_at')
        data = [{'question': qa.question, 'answer': qa.answer} for qa in qas]
        return Response(data, status=status.HTTP_200_OK)
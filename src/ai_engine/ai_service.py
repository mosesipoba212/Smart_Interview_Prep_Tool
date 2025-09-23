"""
Universal AI Service
Supports multiple AI providers: OpenAI, Google Gemini, and fallback templates
"""

import os
import json
import random
from typing import List, Dict, Any, Optional
from datetime import datetime

# Try to import different AI services
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

class UniversalAIService:
    """Universal AI service that can use multiple providers"""
    
    def __init__(self):
        self.providers = []
        self.current_provider = None
        
        # Initialize available providers in order of preference
        self._init_gemini()
        self._init_openai()
        
        # Select the first available provider
        if self.providers:
            self.current_provider = self.providers[0]
            print(f"🤖 AI Service initialized with {self.current_provider['name']}")
        else:
            print("🤖 AI Service initialized with template fallback only")
    
    def _init_gemini(self):
        """Initialize Google Gemini"""
        if GEMINI_AVAILABLE:
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key and api_key != 'your_gemini_api_key_here':
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    self.providers.append({
                        'name': 'Google Gemini (Free)',
                        'type': 'gemini',
                        'client': model,
                        'max_tokens': 2048,
                        'cost': 'FREE'
                    })
                    print("✅ Google Gemini configured successfully")
                except Exception as e:
                    print(f"⚠️ Gemini initialization failed: {e}")
    
    def _init_openai(self):
        """Initialize OpenAI"""
        if OPENAI_AVAILABLE:
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key and api_key != 'your_openai_api_key_here':
                try:
                    client = OpenAI(api_key=api_key)
                    self.providers.append({
                        'name': 'OpenAI GPT',
                        'type': 'openai',
                        'client': client,
                        'model': 'gpt-3.5-turbo',
                        'max_tokens': 1500,
                        'cost': 'PAID'
                    })
                    print("✅ OpenAI configured successfully")
                except Exception as e:
                    print(f"⚠️ OpenAI initialization failed: {e}")
    
    def generate_text(self, prompt: str, max_tokens: int = 500) -> Optional[str]:
        """Generate text using the current AI provider"""
        if not self.current_provider:
            print("⚠️ No AI provider available, using template fallback")
            return None
        
        try:
            provider = self.current_provider
            
            if provider['type'] == 'gemini':
                return self._generate_with_gemini(prompt, max_tokens)
            elif provider['type'] == 'openai':
                return self._generate_with_openai(prompt, max_tokens)
            
        except Exception as e:
            print(f"⚠️ {provider['name']} failed: {e}")
            
            # Try the next provider
            if len(self.providers) > 1:
                print("🔄 Trying next AI provider...")
                self.providers.remove(provider)
                self.current_provider = self.providers[0] if self.providers else None
                return self.generate_text(prompt, max_tokens)
            
            print("🔄 All AI providers failed, using template fallback")
            return None
    
    def _generate_with_gemini(self, prompt: str, max_tokens: int) -> str:
        """Generate text using Google Gemini"""
        response = self.current_provider['client'].generate_content(prompt)
        return response.text.strip()
    
    def _generate_with_openai(self, prompt: str, max_tokens: int) -> str:
        """Generate text using OpenAI"""
        response = self.current_provider['client'].chat.completions.create(
            model=self.current_provider['model'],
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get information about the current provider"""
        if self.current_provider:
            return {
                'name': self.current_provider['name'],
                'type': self.current_provider['type'],
                'cost': self.current_provider['cost'],
                'available': True
            }
        return {
            'name': 'Template Fallback',
            'type': 'fallback',
            'cost': 'FREE',
            'available': True
        }
    
    def list_providers(self) -> List[Dict[str, Any]]:
        """List all available providers"""
        return [
            {
                'name': p['name'],
                'type': p['type'],
                'cost': p['cost']
            }
            for p in self.providers
        ]

# Global instance
ai_service = UniversalAIService()
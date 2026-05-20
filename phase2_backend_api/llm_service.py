"""
LLM Integration Service
Phase 2: Backend API Development
Handles integration with Large Language Models for recommendation generation
"""

import os
import logging
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
import json

logger = logging.getLogger(__name__)


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    async def generate_recommendations(
        self,
        restaurants: List[Dict[str, Any]],
        user_preferences: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate recommendations with explanations"""
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = None
        
        if self.api_key:
            try:
                import openai
                self.client = openai.AsyncOpenAI(api_key=self.api_key)
                logger.info("OpenAI client initialized successfully")
            except ImportError:
                logger.warning("OpenAI package not installed")
                self.client = None
        else:
            logger.warning("OpenAI API key not provided")
    
    async def generate_recommendations(
        self,
        restaurants: List[Dict[str, Any]],
        user_preferences: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate recommendations using OpenAI"""
        if not self.client:
            # Fallback to mock recommendations
            return self._generate_mock_recommendations(restaurants, user_preferences)
        
        try:
            from prompts import get_recommendation_prompt
            
            prompt = get_recommendation_prompt(restaurants, user_preferences)
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a restaurant recommendation expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            # Parse response
            content = response.choices[0].message.content
            return self._parse_llm_response(content, restaurants)
            
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            # Fallback to mock recommendations
            return self._generate_mock_recommendations(restaurants, user_preferences)
    
    def _parse_llm_response(self, content: str, restaurants: List[Dict]) -> List[Dict]:
        """Parse LLM response and attach explanations to restaurants"""
        try:
            # Try to parse as JSON first
            if content.strip().startswith('{'):
                parsed = json.loads(content)
                if isinstance(parsed, list):
                    return parsed
                elif isinstance(parsed, dict) and 'recommendations' in parsed:
                    return parsed['recommendations']
            
            # If not JSON, use simple text parsing
            # For now, return restaurants with generic explanations
            return self._generate_mock_recommendations(restaurants, {})
            
        except Exception as e:
            logger.error(f"Error parsing LLM response: {e}")
            return self._generate_mock_recommendations(restaurants, {})
    
    def _generate_mock_recommendations(
        self,
        restaurants: List[Dict],
        user_preferences: Dict
    ) -> List[Dict]:
        """Generate mock recommendations when LLM is unavailable"""
        recommendations = []
        
        for i, restaurant in enumerate(restaurants[:5]):
            explanation = self._generate_explanation(restaurant, user_preferences)
            rec = restaurant.copy()
            rec['explanation'] = explanation
            recommendations.append(rec)
        
        return recommendations
    
    def _generate_explanation(self, restaurant: Dict, preferences: Dict) -> str:
        """Generate a simple explanation for a restaurant"""
        name = restaurant.get('name', 'This restaurant')
        cuisines = restaurant.get('cuisines', 'various cuisines')
        rating = restaurant.get('rating', 0)
        cost = restaurant.get('cost', 0)
        
        explanation = f"{name} offers {cuisines} with a rating of {rating}/5. "
        
        if cost <= 300:
            explanation += "It's budget-friendly and "
        elif cost <= 700:
            explanation += "It's moderately priced and "
        else:
            explanation += "It's a premium dining option and "
        
        if rating >= 4.0:
            explanation += "highly rated by customers."
        elif rating >= 3.0:
            explanation += "has good customer reviews."
        else:
            explanation += "has mixed reviews."
        
        return explanation


class GroqProvider(LLMProvider):
    """Groq provider (uses OpenAI-compatible API)"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = model or os.getenv("GROQ_MODEL", "llama3-70b-8192")
        self.client = None
        
        logger.info(f"=== GROQ PROVIDER INITIALIZATION ===")
        logger.info(f"API Key present: {bool(self.api_key)}")
        logger.info(f"API Key prefix: {self.api_key[:10] if self.api_key else 'None'}...")
        logger.info(f"Model: {self.model}")
        
        if self.api_key:
            try:
                import openai
                self.client = openai.AsyncOpenAI(
                    api_key=self.api_key,
                    base_url="https://api.groq.com/openai/v1"
                )
                logger.info("✅ Groq client initialized successfully")
                logger.info(f"✅ Base URL: https://api.groq.com/openai/v1")
            except ImportError:
                logger.warning("❌ OpenAI package not installed (required for Groq)")
                self.client = None
        else:
            logger.warning("❌ Groq API key not provided - will use fallback mode")
    
    async def generate_recommendations(
        self,
        restaurants: List[Dict[str, Any]],
        user_preferences: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate recommendations using Groq"""
        logger.info(f"=== GROQ API CALL START ===")
        logger.info(f"Client available: {bool(self.client)}")
        logger.info(f"Number of restaurants: {len(restaurants)}")
        logger.info(f"Model: {self.model}")
        
        if not self.client:
            logger.warning("❌ Groq client not initialized - using FALLBACK to mock recommendations")
            # Fallback to mock recommendations
            return self._generate_mock_recommendations(restaurants, user_preferences)
        
        try:
            from prompts import get_recommendation_prompt
            
            prompt = get_recommendation_prompt(restaurants, user_preferences)
            logger.info(f"📤 Sending request to Groq API...")
            logger.info(f"📤 API Endpoint: https://api.groq.com/openai/v1/chat/completions")
            logger.info(f"📤 Model: {self.model}")
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a restaurant recommendation expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            logger.info(f"✅ Groq API call successful!")
            logger.info(f"✅ Response received from Groq")
            
            # Parse response
            content = response.choices[0].message.content
            logger.info(f"✅ Response content length: {len(content)} characters")
            return self._parse_llm_response(content, restaurants)
            
        except Exception as e:
            logger.error(f"❌ Error calling Groq API: {e}")
            logger.error(f"❌ Type of error: {type(e).__name__}")
            logger.warning("⚠️  Using FALLBACK to mock recommendations due to API error")
            # Fallback to mock recommendations
            return self._generate_mock_recommendations(restaurants, user_preferences)
    
    def _parse_llm_response(self, content: str, restaurants: List[Dict]) -> List[Dict]:
        """Parse LLM response and attach explanations to restaurants"""
        logger.info(f"📥 Parsing LLM response (length: {len(content)} chars)")
        logger.info(f"📥 Response preview: {content[:200]}...")
        
        try:
            # Try to parse as JSON first
            if content.strip().startswith('{'):
                parsed = json.loads(content)
                if isinstance(parsed, list):
                    logger.info(f"✅ Parsed response as list with {len(parsed)} items")
                    return parsed
                elif isinstance(parsed, dict) and 'recommendations' in parsed:
                    logger.info(f"✅ Parsed response as dict with {len(parsed['recommendations'])} recommendations")
                    return parsed['recommendations']
            
            # If not JSON, try to extract JSON from markdown code blocks
            import re
            json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                parsed = json.loads(json_str)
                if isinstance(parsed, list):
                    logger.info(f"✅ Extracted JSON from markdown, parsed as list with {len(parsed)} items")
                    return parsed
                elif isinstance(parsed, dict) and 'recommendations' in parsed:
                    logger.info(f"✅ Extracted JSON from markdown, parsed as dict with {len(parsed['recommendations'])} recommendations")
                    return parsed['recommendations']
            
            # If not JSON, use simple text parsing
            # For now, return restaurants with generic explanations
            logger.warning("⚠️  Could not parse LLM response as JSON, using fallback")
            return self._generate_mock_recommendations(restaurants, {})
            
        except Exception as e:
            logger.error(f"Error parsing LLM response: {e}")
            return self._generate_mock_recommendations(restaurants, {})
    
    def _generate_mock_recommendations(
        self,
        restaurants: List[Dict],
        user_preferences: Dict
    ) -> List[Dict]:
        """Generate mock recommendations when LLM is unavailable"""
        logger.warning(f"⚠️  GROQ PROVIDER: USING MOCK RECOMMENDATIONS (FALLBACK MODE)")
        logger.warning(f"⚠️  This means the Groq API is NOT being called successfully")
        logger.warning(f"⚠️  Number of restaurants: {len(restaurants)}")
        recommendations = []
        
        for i, restaurant in enumerate(restaurants[:5]):
            explanation = self._generate_explanation(restaurant, user_preferences)
            rec = restaurant.copy()
            rec['explanation'] = explanation
            recommendations.append(rec)
        
        logger.warning(f"⚠️  Generated {len(recommendations)} mock recommendations")
        return recommendations
    
    def _generate_explanation(self, restaurant: Dict, preferences: Dict) -> str:
        """Generate a simple explanation for a restaurant"""
        name = restaurant.get('name', 'This restaurant')
        cuisines = restaurant.get('cuisines', 'various cuisines')
        rating = restaurant.get('rating', 0)
        cost = restaurant.get('cost', 0)
        
        explanation = f"{name} offers {cuisines} with a rating of {rating}/5. "
        
        if cost <= 300:
            explanation += "It's budget-friendly and "
        elif cost <= 700:
            explanation += "It's moderately priced and "
        else:
            explanation += "It's a premium dining option and "
        
        if rating >= 4.0:
            explanation += "highly rated by customers."
        elif rating >= 3.0:
            explanation += "has good customer reviews."
        else:
            explanation += "has mixed reviews."
        
        return explanation


class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-sonnet-20240229"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        self.client = None
        
        if self.api_key:
            try:
                import anthropic
                self.client = anthropic.AsyncAnthropic(api_key=self.api_key)
                logger.info("Anthropic client initialized successfully")
            except ImportError:
                logger.warning("Anthropic package not installed")
                self.client = None
        else:
            logger.warning("Anthropic API key not provided")
    
    async def generate_recommendations(
        self,
        restaurants: List[Dict[str, Any]],
        user_preferences: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate recommendations using Anthropic"""
        if not self.client:
            # Fallback to mock recommendations
            openai_fallback = OpenAIProvider()
            return openai_fallback._generate_mock_recommendations(restaurants, user_preferences)
        
        try:
            from prompts import get_recommendation_prompt
            
            prompt = get_recommendation_prompt(restaurants, user_preferences)
            
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = response.content[0].text
            return self._parse_llm_response(content, restaurants)
            
        except Exception as e:
            logger.error(f"Error calling Anthropic API: {e}")
            openai_fallback = OpenAIProvider()
            return openai_fallback._generate_mock_recommendations(restaurants, user_preferences)
    
    def _parse_llm_response(self, content: str, restaurants: List[Dict]) -> List[Dict]:
        """Parse Anthropic response"""
        try:
            if content.strip().startswith('{'):
                parsed = json.loads(content)
                if isinstance(parsed, list):
                    return parsed
                elif isinstance(parsed, dict) and 'recommendations' in parsed:
                    return parsed['recommendations']
            
            # Fallback
            openai_fallback = OpenAIProvider()
            return openai_fallback._generate_mock_recommendations(restaurants, {})
            
        except Exception as e:
            logger.error(f"Error parsing Anthropic response: {e}")
            openai_fallback = OpenAIProvider()
            return openai_fallback._generate_mock_recommendations(restaurants, {})


class LLMService:
    """Main LLM service that manages different providers"""
    
    def __init__(self, provider: Optional[str] = None):
        self.provider_name = provider or os.getenv("LLM_PROVIDER", "openai")
        logger.info(f"=== LLM SERVICE INITIALIZATION ===")
        logger.info(f"Provider configured: {self.provider_name}")
        logger.info(f"LLM_PROVIDER env var: {os.getenv('LLM_PROVIDER', 'Not set')}")
        self.provider = self._initialize_provider()
    
    def _initialize_provider(self) -> LLMProvider:
        """Initialize the configured LLM provider"""
        provider_lower = self.provider_name.lower()
        logger.info(f"Initializing provider: {provider_lower}")
        
        if provider_lower == "anthropic":
            logger.info("Creating AnthropicProvider")
            return AnthropicProvider()
        elif provider_lower == "groq":
            logger.info("Creating GroqProvider")
            return GroqProvider()
        else:
            # Default to OpenAI
            logger.info(f"Provider '{provider_lower}' not recognized, defaulting to OpenAIProvider")
            return OpenAIProvider()
    
    async def generate_recommendations(
        self,
        restaurants: List[Dict[str, Any]],
        user_preferences: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate recommendations using the configured provider"""
        if not restaurants:
            return []
        
        try:
            return await self.provider.generate_recommendations(restaurants, user_preferences)
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            # Return restaurants with basic explanations
            openai_fallback = OpenAIProvider()
            return openai_fallback._generate_mock_recommendations(restaurants, user_preferences)

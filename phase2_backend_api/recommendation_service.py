"""
Recommendation Service
Phase 2: Backend API Development
Orchestrates data filtering and LLM-based recommendation generation
"""

import logging
from typing import List, Dict, Any
from models import RecommendationRequest, RecommendationResponse, Restaurant

logger = logging.getLogger(__name__)


class RecommendationService:
    """Service for generating restaurant recommendations"""
    
    def __init__(self, data_service=None):
        self.data_service = data_service
        self.llm_service = None
        
        # Import LLM service here to avoid circular imports
        try:
            from llm_service import LLMService
            self.llm_service = LLMService()
            logger.info("✅ LLM service initialized successfully")
        except Exception as e:
            logger.warning(f"❌ Could not initialize LLM service: {e}")
            logger.warning("❌ Will use basic recommendations (no LLM)")
    
    async def generate_recommendations(
        self,
        request: RecommendationRequest
    ) -> RecommendationResponse:
        """
        Generate restaurant recommendations based on user preferences
        
        Args:
            request: RecommendationRequest with user preferences
            
        Returns:
            RecommendationResponse with ranked restaurants and explanations
        """
        # Step 1: Filter restaurants based on criteria
        filtered_restaurants = self._filter_restaurants(request)
        
        if filtered_restaurants.empty:
            logger.warning("No restaurants found matching criteria")
            return RecommendationResponse(
                recommendations=[],
                total_found=0,
                query_summary=self._build_query_summary(request)
            )
        
        logger.info(f"Found {len(filtered_restaurants)} restaurants after filtering")
        
        # Step 2: Convert to list of dictionaries for LLM
        restaurants_list = filtered_restaurants.head(10).to_dict('records')
        
        # Step 3: Generate explanations using LLM
        user_preferences = {
            'location': request.location,
            'budget': request.budget,
            'cuisines': request.cuisines,
            'min_rating': request.min_rating,
            'additional_preferences': request.additional_preferences
        }
        
        try:
            if self.llm_service:
                logger.info(f"🤖 Calling LLM service for recommendations")
                logger.info(f"🤖 LLM service type: {type(self.llm_service.provider).__name__}")
                recommendations_with_explanations = await self.llm_service.generate_recommendations(
                    restaurants_list,
                    user_preferences
                )
                logger.info(f"✅ LLM recommendations generated successfully")
            else:
                logger.warning("❌ LLM service not available, using basic recommendations (FALLBACK)")
                recommendations_with_explanations = self._generate_basic_recommendations(
                    restaurants_list,
                    user_preferences
                )
        except Exception as e:
            logger.error(f"❌ Error generating LLM recommendations: {e}")
            logger.warning("⚠️  Using basic recommendations (FALLBACK) due to error")
            # Fallback to basic recommendations
            recommendations_with_explanations = self._generate_basic_recommendations(
                restaurants_list,
                user_preferences
            )
        
        # Step 4: Deduplicate recommendations based on restaurant name + location
        recommendations_with_explanations = self._deduplicate_recommendations(
            recommendations_with_explanations
        )
        
        # Step 5: Convert to Restaurant models
        restaurant_models = []
        for rec in recommendations_with_explanations[:5]:  # Return top 5
            restaurant_models.append(Restaurant(
                name=rec.get('name', ''),
                location=rec.get('location', ''),
                city=rec.get('city', ''),
                cuisines=rec.get('cuisines', ''),
                cost=rec.get('cost', 0.0),
                rating=rec.get('rating', 0.0),
                explanation=rec.get('explanation')
            ))
        
        # Step 5: Build response
        return RecommendationResponse(
            recommendations=restaurant_models,
            total_found=len(filtered_restaurants),
            query_summary=self._build_query_summary(request)
        )
    
    def _filter_restaurants(self, request: RecommendationRequest):
        """Filter restaurants using data service"""
        if not self.data_service:
            raise ValueError("Data service not available")
        
        return self.data_service.filter_restaurants(
            location=request.location,
            budget=request.budget,
            cuisines=request.cuisines,
            min_rating=request.min_rating
        )
    
    def _build_query_summary(self, request: RecommendationRequest) -> Dict[str, Any]:
        """Build a summary of the query for the response"""
        return {
            'location': request.location,
            'budget': request.budget,
            'cuisines': request.cuisines if request.cuisines else 'Any',
            'min_rating': request.min_rating,
            'additional_preferences': request.additional_preferences if request.additional_preferences else 'None'
        }
    
    def _generate_basic_recommendations(
        self,
        restaurants: List[Dict[str, Any]],
        preferences: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate basic recommendations without LLM (fallback)"""
        recommendations = []
        
        for restaurant in restaurants[:5]:
            explanation = self._generate_basic_explanation(restaurant, preferences)
            rec = restaurant.copy()
            rec['explanation'] = explanation
            recommendations.append(rec)
        
        return recommendations
    
    def _deduplicate_recommendations(
        self,
        recommendations: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Deduplicate recommendations based on restaurant name + location"""
        seen = set()
        deduplicated = []
        
        for rec in recommendations:
            name = rec.get('name', '').strip()
            location = rec.get('location', '').strip()
            
            # Create unique key based on name + location
            unique_key = (name.lower(), location.lower())
            
            if unique_key not in seen:
                seen.add(unique_key)
                deduplicated.append(rec)
            else:
                logger.info(f"Duplicate removed: {name} at {location}")
        
        if len(deduplicated) < len(recommendations):
            logger.info(f"Removed {len(recommendations) - len(deduplicated)} duplicate recommendations")
        
        return deduplicated
    
    def _generate_basic_explanation(
        self,
        restaurant: Dict[str, Any],
        preferences: Dict[str, Any]
    ) -> str:
        """Generate a basic explanation for a restaurant"""
        name = restaurant.get('name', 'This restaurant')
        cuisines = restaurant.get('cuisines', 'various cuisines')
        rating = restaurant.get('rating', 0)
        cost = restaurant.get('cost', 0)
        location = restaurant.get('city', restaurant.get('location', ''))
        
        explanation = f"{name} in {location} offers {cuisines}. "
        
        # Add rating context
        if rating >= 4.5:
            explanation += "It has an excellent rating of "
        elif rating >= 4.0:
            explanation += "It has a very good rating of "
        elif rating >= 3.5:
            explanation += "It has a good rating of "
        else:
            explanation += "It has a rating of "
        
        explanation += f"{rating}/5. "
        
        # Add cost context
        budget = preferences.get('budget', 0)
        if cost <= budget * 0.5:
            explanation += "The cost is well within your budget. "
        elif cost <= budget:
            explanation += "The cost fits your budget. "
        else:
            explanation += "Note: Cost may exceed your budget. "
        
        # Add cuisine context
        preferred_cuisines = preferences.get('cuisines', [])
        if preferred_cuisines:
            for cuisine in preferred_cuisines:
                if cuisine.lower() in cuisines.lower():
                    explanation += f"It serves your preferred {cuisine} cuisine. "
                    break
        
        # Add additional preferences context
        additional = preferences.get('additional_preferences', '')
        if additional:
            explanation += f"Based on your preference for '{additional}', this could be a good match."
        
        return explanation.strip()

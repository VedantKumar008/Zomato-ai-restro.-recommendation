"""
Prompt Templates for LLM
Phase 2: Backend API Development
Contains prompt templates for recommendation generation
"""

from typing import List, Dict, Any


def get_recommendation_prompt(
    restaurants: List[Dict[str, Any]],
    user_preferences: Dict[str, Any]
) -> str:
    """
    Generate a prompt for the LLM to create restaurant recommendations
    
    Args:
        restaurants: List of restaurant dictionaries
        user_preferences: Dictionary of user preferences
        
    Returns:
        Formatted prompt string
    """
    
    # Build restaurant context
    restaurant_context = ""
    for i, restaurant in enumerate(restaurants, 1):
        restaurant_context += f"""
{i}. Name: {restaurant.get('name', 'N/A')}
   Location: {restaurant.get('location', 'N/A')}
   City: {restaurant.get('city', 'N/A')}
   Cuisines: {restaurant.get('cuisines', 'N/A')}
   Cost for Two: ₹{restaurant.get('cost', 0):.0f}
   Rating: {restaurant.get('rating', 0)}/5
"""
    
    # Build user preferences context
    preferences_context = f"""
User Preferences:
- Location: {user_preferences.get('location', 'N/A')}
- Budget: ₹{user_preferences.get('budget', 0):.0f} (maximum cost for two)
- Cuisines: {', '.join(user_preferences.get('cuisines', ['Any']))}
- Minimum Rating: {user_preferences.get('min_rating', 0)}/5
- Additional Preferences: {user_preferences.get('additional_preferences', 'None')}
"""
    
    # Build the full prompt
    prompt = f"""You are a restaurant recommendation expert. Your task is to analyze a list of restaurants and provide personalized recommendations with explanations.

{preferences_context}

Available Restaurants:
{restaurant_context}

Instructions:
1. Analyze each restaurant based on how well it matches the user's preferences
2. Rank the restaurants from best to worst match
3. For the top 5 restaurants, provide a personalized explanation (2-3 sentences) explaining:
   - Why this restaurant is a good match for the user
   - What makes it special or noteworthy
   - Any relevant context based on their preferences
4. Consider factors like cuisine match, budget fit, rating quality, and additional preferences
5. Be specific and helpful in your explanations

IMPORTANT: You must respond ONLY with valid JSON. Do not include any other text, explanations, or markdown formatting. Your entire response must be a single JSON object.

Please provide your response in the following JSON format:
{{
  "recommendations": [
    {{
      "name": "Restaurant Name",
      "location": "Location",
      "city": "City",
      "cuisines": "Cuisines",
      "cost": 800.0,
      "rating": 4.2,
      "explanation": "Your personalized explanation here..."
    }}
  ]
}}

Only include the top 5 recommendations in your response. Remember: respond with ONLY the JSON object, nothing else."""
    
    return prompt


def get_few_shot_examples() -> str:
    """
    Get few-shot examples for the LLM to learn from
    
    Returns:
        String containing example prompts and responses
    """
    examples = """
Example 1:
User Preferences:
- Location: Bangalore
- Budget: ₹1000
- Cuisines: North Indian, Chinese
- Minimum Rating: 4.0
- Additional Preferences: family-friendly

Available Restaurants:
1. Name: Paradise Hotel
   Location: Bangalore, Indiranagar
   City: Bangalore
   Cuisines: North Indian, Biryani
   Cost for Two: ₹800
   Rating: 4.5/5

2. Name: Chinese Corner
   Location: Bangalore, Koramangala
   City: Bangalore
   Cuisines: Chinese, Thai
   Cost for Two: ₹600
   Rating: 4.2/5

Response:
{
  "recommendations": [
    {
      "name": "Paradise Hotel",
      "location": "Bangalore, Indiranagar",
      "city": "Bangalore",
      "cuisines": "North Indian, Biryani",
      "cost": 800.0,
      "rating": 4.5,
      "explanation": "Paradise Hotel is an excellent choice for your North Indian cuisine preference. With a high rating of 4.5/5 and cost well within your ₹1000 budget, it offers authentic biryani and North Indian dishes. The restaurant is known for its family-friendly atmosphere and generous portions, making it perfect for family dining."
    },
    {
      "name": "Chinese Corner",
      "location": "Bangalore, Koramangala",
      "city": "Bangalore",
      "cuisines": "Chinese, Thai",
      "cost": 600.0,
      "rating": 4.2,
      "explanation": "Chinese Corner perfectly matches your preference for Chinese cuisine. At ₹600 for two, it's very budget-friendly while maintaining a solid 4.2/5 rating. The restaurant offers a variety of Chinese and Thai dishes in a casual setting suitable for families."
    }
  ]
}

Example 2:
User Preferences:
- Location: Delhi
- Budget: ₹500
- Cuisines: Italian
- Minimum Rating: 3.5
- Additional Preferences: romantic ambiance

Available Restaurants:
1. Name: Italiano
   Location: Delhi, Connaught Place
   City: Delhi
   Cuisines: Italian, Continental
   Cost for Two: ₹1200
   Rating: 4.5/5

2. Name: Pizza Paradise
   Location: Delhi, Saket
   City: Delhi
   Cuisines: Italian, Pizza
   Cost for Two: ₹400
   Rating: 3.8/5

Response:
{
  "recommendations": [
    {
      "name": "Pizza Paradise",
      "location": "Delhi, Saket",
      "city": "Delhi",
      "cuisines": "Italian, Pizza",
      "cost": 400.0,
      "rating": 3.8,
      "explanation": "Pizza Paradise fits your budget perfectly at ₹400 for two and offers Italian cuisine as requested. While the rating of 3.8/5 is good rather than excellent, it provides value for money with authentic Italian pizzas. The casual atmosphere might not be ideal for a romantic setting, but the food quality makes it worth considering."
    }
  ]
}
"""
    return examples


def get_system_prompt() -> str:
    """
    Get the system prompt for the LLM
    
    Returns:
        System prompt string
    """
    return """You are a knowledgeable restaurant recommendation expert with deep understanding of Indian cuisine, dining preferences, and restaurant quality. Your goal is to provide personalized, helpful restaurant recommendations that match users' specific needs and preferences.

When making recommendations:
- Consider the user's budget constraints seriously
- Prioritize restaurants that match cuisine preferences
- Factor in rating quality and customer satisfaction
- Provide context about why each recommendation is a good fit
- Be honest about trade-offs (e.g., great food but higher price)
- Keep explanations concise but informative (2-3 sentences per recommendation)
- Rank restaurants from best to worst match

Your responses should always be in valid JSON format for easy parsing by the application."""

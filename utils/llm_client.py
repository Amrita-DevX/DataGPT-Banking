"""
LLM Client - Handles communication with Groq API
This file wraps the Groq API for easy use throughout the application
"""

from groq import Groq
import os

class LLMClient:
    """
    Wrapper class for Groq API
    Handles all communication with the LLM for SQL generation and insights
    """
    
    def __init__(self, api_key=None, model="llama-3.3-70b-versatile"):
        """
        Initialize LLM client
        
        Args:
            api_key: Groq API key (if None, reads from environment)
            model: Which Groq model to use
        """
        # Get API key from parameter or environment variable
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = model
        
        # Validate API key exists
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found. Set it as environment variable.")
        
        # Initialize Groq client
        self.client = Groq(api_key=self.api_key)
    
    def generate(self, prompt, temperature=0.1, max_tokens=1000):
        """
        Generate response from LLM
        
        Args:
            prompt: The prompt to send to LLM
            temperature: Controls randomness (0.0-1.0, lower = more consistent)
            max_tokens: Maximum length of response
            
        Returns:
            str: LLM response text
            
        Raises:
            Exception: If API call fails
        """
        try:
            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # Extract and return response text
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            # Re-raise with more context
            raise Exception(f"LLM API Error: {str(e)}")
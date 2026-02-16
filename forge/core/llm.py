"""DeepSeek API client with streaming support."""

import os
from typing import List, Dict, Any, Generator
from openai import OpenAI


class DeepSeekClient:
    """Client for interacting with DeepSeek API."""
    
    def __init__(self, api_key: str = None):
        """Initialize the DeepSeek client.
        
        Args:
            api_key: DeepSeek API key. If None, reads from DEEPSEEK_API_KEY env var.
        """
        self.api_key = api_key or os.getenv('DEEPSEEK_API_KEY')
        if not self.api_key:
            raise ValueError("DeepSeek API key must be provided or set in DEEPSEEK_API_KEY environment variable")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com/v1"
        )
    
    def stream_chat(self, 
                    messages: List[Dict[str, str]], 
                    model: str = "deepseek-chat",
                    temperature: float = 0.7,
                    max_tokens: int = 4096) -> Generator:
        """Stream a chat completion from DeepSeek.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model name to use (default: deepseek-chat)
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            
        Yields:
            Chunks from the streaming response
        """
        try:
            stream = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            return stream
        except Exception as e:
            raise Exception(f"DeepSeek API error: {e}")
    
    def chat(self, 
             messages: List[Dict[str, str]], 
             model: str = "deepseek-chat",
             temperature: float = 0.7,
             max_tokens: int = 4096) -> str:
        """Non-streaming chat completion.
        
        Args:
            messages: List of message dictionaries
            model: Model name to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            The model's response text
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"DeepSeek API error: {e}")

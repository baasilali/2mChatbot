import { OpenAIStream, StreamingTextResponse } from 'ai';
import OpenAI from 'openai';

// Create an OpenAI API client
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// IMPORTANT! Set the runtime to edge
export const runtime = 'edge';

export async function POST(req: Request) {
  console.log('🚀 API Route Hit!');
  console.log('Environment check:', {
    hasApiKey: !!process.env.OPENAI_API_KEY,
    apiKeyLength: process.env.OPENAI_API_KEY?.length
  });
  
  try {
    console.log('Received chat request');
    const { messages } = await req.json();
    console.log('Messages:', JSON.stringify(messages, null, 2));

    if (!process.env.OPENAI_API_KEY) {
      console.error('❌ No OpenAI API key found!');
      return new Response(JSON.stringify({ error: 'OpenAI API key not configured' }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // Create the completion with streaming
    const response = await openai.chat.completions.create({
      model: 'gpt-4o-mini',
      stream: true,
      messages: [
        {
          role: 'system',
          content: `You are a CS2 trading expert. You have access to pattern templates and market data.
          When analyzing patterns, consider:
          1. Pattern rarity and desirability
          2. Current market prices
          3. Historical price trends
          4. Pattern-specific overpay potential
          
          Always provide specific, actionable advice.`
        },
        ...messages
      ],
      temperature: 0.7,
      max_tokens: 1000,
    });

    console.log('OpenAI response received');

    // Convert the response to a readable stream
    const stream = OpenAIStream(response);

    // Return the streaming response
    return new StreamingTextResponse(stream);
    
  } catch (error: any) {
    console.error('❌ Error in chat API:', error);
    
    // Handle specific OpenAI API errors
    if (error.response?.status === 404) {
      return new Response(JSON.stringify({ 
        error: 'Model not found. Please check your OpenAI API access and model name.' 
      }), {
        status: 404,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    if (error.response?.status === 401) {
      return new Response(JSON.stringify({ 
        error: 'Invalid API key. Please check your OpenAI API key configuration.' 
      }), {
        status: 401,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    return new Response(JSON.stringify({ 
      error: error.message || 'Failed to process chat request' 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
} 
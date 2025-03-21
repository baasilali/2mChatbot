'use client';

import { useChat } from 'ai/react';
import MessageBubble from './MessageBubble';
import ChatInput from './ChatInput';

export default function ChatContainer() {
  const { messages, input, handleInputChange, handleSubmit, isLoading, error } = useChat({
    api: '/api/chat',
    onResponse: (response) => {
      console.log('🚀 API Response:', response);
    },
    onFinish: (message) => {
      console.log('✅ Chat finished:', message);
    },
    onError: (error) => {
      console.error('❌ Chat error:', error);
    },
  });

  const handleError = (error: Error) => {
    console.error('Error in chat:', error);
    // You can add additional error handling here
  };

  console.log('📝 Current messages:', messages);
  console.log('🔍 Current input:', input);
  console.log('⌛ Loading state:', isLoading);
  if (error) console.error('❌ Error state:', error);

  return (
    <div className="flex flex-col h-[calc(100vh-64px)] bg-gray-50">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
            <strong className="font-bold">Error: </strong>
            <span className="block sm:inline">
              {error.message.includes('API key') 
                ? 'Please check your OpenAI API key configuration.'
                : error.message.includes('Model not found')
                ? 'The AI model is currently unavailable. Please try again later.'
                : 'An error occurred while processing your request. Please try again.'}
            </span>
          </div>
        )}
        {messages.map((message) => (
          <MessageBubble
            key={message.id}
            content={message.content}
            isUser={message.role === 'user'}
            timestamp={message.createdAt?.toISOString()}
          />
        ))}
      </div>
      <ChatInput 
        onSend={(message) => handleSubmit(new Event('submit') as any)}
        isLoading={isLoading}
        value={input}
        onChange={handleInputChange}
      />
    </div>
  );
} 
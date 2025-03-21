'use client';

interface MessageBubbleProps {
  content: string;
  isUser: boolean;
  timestamp?: string;
}

export default function MessageBubble({ content, isUser, timestamp }: MessageBubbleProps) {
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div
        className={`max-w-[80%] rounded-lg p-4 ${
          isUser
            ? 'bg-blue-600 text-white rounded-br-none'
            : 'bg-white text-gray-900 rounded-bl-none shadow-sm border border-gray-200'
        }`}
      >
        <p className="whitespace-pre-wrap">{content}</p>
        {timestamp && (
          <span className="text-xs mt-1 block opacity-70">
            {new Date(timestamp).toISOString()}
          </span>
        )}
      </div>
    </div>
  );
} 
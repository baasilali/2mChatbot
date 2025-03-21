declare module 'ai' {
  export interface Message {
    id: string;
    content: string;
    role: 'user' | 'assistant' | 'system';
    createdAt?: Date;
  }

  export interface ChatRequest {
    messages: Message[];
  }

  export interface ChatResponse {
    id: string;
    choices: Array<{
      message: Message;
      finish_reason: string;
    }>;
  }

  export function OpenAIStream(response: any): ReadableStream;
  export class StreamingTextResponse extends Response {
    constructor(stream: ReadableStream);
  }
} 
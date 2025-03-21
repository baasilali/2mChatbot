import Header from '@/components/layout/Header';
import ChatContainer from '@/components/chat/ChatContainer';

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="container mx-auto bg-white shadow-sm">
        <ChatContainer />
      </main>
    </div>
  );
}

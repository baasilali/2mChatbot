'use client';

import Link from 'next/link';

export default function Header() {
  return (
    <header className="bg-gray-900 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link href="/" className="text-xl font-bold">
          CS2 Trading Assistant
        </Link>
        <nav className="space-x-4">
          <Link href="/patterns" className="hover:text-gray-300">
            Patterns
          </Link>
          <Link href="/trades" className="hover:text-gray-300">
            Trades
          </Link>
          <Link href="/market" className="hover:text-gray-300">
            Market
          </Link>
        </nav>
      </div>
    </header>
  );
} 
import React, { useState, useRef, useEffect } from 'react';
import { Bot, Send, User } from 'lucide-react';
import { Chat } from '../types';
import ChatMessage from './ChatMessage';
import EmptyState from './EmptyState';

interface ChatWindowProps {
  chat: Chat | null;
  onSendMessage: (message: string) => void;
  onNewChat: () => void;
}

const ChatWindow: React.FC<ChatWindowProps> = ({ chat, onSendMessage, onNewChat }) => {
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const messagesContainerRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when messages change
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [chat?.messages]);

  // Focus input when chat changes
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, [chat]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim()) {
      onSendMessage(inputValue);
      setInputValue('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  // Auto-resize textarea
  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const target = e.target;
    setInputValue(target.value);
    
    // Reset height to auto to get the correct scrollHeight
    target.style.height = 'auto';
    
    // Set the height to the scrollHeight + border
    const maxHeight = 150; // Max height in pixels
    target.style.height = `${Math.min(target.scrollHeight, maxHeight)}px`;
  };

  return (
    <div className="flex flex-col h-full bg-black">
      {/* Message area */}
      <div 
        ref={messagesContainerRef}
        className="flex-1 overflow-y-auto p-4 md:p-6"
      >
        {!chat || chat.messages.length === 0 ? (
          <EmptyState onNewChat={onNewChat} />
        ) : (
          <div className="max-w-3xl mx-auto space-y-6">
            {chat.messages.map((message, i) => (
              <ChatMessage 
                key={message.id} 
                message={message} 
                isLastMessage={i === chat.messages.length - 1} 
              />
            ))}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input area */}
      <div className="border-t border-gray-800 p-4 pb-6">
        <form onSubmit={handleSubmit} className="max-w-3xl mx-auto">
          <div className="relative">
            <textarea
              ref={inputRef}
              value={inputValue}
              onChange={handleInput}
              onKeyDown={handleKeyDown}
              placeholder="Send a message..."
              className="w-full bg-gray-900 border border-gray-700 focus:border-gray-500 rounded-lg py-3 pl-4 pr-12 resize-none overflow-auto text-white max-h-[150px]"
              style={{ minHeight: '56px' }}
              rows={1}
            />
            <button
              type="submit"
              disabled={!inputValue.trim()}
              className={`absolute right-3 bottom-[13px] rounded-md p-1 ${
                inputValue.trim() 
                  ? 'text-white hover:bg-gray-700' 
                  : 'text-gray-500 cursor-not-allowed'
              }`}
            >
              <Send size={20} />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ChatWindow;
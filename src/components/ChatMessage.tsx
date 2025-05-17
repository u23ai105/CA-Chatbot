import React from 'react';
import { Bot, User } from 'lucide-react';
import { Message } from '../types';
import Loader from './Loader';

interface ChatMessageProps {
  message: Message;
  isLastMessage: boolean;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message, isLastMessage }) => {
  const isAssistant = message.role === 'assistant';
  const isThinking = isAssistant && message.content === '' && isLastMessage;

  return (
    <div 
      className={`flex items-start animate-fadeIn ${
        isAssistant ? 'bg-gray-900 py-6' : 'py-6'
      }`}
    >
      <div className="max-w-3xl w-full mx-auto flex gap-4">
        <div className={`flex-shrink-0 h-8 w-8 rounded-full flex items-center justify-center ${
          isAssistant ? 'bg-purple-600' : 'bg-blue-600'
        }`}>
          {isAssistant ? <Bot size={16} /> : <User size={16} />}
        </div>
        
        <div className="flex-1 min-w-0">
          <div className="font-medium mb-1">
            {isAssistant ? 'Assistant' : 'You'}
          </div>
          
          {isThinking ? (
            <Loader />
          ) : (
            <div className="whitespace-pre-wrap">
              {message.content || 'No content'}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;
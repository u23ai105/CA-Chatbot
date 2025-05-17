import React from 'react';
import { Bot, PlusCircle } from 'lucide-react';

interface EmptyStateProps {
  onNewChat: () => void;
}

const EmptyState: React.FC<EmptyStateProps> = ({ onNewChat }) => {
  const exampleQuestions = [
    "What is the difference between artificial intelligence and machine learning?",
    "Can you explain quantum computing in simple terms?",
    "What are some effective strategies for improving team collaboration?",
    "How can I optimize my website for better performance?"
  ];

  return (
    <div className="flex flex-col items-center justify-center h-full max-w-2xl mx-auto text-center px-4">
      <div className="mb-8">
        <div className="h-20 w-20 rounded-full bg-gradient-to-r from-purple-600 to-blue-600 flex items-center justify-center mx-auto mb-6">
          <Bot size={40} />
        </div>
        <h1 className="text-2xl font-bold mb-2">Welcome to CA Chatbot</h1>
        <p className="text-gray-400 mb-8">
          Your AI assistant for insightful conversations and helpful answers
        </p>
      </div>

      <div className="w-full max-w-md mb-8">
        <h2 className="text-lg font-medium mb-4">Try asking something like:</h2>
        <div className="grid gap-3">
          {exampleQuestions.map((question, index) => (
            <button
              key={index}
              onClick={() => onNewChat()}
              className="text-left p-3 rounded-lg border border-gray-700 hover:bg-white hover:bg-opacity-5 transition-colors text-sm"
            >
              {question}
            </button>
          ))}
        </div>
      </div>

      <button
        onClick={onNewChat}
        className="flex items-center gap-2 bg-white bg-opacity-10 hover:bg-opacity-20 text-white py-3 px-6 rounded-lg transition-all duration-300 border border-gray-700"
      >
        <PlusCircle size={18} />
        <span>Start a new chat</span>
      </button>
    </div>
  );
};

export default EmptyState;
import React from 'react';
import { Chat } from '../types';
import { PlusCircle, MessageSquare, Trash2 } from 'lucide-react';

interface SidebarProps {
  chats: Chat[];
  currentChatId: string | null;
  onNewChat: () => void;
  onSelectChat: (chatId: string) => void;
  onDeleteChat: (chatId: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({
  chats,
  currentChatId,
  onNewChat,
  onSelectChat,
  onDeleteChat
}) => {
  // Format timestamp to readable date
  const formatDate = (timestamp: number) => {
    const date = new Date(timestamp);
    return date.toLocaleDateString();
  };

  return (
    <div className="flex flex-col h-full overflow-hidden">
      {/* New Chat Button */}
      <div className="p-4">
        <button
          onClick={onNewChat}
          className="w-full flex items-center justify-center gap-2 bg-white bg-opacity-10 hover:bg-opacity-20 text-white py-3 px-4 rounded-lg transition-all duration-300 border border-gray-700"
        >
          <PlusCircle size={18} />
          <span>New Chat</span>
        </button>
      </div>

      {/* Chat History */}
      <div className="flex-1 overflow-y-auto px-2 pb-4">
        <h2 className="text-gray-400 text-xs font-semibold uppercase tracking-wider px-3 py-2">
          Chat History
        </h2>
        
        {chats.length === 0 ? (
          <div className="text-gray-500 text-sm px-3 py-2">
            No previous chats
          </div>
        ) : (
          <ul className="space-y-1">
            {chats.map((chat) => (
              <li key={chat.id}>
                <div
                  className={`flex items-center justify-between px-3 py-2 rounded-lg cursor-pointer group ${
                    chat.id === currentChatId
                      ? 'bg-white bg-opacity-10'
                      : 'hover:bg-white hover:bg-opacity-5'
                  }`}
                  onClick={() => onSelectChat(chat.id)}
                >
                  <div className="flex items-center flex-1 min-w-0">
                    <MessageSquare size={16} className="flex-shrink-0 mr-2 text-gray-400" />
                    <div className="truncate">
                      <div className="truncate text-sm font-medium">
                        {chat.title || 'New Chat'}
                      </div>
                      <div className="text-xs text-gray-500">
                        {formatDate(chat.timestamp)}
                      </div>
                    </div>
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onDeleteChat(chat.id);
                    }}
                    className="p-1 rounded-full opacity-0 group-hover:opacity-100 hover:bg-gray-700 transition-opacity"
                    aria-label="Delete chat"
                  >
                    <Trash2 size={16} className="text-gray-400" />
                  </button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* Footer */}
      <div className="p-4 text-xs text-gray-500 border-t border-gray-800">
        <div>CA Chatbot &copy; {new Date().getFullYear()}</div>
      </div>
    </div>
  );
};

export default Sidebar;
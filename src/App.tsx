import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import ChatWindow from './components/ChatWindow';
import { Chat, Message } from './types';
import { v4 as uuidv4 } from 'uuid';

function App() {
  const [chats, setChats] = useState<Chat[]>([]);
  const [currentChatId, setCurrentChatId] = useState<string | null>(null);
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);

  useEffect(() => {
    const savedChats = localStorage.getItem('chats');
    if (savedChats) {
      const parsedChats = JSON.parse(savedChats);
      setChats(parsedChats);
      
      if (parsedChats.length > 0 && !currentChatId) {
        setCurrentChatId(parsedChats[0].id);
      }
    }
  }, []);

  useEffect(() => {
    localStorage.setItem('chats', JSON.stringify(chats));
  }, [chats]);

  const createNewChat = () => {
    const newChatId = uuidv4();
    const newChat: Chat = {
      id: newChatId,
      title: 'New Chat',
      messages: [],
      timestamp: Date.now()
    };
    setChats([newChat, ...chats]);
    setCurrentChatId(newChatId);
    setIsMobileSidebarOpen(false);
  };

  const getCurrentChat = () => {
    return chats.find(chat => chat.id === currentChatId) || null;
  };

  const updateChatTitle = (chatId: string, message: string) => {
    setChats(prevChats => 
      prevChats.map(chat => 
        chat.id === chatId 
          ? { 
              ...chat, 
              title: message.length > 30 
                ? `${message.substring(0, 30)}...` 
                : message 
            } 
          : chat
      )
    );
  };

  const addMessage = async (content: string) => {
    if (!content.trim() || !currentChatId) return;

    const userMessage: Message = {
      id: uuidv4(),
      role: 'user',
      content,
      timestamp: Date.now()
    };

    setChats(prevChats => 
      prevChats.map(chat => 
        chat.id === currentChatId 
          ? { 
              ...chat, 
              messages: [...chat.messages, userMessage],
              timestamp: Date.now()
            } 
          : chat
      )
    );

    const currentChat = chats.find(chat => chat.id === currentChatId);
    if (currentChat && currentChat.messages.length === 0) {
      updateChatTitle(currentChatId, content);
    }

    const tempBotMessageId = uuidv4();
    setChats(prevChats => 
      prevChats.map(chat => 
        chat.id === currentChatId 
          ? { 
              ...chat, 
              messages: [
                ...chat.messages,
                { 
                  id: tempBotMessageId, 
                  role: 'assistant', 
                  content: '', 
                  timestamp: Date.now() 
                }
              ],
            } 
          : chat
      )
    );

    try {
      const response = await fetch('http://localhost:3000/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: content })
      });
      
      if (!response.ok) {
        throw new Error('Failed to get response from server');
      }
      
      const data = await response.json();
      
      setChats(prevChats => 
        prevChats.map(chat => 
          chat.id === currentChatId 
            ? { 
                ...chat, 
                messages: chat.messages.map(msg => 
                  msg.id === tempBotMessageId 
                    ? { ...msg, content: data.answer } 
                    : msg
                ) 
              } 
            : chat
        )
      );
    } catch (error) {
      console.error('Error getting response:', error);
      
      setChats(prevChats => 
        prevChats.map(chat => 
          chat.id === currentChatId 
            ? { 
                ...chat, 
                messages: chat.messages.map(msg => 
                  msg.id === tempBotMessageId 
                    ? { ...msg, content: 'Sorry, there was an error processing your request.' } 
                    : msg
                ) 
              } 
            : chat
        )
      );
    }
  };

  const selectChat = (chatId: string) => {
    setCurrentChatId(chatId);
    setIsMobileSidebarOpen(false);
  };

  const deleteChat = (chatId: string) => {
    setChats(prevChats => prevChats.filter(chat => chat.id !== chatId));
    
    if (chatId === currentChatId) {
      const remainingChats = chats.filter(chat => chat.id !== chatId);
      setCurrentChatId(remainingChats.length > 0 ? remainingChats[0].id : null);
    }
  };

  const toggleMobileSidebar = () => {
    setIsMobileSidebarOpen(!isMobileSidebarOpen);
  };

  return (
    <div className="flex h-screen bg-black text-white overflow-hidden">
      <button 
        className="md:hidden fixed top-4 left-4 z-50 text-white p-2"
        onClick={toggleMobileSidebar}
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
      </button>

      <div 
        className={`w-72 flex-shrink-0 bg-black border-r border-gray-800 md:relative fixed inset-y-0 left-0 z-40 transform transition-transform duration-300 ease-in-out md:translate-x-0 ${
          isMobileSidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <Sidebar 
          chats={chats} 
          currentChatId={currentChatId} 
          onNewChat={createNewChat} 
          onSelectChat={selectChat} 
          onDeleteChat={deleteChat} 
        />
      </div>

      <div 
        className={`md:hidden fixed inset-0 bg-black bg-opacity-50 z-30 transition-opacity duration-300 ${
          isMobileSidebarOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'
        }`}
        onClick={() => setIsMobileSidebarOpen(false)}
      ></div>

      <div className="flex-1 flex flex-col overflow-hidden">
        <ChatWindow 
          chat={getCurrentChat()} 
          onSendMessage={addMessage} 
          onNewChat={createNewChat}
        />
      </div>
    </div>
  );
}

export default App;
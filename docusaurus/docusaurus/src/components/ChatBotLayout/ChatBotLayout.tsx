import React, { useState } from 'react';
import ChatBot from '../ChatBot';
import './ChatBotLayout.css';

const ChatBotLayout = ({ children }) => {
  const [isChatOpen, setIsChatOpen] = useState(false);

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  return (
    <div className="chatbot-layout">
      <div className="content">
        {children}
      </div>
      <div className={`chatbot-panel ${isChatOpen ? 'open' : 'closed'}`}>
        <div className="chatbot-header-bar">
          <h3>AI Assistant</h3>
          <button className="toggle-button" onClick={toggleChat}>
            {isChatOpen ? '−' : '+'}
          </button>
        </div>
        {isChatOpen && (
          <div className="chatbot-content">
            <ChatBot />
          </div>
        )}
      </div>
      {!isChatOpen && (
        <button className="chatbot-toggle-float" onClick={toggleChat}>
          💬 AI Assistant
        </button>
      )}
    </div>
  );
};

export default ChatBotLayout;
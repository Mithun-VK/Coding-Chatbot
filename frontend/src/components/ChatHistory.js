import React, { useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus, vs } from 'react-syntax-highlighter/dist/esm/styles/prism';

function ChatHistory({ messages, loading }) {
  const messagesEndRef = useRef(null);
  const theme = document.body.className === 'dark' ? vscDarkPlus : vs;

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const renderMessage = (message) => {
    const isUser = message.role === 'user';
    
    return (
      <motion.div
        key={message.id}
        className={`message ${isUser ? 'user-message' : 'assistant-message'} ${message.type}`}
        initial={{ opacity: 0, y: 20, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        exit={{ opacity: 0, scale: 0.95 }}
        transition={{ duration: 0.3 }}
      >
        <div className="message-avatar">
          {isUser ? (
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="8" r="4" stroke="currentColor" strokeWidth="2"/>
              <path d="M6 21v-2a4 4 0 014-4h4a4 4 0 014 4v2" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
            </svg>
          ) : (
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          )}
        </div>

        <div className="message-content">
          {message.type === 'code' ? (
            <div className="inline-code-block">
              <SyntaxHighlighter
                language={message.language || 'javascript'}
                style={theme}
                customStyle={{
                  margin: 0,
                  padding: '1rem',
                  borderRadius: '8px',
                  fontSize: '0.85rem'
                }}
              >
                {message.content}
              </SyntaxHighlighter>
            </div>
          ) : (
            <div className="message-text">
              {message.content}
            </div>
          )}
        </div>
      </motion.div>
    );
  };

  return (
    <div className="chat-history">
      <AnimatePresence>
        {messages.length === 0 && !loading && (
          <motion.div
            className="empty-state"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
          >
            <div className="empty-icon">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" stroke="url(#gradient)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <defs>
                  <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#6366f1" />
                    <stop offset="100%" stopColor="#a855f7" />
                  </linearGradient>
                </defs>
              </svg>
            </div>
            <h2>Start Creating Amazing Code</h2>
            <p>Choose a mode and describe what you want to build</p>
          </motion.div>
        )}

        {messages.map(renderMessage)}
      </AnimatePresence>

      {loading && (
        <motion.div
          className="message assistant-message typing"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="message-avatar">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </div>
          <div className="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </motion.div>
      )}

      <div ref={messagesEndRef} />
    </div>
  );
}

export default ChatHistory;

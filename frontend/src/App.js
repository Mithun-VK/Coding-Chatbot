import React, { useState, useEffect } from 'react';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { motion, AnimatePresence } from 'framer-motion';
import Header from './components/Header';
import ChatBox from './components/ChatBox';
import CodeDisplay from './components/CodeDisplay';
import ChatHistory from './components/ChatHistory';
import FeatureButtons from './components/FeatureButtons';
import LoadingAnimation from './components/LoadingAnimation';
import './styles/App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [currentCode, setCurrentCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [activeMode, setActiveMode] = useState('generate'); // generate, chat, explain, improve
  const [chatHistory, setChatHistory] = useState([]);
  const [selectedLanguage, setSelectedLanguage] = useState('auto');
  const [theme, setTheme] = useState('dark');

  // Load saved state from localStorage
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    const savedMessages = JSON.parse(localStorage.getItem('messages') || '[]');
    const savedLanguage = localStorage.getItem('language') || 'auto';
    
    setTheme(savedTheme);
    setMessages(savedMessages);
    setSelectedLanguage(savedLanguage);
    document.body.className = savedTheme;
  }, []);

  // Save state to localStorage
  useEffect(() => {
    localStorage.setItem('messages', JSON.stringify(messages));
    localStorage.setItem('theme', theme);
    localStorage.setItem('language', selectedLanguage);
  }, [messages, theme, selectedLanguage]);

  const addMessage = (message) => {
    setMessages(prev => [...prev, { ...message, id: Date.now() }]);
  };

  const clearChat = () => {
    setMessages([]);
    setCurrentCode('');
    setChatHistory([]);
    localStorage.removeItem('messages');
  };

  const toggleTheme = () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
    document.body.className = newTheme;
  };

  return (
    <div className={`app ${theme}`}>
      <div className="animated-background">
        <div className="gradient-orb orb-1"></div>
        <div className="gradient-orb orb-2"></div>
        <div className="gradient-orb orb-3"></div>
      </div>

      <Header 
        theme={theme} 
        toggleTheme={toggleTheme}
        clearChat={clearChat}
        messageCount={messages.length}
      />

      <ToastContainer
        position="top-right"
        autoClose={3000}
        hideProgressBar={false}
        newestOnTop={true}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme={theme}
      />

      <div className="app-container">
        <motion.div 
          className="main-content"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <FeatureButtons 
            activeMode={activeMode}
            setActiveMode={setActiveMode}
            selectedLanguage={selectedLanguage}
            setSelectedLanguage={setSelectedLanguage}
          />

          <div className="chat-section">
            <ChatHistory 
              messages={messages}
              loading={loading}
            />

            <ChatBox
              addMessage={addMessage}
              setCurrentCode={setCurrentCode}
              loading={loading}
              setLoading={setLoading}
              activeMode={activeMode}
              chatHistory={chatHistory}
              setChatHistory={setChatHistory}
              selectedLanguage={selectedLanguage}
            />
          </div>

          <AnimatePresence>
            {(currentCode || loading) && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.3 }}
              >
                <CodeDisplay
                  code={currentCode}
                  loading={loading}
                  language={selectedLanguage}
                />
              </motion.div>
            )}
          </AnimatePresence>

          {loading && <LoadingAnimation />}
        </motion.div>
      </div>
    </div>
  );
}

export default App;

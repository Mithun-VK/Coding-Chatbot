import React from 'react';
import { motion } from 'framer-motion';

function FeatureButtons({ activeMode, setActiveMode, selectedLanguage, setSelectedLanguage }) {
  const modes = [
    { id: 'generate', label: 'Generate', icon: '⚡', description: 'Create new code' },
    { id: 'chat', label: 'Chat', icon: '💬', description: 'Ask questions' },
    { id: 'explain', label: 'Explain', icon: '📖', description: 'Understand code' },
    { id: 'improve', label: 'Improve', icon: '✨', description: 'Optimize code' }
  ];

  const languages = [
    'auto', 'javascript', 'python', 'java', 'cpp', 'typescript', 'go', 'rust', 'php', 'ruby'
  ];

  return (
    <div className="feature-section">
      <div className="mode-selector">
        {modes.map((mode) => (
          <motion.button
            key={mode.id}
            className={`mode-btn ${activeMode === mode.id ? 'active' : ''}`}
            onClick={() => setActiveMode(mode.id)}
            whileHover={{ scale: 1.05, y: -2 }}
            whileTap={{ scale: 0.95 }}
          >
            <span className="mode-icon">{mode.icon}</span>
            <div className="mode-info">
              <span className="mode-label">{mode.label}</span>
              <span className="mode-description">{mode.description}</span>
            </div>
          </motion.button>
        ))}
      </div>

      <div className="language-selector">
        <label htmlFor="language">Language:</label>
        <select
          id="language"
          value={selectedLanguage}
          onChange={(e) => setSelectedLanguage(e.target.value)}
          className="language-select"
        >
          {languages.map((lang) => (
            <option key={lang} value={lang}>
              {lang === 'auto' ? 'Auto Detect' : lang.charAt(0).toUpperCase() + lang.slice(1)}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}

export default FeatureButtons;

import React from 'react';
import { motion } from 'framer-motion';

function LoadingAnimation() {
  return (
    <motion.div
      className="loading-overlay"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <div className="loading-content">
        <div className="loading-spinner">
          <motion.div
            className="spinner-ring"
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
          />
        </div>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          Generating your code...
        </motion.p>
      </div>
    </motion.div>
  );
}

export default LoadingAnimation;

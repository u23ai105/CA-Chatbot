import React from 'react';

const Loader: React.FC = () => {
  return (
    <div className="flex items-center space-x-2">
      <span className="text-gray-300">Thinking</span>
      <div className="flex space-x-1">
        <div className="animate-pulse h-1.5 w-1.5 bg-gray-300 rounded-full delay-0"></div>
        <div className="animate-pulse h-1.5 w-1.5 bg-gray-300 rounded-full delay-300"></div>
        <div className="animate-pulse h-1.5 w-1.5 bg-gray-300 rounded-full delay-600"></div>
      </div>
    </div>
  );
};

export default Loader;
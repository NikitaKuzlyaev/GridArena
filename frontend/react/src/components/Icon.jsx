import React from 'react';
import heartIcon from '../assets/icons/heart.svg';
import heartFillIcon from '../assets/icons/heart-fill.svg';

const Icon = ({ name, className = '', style = {}, ...props }) => {
  const getIconSrc = (iconName) => {
    switch (iconName) {
      case 'heart':
        return heartIcon;
      case 'heart-fill':
        return heartFillIcon;
      default:
        return null;
    }
  };

  const iconSrc = getIconSrc(name);
  
  if (!iconSrc) {
    console.warn(`Icon "${name}" not found`);
    return null;
  }

  return (
    <img 
      src={iconSrc} 
      alt={name}
      className={className}
      style={{ 
        width: '16px', 
        height: '16px', 
        verticalAlign: 'middle',
        ...style 
      }}
      {...props}
    />
  );
};

export default Icon; 
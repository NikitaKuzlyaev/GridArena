import React from 'react';

function ErrorBlock({ code, message }) {
  return (
    <div style={{ textAlign: 'center', marginTop: '40px', color: 'red' }}>
      <h2>Ошибка {code}</h2>
      <p>{message}</p>
    </div>
  );
}

export default ErrorBlock;

import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';

function Home() {
  const [markdown, setMarkdown] = useState('');

  useEffect(() => {
    fetch('/main.md')
      .then((res) => res.text())
      .then(setMarkdown);
  }, []);

  return (
    <div className="markdown-body" style={{ maxWidth: 700, margin: '32px auto', padding: 24, background: '#fff', borderRadius: 8, textAlign: 'left' }}>
      <ReactMarkdown>{markdown}</ReactMarkdown>
    </div>
  );
}

export default Home; 
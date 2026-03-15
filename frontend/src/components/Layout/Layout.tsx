import React from 'react';
import Header from './Header';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div style={{ minHeight: '100vh' }}>
      <Header />
      <main
        className="fade-in"
        style={{
          maxWidth: 1400,
          margin: '0 auto',
          padding: 24,
        }}
      >
        {children}
      </main>
    </div>
  );
};

export default Layout;

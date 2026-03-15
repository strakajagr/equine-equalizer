import React from 'react';
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate
} from 'react-router-dom';
import Layout from './components/Layout/Layout';
import TodayPage from './pages/TodayPage';
import ValuePlaysPage from './pages/ValuePlaysPage';
import HistoryPage from './pages/HistoryPage';

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Navigate to="/today" />} />
          <Route path="/today" element={<TodayPage />} />
          <Route path="/value" element={<ValuePlaysPage />} />
          <Route path="/history" element={<HistoryPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;

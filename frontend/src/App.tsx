import React from 'react';
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate
} from 'react-router-dom';
import Layout from './components/Layout/Layout';
import TodayPage from './pages/TodayPage';
import GonzoPage from './pages/GonzoPage';
import ValuePlaysPage from './pages/ValuePlaysPage';
import LongshotPage from './pages/LongshotPage';
import HistoryPage from './pages/HistoryPage';
import DashboardPage from './pages/DashboardPage';
import BetBuilderPage from './pages/BetBuilderPage';
import PerformancePage from './pages/PerformancePage';
import ComparePage from './pages/ComparePage';

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Navigate to="/today" />} />
          <Route path="/today" element={<TodayPage />} />
          <Route path="/gonzo" element={<GonzoPage />} />
          <Route path="/compare" element={<ComparePage />} />
          <Route path="/builder" element={<BetBuilderPage />} />
          <Route path="/value" element={<ValuePlaysPage />} />
          <Route path="/longshots" element={<LongshotPage />} />
          <Route path="/performance" element={<PerformancePage />} />
          <Route path="/history" element={<HistoryPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;

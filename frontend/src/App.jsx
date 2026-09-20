import React, { useState } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import BottomNav from './components/BottomNav';
import MoreNavSheet from './components/MoreNavSheet';
import InstallPwaBanner from './components/InstallPwaBanner';
import OfflineBanner from './components/OfflineBanner';
import DisclaimerFooter from './components/DisclaimerFooter';

import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import RiskMonitoringPage from './pages/RiskMonitoringPage';
import LocationDetailsPage from './pages/LocationDetailsPage';
import WaterQualityPage from './pages/WaterQualityPage';
import RainfallPage from './pages/RainfallPage';
import HealthTrendsPage from './pages/HealthTrendsPage';
import LocationsPage from './pages/LocationsPage';
import AlertsPage from './pages/AlertsPage';
import DataExplorerPage from './pages/DataExplorerPage';
import ModelStatusPage from './pages/ModelStatusPage';
import DataQualityPage from './pages/DataQualityPage';
import SystemInfoPage from './pages/SystemInfoPage';

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(true);
  const [userRole, setUserRole] = useState('HEALTH_OFFICIAL');
  const [dataType, setDataType] = useState('REAL_PUBLIC_SOURCE');
  const [activeTab, setActiveTab] = useState('dashboard');
  const [selectedDistrict, setSelectedDistrict] = useState(null);
  const [isMoreSheetOpen, setIsMoreSheetOpen] = useState(false);

  const handleSelectLocation = (district) => {
    setSelectedDistrict(district);
    setActiveTab('location_details');
  };

  if (!isAuthenticated) {
    return <LoginPage onLogin={(role) => { setUserRole(role); setIsAuthenticated(true); }} />;
  }

  const renderTabContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <DashboardPage dataType={dataType} onSelectLocation={handleSelectLocation} />;
      case 'risk_monitoring':
        return <RiskMonitoringPage dataType={dataType} onSelectLocation={handleSelectLocation} />;
      case 'location_details':
        return (
          <LocationDetailsPage
            districtName={selectedDistrict || 'Ntr'}
            dataType={dataType}
            onBack={() => setActiveTab('risk_monitoring')}
          />
        );
      case 'water_quality':
        return <WaterQualityPage dataType={dataType} />;
      case 'rainfall':
        return <RainfallPage dataType={dataType} />;
      case 'health_trends':
        return <HealthTrendsPage dataType={dataType} />;
      case 'locations':
        return <LocationsPage dataType={dataType} onSelectLocation={handleSelectLocation} />;
      case 'alerts':
        return <AlertsPage dataType={dataType} onSelectLocation={handleSelectLocation} />;
      case 'data_explorer':
        return <DataExplorerPage dataType={dataType} />;
      case 'model_status':
        return <ModelStatusPage />;
      case 'data_quality':
        return <DataQualityPage />;
      case 'system_info':
        return <SystemInfoPage />;
      default:
        return <DashboardPage dataType={dataType} onSelectLocation={handleSelectLocation} />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col justify-between font-sans antialiased text-slate-900">
      <div>
        {/* PWA Install & Offline Banners */}
        <InstallPwaBanner />
        <OfflineBanner />

        {/* Top Header */}
        <Header
          dataType={dataType}
          setDataType={setDataType}
          userRole={userRole}
          setUserRole={setUserRole}
        />
        
        <div className="flex">
          {/* Desktop Sidebar (>1024px) */}
          <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
          
          {/* Main Content View (with mobile bottom padding for bottom nav) */}
          <main className="flex-1 p-3 sm:p-6 max-w-7xl mx-auto overflow-x-hidden pb-20 lg:pb-6">
            {renderTabContent()}
          </main>
        </div>
      </div>

      {/* Mobile Bottom Navigation Bar (≤1024px) */}
      <BottomNav
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onOpenMore={() => setIsMoreSheetOpen(true)}
      />

      {/* Mobile Slide-Up Menu Sheet */}
      <MoreNavSheet
        isOpen={isMoreSheetOpen}
        onClose={() => setIsMoreSheetOpen(false)}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
      />

      <DisclaimerFooter />
    </div>
  );
}

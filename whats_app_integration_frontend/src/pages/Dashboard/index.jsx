import React from 'react';
import Navbar from '../../components/common/Navbar';
import PageHeader from '../../components/common/PageHeader';
import Notifications from '../../components/common/Notifications';
import UserProfile from '../../components/common/UserProfile';
import Footer from '../../components/common/Footer';
import QuickAction from '../../components/common/QuickAction';
import QuickStat from './QuickStat';
import RecentActivity from './RecentActivity';
import WelcomeSection from './WelcomeSection';

function Dashboard({ token, onLogout }) {
  return (
    <div className="d-flex bg-light">
      <Navbar />
      <div className="flex-grow-1 p-4">
        <PageHeader title="Dashboard" onLogout={onLogout} />
        <Notifications />
        <WelcomeSection name="John Doe" />
        <div className="row mb-4">
          <div className="col-md-3">
            <QuickStat title="Messages Sent" value="1,234" />
          </div>
          <div className="col-md-3">
            <QuickStat title="Active Chats" value="45" />
          </div>
          <div className="col-md-3">
            <QuickStat title="Pending Tickets" value="12" />
          </div>
          <div className="col-md-3">
            <QuickStat title="New Users" value="8" />
          </div>
        </div>
        <RecentActivity />
        <div className="row mb-4">
          <QuickAction title="Send a Message" />
          <QuickAction title="View Chats" type="secondary" />
          <QuickAction title="Create a Ticket" type="outline-primary" />
        </div>
        <UserProfile />
        <Footer />
      </div>
    </div>
  );
}

export default Dashboard;
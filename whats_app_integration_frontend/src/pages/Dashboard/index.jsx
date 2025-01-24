import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Navbar from '../../components/common/Navbar';
import PageHeader from '../../components/common/PageHeader';
import Notifications from '../../components/common/Notifications';
import UserProfile from '../../components/common/UserProfile';
import Footer from '../../components/common/Footer';
import QuickAction from '../../components/common/QuickAction';
import QuickStat from './QuickStat';
import RecentActivity from './RecentActivity';
import WelcomeSection from './WelcomeSection';
import { useAuth } from '../../services/AuthContext'; // Import the context hook

function Dashboard() {
  const { token, handleLogout } = useAuth(); // Get token and handleLogout from context
  const [stats, setStats] = useState(null); // Null for no data
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isReady, setIsReady] = useState(false); // New state to track if the component is ready

  useEffect(() => {
    const initialize = async () => {
      await new Promise((resolve) => setTimeout(resolve, 100)); // Optional delay
      setIsReady(true);
    };

    initialize();
  }, []);

  useEffect(() => {
    if (!isReady || !token) return;

    const fetchStats = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_API_BASE_URL}users/stats`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        // Check if the response has data; otherwise, set an empty state
        if (response.data.messages_sent === 0 && response.data.threads_created === 0) {
          setError('No data available at the moment.');
        } else {
          setStats({
            messagesSent: response.data.messages_sent,
            threadsCreated: response.data.threads_created,
          });
        }
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch stats. Please try again later.');
        setLoading(false);
        console.error('Error fetching stats:', err);
      }
    };

    fetchStats();
  }, [isReady, token]);

  return (
    <div className="d-flex bg-light">
      <Navbar />
      <div className="flex-grow-1 p-4">
        <PageHeader title="Dashboard" onLogout={handleLogout} />
        <Notifications />
        <WelcomeSection name="John Doe" />

        {loading ? (
          <div>Loading stats...</div>
        ) : error ? (
          <div className="alert alert-danger">{error}</div>
        ) : stats ? (
          <>
            <div className="row mb-4">
              <div className="col-md-3">
                <QuickStat title="Messages Sent" value={stats.messagesSent} />
              </div>
              <div className="col-md-3">
                <QuickStat title="Number of conversations created" value={stats.threadsCreated} />
              </div>
              <div className="col-md-3">
                <QuickStat title="Pending Tickets" value="Feature will be implemented soon" />
              </div>
              <div className="col-md-3">
                <QuickStat title="New Users" value="Feature will be implemented soon" />
              </div>
            </div>
            <RecentActivity />
            <div className="row mb-4">
              <QuickAction title="Send a Message" />
              <QuickAction title="View Chats" type="secondary" />
              <QuickAction title="Create a Ticket" type="outline-primary" />
            </div>
          </>
        ) : (
          <div className="alert alert-warning">
            Unable to display stats. Please try again later.
          </div>
        )}

        <UserProfile />
        <Footer />
      </div>
    </div>
  );
}

export default Dashboard;

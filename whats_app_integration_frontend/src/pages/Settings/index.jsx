import Navbar from '../../components/common/Navbar';
import PageHeader from '../../components/common/PageHeader';
import Footer from '../../components/common/Footer';

function Settings() {
  return (
    <div className='d-flex bg-light'>
      <Navbar />
      <div className="flex-grow-1 p-4">
        <PageHeader title="Settings" />
        <h1>Settings will be implemented soon!</h1>
        <Footer />
      </div>
    </div>
  );
}

export default Settings;
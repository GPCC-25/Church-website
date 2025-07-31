import { Outlet, NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';


export default function UserLayout() {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout =() => {
    logout();
    navigate("/login");
  }

  return (
    <div className="flex">
      <aside className="w-64 bg-gray-800 text-white p-4">
        <nav className="space-y-2">
          <NavLink to="/dashboard">Dashboard</NavLink>
          <NavLink to="/announcements">Announcements</NavLink>
          <NavLink to="/events">Events</NavLink>
          <NavLink to="/feedbackandsuggestions">FeedbackAndSuggestions</NavLink>
          <NavLink to="/mediacenter">MediaCenter</NavLink>
          <NavLink to="/onboarding">Onboarding</NavLink>
          <NavLink to="/prayerandtestimonies">PrayerAndTestimonies</NavLink>
          <NavLink to="/profile">Profile</NavLink>
          <NavLink to="/tithesandcollections">TithesAndCollections</NavLink>
        </nav>
        <button
          onClick={handleLogout}
          className="mt-6 px-4 py-2 bg-red-600 text-white rounded">
            Logout
        </button>
      </aside>
      <main className="flex-1 p-6">
        <Outlet />
      </main>
    </div>
  );
}

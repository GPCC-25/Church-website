import { Outlet, NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

export default function AdminLayout() {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  }
  return (
    <div className="flex">
      <aside className="w-64 bg-gray-900 text-white p-4">
        <nav className="space-y-2">
          <NavLink to="/admin/dashboard">Admin Dashboard</NavLink>
          <button 
            onClick={handleLogout}
            className="mt-6 px-4 py-2 bg-red-600 text-white rounded"
          >
            Logout
          </button>

        </nav>
      </aside>
      <main className="flex-1 p-6">
        <Outlet />
      </main>
    </div>
  );
}

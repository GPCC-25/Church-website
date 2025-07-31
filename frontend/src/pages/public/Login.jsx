
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [role, setRole] = useState('member');

  const handleLogin = () => {
    const mockUser = {
      name: 'Shadrack',
      role: role // 'admin' or 'member'
    };

    login(mockUser);

    if (role === 'admin') {
      navigate('/admin/dashboard');
    } else {
      navigate('/dashboard');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-20 p-6 bg-white shadow rounded">
      <h1 className="text-2xl font-bold mb-4">Login</h1>

      <label className="block mb-2">Login as:</label>
      <select
        value={role}
        onChange={(e) => setRole(e.target.value)}
        className="mb-4 p-2 border rounded w-full"
      >
        <option value="member">Member</option>
        <option value="admin">Admin</option>
      </select>

      <button
        onClick={handleLogin}
        className="bg-blue-600 text-white px-4 py-2 rounded w-full"
      >
        Simulate Login
      </button>
    </div>
  );
}


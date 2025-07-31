/*import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext"; 

export default function ProtectedRoute({ children }){
  const { user } = useAuth();

  if(!user){
    return <Navigate to="/login" replace />;
  }

  return children;
}*/

import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function ProtectedRoute({ children }) {
  const { user } = useAuth();
  const location = useLocation();

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  // Protect admin routes
  if (location.pathname.startsWith('/admin') && user.role !== 'admin') {
    return <Navigate to="/dashboard" replace />;
  }

  // Protect member routes
  if (!location.pathname.startsWith('/admin') && user.role !== 'member') {
    return <Navigate to="/admin/dashboard" replace />;
  }

  return children;
}

import { BrowserRouter, Routes, Route} from 'react-router-dom';

import Home from './pages/public/Home';
import Login from './pages/public/Login';
import SignUp from './pages/public/SignUp';

import Dashboard from './pages/user/Dashboard';
import Profile from './pages/user/Profile';
import TithesAndCollections from './pages/user/TithesAndCollections';
import Events from './pages/user/Events';
import PrayerAndTestimonies from './pages/user/PrayerAndTestimonies';
import Announcements from './pages/user/Announcements';
import MediaCenter from './pages/user/MediaCenter';
import Attendance from './pages/user/Attendance';
import Onboarding from './pages/user/Onboarding';
import FeedbackAndSuggestions from './pages/user/FeedbackAndSuggestions';

import AdminDashboard from './pages/Admin/AdminDashboard';

import UserLayout from './layouts/UserLayout';
import AdminLayout from './layouts/AdminLayout';

import ProtectedRoute from './routes/ProtectedRoute';
import PublicOnlyRoute from './routes/PublicOnlyRoute';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route
          path="/" 
          element=
          {
            <PublicOnlyRoute>
              <Home />
            </PublicOnlyRoute>
          }
        />
        <Route
          path="/login" 
          element=
          {
            <PublicOnlyRoute>
              <Login />
            </PublicOnlyRoute>
          }
        />
        <Route
          path="signup" 
          element=
          {
            <PublicOnlyRoute>
              <SignUp />
            </PublicOnlyRoute>
          }
        />

        {/* User Routes */}
        <Route element={<UserLayout />}>
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <Profile />
              </ProtectedRoute>
            }
          />
          <Route
            path="/tithesandcollections"
            element={
              <ProtectedRoute>
                <TithesAndCollections />
              </ProtectedRoute>
            }
          />
          <Route
            path="/events"
            element={
              <ProtectedRoute>
                <Events />
              </ProtectedRoute>
            }
          />
          <Route
            path="/prayerandtestimonies"
            element={
              <ProtectedRoute>
                <PrayerAndTestimonies />
              </ProtectedRoute>
            }
          />
          <Route
            path="/announcements"
            element={
              <ProtectedRoute>
                <Announcements />
              </ProtectedRoute>
            }
          />
          <Route
            path="/mediacenter"
            element={
              <ProtectedRoute>
                <MediaCenter />
              </ProtectedRoute>
            }
          />
          <Route
            path="/attendance"
            element={
              <ProtectedRoute>
                <Attendance />
              </ProtectedRoute>
            }
          />
          <Route
            path="/onboarding"
            element={
              <ProtectedRoute>
                <Onboarding />
              </ProtectedRoute>
            }
          />
          <Route
            path="/feedbackandsuggestions"
            element={
              <ProtectedRoute>
                <FeedbackAndSuggestions />
              </ProtectedRoute>
            }
          />
        </Route>

        {/* Admin Routes */}
        <Route element={<AdminLayout />}>
          <Route
            path="/admin/dashboard"
            element={
              <ProtectedRoute>
                <AdminDashboard />
              </ProtectedRoute>
            }
          />
        </Route>

      </Routes>
    </BrowserRouter>
  );
}

export default App;

import { useState, useEffect } from 'react';
import { Calendar, Clock, MapPin, Users, Plus, Heart, User } from 'lucide-react';

export default function Events() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [showVolunteerModal, setShowVolunteerModal] = useState(false);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [selectedRole, setSelectedRole] = useState('');

  // Using environment variable for API base URL
  const API_BASE = import.meta.env.VITE_PUBLIC_API_URL;

  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE}/events/`);
      if (response.ok) {
        const data = await response.json();
        setEvents(data);
      }
    } catch (error) {
      console.error('Error fetching events:', error);
    } finally {
      setLoading(false);
    }
  };

  const registerForEvent = async (eventId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE}/events/${eventId}/register`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        alert('Successfully registered for the event!');
        fetchEvents(); // Refresh events to update registration status
      } else {
        const error = await response.json();
        alert(error.detail || 'Failed to register for event');
      }
    } catch (error) {
      console.error('Error registering for event:', error);
      alert('Failed to register for event');
    }
  };

  const volunteerForEvent = async () => {
    if (!selectedEvent || !selectedRole) return;

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE}/events/${selectedEvent.id}/volunteer?role=${selectedRole}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        alert('Successfully signed up to volunteer!');
        setShowVolunteerModal(false);
        setSelectedEvent(null);
        setSelectedRole('');
        fetchEvents();
      } else {
        const error = await response.json();
        alert(error.detail || 'Failed to sign up as volunteer');
      }
    } catch (error) {
      console.error('Error volunteering for event:', error);
      alert('Failed to sign up as volunteer');
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const formatTime = (dateString) => {
    return new Date(dateString).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const filteredEvents = events.filter(event => {
    if (filter === 'all') return true;
    if (filter === 'services') return event.event_type === 'service';
    if (filter === 'special') return event.event_type !== 'service';
    return true;
  });

  const openVolunteerModal = (event) => {
    setSelectedEvent(event);
    setShowVolunteerModal(true);
  };

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto p-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/3 mb-6"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="h-64 bg-gray-200 rounded-lg"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Church Events</h1>
        <p className="text-gray-600">
          Join us for worship, fellowship, and community events
        </p>
      </div>

      {/* Filter Tabs */}
      <div className="flex space-x-1 mb-8 bg-gray-100 p-1 rounded-lg">
        <button
          onClick={() => setFilter('all')}
          className={`flex-1 py-2 px-4 rounded-md font-medium transition-colors ${
            filter === 'all'
              ? 'bg-white text-blue-600 shadow-sm'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          All Events
        </button>
        <button
          onClick={() => setFilter('services')}
          className={`flex-1 py-2 px-4 rounded-md font-medium transition-colors ${
            filter === 'services'
              ? 'bg-white text-blue-600 shadow-sm'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          Services
        </button>
        <button
          onClick={() => setFilter('special')}
          className={`flex-1 py-2 px-4 rounded-md font-medium transition-colors ${
            filter === 'special'
              ? 'bg-white text-blue-600 shadow-sm'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          Special Events
        </button>
      </div>

      {/* Events Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredEvents.length === 0 ? (
          <div className="col-span-full text-center py-12">
            <Calendar className="w-16 h-16 mx-auto mb-4 text-gray-300" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">No Events Found</h3>
            <p className="text-gray-500">
              {filter === 'all' 
                ? 'No events are currently scheduled.' 
                : `No ${filter} events are currently scheduled.`
              }
            </p>
          </div>
        ) : (
          filteredEvents.map((event) => (
            <div key={event.id} className="bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow">
              <div className="p-6">
                {/* Event Header */}
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900 mb-1">{event.title}</h3>
                    <span className={`inline-block px-2 py-1 text-xs font-medium rounded-full ${
                      event.event_type === 'service' 
                        ? 'bg-blue-100 text-blue-800' 
                        : 'bg-green-100 text-green-800'
                    }`}>
                      {event.event_type}
                    </span>
                  </div>
                </div>

                {/* Event Description */}
                <p className="text-gray-600 text-sm mb-4 line-clamp-3">{event.description}</p>

                {/* Event Details */}
                <div className="space-y-2 mb-4">
                  <div className="flex items-center text-sm text-gray-500">
                    <Calendar className="w-4 h-4 mr-2" />
                    {formatDate(event.start_time)}
                  </div>
                  <div className="flex items-center text-sm text-gray-500">
                    <Clock className="w-4 h-4 mr-2" />
                    {formatTime(event.start_time)} - {formatTime(event.end_time)}
                  </div>
                  <div className="flex items-center text-sm text-gray-500">
                    <MapPin className="w-4 h-4 mr-2" />
                    {event.location}
                  </div>
                </div>

                {/* Registration Info */}
                {event.registration_required && (
                  <div className="mb-4 p-3 bg-blue-50 rounded-lg">
                    <div className="flex items-center text-sm text-blue-800">
                      <Users className="w-4 h-4 mr-2" />
                      Registration Required
                    </div>
                    {event.max_attendees && (
                      <p className="text-xs text-blue-600 mt-1">
                        Limited to {event.max_attendees} attendees
                      </p>
                    )}
                  </div>
                )}

                {/* Volunteer Info */}
                {event.volunteers_needed && (
                  <div className="mb-4 p-3 bg-green-50 rounded-lg">
                    <div className="flex items-center text-sm text-green-800">
                      <Heart className="w-4 h-4 mr-2" />
                      Volunteers Needed
                    </div>
                    <p className="text-xs text-green-600 mt-1">
                      Roles: {event.volunteer_roles.join(', ')}
                    </p>
                  </div>
                )}

                {/* Action Buttons */}
                <div className="flex space-x-2">
                  {event.registration_required && (
                    <button
                      onClick={() => registerForEvent(event.id)}
                      className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
                    >
                      Register
                    </button>
                  )}
                  {event.volunteers_needed && (
                    <button
                      onClick={() => openVolunteerModal(event)}
                      className="flex-1 bg-green-600 text-white py-2 px-4 rounded-lg hover:bg-green-700 transition-colors text-sm font-medium"
                    >
                      Volunteer
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Volunteer Modal */}
      {showVolunteerModal && selectedEvent && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-xl font-semibold mb-4">Volunteer for {selectedEvent.title}</h3>
            <p className="text-gray-600 mb-4">
              Choose a volunteer role for this event:
            </p>
            
            <div className="space-y-3 mb-6">
              {selectedEvent.volunteer_roles.map((role) => (
                <label key={role} className="flex items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
                  <input
                    type="radio"
                    name="volunteerRole"
                    value={role}
                    checked={selectedRole === role}
                    onChange={(e) => setSelectedRole(e.target.value)}
                    className="mr-3"
                  />
                  <span className="text-sm font-medium text-gray-700 capitalize">{role}</span>
                </label>
              ))}
            </div>

            <div className="flex space-x-3">
              <button
                onClick={volunteerForEvent}
                disabled={!selectedRole}
                className="flex-1 bg-green-600 text-white py-2 px-4 rounded-lg hover:bg-green-700 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
              >
                Sign Up
              </button>
              <button
                onClick={() => {
                  setShowVolunteerModal(false);
                  setSelectedEvent(null);
                  setSelectedRole('');
                }}
                className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-400 transition-colors"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

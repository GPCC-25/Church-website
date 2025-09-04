import { useState, useEffect } from 'react';
import { Calendar, Clock, MapPin, Phone, Mail, Users, Heart, ArrowRight, Play } from 'lucide-react';

export default function Home() {
  const [upcomingEvents, setUpcomingEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  // TODO: Replace with your church's API base URL
  const API_BASE = 'http://localhost:8000'; // Update this to your backend URL

  useEffect(() => {
    fetchUpcomingEvents();
  }, []);

  const fetchUpcomingEvents = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE}/events/`);
      if (response.ok) {
        const data = await response.json();
        // Get next 3 upcoming events
        setUpcomingEvents(data.slice(0, 3));
      }
    } catch (error) {
      console.error('Error fetching events:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric'
    });
  };

  const formatTime = (dateString) => {
    return new Date(dateString).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-blue-900 to-blue-700 text-white">
        <div className="max-w-7xl mx-auto px-6 py-20">
          <div className="text-center">
            {/* TODO: Replace with your church's name */}
            <h1 className="text-5xl font-bold mb-6">Welcome to Grace Community Church</h1>
            <p className="text-xl mb-8 max-w-3xl mx-auto">
              Join us in worship, fellowship, and growing together in faith. 
              We're a community dedicated to serving God and loving our neighbors.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a 
                href="/login" 
                className="bg-white text-blue-900 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors flex items-center justify-center gap-2"
              >
                Join Our Community
                <ArrowRight className="w-4 h-4" />
              </a>
              <a 
                href="#services" 
                className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-blue-900 transition-colors"
              >
                Learn More
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* Service Times Section */}
      <div id="services" className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Service Times</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Join us for worship and fellowship. All are welcome!
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center p-6 bg-blue-50 rounded-lg">
              <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <Calendar className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Sunday Morning</h3>
              <p className="text-gray-600 mb-2">9:00 AM - 10:30 AM</p>
              <p className="text-sm text-gray-500">Main Sanctuary</p>
            </div>

            <div className="text-center p-6 bg-green-50 rounded-lg">
              <div className="w-16 h-16 bg-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <Users className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Sunday Evening</h3>
              <p className="text-gray-600 mb-2">6:00 PM - 7:30 PM</p>
              <p className="text-sm text-gray-500">Fellowship Hall</p>
            </div>

            <div className="text-center p-6 bg-purple-50 rounded-lg">
              <div className="w-16 h-16 bg-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <Heart className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Wednesday Prayer</h3>
              <p className="text-gray-600 mb-2">7:00 PM - 8:00 PM</p>
              <p className="text-sm text-gray-500">Prayer Room</p>
            </div>
          </div>
        </div>
      </div>

      {/* Upcoming Events Section */}
      <div className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Upcoming Events</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Join us for special services, community events, and fellowship opportunities.
            </p>
          </div>

          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {[...Array(3)].map((_, i) => (
                <div key={i} className="bg-white rounded-lg p-6 shadow-sm animate-pulse">
                  <div className="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
                  <div className="h-3 bg-gray-200 rounded w-full mb-2"></div>
                  <div className="h-3 bg-gray-200 rounded w-2/3"></div>
                </div>
              ))}
            </div>
          ) : upcomingEvents.length === 0 ? (
            <div className="text-center py-12">
              <Calendar className="w-16 h-16 mx-auto mb-4 text-gray-300" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">No Upcoming Events</h3>
              <p className="text-gray-500">Check back soon for upcoming events and services.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {upcomingEvents.map((event) => (
                <div key={event.id} className="bg-white rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between mb-4">
                    <h3 className="text-lg font-semibold text-gray-900">{event.title}</h3>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                      event.event_type === 'service' 
                        ? 'bg-blue-100 text-blue-800' 
                        : 'bg-green-100 text-green-800'
                    }`}>
                      {event.event_type}
                    </span>
                  </div>
                  <p className="text-gray-600 text-sm mb-4 line-clamp-3">{event.description}</p>
                  <div className="space-y-2">
                    <div className="flex items-center text-sm text-gray-500">
                      <Calendar className="w-4 h-4 mr-2" />
                      {formatDate(event.start_time)}
                    </div>
                    <div className="flex items-center text-sm text-gray-500">
                      <Clock className="w-4 h-4 mr-2" />
                      {formatTime(event.start_time)}
                    </div>
                    <div className="flex items-center text-sm text-gray-500">
                      <MapPin className="w-4 h-4 mr-2" />
                      {event.location}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          <div className="text-center mt-8">
            <a 
              href="/login" 
              className="inline-flex items-center text-blue-600 hover:text-blue-700 font-medium"
            >
              View All Events
              <ArrowRight className="w-4 h-4 ml-1" />
            </a>
          </div>
        </div>
      </div>

      {/* About Section */}
      <div className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-6">About Our Church</h2>
              <p className="text-gray-600 mb-6">
                {/* TODO: Replace with your church's mission statement and description */}
                Grace Community Church has been serving our community for over 50 years. 
                We are committed to sharing the love of Christ through worship, fellowship, 
                and service to others. Our diverse congregation welcomes people from all 
                walks of life to join us in growing in faith and building meaningful relationships.
              </p>
              <p className="text-gray-600 mb-8">
                We believe in the power of community, the importance of prayer, and the 
                transformative love of Jesus Christ. Whether you're new to faith or have 
                been walking with God for years, you'll find a place to belong here.
              </p>
              <a 
                href="/login" 
                className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors inline-flex items-center gap-2"
              >
                Join Our Community
                <ArrowRight className="w-4 h-4" />
              </a>
            </div>
            <div className="bg-gray-200 rounded-lg h-96 flex items-center justify-center">
              {/* TODO: Replace with your church's image */}
              <div className="text-center text-gray-500">
                <Users className="w-16 h-16 mx-auto mb-4" />
                <p>Church Image Placeholder</p>
                <p className="text-sm">Add your church photo here</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Contact Section */}
      <div className="py-16 bg-blue-900 text-white">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Get In Touch</h2>
            <p className="text-blue-100 max-w-2xl mx-auto">
              We'd love to hear from you. Reach out to us with any questions or to learn more about our community.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-800 rounded-full flex items-center justify-center mx-auto mb-4">
                <MapPin className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Visit Us</h3>
              {/* TODO: Replace with your church's address */}
              <p className="text-blue-100">
                123 Church Street<br />
                Your City, State 12345
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-blue-800 rounded-full flex items-center justify-center mx-auto mb-4">
                <Phone className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Call Us</h3>
              {/* TODO: Replace with your church's phone number */}
              <p className="text-blue-100">(555) 123-4567</p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-blue-800 rounded-full flex items-center justify-center mx-auto mb-4">
                <Mail className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Email Us</h3>
              {/* TODO: Replace with your church's email */}
              <p className="text-blue-100">info@gracechurch.com</p>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center">
            <p className="text-gray-400">
              © 2024 Grace Community Church. All rights reserved.
            </p>
            <p className="text-gray-500 text-sm mt-2">
              Built with love for our community
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

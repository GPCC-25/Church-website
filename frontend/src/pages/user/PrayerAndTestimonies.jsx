import { useState, useEffect } from 'react';
import { Heart, MessageCircle, Plus, Clock, User } from 'lucide-react';

export default function PrayerAndTestimonies() {
  const [activeTab, setActiveTab] = useState('prayer');
  const [prayerRequests, setPrayerRequests] = useState([]);
  const [testimonies, setTestimonies] = useState([]);
  const [showPrayerForm, setShowPrayerForm] = useState(false);
  const [showTestimonyForm, setShowTestimonyForm] = useState(false);
  const [loading, setLoading] = useState(false);

  // Form states
  const [prayerForm, setPrayerForm] = useState({
    title: '',
    description: '',
    is_public: true,
    is_anonymous: false
  });

  const [testimonyForm, setTestimonyForm] = useState({
    title: '',
    content: '',
    is_anonymous: false
  });

  // TODO: Replace with your church's API base URL
  const API_BASE = import.meta.env.VITE_PUBLIC_API_URL; // Update this to your backend URL

  useEffect(() => {
    fetchPrayerRequests();
    fetchTestimonies();
  }, []);

  const fetchPrayerRequests = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE}/prayer/prayer-requests`);
      if (response.ok) {
        const data = await response.json();
        setPrayerRequests(data);
      }
    } catch (error) {
      console.error('Error fetching prayer requests:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchTestimonies = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE}/prayer/testimonies`);
      if (response.ok) {
        const data = await response.json();
        setTestimonies(data);
      }
    } catch (error) {
      console.error('Error fetching testimonies:', error);
    } finally {
      setLoading(false);
    }
  };

  const submitPrayerRequest = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE}/prayer/prayer-requests`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(prayerForm)
      });

      if (response.ok) {
        setPrayerForm({ title: '', description: '', is_public: true, is_anonymous: false });
        setShowPrayerForm(false);
        fetchPrayerRequests();
      }
    } catch (error) {
      console.error('Error submitting prayer request:', error);
    }
  };

  const submitTestimony = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE}/prayer/testimonies`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(testimonyForm)
      });

      if (response.ok) {
        setTestimonyForm({ title: '', content: '', is_anonymous: false });
        setShowTestimonyForm(false);
        fetchTestimonies();
      }
    } catch (error) {
      console.error('Error submitting testimony:', error);
    }
  };

  const incrementPrayerCount = async (requestId) => {
    try {
      const token = localStorage.getItem('token');
      await fetch(`${API_BASE}/prayer/prayer-requests/${requestId}/pray`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ increment: 1 })
      });
      fetchPrayerRequests();
    } catch (error) {
      console.error('Error incrementing prayer count:', error);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Prayer & Testimonies</h1>
        <p className="text-gray-600">
          Share your prayer requests and testimonies with our church community
        </p>
      </div>

      {/* Tab Navigation */}
      <div className="flex space-x-1 mb-8 bg-gray-100 p-1 rounded-lg">
        <button
          onClick={() => setActiveTab('prayer')}
          className={`flex-1 py-2 px-4 rounded-md font-medium transition-colors ${
            activeTab === 'prayer'
              ? 'bg-white text-blue-600 shadow-sm'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          Prayer Requests
        </button>
        <button
          onClick={() => setActiveTab('testimonies')}
          className={`flex-1 py-2 px-4 rounded-md font-medium transition-colors ${
            activeTab === 'testimonies'
              ? 'bg-white text-blue-600 shadow-sm'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          Testimonies
        </button>
      </div>

      {/* Prayer Requests Tab */}
      {activeTab === 'prayer' && (
        <div>
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-semibold text-gray-900">Prayer Requests</h2>
            <button
              onClick={() => setShowPrayerForm(true)}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
            >
              <Plus className="w-4 h-4" />
              Submit Prayer Request
            </button>
          </div>

          {/* Prayer Request Form Modal */}
          {showPrayerForm && (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
              <div className="bg-white rounded-lg p-6 w-full max-w-md">
                <h3 className="text-xl font-semibold mb-4">Submit Prayer Request</h3>
                <form onSubmit={submitPrayerRequest} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Title
                    </label>
                    <input
                      type="text"
                      value={prayerForm.title}
                      onChange={(e) => setPrayerForm({...prayerForm, title: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Description
                    </label>
                    <textarea
                      value={prayerForm.description}
                      onChange={(e) => setPrayerForm({...prayerForm, description: e.target.value})}
                      rows={4}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  </div>
                  <div className="flex items-center space-x-4">
                    <label className="flex items-center">
                      <input
                        type="checkbox"
                        checked={prayerForm.is_public}
                        onChange={(e) => setPrayerForm({...prayerForm, is_public: e.target.checked})}
                        className="mr-2"
                      />
                      <span className="text-sm text-gray-700">Make public</span>
                    </label>
                    <label className="flex items-center">
                      <input
                        type="checkbox"
                        checked={prayerForm.is_anonymous}
                        onChange={(e) => setPrayerForm({...prayerForm, is_anonymous: e.target.checked})}
                        className="mr-2"
                      />
                      <span className="text-sm text-gray-700">Submit anonymously</span>
                    </label>
                  </div>
                  <div className="flex space-x-3 pt-4">
                    <button
                      type="submit"
                      className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors"
                    >
                      Submit
                    </button>
                    <button
                      type="button"
                      onClick={() => setShowPrayerForm(false)}
                      className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-400 transition-colors"
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              </div>
            </div>
          )}

          {/* Prayer Requests List */}
          <div className="space-y-4">
            {loading ? (
              <div className="text-center py-8">Loading prayer requests...</div>
            ) : prayerRequests.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                No prayer requests yet. Be the first to submit one!
              </div>
            ) : (
              prayerRequests.map((request) => (
                <div key={request.id} className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
                  <div className="flex justify-between items-start mb-3">
                    <h3 className="text-lg font-semibold text-gray-900">{request.title}</h3>
                    <span className="text-sm text-gray-500 flex items-center gap-1">
                      <Clock className="w-4 h-4" />
                      {formatDate(request.created_at)}
                    </span>
                  </div>
                  <p className="text-gray-700 mb-4">{request.description}</p>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <button
                        onClick={() => incrementPrayerCount(request.id)}
                        className="flex items-center space-x-2 text-red-600 hover:text-red-700 transition-colors"
                      >
                        <Heart className="w-5 h-5" />
                        <span>{request.prayer_count || 0} prayers</span>
                      </button>
                      <div className="flex items-center space-x-2 text-gray-500">
                        <MessageCircle className="w-4 h-4" />
                        <span>{request.comments?.length || 0} comments</span>
                      </div>
                    </div>
                    {!request.is_anonymous && (
                      <div className="flex items-center space-x-2 text-gray-500">
                        <User className="w-4 h-4" />
                        <span className="text-sm">{request.member_name || 'Anonymous'}</span>
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {/* Testimonies Tab */}
      {activeTab === 'testimonies' && (
        <div>
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-semibold text-gray-900">Testimonies</h2>
            <button
              onClick={() => setShowTestimonyForm(true)}
              className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors flex items-center gap-2"
            >
              <Plus className="w-4 h-4" />
              Share Testimony
            </button>
          </div>

          {/* Testimony Form Modal */}
          {showTestimonyForm && (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
              <div className="bg-white rounded-lg p-6 w-full max-w-md">
                <h3 className="text-xl font-semibold mb-4">Share Your Testimony</h3>
                <form onSubmit={submitTestimony} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Title
                    </label>
                    <input
                      type="text"
                      value={testimonyForm.title}
                      onChange={(e) => setTestimonyForm({...testimonyForm, title: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Your Testimony
                    </label>
                    <textarea
                      value={testimonyForm.content}
                      onChange={(e) => setTestimonyForm({...testimonyForm, content: e.target.value})}
                      rows={6}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                      placeholder="Share how God has worked in your life..."
                      required
                    />
                  </div>
                  <div>
                    <label className="flex items-center">
                      <input
                        type="checkbox"
                        checked={testimonyForm.is_anonymous}
                        onChange={(e) => setTestimonyForm({...testimonyForm, is_anonymous: e.target.checked})}
                        className="mr-2"
                      />
                      <span className="text-sm text-gray-700">Submit anonymously</span>
                    </label>
                  </div>
                  <div className="flex space-x-3 pt-4">
                    <button
                      type="submit"
                      className="flex-1 bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 transition-colors"
                    >
                      Share
                    </button>
                    <button
                      type="button"
                      onClick={() => setShowTestimonyForm(false)}
                      className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-400 transition-colors"
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              </div>
            </div>
          )}

          {/* Testimonies List */}
          <div className="space-y-4">
            {loading ? (
              <div className="text-center py-8">Loading testimonies...</div>
            ) : testimonies.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                No testimonies yet. Share how God has blessed you!
              </div>
            ) : (
              testimonies.map((testimony) => (
                <div key={testimony.id} className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
                  <div className="flex justify-between items-start mb-3">
                    <h3 className="text-lg font-semibold text-gray-900">{testimony.title}</h3>
                    <span className="text-sm text-gray-500 flex items-center gap-1">
                      <Clock className="w-4 h-4" />
                      {formatDate(testimony.created_at)}
                    </span>
                  </div>
                  <p className="text-gray-700 mb-4 whitespace-pre-wrap">{testimony.content}</p>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2 text-gray-500">
                      <MessageCircle className="w-4 h-4" />
                      <span>{testimony.comments?.length || 0} comments</span>
                    </div>
                    {!testimony.is_anonymous && (
                      <div className="flex items-center space-x-2 text-gray-500">
                        <User className="w-4 h-4" />
                        <span className="text-sm">{testimony.member_name || 'Anonymous'}</span>
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
}

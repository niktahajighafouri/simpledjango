import React, { useState, useEffect } from 'react';
import { PlusCircle, Trash2, CheckCircle, Circle, Calendar, Tag, BarChart2, Clock, AlertCircle, User, List } from 'lucide-react';
import axios from 'axios';

interface SubTask {
  id: number;
  title: string;
  description: string;
  status: 'TODO' | 'IN_PROGRESS' | 'DONE';
  created_at: string;
  updated_at: string;
}

interface Task {
  id: number;
  title: string;
  description: string;
  due_date: string;
  status: 'TODO' | 'IN_PROGRESS' | 'DONE';
  priority: 'LOW' | 'MEDIUM' | 'HIGH';
  assigned_to?: {
    id: number;
    username: string;
  };
  created_by: {
    id: number;
    username: string;
  };
  created_at: string;
  updated_at: string;
  subtasks: SubTask[];
}

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

const statusOptions = [
  { value: 'TODO', label: 'To Do' },
  { value: 'IN_PROGRESS', label: 'In Progress' },
  { value: 'DONE', label: 'Done' },
];

const priorityOptions = [
  { value: 'LOW', label: 'Low' },
  { value: 'MEDIUM', label: 'Medium' },
  { value: 'HIGH', label: 'High' },
];

function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTask, setNewTask] = useState({
    title: '',
    description: '',
    due_date: '',
    status: 'TODO' as const,
    priority: 'MEDIUM' as const,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showDashboard, setShowDashboard] = useState(false);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await api.get('/tasks/');
      setTasks(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch tasks. Please try again later.');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const addTask = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await api.post('/tasks/', {
        ...newTask,
        created_by: 1, // This should be the logged-in user's ID
      });
      setTasks([...tasks, response.data]);
      setNewTask({
        title: '',
        description: '',
        due_date: '',
        status: 'TODO',
        priority: 'MEDIUM',
      });
      setError(null);
    } catch (err) {
      setError('Failed to add task. Please try again.');
      console.error('Error adding task:', err);
    }
  };

  const updateTaskStatus = async (taskId: number, newStatus: Task['status']) => {
    try {
      const response = await api.patch(`/tasks/${taskId}/`, {
        status: newStatus,
      });
      setTasks(tasks.map(task => 
        task.id === taskId ? response.data : task
      ));
      setError(null);
    } catch (err) {
      setError('Failed to update task. Please try again.');
      console.error('Error updating task:', err);
    }
  };

  const deleteTask = async (taskId: number) => {
    try {
      await api.delete(`/tasks/${taskId}/`);
      setTasks(tasks.filter(task => task.id !== taskId));
      setError(null);
    } catch (err) {
      setError('Failed to delete task. Please try again.');
      console.error('Error deleting task:', err);
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'HIGH': return 'text-red-500';
      case 'MEDIUM': return 'text-yellow-500';
      case 'LOW': return 'text-green-500';
      default: return 'text-gray-500';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'DONE': return 'bg-green-100 text-green-800';
      case 'IN_PROGRESS': return 'bg-yellow-100 text-yellow-800';
      case 'TODO': return 'bg-purple-100 text-purple-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const Dashboard = () => {
    const totalTasks = tasks.length;
    const completedTasks = tasks.filter(t => t.status === 'DONE').length;
    const inProgressTasks = tasks.filter(t => t.status === 'IN_PROGRESS').length;
    const todoTasks = tasks.filter(t => t.status === 'TODO').length;
    const highPriorityTasks = tasks.filter(t => t.priority === 'HIGH' && t.status !== 'DONE').length;

    const statusDistribution = [
      { label: 'To Do', count: todoTasks, color: 'bg-purple-500' },
      { label: 'In Progress', count: inProgressTasks, color: 'bg-yellow-500' },
      { label: 'Done', count: completedTasks, color: 'bg-green-500' },
    ];

    return (
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-6">
        <div className="col-span-2 grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-white p-4 rounded-lg shadow-md">
            <h3 className="text-gray-600 text-sm font-medium">Total Tasks</h3>
            <p className="text-2xl font-bold text-gray-800">{totalTasks}</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-md">
            <h3 className="text-gray-600 text-sm font-medium">Completed</h3>
            <p className="text-2xl font-bold text-green-600">{completedTasks}</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-md">
            <h3 className="text-gray-600 text-sm font-medium">In Progress</h3>
            <p className="text-2xl font-bold text-yellow-600">{inProgressTasks}</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-md">
            <h3 className="text-gray-600 text-sm font-medium">High Priority</h3>
            <p className="text-2xl font-bold text-red-600">{highPriorityTasks}</p>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold mb-4 text-gray-800">Status Distribution</h3>
          <div className="space-y-4">
            {statusDistribution.map(status => (
              <div key={status.label} className="flex items-center">
                <span className="w-24 text-sm text-gray-600">{status.label}</span>
                <div className="flex-1 h-4 bg-gray-100 rounded-full overflow-hidden">
                  <div 
                    className={`h-full ${status.color} rounded-full`}
                    style={{ width: `${(status.count / totalTasks) * 100}%` }}
                  ></div>
                </div>
                <span className="ml-2 text-sm text-gray-600">{status.count}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold mb-4 text-gray-800">Recent Activity</h3>
          <div className="space-y-3">
            {tasks.slice(0, 5).map(task => (
              <div key={task.id} className="flex items-center justify-between text-sm">
                <span className="text-gray-700">{task.title}</span>
                <span className={`px-2 py-1 rounded-full text-xs ${getStatusColor(task.status)}`}>
                  {task.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-800 to-indigo-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-xl shadow-2xl overflow-hidden">
          <div className="bg-gradient-to-r from-pink-600 via-purple-700 to-indigo-800 px-6 py-8 text-white">
            <div className="flex justify-between items-center">
              <div>
                <h1 className="text-3xl font-bold">Task Manager Pro</h1>
                <p className="mt-2 text-pink-200">Organize your projects efficiently</p>
              </div>
              <button
                onClick={() => setShowDashboard(!showDashboard)}
                className="flex items-center gap-2 px-4 py-2 bg-white/10 rounded-lg hover:bg-white/20 transition-colors duration-200"
              >
                <BarChart2 size={20} />
                <span>{showDashboard ? 'View Tasks' : 'Dashboard'}</span>
              </button>
            </div>
          </div>

          {error && (
            <div className="bg-red-50 border-l-4 border-red-500 p-4">
              <p className="text-red-700">{error}</p>
            </div>
          )}

          {showDashboard ? (
            <Dashboard />
          ) : (
            <>
              <form onSubmit={addTask} className="p-6 border-b border-gray-200">
                <div className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <input
                      type="text"
                      value={newTask.title}
                      onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
                      placeholder="Task title..."
                      className="px-4 py-2 bg-gray-50 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    />
                    <input
                      type="date"
                      value={newTask.due_date}
                      onChange={(e) => setNewTask({ ...newTask, due_date: e.target.value })}
                      className="px-4 py-2 bg-gray-50 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    />
                  </div>
                  <textarea
                    value={newTask.description}
                    onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
                    placeholder="Task description..."
                    className="w-full px-4 py-2 bg-gray-50 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    rows={3}
                  />
                  <div className="flex gap-4">
                    <select
                      value={newTask.status}
                      onChange={(e) => setNewTask({ ...newTask, status: e.target.value as Task['status'] })}
                      className="px-4 py-2 bg-gray-50 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    >
                      {statusOptions.map(option => (
                        <option key={option.value} value={option.value}>{option.label}</option>
                      ))}
                    </select>
                    <select
                      value={newTask.priority}
                      onChange={(e) => setNewTask({ ...newTask, priority: e.target.value as Task['priority'] })}
                      className="px-4 py-2 bg-gray-50 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    >
                      {priorityOptions.map(option => (
                        <option key={option.value} value={option.value}>{option.label}</option>
                      ))}
                    </select>
                    <button
                      type="submit"
                      className="bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700 transition-colors duration-200 flex items-center gap-2"
                    >
                      <PlusCircle size={20} />
                      Add Task
                    </button>
                  </div>
                </div>
              </form>

              <div className="divide-y divide-gray-200 max-h-[600px] overflow-y-auto">
                {loading ? (
                  <div className="p-4 text-center text-gray-600">Loading tasks...</div>
                ) : tasks.length === 0 ? (
                  <div className="p-8 text-center">
                    <div className="inline-block p-4 bg-gray-100 rounded-full mb-4">
                      <AlertCircle size={32} className="text-gray-400" />
                    </div>
                    <p className="text-gray-600">No tasks yet. Add one above!</p>
                  </div>
                ) : (
                  <ul>
                    {tasks.map(task => (
                      <li key={task.id} className="p-4 hover:bg-gray-50 transition-colors duration-150">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-3 flex-1">
                            <button
                              onClick={() => updateTaskStatus(task.id, task.status === 'DONE' ? 'TODO' : 'DONE')}
                              className="text-gray-400 hover:text-gray-600 transition-colors duration-200"
                            >
                              {task.status === 'DONE' ? (
                                <CheckCircle className="text-green-500" size={24} />
                              ) : (
                                <Circle size={24} />
                              )}
                            </button>
                            <div className="flex-1">
                              <div className="flex items-center gap-2">
                                <span className={`text-lg ${task.status === 'DONE' ? 'line-through text-gray-400' : 'text-gray-700'}`}>
                                  {task.title}
                                </span>
                                <span className={`px-2 py-1 rounded-full text-xs ${getStatusColor(task.status)}`}>
                                  {task.status}
                                </span>
                              </div>
                              <p className="text-gray-500 text-sm mt-1">{task.description}</p>
                              <div className="flex gap-4 mt-2">
                                <span className="flex items-center text-sm text-gray-500">
                                  <Calendar size={14} className="mr-1" />
                                  {new Date(task.due_date).toLocaleDateString()}
                                </span>
                                <span className={`flex items-center text-sm ${getPriorityColor(task.priority)}`}>
                                  <Tag size={14} className="mr-1" />
                                  {task.priority}
                                </span>
                                {task.assigned_to && (
                                  <span className="flex items-center text-sm text-gray-500">
                                    <User size={14} className="mr-1" />
                                    {task.assigned_to.username}
                                  </span>
                                )}
                                {task.subtasks.length > 0 && (
                                  <span className="flex items-center text-sm text-gray-500">
                                    <List size={14} className="mr-1" />
                                    {task.subtasks.length} subtasks
                                  </span>
                                )}
                              </div>
                            </div>
                          </div>
                          <button
                            onClick={() => deleteTask(task.id)}
                            className="text-gray-400 hover:text-red-500 transition-colors duration-200 ml-4"
                          >
                            <Trash2 size={20} />
                          </button>
                        </div>
                      </li>
                    ))}
                  </ul>
                )}
              </div>

              <div className="px-6 py-4 bg-gray-50">
                <p className="text-sm text-gray-600 text-center">
                  {tasks.length} task{tasks.length !== 1 ? 's' : ''} total • {tasks.filter(t => t.status === 'DONE').length} completed
                </p>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
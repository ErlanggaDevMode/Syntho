import { useState } from 'react'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col items-center justify-center p-4">
      <div className="max-w-md w-full bg-slate-900 border border-slate-800 rounded-xl p-8 shadow-2xl text-center space-y-6">
        <h1 className="text-3xl font-bold tracking-tight text-purple-400">Syntho Dashboard</h1>
        <p className="text-slate-400">
          Welcome to your self-hosted notes and expense tracking assistant.
        </p>
        <button
          onClick={() => setCount((c) => c + 1)}
          className="px-6 py-2 bg-purple-600 hover:bg-purple-500 active:bg-purple-700 text-white rounded-lg font-medium shadow-md transition-all"
        >
          Count: {count}
        </button>
      </div>
    </div>
  )
}

export default App

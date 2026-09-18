import Dashboard from "./pages/Dashboard";
import "./App.css";

function App() {
  return (
    <div className="app">

      <header className="command-header">

        <div className="command-brand">

          <div className="command-logo">
            AI
          </div>

          <div>
            <div className="command-title">
              INCIDENT AI
            </div>

            <div className="command-subtitle">
              Autonomous Resolution Engine
            </div>
          </div>

        </div>


        <div className="command-center">

          <span className="system-indicator"></span>

          <span>
            ENTERPRISE OPERATIONS
          </span>

        </div>


        <div className="command-status">

          <span className="status-dot"></span>

          <div>
            <strong>
              AI AGENT ONLINE
            </strong>

            <small>
              Local inference
            </small>
          </div>

        </div>

      </header>


      <main className="main-content">

        <Dashboard />

      </main>


      <footer className="command-footer">

        <span>
          INCIDENT AI
        </span>

        <span>
          AUTONOMOUS INCIDENT RESOLUTION
        </span>

        <span>
          SYSTEM ONLINE
        </span>

      </footer>

    </div>
  );
}

export default App;
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Dashboard() {

  const navigate = useNavigate();

  const { logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <div style={{ padding: 40 }}>

      <h1>Dashboard</h1>

      <button onClick={handleLogout}>
        Logout
      </button>

    </div>
  );
}

export default Dashboard;
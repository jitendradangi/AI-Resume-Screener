import { createContext, useContext, useState, useEffect } from "react";
import {
  saveToken,
  removeToken,
  getToken,
} from "../services/authService";
import { getUserProfile } from "../services/userService";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(getToken());
  const [user, setUser] = useState(null);

  const fetchUser = async () => {
    if (!getToken()) {
      setUser(null);
      return;
    }
    try {
      const profile = await getUserProfile();
      console.log("Profile data from API:", profile);
      console.log("Profile full_name:", profile?.full_name);
      console.log("Profile email:", profile?.email);
      
      // The API should return the user object directly
      if (profile && typeof profile === 'object') {
        setUser(profile);
      } else {
        console.warn("Unexpected profile data structure:", profile);
        setUser(null);
      }
    } catch (err) {
      console.error("Failed to fetch user profile in AuthContext:", err);
      setUser(null);
    }
  };

  useEffect(() => {
    if (token) {
      fetchUser();
    } else {
      setUser(null);
    }
  }, [token]);

  const login = async (jwtToken) => {
    saveToken(jwtToken);
    setToken(jwtToken);
    // Force immediate user fetch
    await fetchUser();
  };

  const logout = () => {
    removeToken();
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        setUser,
        fetchUser,
        login,
        logout,
        isAuthenticated: !!token,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);

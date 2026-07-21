import { createContext, useContext, useState } from "react";
import {
  saveToken,
  removeToken,
  getToken,
} from "../services/authService";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {

  const [token, setToken] = useState(getToken());

  const login = (jwtToken) => {
    saveToken(jwtToken);
    setToken(jwtToken);
  };

  const logout = () => {
    removeToken();
    setToken(null);
  };

  return (
    <AuthContext.Provider
      value={{
        token,
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
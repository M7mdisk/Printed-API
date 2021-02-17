import React, {useState, useEffect} from 'react';
import { UserContext } from '../../contexts/userContext.js';
import '../../css/style.scss';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import AOS from 'aos';
import { focusHandling } from 'cruip-js-toolkit';

import Home from '../../pages/Home';
import SignIn from '../../pages/SignIn';
import SignUp from '../../pages/SignUp';
import ResetPassword from '../../pages/ResetPassword';


import LoginPage from '../../pages/LoginPage.js';
import HomePage from '../../pages/HomePage.js';
import AuthenticatedPing from '../../pages/AuthenticatedPing.js';
import Dashboard from '../../pages/Dashboard'
import { logoutUser } from '../../api/auth.js';

import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useLocation
} from "react-router-dom";


function App() {

  const location = useLocation();

  useEffect(() => {
    AOS.init({
      once: true,
      disable: 'phone',
      duration: 700,
      easing: 'ease-out-cubic',
    });
  });

  useEffect(() => {
    document.querySelector('html').style.scrollBehavior = 'auto'
    window.scroll({ top: 0 })
    document.querySelector('html').style.scrollBehavior = ''
    focusHandling('outline');
  }, [location.pathname]); // triggered on route change

  const [user, setUser] = useState(null);
  const isUserLoggedIn = () => {
    return !!user;
  }
  const logout = (event) => {
    event.preventDefault();
    logoutUser();
    setUser(null);
  }

  return (
    <>
    <UserContext.Provider value={{user, setUser, isUserLoggedIn}}>
      <Switch>
        <Route exact path="/">
          <Home />
        </Route>
        <Route path="/signin">
          <SignIn />
        </Route>
        <Route path="/signup">
          <SignUp />
        </Route>
        <Route path="/reset-password">
          <ResetPassword />
        </Route>
        <Route  path="/ping">
          <AuthenticatedPing/>
        </Route>
        <Route  path="/dashboard">
          <Dashboard/>
        </Route>
      </Switch>
      </UserContext.Provider>
    </>
  );
}

  /* referring to <UserContext.Provider value={{user, setUser, isUserLoggedIn}}> and other instances.
  * since the values are stored as variables in context, it's not necessary to escape the values for XSS-sake.
  */


//   return (
//     <div className="App">
//       <UserContext.Provider value={{user, setUser, isUserLoggedIn}}>
//         <Router>
//           <Container>
//             <Navbar bg="light" expand="lg">
//               <Navbar.Brand href="#home">DRF SampleJWT React Sample</Navbar.Brand>
//               <Navbar.Toggle aria-controls="basic-navbar-nav" />
//               <Navbar.Collapse id="basic-navbar-nav">
//                 <Nav className="mr-auto">
//                   <Nav.Link as={Link} to="/">Home</Nav.Link>
//                 </Nav>
//                 <Nav className="justify-content-end">
//                   <Nav.Link as={Link} to="/ping">Ping</Nav.Link>
//                   { isUserLoggedIn() ?
//                     <Nav.Link as={Link} onClick={logout}>Logout</Nav.Link>
//                     :
//                     <Nav.Link as={Link} to="/login">Login</Nav.Link>
//                   }
//                 </Nav>
//               </Navbar.Collapse>
//             </Navbar>
//             <Switch>
//                 <Route exact path="/login">
//                   <LoginPage/>
//                 </Route>
//                 <Route exact path="/ping">
//                   <AuthenticatedPing/>
//                 </Route>
//                 <Route exact path="/">
//                   <HomePage/>
//                 </Route>
//             </Switch>
//           </Container>
//         </Router>

//       </UserContext.Provider>
//     </div>
//   );
// }

export default App;

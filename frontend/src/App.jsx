import { useAuth } from './context/AuthContext';
import Header from './components/Header/Header';
import ProductList from './components/ProductList/ProductList';
import ShoppingCart from './components/ShoppingCart/ShoppingCart';
import Login from './components/Login/Login';
import styled from 'styled-components';

const MainContainer = styled.div`
  width: 100%;
  max-width: 1800px;
  margin: 0 auto;
  padding: 30px 30px 0 30px;
`;

const ContentWrapper = styled.div`
  display: grid;
  grid-template-columns: 1fr;
  gap: 30px;

  /* ≥900px: item and cart in the same row */
  @media (min-width: 900px) {
    grid-template-columns: minmax(0, 1fr) minmax(300px, 350px);
  }

  /* ≥1200px: adjust spacing */
  @media (min-width: 1200px) {
    gap: 40px;
    grid-template-columns: minmax(0, 1fr) minmax(320px, 380px);
  }

  /* ≥1600px: cart wider */
  @media (min-width: 1600px) {
    grid-template-columns: minmax(0, 1fr) minmax(350px, 400px);
  }
`;

// Main content component with auth check
function AppContent() {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <MainContainer>
        <div>Loading...</div>
      </MainContainer>
    );
  }

  return (
    <MainContainer>
      <ContentWrapper>
        <ProductList />
        {/* Show ShoppingCart when logged in, Login when not logged in */}
        {isAuthenticated ? (
          <ShoppingCart />
        ) : (
          <Login />
        )}
      </ContentWrapper>
    </MainContainer>
  );
}

function App() {
  return (
    <>
      <Header />
      <AppContent />
    </>
  );
}

export default App;

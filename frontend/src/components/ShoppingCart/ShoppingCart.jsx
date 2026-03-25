import { memo, useState } from 'react';
import { useCartOperations } from '../../hooks/useCart';
import { formatCurrency, formatNumber } from '../../utils/formatters';
import CartItem from '../CartItem/CartItem';
import ConfirmationModal from '../Modal/Modal';
import * as S from './ShoppingCart.styles';

const ShoppingCart = () => {
  const {
    cartItems,
    loading,
    error,
    stockError,
    clearStockError,
    getTotalPrice,
    getTotalCount,
    clearCart,
  } = useCartOperations();
  const [showClearConfirm, setShowClearConfirm] = useState(false);

  if (loading) {
    return <S.Container>Loading cart...</S.Container>;
  }

  // Show general error for non-stock-related errors
  if (error && !stockError) {
    return <S.ErrorMessage>{error}</S.ErrorMessage>;
  }

  const totalCount = getTotalCount();
  const totalPrice = getTotalPrice();

  const handleClearCart = async () => {
    try {
      await clearCart();
      setShowClearConfirm(false);
    } catch (error) {
      console.error('Failed to clear cart:', error);
      // Error could be shown to user via toast/notification
    }
  };

  return (
    <S.Container>
      <S.Title>
        <S.CartIcon>🛒</S.CartIcon>
        Shopping Cart
      </S.Title>

      {/* Stock Error Alert */}
      {stockError && (
        <S.StockErrorAlert>
          <S.ErrorContent>
            <S.ErrorIcon>⚠️</S.ErrorIcon>
            <S.ErrorMessageText>{stockError}</S.ErrorMessageText>
          </S.ErrorContent>
          <S.CloseButton onClick={clearStockError}>×</S.CloseButton>
        </S.StockErrorAlert>
      )}

      {totalCount === 0 ? (
        <S.EmptyCart>Your cart is empty</S.EmptyCart>
      ) : (
        <S.CartContent>
          <S.CartSummary>
            <S.ItemCount>{formatNumber(totalCount)} item(s)</S.ItemCount>
            <S.ClearCartButton onClick={() => setShowClearConfirm(true)}>
              🗑️ Clear All
            </S.ClearCartButton>
          </S.CartSummary>

          <S.CartItemsList>
            {cartItems.map((item) => (
              <CartItem key={item.id} item={item} />
            ))}
          </S.CartItemsList>

          <S.TotalSection>
            <S.TotalLabel>Total:</S.TotalLabel>
            <S.TotalAmount>{formatCurrency(totalPrice)}</S.TotalAmount>
          </S.TotalSection>
        </S.CartContent>
      )}

      <ConfirmationModal
        isOpen={showClearConfirm}
        title="Clear Cart"
        message="Clear all items from cart?"
        confirmText="Clear All"
        cancelText="Cancel"
        onConfirm={handleClearCart}
        onCancel={() => setShowClearConfirm(false)}
        type="danger"
      />
    </S.Container>
  );
};

export default memo(ShoppingCart);
